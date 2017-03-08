'''
Created on Oct 14, 2015

This script identifies primary and non primary direction of dual carriageway centerlines 
it is based on geometric relationship between the dual carraigeway and the KDOT centerline 

a point is created at the center of each dual carriageway (NG911) road centerline segment
points located along a non-primary direction highway (KDOT State Highways) are selected
point offset distance and direction from the centerline is measured
Offset direction and distance are used to flag the NG911 primary and non-primary directions

Assumptions:
divided routes in NG911 are represented with Dual Carriageway
The carraigway representations exist on either side of the centerline representation

Steps captured from G:\GISdata\MXD\2016010602_ConflationII_Primary Direction Calculator.mxd gp history

revised in G:\GISdata\MXD\2016010301_ConflationR6 Dual Carriagway Directions.mxd

modified 7/21/2016
modified 1/3/2017

@author: kyleg
'''

#source information:
#this is the path to the Conflation road centerlines - all of them

GeodatabaseName = r"ConflationR6"
ConflationDatabase  = r"Database Connections/"+GeodatabaseName+"_sde.sde"
Roads = ConflationDatabase + "\\" + GeodatabaseName +".SDE.NG911\\"+GeodatabaseName+".SDE.RoadCenterlines"


#here are the GIS routes with measures extracted regularly from EXOR using the FME extraction and 
#python route reference tools from DT00ar60 - #  all routes in all directions including riders
CRND = r'Database Connections\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.CRND'
SRND = r'Database Connections\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.SRND'


from arcpy import (DeleteRows_management, LocateFeaturesAlongRoutes_lr, SelectLayerByLocation_management, MakeRouteEventLayer_lr,  SelectLayerByAttribute_management, env,
                   MakeFeatureLayer_management, FeatureVerticesToPoints_management, FeatureClassToFeatureClass_conversion, Delete_management)

env.overwriteOutput = 1
MakeFeatureLayer_management(Roads, "RoadCenterlines")

#load those centerlines to in memory workspace, then itereate the function here, develop script and test
def SecondaryDirectionFinder():
    #make a point at the center of each line segment for a highway
    #No way currently to do this for RML highways,  NUSYS provides the directional layer for C highwyas
    #FeatureToPoint_management("State Highways", "in_memory/HighwayPoints", "INSIDE")
    #maybe two ways to do this, this time, I'm using midpoint from feature to point - catch 
    FeatureVerticesToPoints_management("RoadCenterlines", out_feature_class="in_memory/HighwayPoints", point_location="MID")
    #FeatureToPoint_management(Roads, "in_memory/HighwayPoints", "INSIDE")
    FeatureClassToFeatureClass_conversion(SRND, "in_memory", "SRND_NPD", where_clause="NETWORK_DIRECTION IN ( 'SB' , 'WB' )")
    
    #CRND Secondary Direction is the CRND layer where "NETWORK_DIRECTION IN ( 'SB' , 'WB' )" 
    #Locate Features Along Routes will calculate a +/- offset distance of the dual carriageway points from the CRND centerline
    LocateFeaturesAlongRoutes_lr("HighwayPoints", "SRND_NPD", "NE_UNIQUE", "500 Feet", "in_memory/HighwayPointsMeasures", "RID POINT MEAS", "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    
    #All the Highway Points are no longer needed and can be freed from memory
    Delete_management("HighwayPoints")
     
    #since we located along all routes instead of the nearest routes, we need to select the rows that have the correct LRS key 
    #SelectLayerByAttribute_management("in_memory/HighwayPointsMeasures", "NEW_SELECTION", """SUBSTRING( "RID", 1, 7) NOT  LIKE SUBSTRING("StateKey1", 4, 7)""")
    
    
    #Using State_System_LRSKey from Conflation just in case the StateKey1 has not yet been added or calculated.  
    SelectLayerByAttribute_management("HighwayPointsMeasures", "NEW_SELECTION", """SUBSTRING( "RID", 1, 7) NOT  LIKE SUBSTRING("State_System_LRSKey" ,4, 7)""")
    DeleteRows_management(in_rows="HighwayPointsMeasures")
    # point events are located along the routes that KDOT says are divided on the dual carriageway
    MakeRouteEventLayer_lr("SRND_NPD", "NE_UNIQUE", "HighwayPointsMeasures", "rid POINT MEAS", "HighwayPointEvents", offset_field="Distance", add_error_field="ERROR_FIELD", add_angle_field="ANGLE_FIELD", angle_type="NORMAL", complement_angle="ANGLE", offset_direction="RIGHT", point_event_type="POINT")

    #select the secondary direction points based on the offset direction
    MakeFeatureLayer_management("HighwayPointEvents", "NPD_ID", """"Distance">=0""")
    
    # some random points, due to the 500 ft buffer I think, are getting included.  Select the event points that do not intersect a state highway road centerline feature 
    #
    SelectLayerByLocation_management("NPD_ID", "INTERSECT", "RoadCenterlines", "1 Feet", "NEW_SELECTION")

    #sometimes (center turn lanes, left turn lanes, painted medians, median terminus locations) 
    #there is a difference between what KDOT says is Divided and the dual carriagway geometry.
    #Consider this and determine how to handle divided highways in the route Keys/route structures.  
    #this next step will only factor in the 

    FeatureClassToFeatureClass_conversion("NPD_ID", ConflationDatabase + "\\" +GeodatabaseName+".SDE.KANSAS_DOT", "Non_Primary_Divided_Highway", '"Distance">=0')
    #select the secondary direction segments
    #SelectLayerByLocation_management(in_layer="State Highways", overlap_type="INTERSECT", select_features="HighwayPoints_SEcondaryDirections", search_distance="0 Feet", selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")
    
    # calculate the direction column with a "1", temporarily indicating that these routes are secondary direction
    
    
    
SecondaryDirectionFinder()   

 #CalculateField_management(in_table="State Highways", field="KDOT_DIRECTION_CALC", expression="1", expression_type="VB", code_block="")
    
    # now go to SQL managemetn studio and calculate the LRS keys to correct for the secondary direction
    # #  F:\Cart\projects\Conflation\SQL\SQLServer\Conflation2012\KHUB  is where that SQL query lives, its the "Calculate Non Primary Direction"  SQL file
    
    