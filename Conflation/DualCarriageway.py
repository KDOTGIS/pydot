'''
Created on Oct 14, 2015

Steps captured from G:\GISdata\MXD\2016010602_ConflationII_Primary Direction Calculator.mxd gp history

modified 7/21/2016

@author: kyleg
'''

#source information:
#this is the path to the Conflation road centerlines - all of them


ConflationDatabase  = r"Database Connections/Conflation2012_sde.sde"
Roads = ConflationDatabase + r"\Conflation.SDE.NG911\Conflation.SDE.RoadCenterlines"

#here are the GIS routes with measures extracted regularly from EXOR using the FME extraction and python route reference tools from DT00ar60 - 
#  all routes in all directions including riders
CRND = r'Database Connections\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.CRND'
SRND = r'Database Connections\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.SRND'


from arcpy import (DeleteRows_management, LocateFeaturesAlongRoutes_lr, SelectLayerByLocation_management, MakeRouteEventLayer_lr,  SelectLayerByAttribute_management,
                   MakeFeatureLayer_management, CalculateField_management, FeatureVerticesToPoints_management, FeatureClassToFeatureClass_conversion)

def SecondaryDirectionFinder():
    #make a point at the center of each line segment for a highway
    #No way currently to do this for RML highways,  NUSYS provides the directional layer for C highwyas
    #FeatureToPoint_management("State Highways", "in_memory/HighwayPoints", "INSIDE")
    #maybe two ways to do this, this time, I'm using midpoint from feature to point - catch 
    FeatureVerticesToPoints_management(in_features="RoadCenterlines", out_feature_class="in_memory/HighwayPoints", point_location="MID")
    
    FeatureClassToFeatureClass_conversion(SRND, "in_memory", "SRND_NPD", where_clause="NETWORK_DIRECTION IN ( 'SB' , 'WB' )")
    
    #CRND SEcondary Direction is the CRND layer where "NETWORK_DIRECTION IN ( 'SB' , 'WB' )" 
    #Locate Features Along Routes will calculate a +/- offset distance of the dual carriageway points from the CRND centerline
    LocateFeaturesAlongRoutes_lr("HighwayPoints", "SRND_NPD", "NE_UNIQUE", "500 Feet", "in_memory/HighwayPointsMeasures", "RID POINT MEAS", "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "HighwayPointsMeasures"
    SelectLayerByAttribute_management(in_layer_or_view="HighwayPointsMeasures", selection_type="NEW_SELECTION", where_clause="""SUBSTRING( "RID", 1, 7) NOT  LIKE SUBSTRING("StateKey1", 1, 7)""")

    DeleteRows_management(in_rows="HighwayPointsMeasures")
    
    MakeRouteEventLayer_lr("SRND_NPD", "NE_UNIQUE", "HighwayPointsMeasures", "rid POINT MEAS", "HighwayPointEvents", offset_field="Distance", add_error_field="ERROR_FIELD", add_angle_field="ANGLE_FIELD", angle_type="NORMAL", complement_angle="ANGLE", offset_direction="RIGHT", point_event_type="POINT")
    
    #select the secondary direction points
    MakeFeatureLayer_management("HighwayPointEvents", "NPD_ID", """"Distance">=0""")
    
    
    # some random points, due to the 500 ft buffer I think, are getting included.  Select the event points that do not intersect a state highway road centerline feature 
    #
    SelectLayerByLocation_management(in_layer="NPD_ID", overlap_type="INTERSECT", select_features="RoadCenterlines", search_distance="1 Feet", selection_type="NEW_SELECTION", invert_spatial_relationship="INVERT")

    FeatureClassToFeatureClass_conversion("NPD_ID", "Database Connections/Conflation2012_sde.sde/Conflation.SDE.KANSAS_DOT", "Non_Primary_Divided_Highway", '"Distance">=0')
    #select the secondary direction segments
    #SelectLayerByLocation_management(in_layer="State Highways", overlap_type="INTERSECT", select_features="HighwayPoints_SEcondaryDirections", search_distance="0 Feet", selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")
    
    # calculate the direction column with a "1", temporarily indicating that these routes are secondary direction
    
    #CalculateField_management(in_table="State Highways", field="KDOT_DIRECTION_CALC", expression="1", expression_type="VB", code_block="")
    
    # now go to SQL managemetn studio and calculate the LRS keys to correct for the secondary direction
    # #  F:\Cart\projects\Conflation\SQL\SQLServer\Conflation2012\KHUB  is where that SQL query lives, its the "Calculate Non Primary Direction"  SQL file