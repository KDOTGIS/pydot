'''
Created on Aug 31, 2015

@author: kyleg
'''

if __name__ == '__main__':
    pass

print "importing functions from arcpy"
from arcpy import (MakeFeatureLayer_management, CreateFileGDB_management, env, LocateFeaturesAlongRoutes_lr, Exists, Delete_management, 
                   FeatureClassToFeatureClass_conversion, MakeRouteEventLayer_lr, FeatureToPoint_management, Intersect_analysis,
                   Dissolve_management, DeleteFeatures_management, AddField_management, CalculateField_management, CreateRoutes_lr,Append_management,
                   MakeTableView_management, AddJoin_management, Buffer_analysis, FlipLine_edit, RemoveJoin_management)
NUSYS = r"Database Connections/RO@sqlgisprod_GIS_cansys.sde/GIS_CANSYS.SHARED.Nusys"
NonState = r"Database Connections/SDEPROD_SHARED.sde/SHARED.NON_STATE_SYSTEM"


destdb = r"C:/temp/Nusys_Check.gdb"
env.overwriteOutput = True

try:
    print "re-setting the working geodatabase in C:temp folder"
    if Exists(destdb):
        Delete_management(destdb)
        CreateFileGDB_management(r"C:/TEMP", "Nusys_Check.gdb")
        print "recreated the geodatabase"
    else:
        CreateFileGDB_management(r"C:/TEMP", "Nusys_Check.gdb")
        print "created the new geodatabase"
except:
    CreateFileGDB_management(r"C:/TEMP", "Nusys_Check.gdb")
    print "DB could not be deleted"

env.workspace = r"C:/TEMP/Nusys_Check.gdb"

MakeFeatureLayer_management(NonState, "NonState", "(LRS_KEY like '%C%' OR LRS_ROUTE_PREFIX = 'C') AND MILEAGE_COUNTED = -1")

#NonState System has unique IDS that are also the non_persistent Object ID's
#To force persistence on the Unique IDS, perform an intersect to the state boundary layer
print "buffering the state boundary"
Buffer_analysis(r"Database Connections/SDEPROD_SHARED.sde/SHARED.STATE_BOUNDARY", r"C:/temp/Nusys_Check.gdb/State_Boundary_1Mile", "5280 Feet", "FULL", "ROUND", "NONE", "", "PLANAR")
print "intersecting non_state system to the state boundary to preserve Object ID's and eliminate non-spatial segments"
MakeFeatureLayer_management(r"C:/temp/Nusys_Check.gdb/State_Boundary_1Mile", "StateBnd" )
Intersect_analysis("NonState #;StateBnd #", r"C:/temp/Nusys_Check.gdb/Non_State_Classified", "ALL", "-1 Unknown", "LINE")
print "adding layers to gp workflow or MXD"
NonState_fx = r'C:/temp/Nusys_Check.gdb/Non_State_Classified'

MakeFeatureLayer_management(NUSYS, "Nusys_Extract", "NSEC_SUB_CLASS <> 'R'" )
MakeFeatureLayer_management(NonState_fx, "Non_State_Classified" )

def LinearReferenceCheck():
    print "locating NON_STATE_SYSTEM features along the NUSYS Rotue - creates an event table with Route/begin/end mileage"
    print "the tolerance for this process is 20 feet.  Because this is not an exact process, it is for reference purposes only to compare segmentation mileage"
    print "it looks like unless calculated segment per segment, this will not ever be exact"
    LocateFeaturesAlongRoutes_lr(NonState_fx, NUSYS, "ROUTE", "20 Feet", "Nonstate_Nusys_LFAR", "RID LINE FMEAS TMEAS", "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    MakeRouteEventLayer_lr(in_routes="Nusys_Extract", route_id_field="route", in_table="Nonstate_Nusys_LFAR", in_event_properties="rid LINE fmeas tmeas", out_layer="Nonstate_Nusys_LFAR Events", offset_field="", add_error_field="ERROR_FIELD", add_angle_field="NO_ANGLE_FIELD", angle_type="NORMAL", complement_angle="ANGLE", offset_direction="LEFT", point_event_type="POINT")

def Non_State_Centerpoint_Check():
    MakeFeatureLayer_management(in_features="Database Connections/SDEPROD_SHARED.sde/SHARED.NON_STATE_SYSTEM", out_layer="C_Routes", where_clause="LRS_KEY like '%C%' OR  LRS_ROUTE_PREFIX = 'C'")
    FeatureToPoint_management(NonState_fx, "C_Routes_Point", "INSIDE")
    #LocateFeaturesAlongRoutes_lr(NonState_fx, NUSYS, "ROUTE", "50 Feet", "Nonstate_Point_LFAR", "RID LINE FMEAS TMEAS", "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    Intersect_analysis("Nusys_Extract #;C_Routes #", out_feature_class="C:/temp/Nusys_Check.gdb/C_Routes_Point_Int5", join_attributes="ALL", cluster_tolerance="5 Feet", output_type="POINT")
    
    Dissolve_management("C_Routes_Point_Int5", out_feature_class="C:/temp/Nusys_Check.gdb/C_Routes_Point_Int_Route_Mileage_5D", dissolve_field="ROUTE;DIVIDED_UNDIVIDED;LRS_KEY", statistics_fields="COUNTY_BEGIN_MP MIN;COUNTY_END_MP MAX;LRS_BEG_CNTY_LOGMILE MIN;LRS_END_CNTY_LOGMILE MAX", multi_part="MULTI_PART", unsplit_lines="DISSOLVE_LINES")

    AddField_management(in_table="C_Routes_Point_Int_Route_Mileage_5D", field_name="Check_LRS", field_type="TEXT", field_precision="", field_scale="", field_length="15", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
    CalculateField_management(in_table="C_Routes_Point_Int_Route_Mileage_5D", field="Check_LRS", expression="!LRS_KEY![:11]", expression_type="PYTHON_9.3", code_block="")
    
    AddField_management(in_table="C_Routes_Point_Int_Route_Mileage_5D", field_name="Check_Route", field_type="TEXT", field_precision="", field_scale="", field_length="15", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
    CalculateField_management(in_table="C_Routes_Point_Int_Route_Mileage_5D", field="Check_Route", expression="!Route![:11]", expression_type="PYTHON_9.3", code_block="")    
    
    MakeFeatureLayer_management("C_Routes_Point_Int_Route_Mileage_5D", out_layer="C_Routes_Check_Del", where_clause="Check_Route <> Check_LRS OR Check_Route is null OR Check_LRS is null")
    DeleteFeatures_management("C_Routes_Check_Del")
    
def CheckRouteShapeLength():
    print "creating Non_State_Routes by the Shape Length"
    MakeFeatureLayer_management("C:/temp/Nusys_Check.gdb/Non_State_Classified", "BackwardSegs", "LRS_BACKWARDS = -1 AND MILEAGE_COUNTED = -1")
    FlipLine_edit("BackwardSegs") 
    Dissolve_management("Non_State_Classified", "C:/TEMP/Nusys_Check.gdb/TotalRouteShapeLength", "LRS_KEY", "", "MULTI_PART", "DISSOLVE_LINES")
    AddField_management("TotalRouteShapeLength", "Mileage", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management("TotalRouteShapeLength", "Mileage", "Round([LINEARGEOMETRY_Length] /5280, 3)", "VB", "")
    AddField_management("TotalRouteShapeLength", "Zero", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management("TotalRouteShapeLength", "Zero", "0", "VB", "")

    #MakeFeatureLayer_management(in_features="C:/temp/Nusys_Check.gdb/TotalRouteShapeLength", out_layer="ForwardRoutes", where_clause="LRS_BACKWARDS = 0")

    CreateRoutes_lr("TotalRouteShapeLength", "LRS_KEY", destdb+"\ShapeLengthRoute", "TWO_FIELDS", "Zero", "Mileage", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    #Flip them back to the original direction
    FlipLine_edit(in_features="BackwardSegs") 
    LocateFeaturesAlongRoutes_lr("Non_State_Classified", "ShapeLengthRoute", "LRS_KEY", "0 Feet", "C:/temp/Nusys_Check.gdb/NON_STATE_EVENTS", "RID LINE FMEAS TMEAS", "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    AddField_management("NON_STATE_EVENTS", "CheckBegin", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("NON_STATE_EVENTS", "CheckEnd", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    
    CalculateField_management("NON_STATE_EVENTS", "CheckBegin", "abs(!LRS_BEG_CNTY_LOGMILE!- !FMEAS!)", "PYTHON_9.3", "")
    CalculateField_management("NON_STATE_EVENTS", "CheckEnd", "abs(!LRS_END_CNTY_LOGMILE!- !TMEAS!)", "PYTHON_9.3", "")
   
    MakeRouteEventLayer_lr("ShapeLengthRoute", "LRS_KEY", "NON_STATE_EVENTS", "rid LINE fmeas tmeas", "LRS_Review_Events", "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")

CheckRouteShapeLength()
print "script completed successfully"