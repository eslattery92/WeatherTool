# This tool loads weather data using an API to a postgres table

import psycopg2
import urllib2
import json
import time

key = "1dd663cc894a2191"


conn = psycopg2.connect("dbname='Weather' user='postgres' host='localhost' password='swimming12'")
cur = conn.cursor()
# cur.execute("""CREATE TABLE historic_data
#        (id SERIAL PRIMARY KEY NOT NULL,
#         city_id BIGINT NOT NULL,
#         city VARCHAR(40) NOT NULL,
#         state VARCHAR(2) NOT NULL,
#         days_sun VARCHAR(3) NOT NULL,
#         total_precip VARCHAR(3) NOT NULL)""")
#
# conn.commit()

# cur.execute("""CREATE TABLE weather_data AS SELECT gid, objectid, city, state FROM cities""")

# cur.execute("""ALTER TABLE weather_data ADD COLUMN current_temp VARCHAR(3)""")



# url = "http://api.wunderground.com/api/1dd663cc894a2191/geolookup/conditions/q/" + state_name + "/" + \
#       + city_name + ".json"""


cur.execute("""SELECT city, state FROM weather_data""")
info = cur.fetchall()
loc_temp = {}
for i in info:
    if len(i[0].split()) == 2:
        city = i[0].split()[0] + "_" + i[0].split()[1]
    if len(i[0].split()) == 1:
        city = i[0]
    # print city

    state = i[1]
    # print city, state

    url = "http://api.wunderground.com/api/1dd663cc894a2191/geolookup/conditions/q/" + state + "/" + city + ".json"

    access_url = urllib2.urlopen(url)
    time.sleep(10)
    json_string = access_url.read()

    parsing_json = json.loads(json_string)

    location = parsing_json['location']['city']
    temp_f = parsing_json['current_observation']['temp_f']

    loc_temp[location] = temp_f


for loc, temp in loc_temp.iteritems():
    int_temp = int(temp)

    cur.execute("""UPDATE weather_data SET current_temp = (%s) WHERE city = (%s);""", (int_temp, loc))
    conn.commit()




























 # url = "http://api.wunderground.com/api/1dd663cc894a2191/geolookup/conditions/q/IA/Cedar_Rapids.json"




























# conn.commit()


























