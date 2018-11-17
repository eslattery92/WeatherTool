# This program takes a shapefile of all cities in the United States with populations over 250k
# and for all cities within 50 miles of another city on the list, the less populated city is deleted

import arcpy
arcpy.env.workspace = "C:/Weather/Locations.gdb"
cities = "C:/Weather/all_cities.shp"


def find_close():
    arcpy.PointDistance_analysis(cities, cities, "pointdistance", "50 Miles")

    pop_dict = {}
    with arcpy.da.SearchCursor(cities, ["FID", "Population"]) as cursor:
        for row in cursor:
            pop_dict[row[0]] = row[1]

    higher_pop = []
    with arcpy.da.SearchCursor("pointdistance", ["INPUT_FID", "NEAR_FID"]) as cursor:
        for row in cursor:
            if pop_dict[row[0]] < pop_dict[row[1]]:
                higher_pop.append(row[0])

    global higher_pop_set
    higher_pop_set = set(higher_pop)

    delete_close()


def delete_close():
    with arcpy.da.UpdateCursor(cities, ["FID", "City", "Population"]) as cursor:
        for row in cursor:
            if row[0] in higher_pop_set:
                cursor.deleteRow()


find_close()



