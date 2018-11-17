import arcpy


db_connection = "Database Connections/OLE DB Connection.odc/public.weather_data"

# arcpy.TableToTable_conversion(db_connection, "C:/Weather/Locations.gdb", "temperatures")

cities = "C:/Weather/cities.shp"
weather_data = "C:/Weather/Locations.gdb/temperatures"

# arcpy.JoinField_management(cities, "City", weather_data, "city", "current_temp")




mxd = arcpy.mapping.MapDocument("C:/Weather/weathermap.mxd")
output = "C:/Weather/map4.pdf"
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
df.scale = 17000000
dfew = df.elementWidth/0.004
dfeh = df.elementHeight/0.004
arcpy.mapping.ExportToPDF(mxd, output, df, df_export_width=dfew, df_export_height=dfeh)



























































