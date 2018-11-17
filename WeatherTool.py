# This tool displays current temperatures for cities over 250k on a map
# Note: A tool was run on the original dataset to delete cities with the minimum population
# that were within 50 miles of a city with a bigger population.
# Therefore, a city like Newark (< 50 miles from New York City) is not included in this project.
# I used the PostGIS Shapefile loader to upload the cities.shp into Postgressql
# I also connected to the postgres database using the GUI (ODBC connection)

import arcpy
import psycopg2
import urllib2
import json
import time
arcpy.env.overwriteOutput = True

conn = psycopg2.connect("dbname='Weather' user='postgres' host='localhost' password='swimming12'")
cur = conn.cursor()


def create_table():

    cur.execute("""CREATE TABLE temperatures AS SELECT gid, objectid, city, state FROM cities""")
    conn.commit()
    cur.execute("""ALTER TABLE temperatures ADD COLUMN current_temp INT""")
    conn.commit()

    obtain_data()


def obtain_data():

    cur.execute("""SELECT city, state FROM temperatures""")
    info = cur.fetchall()
    global loc_temp
    loc_temp = {}


    for i in info:
        if len(i[0].split()) == 2:
            city = i[0].split()[0] + "_" + i[0].split()[1]
        if len(i[0].split()) == 1:
            city = i[0]

        state = i[1]

        url = "http://api.wunderground.com/api/1dd663cc894a2191/geolookup/conditions/q/" + state + "/" + city + ".json"

        access_url = urllib2.urlopen(url)
        time.sleep(10)
        json_string = access_url.read()

        parsing_json = json.loads(json_string)

        location = parsing_json['location']['city']
        temp_f = parsing_json['current_observation']['temp_f']

        loc_temp[location] = temp_f

    load_data()


def load_data():

    for loc, temp in loc_temp.iteritems():
        int_temp = int(temp)

        cur.execute("""UPDATE temperatures SET current_temp = (%s) WHERE city = (%s);""", (int_temp, loc))
        conn.commit()

    connecting_pg_arc()


def connecting_pg_arc():

    db_connection = "Database Connections/OLE DB Connection.odc/public.temperatures"
    arcpy.TableToTable_conversion(db_connection, "C:/Weather/Locations.gdb", "temperatures")

    cities = "C:/Weather/cities.shp"
    weather_data = "C:/Weather/Locations.gdb/temperatures"

    arcpy.JoinField_management(cities, "City", weather_data, "city", "current_temp")

# Then I changed the symbology and labeling of the map through the GUI


create_table()

