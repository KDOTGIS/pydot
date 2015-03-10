'''
Created on Mar 25, 2013

@author: kyleg
'''
import arcpy
inputfc = 'NonState2008_2013'
GCresult= 'GC_SDC'
Geocoder = r'\\gisdata\arcgis\GISdata\DASC\DataMaps101\Street_Addresses_US'

GCContainer = r'\\gisdata\arcgis\GISdata\KDOT\BTP\Projects\AccidentGeocode\AccidentData_2012.mdb'
arcpy.env.workspace = GCContainer
offField = "AccidentOffset"
#Use File Geodatabases here
#add field and concatenate fields to match intersection addresses to
arcpy.AddField_management(inputfc,"INTERSECTION","TEXT","#","#","50","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management(inputfc, "INTERSECTION","""[ON_ROAD_KDOT_PFX_DIR] &" " & [ON_ROAD_KDOT_NAME]&" " & [ON_ROAD_KDOT_TYPE]&" " & [ON_ROAD_KDOT_SFX_DIR]&" @ " & [AT_ROAD_KDOT_PFX_DIR]&" " & [AT_ROAD_KDOT_NAME]&" " & [AT_ROAD_KDOT_TYPE]&" " & [AT_ROAD_KDOT_SFX_DIR]""","VB","#")
#add field and calculate with offset distance + units
arcpy.AddField_management(inputfc,offField,"TEXT","#","#","50","#","NULLABLE","NON_REQUIRED","#")
#if units are feet....
arcpy.SelectLayerByAttribute_management(inputfc,"NEW_SELECTION","AT_ROAD_KDOT_DIST_UOM = 'F'")
arcpy.CalculateField_management(inputfc,offField,""" [AT_ROAD_KDOT_DISTANCE] &" feet""""","VB","#")
#if units are miles...
arcpy.SelectLayerByAttribute_management(inputfc,"NEW_SELECTION","AT_ROAD_KDOT_DIST_UOM = 'M'")
arcpy.CalculateField_management(inputfc,offField,"[AT_ROAD_KDOT_DISTANCE]&' miles'","VB","#")

#arcpy.SelectLayerByAttribute_management(inputfc,"NEW_SELECTION","[AccidentOffset] IS NOT NULL")
#clear the selction
arcpy.SelectLayerByAttribute_management(inputfc,"CLEAR_SELECTION")

#hard set the coordinate system and to operate in WGS84 Lat Long datum
wgs = r"\\GISDATA\ArcGIS\GISDATA\Layers\CoordSys\WGS 1984.prj"
arcpy.env.outputCoordinateSystem = wgs
#do the geocode - address match the intersections
arcpy.GeocodeAddresses_geocoding(inputfc,Geocoder,"Street Intersection VISIBLE NONE;City City_name VISIBLE NONE;State State VISIBLE NONE;ZIP <None> VISIBLE NONE", GCContainer+"//"+GCresult,"STATIC")

#This is the first result - if the At road offset is null, this is the final location.  If the at road offset is not null, then continue...
#this is a good time to rematch the addresses that tied or missed, or scored below an acceptable threshold.  This is a manual process.
#depending on how we want this process to run, I might need to add some automation code or a subroutine here
#arcpy.RematchAddresses_geocoding()

inlyr = GCresult+"Buffer"
#Doing this buffer gets our offset to a common datum - units are now in DD
arcpy.Buffer_analysis(GCresult,inlyr,"AccidentOffset","FULL","ROUND","NONE","#")
#add the XY fields for accidents that need to be offset from the intersection
arcpy.AddField_management(inlyr,"Accident_X","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(inlyr,"Accident_Y","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")

#offset the accidents by a vector direction and distance in the Accident X,Y fields
arcpy.SelectLayerByAttribute_management(inlyr,"NEW_SELECTION","[AT_ROAD_KDOT_DIRECTION] = 'E'")
arcpy.CalculateField_management(inlyr,"Accident_X","[X]+ [BUFF_DIST]","VB","#")
arcpy.CalculateField_management(inlyr,"Accident_Y","[Y]","VB","#")

arcpy.SelectLayerByAttribute_management(inlyr,"NEW_SELECTION","[AT_ROAD_KDOT_DIRECTION] = 'W'")
arcpy.CalculateField_management(inlyr,"Accident_X","[X]- [BUFF_DIST]","VB","#")
arcpy.CalculateField_management(inlyr,"Accident_Y","[Y]","VB","#")

arcpy.SelectLayerByAttribute_management(inlyr,"NEW_SELECTION","[AT_ROAD_KDOT_DIRECTION] = 'N'")
arcpy.CalculateField_management(inlyr,"Accident_X","[X]","VB","#")
arcpy.CalculateField_management(inlyr,"Accident_Y","[Y]+[BUFF_DIST]","VB","#")

arcpy.SelectLayerByAttribute_management(inlyr,"NEW_SELECTION","[AT_ROAD_KDOT_DIRECTION] = 'S'")
arcpy.CalculateField_management(inlyr,"Accident_X","[X]","VB","#")
arcpy.CalculateField_management(inlyr,"Accident_Y","[Y]-[BUFF_DIST]","VB","#")

arcpy.SelectLayerByAttribute_management(inlyr,"NEW_SELECTION","[AT_ROAD_KDOT_DIRECTION] = 'NE'")
arcpy.CalculateField_management(inlyr,"Accident_X","[X]+[BUFF_DIST]*.707","VB","#")
arcpy.CalculateField_management(inlyr,"Accident_Y","[Y]+[BUFF_DIST]*.707","VB","#")

arcpy.SelectLayerByAttribute_management(inlyr,"NEW_SELECTION","[AT_ROAD_KDOT_DIRECTION] = 'NW'")
arcpy.CalculateField_management(inlyr,"Accident_X","[X]-[BUFF_DIST]*.707","VB","#")
arcpy.CalculateField_management(inlyr,"Accident_Y","[Y]+[BUFF_DIST]*.707","VB","#")

arcpy.SelectLayerByAttribute_management(inlyr,"NEW_SELECTION","[AT_ROAD_KDOT_DIRECTION] = 'SE'")
arcpy.CalculateField_management(inlyr,"Accident_X","[X]+[BUFF_DIST]*.707","VB","#")
arcpy.CalculateField_management(inlyr,"Accident_Y","[Y]-[BUFF_DIST]*.707","VB","#")

arcpy.SelectLayerByAttribute_management(inlyr,"NEW_SELECTION","[AT_ROAD_KDOT_DIRECTION] = 'SW'")
arcpy.CalculateField_management(inlyr,"Accident_X","[X]-[BUFF_DIST]*.707","VB","#")
arcpy.CalculateField_management(inlyr,"Accident_Y","[Y]-[BUFF_DIST]*.707","VB","#")

#Make table view, locate XY, check

arcpy.MakeTableView_management(inlyr,inlyr+"_tbl","#","#","#")
arcpy.MakeXYEventLayer_management(inlyr+"_tbl","Accident_X","Accident_Y","Accident_Locations", wgs, "#")

arcpy.FeatureClassToFeatureClass_conversion("Accident_Locations", GCContainer, "Offset_accidents","#","#","#")
inlyr = 'Offset_accidents'
#snap the accidents offset XY location to the nearest street
arcpy.Near_analysis(inlyr,"GIS.Streets","0.5 Miles","LOCATION","ANGLE")
arcpy.MakeTableView_management(inlyr,inlyr+"_tbl","#","#","#")
arcpy.MakeXYEventLayer_management(inlyr+"_tbl","NEAR_X","NEAR_Y","Accident_Locations_OnRoad", wgs, "#")

#Consider a check for near distance here and flag for distance values greater than a threshhold. 
#This is not needed based on the distance parameter I put in testing at 0.5 miles.
#might want the user to for check the offset distance vs the near distance
#query on road accident field vs snapped to road name... if different, handle 

#spatial join - took 1 hour for Topeka offset points, this gets us the ON ROAD vs the NEAREST ROAD that we are snapped to
arcpy.SpatialJoin_analysis("Accident_Locations_OnRoad","streets",GCContainer+"/Offset_accidents_CHECK","JOIN_ONE_TO_ONE","KEEP_ALL","#","INTERSECT","#","#")
#if it still takes this long, might try some other methods to get this information built

#query and display records where the ON ROAD isnt the road the point is snapped to.
arcpy.MakeFeatureLayer_management("Offset_accidents_CHECK","Offset_accidents_CHECK_Layer","[ON_ROAD_KDOT_NAME] NOT LIKE [NAME]","#","#")
#Topeka has 206 records, a majority of which had tied matching to begin with.  
#some of the other ones have long offsets more might need to be reviewed more
#One option from this point could be to generate a proximity near table for comparison of the on road locaions...



