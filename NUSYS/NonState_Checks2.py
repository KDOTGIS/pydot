'''
Created on Sep 10, 2015

@author: kyleg
'''
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
                   MakeTableView_management, AddJoin_management, Buffer_analysis, FlipLine_edit, RemoveJoin_management, GetParameterAsText, 
                   AddIndex_management, TableToTable_conversion, SelectLayerByAttribute_management)
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


def CreateNUSYSLocal():
    MakeFeatureLayer_management(NonState, "NonState", "(LRS_KEY LIKE '%C%' OR LRS_ROUTE_PREFIX = 'C') AND (MILEAGE_COUNTED = -1 OR SURFACE = 'Propose')")
    
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

def CreateNonStateRoutes():
    FeatureClassToFeatureClass_conversion(in_features="Database Connections/SDEPROD_SHARED.sde/SHARED.NON_STATE_SYSTEM", out_path="C:/temp/Nusys_Check.gdb", out_name="Non_State_System", where_clause="", field_mapping="#", config_keyword="")
    NonState = r"C:/temp/Nusys_Check.gdb/Non_State_System"
    MakeFeatureLayer_management(NonState, "NonState", "MILEAGE_COUNTED = -1 AND SURFACE NOT LIKE 'Propose'")
    MakeFeatureLayer_management(NonState, "BackwardSegs", "LRS_BACKWARDS = -1")
    FlipLine_edit("BackwardSegs") 
    CreateRoutes_lr("NonState", "LRS_KEY", destdb+"\Route", "TWO_FIELDS", "LRS_BEG_CNTY_LOGMILE", "LRS_BEG_CNTY_LOGMILE", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    #Flip them back to the original direction
    FlipLine_edit(in_features="BackwardSegs") 
# need to add some logic to check for Local LRS Keys, 

def CheckRouteShapeLength():
    print "CreateNUSYSLocal() is a prerequisite function to this one "
    print "creating Non_State_Routes by the Shape Length"
    MakeFeatureLayer_management("C:/temp/Nusys_Check.gdb/Non_State_Classified", "BackwardSegs", "LRS_BACKWARDS = -1 AND (MILEAGE_COUNTED = -1 OR SURFACE = 'Propose')")
    FlipLine_edit("BackwardSegs") 
    Dissolve_management("Non_State_Classified", "C:/TEMP/Nusys_Check.gdb/TotalRouteShapeLength", "LRS_KEY", "", "MULTI_PART", "DISSOLVE_LINES")
    AddField_management("TotalRouteShapeLength", "Mileage", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management("TotalRouteShapeLength", "Mileage", "Round([Lineargeometry_Length] /5280, 3)", "VB", "")
    AddField_management("TotalRouteShapeLength", "Zero", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management("TotalRouteShapeLength", "Zero", "0", "VB", "")

    #MakeFeatureLayer_management(in_features="C:/temp/Nusys_Check.gdb/TotalRouteShapeLength", out_layer="ForwardRoutes", where_clause="LRS_BACKWARDS = 0")

    CreateRoutes_lr("TotalRouteShapeLength", "LRS_KEY", destdb+"\ShapeLengthRoute", "TWO_FIELDS", "Zero", "Mileage", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    #Flip them back to the original direction
    FlipLine_edit(in_features="BackwardSegs") 
    LocateFeaturesAlongRoutes_lr("Non_State_Classified", "ShapeLengthRoute", "LRS_KEY", "0 Feet", "C:/temp/Nusys_Check.gdb/NON_STATE_EVENTS", "RID LINE FMEAS TMEAS", "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    AddField_management("NON_STATE_EVENTS", "AdjBegin", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("NON_STATE_EVENTS", "AdjEnd", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("NON_STATE_EVENTS", "ADJ_BEGLOG","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("NON_STATE_EVENTS", "ADJ_ENDLOG","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("NON_STATE_EVENTS", "ADJ_LENGTH","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("NON_STATE_EVENTS", "CHANGE","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    
    CalculateField_management(in_table="NON_STATE_EVENTS", field="AdjBegin", expression="round( [FMEAS] ,3)", expression_type="VB", code_block="")
    CalculateField_management(in_table="NON_STATE_EVENTS", field="AdjEnd", expression="round( [TMEAS] ,3)", expression_type="VB", code_block="")
    CalculateField_management(in_table="NON_STATE_EVENTS", field="ADJ_BEGLOG", expression="[AdjBegin] - [LRS_BEG_CNTY_LOGMILE]", expression_type="VB", code_block="")
    CalculateField_management(in_table="NON_STATE_EVENTS", field="ADJ_ENDLOG", expression="[AdjEnd] - [LRS_END_CNTY_LOGMILE]", expression_type="VB", code_block="")
    CalculateField_management(in_table="NON_STATE_EVENTS", field="ADJ_LENGTH", expression="[AdjEnd] - [AdjBegin]", expression_type="VB", code_block="")
    CalculateField_management(in_table="NON_STATE_EVENTS", field="CHANGE", expression="[LENGTH] - [ADJ_LENGTH]", expression_type="VB", code_block="")
       
    MakeRouteEventLayer_lr("ShapeLengthRoute", "LRS_KEY", "NON_STATE_EVENTS", "rid LINE fmeas tmeas", "LRS_Review_Events", "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
# add a function to write the adjusted beglog and end log back to the NON_STATE_SYSTEM FC in Oracle

def UpdateGISPROD_NON_STATE_Check():

    print "what route number should be updated?"
    try:
        RID = GetParameterAsText(0)
    except:
        RID = '460C0387500W0'
    RIDExp = "RID = '"+RID+"'"
    MakeTableView_management(r"C:\temp\Nusys_Check.gdb\NON_STATE_EVENTS", "UpdateGISPROD","#", "in_memory")
    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "UpdateGISPROD"
    TableToTable_conversion(in_rows="UpdateGISPROD", out_path="in_memory", out_name="updatetblh", RIDExp, "#", config_keyword="")
    AddIndex_management("updatetblh", "FID_NON_STATE_SYSTEM", "ID2", "UNIQUE", "ASCENDING")
    MakeFeatureLayer_management(NonState, "NonStateAll")
    AddJoin_management("NonStateAll", "ID2", "updatetblh", "FID_NON_STATE_SYSTEM", "KEEP_COMMON")
    print "Check the numbers one more time, and review"
    print "start Edit session on NON_STATE_SYSTEM now and type /'Calc()/' if it all looks good "

def Calc():
    SelectLayerByAttribute_management(in_layer_or_view="NonStateAll", selection_type="NEW_SELECTION", where_clause="1=1")
    CalculateField_management("NonStateAll", "SHARED.NON_STATE_SYSTEM.LRS_BEG_CNTY_LOGMILE", "[updatetblh.AdjBegin]", "VB", "")
    CalculateField_management("NonStateAll", "SHARED.NON_STATE_SYSTEM.LRS_END_CNTY_LOGMILE", "[updatetblh.AdjEnd]", "VB", "")
    print "adjusted begin and end logmiles were recalculated to the source GISPROD database"
    print "end your edit session"
# Need to call the specific UAB and/or LRS KEY to update 
# ie Enter a Layer (restricted) to UPDATE to prevent update of the entire dataset 

# need a node layer, with node ID, and a script to chain begin/end node IDs to segmentation.  Bill does this now.  Bill has node values in a table - ask bill about the "Nodes".   

CreateNUSYSLocal()
CheckRouteShapeLength()
print "script completed successfully"
