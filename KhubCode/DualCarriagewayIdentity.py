'''
Created on Oct 14, 2015

This script identifies primary and non primary direction of dual carriageway centerlines 
it is based on geometric relationship between the dual carraigeway and the KDOT centerline 

a point is created at the center of each dual carriageway (NG911) road centerline segment
points located along a non-primary direction highway (KDOT State Highways) are selected
point offset distance and direction from the centerline is measured
Offset direction and distance are used to flag the NG911 primary and non-primary directions

The result of this script exports to the SQL server database, but does not make changes to the roadcenterline feature class
Review the resulting output then:
    
use SQL management studio and calculate the LRS keys to correct for the secondary direction using a SQL update query like the one at
F:\Cart\projects\Conflation\SQL\SQLServer\Conflation2012\KHUB  is where that SQL query lives, its the "Calculate Non Primary Direction"  SQL file
or... script a pymssql cursor someday when time is abundant

Assumptions:
divided routes in NG911 are represented with Dual Carriageway
The carraigway representations exist on either side of the centerline representation

Steps captured from G:\GISdata\MXD\2016010602_ConflationII_Primary Direction Calculator.mxd gp history

revised in G:\GISdata\MXD\2016010301_ConflationR6 Dual Carriagway Directions.mxd

modified 7/21/2016
modified 1/3/2017
modified 2/14/2017 - changed function names, added function to handle NUSYS routes

@author: kyleg
'''
from KhubCode.EliminateOverlaps import roadcenterlines

#source information:
#this is the path to the Conflation road centerlines - all of them

GeodatabaseName = r"Conflation"
ConflationDatabase  = r"Database Connections/"+GeodatabaseName+"2012_sde.sde"
Roads = ConflationDatabase + "\\" + GeodatabaseName +".SDE.NG911\\"+GeodatabaseName+".SDE.RoadCenterlines"
#Roads = r"\\gisdata\planning\Cart\projects\Conflation\GIS_DATA\GEO_COMM\STATEWIDE_20170212\STATEWIDE_20170212.gdb\NG911\RoadCenterlines"


#here are the GIS routes with measures extracted regularly from EXOR using the FME extraction and 
#python route reference tools from DT00ar60 - #  all routes in all directions including riders
CRND = r'Database Connections\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.CRND'
SRND = r'Database Connections\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.SRND'
NSND = r'Database Connections\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.NSND'


from arcpy import (DeleteRows_management, LocateFeaturesAlongRoutes_lr, SelectLayerByLocation_management, MakeRouteEventLayer_lr,  SelectLayerByAttribute_management, env,
                   MakeFeatureLayer_management, FeatureVerticesToPoints_management, FeatureClassToFeatureClass_conversion, Delete_management, SpatialJoin_analysis)

env.overwriteOutput = 1
#MakeFeatureLayer_management(Roads, "RoadCenterlines")
MakeFeatureLayer_management(Roads, "RoadCenterlinesSS", "LRS_ROUTE_PREFIX in ('I', 'U', 'K')")
MakeFeatureLayer_management(Roads, "RoadCenterlinesC", "LRS_ROUTE_PREFIX in ('C')")
#load those centerlines to in memory workspace, then itereate the function here, develop script and test

def main():
    DirectionalUrbanClass()   
    #DirectionalStateSys()

def DirectionalUrbanClass():
    #do the same as for State Sys but for Non State Urban Classified Highways (Nusys)
    FeatureVerticesToPoints_management("RoadCenterlinesC", "in_memory/UrbanPoints", "MID")
    FeatureClassToFeatureClass_conversion(NSND, "in_memory", "NSND_NPD", where_clause="NETWORK_DIRECTION IN ( 'SB' , 'WB' )")
    LocateFeaturesAlongRoutes_lr("UrbanPoints", "NSND_NPD", "NE_UNIQUE", "200 Feet", "in_memory/UrbanPointsMeasures", "RID POINT MEAS", "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    Delete_management("UrbanPoints")
    #is the query stil valid for non state system?  Explore hte NE Unique.  State System did not use the county number prefix
    

    SelectLayerByAttribute_management("UrbanPointsMeasures", "NEW_SELECTION", """SUBSTRING( "RID", 4, 7) NOT  LIKE SUBSTRING("NON_State_System_LRSKey" ,4, 7)""")

    DeleteRows_management(in_rows="UrbanPointsMeasures")
    MakeRouteEventLayer_lr("NSND_NPD", "NE_UNIQUE", "UrbanPointsMeasures", "rid POINT MEAS", "UrbanPointEvents", offset_field="Distance", add_error_field="ERROR_FIELD", add_angle_field="ANGLE_FIELD", angle_type="NORMAL", complement_angle="ANGLE", offset_direction="RIGHT", point_event_type="POINT")
    MakeFeatureLayer_management("UrbanPointEvents", "UNPD_ID", """"Distance">=0""")
    SelectLayerByLocation_management("UNPD_ID", "INTERSECT", "RoadCenterlinesC", "1 Feet", "NEW_SELECTION")
    
    #at this point, there are a lot of false positives, places with single carriagway roads and nusys divided
    #we need to incorporate the check overlap process to identify where their are single and dual carriagways here
    #starting with the technique to find sausages or dual carraigeways
    #SpatialJoin_analysis("UNPD_ID", "RoadCenterlinesC", "in_memory/ValidateSausages120", "JOIN_ONE_TO_ONE", "KEEP_ALL", '#', "INTERSECT", "120 Feet", "Distance")
    
    #this Spatial Join step is improving the results, removing most false positives.  It still shows overlapping segments 
    #it would be improved even more, potentially, by testing the non-primary direction against dissolve somehow.  
    #except, the calculate method is by segment to the source, a dissolve would complicate the process of calculating back to the source data
    #we are looking for count grater than 0 of the offset point to hte segment, so a dissolved segment should work
    import EliminateOverlaps
    from EliminateOverlaps import CollectorDissolve
    #set the roadcenterline input and dissolve output for RoadCenterline dissolve for this subroutine
    roadcenterlines = "RoadCenterlinesC"
    ClassOutput = r"in_memory/RMC2"
    CollectorDissolve()
    SpatialJoin_analysis("UNPD_ID", "RMC2dissolve", "in_memory/ValidateSausages120", "JOIN_ONE_TO_ONE", "KEEP_ALL", '#', "INTERSECT", "120 Feet", "Distance")
    #Results look great!
    #FeatureClassToFeatureClass_conversion("UNPD_ID", ConflationDatabase + "\\" +GeodatabaseName+".SDE.KANSAS_DOT", "Non_Primary_Divided_C_Route", '"Distance">=0')
    
    
def DirectionalStateSys():
    #make a point at the center of each line segment for a highway
    #No way currently to do this for RML highways,  NUSYS provides the directional layer for C highwyas
    #FeatureToPoint_management("State Highways", "in_memory/HighwayPoints", "INSIDE")
    #maybe two ways to do this, this time, I'm using midpoint from feature to point - catch 
    FeatureVerticesToPoints_management("RoadCenterlinesSS", "in_memory/HighwayPoints", "MID")
    
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
    SelectLayerByLocation_management("NPD_ID", "INTERSECT", "RoadCenterlinesSS", "1 Feet", "NEW_SELECTION")
    
    #sometimes (center turn lanes, left turn lanes, painted medians, median terminus locations) 
    #there is a difference between what KDOT says is Divided and the dual carriagway geometry.
    #Consider this and determine how to handle divided highways in the route Keys/route structures.  
    #this next step will only factor in the 

    FeatureClassToFeatureClass_conversion("NPD_ID", ConflationDatabase + "\\" +GeodatabaseName+".SDE.KANSAS_DOT", "Non_Primary_Divided_Highway", '"Distance">=0')
    
    #select the secondary direction segments
    #SelectLayerByLocation_management(in_layer="State Highways", overlap_type="INTERSECT", select_features="HighwayPoints_SEcondaryDirections", search_distance="0 Feet", selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")
    
    # calculate the direction column with a "1", temporarily indicating that these routes are secondary direction
    
    
main()



    
    