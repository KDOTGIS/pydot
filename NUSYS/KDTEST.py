'''
Created on Sep 24, 2015

@author: kyleg
'''
'''
Created on Sep 10, 2015

@author: kyleg
'''

print "importing functions from arcpy"
from arcpy import (MakeFeatureLayer_management, CreateFileGDB_management, env, LocateFeaturesAlongRoutes_lr, Exists, Delete_management,
                   FeatureClassToFeatureClass_conversion, MakeRouteEventLayer_lr, FeatureToPoint_management, Intersect_analysis,
                   Dissolve_management, DeleteFeatures_management, AddField_management, CalculateField_management, CreateRoutes_lr,Append_management,
                   MakeTableView_management, AddJoin_management, Buffer_analysis, FlipLine_edit, RemoveJoin_management, GetParameterAsText,
                   AddIndex_management, TableToTable_conversion, SelectLayerByAttribute_management, GetCount_management, DeleteRows_management, ListTables)

NUSYS = r"\\gisdata\arcgis\GISdata\Connection_files\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.Nusys"
NonState = r"\\gisdata\arcgis\GISdata\Connection_files\shared@sdeprod.sde\SHARED.NON_STATE_SYSTEM"
StateBnd = r"\\gisdata\arcgis\GISdata\Connection_files\shared@sdeprod.sde\SHARED.STATE_BOUNDARY"
HPMS_DATA = r"\\cansystest\cansys\KDOT\HPMS\Databases\HPMS_EVENT.gdb"

destdb = r"in_memory"
env.overwriteOutput = True

env.workspace = r"in_memory"

def CRB():
    print "querying the shared.NON_STATE_SYSTEM to obtain only urban classified primary C routes with mileage that should be counted and for resolution segments."
    MakeFeatureLayer_management(NonState, "NonStateCP", "((LRS_KEY LIKE '%C%' OR LRS_ROUTE_PREFIX = 'C') AND (MILEAGE_COUNTED = -1)) OR (LRS_DIR_OF_TRAVEL = 'P' and SURFACE = 'Propose')")

    print "querying the shared.NON_STATE_SYSTEM to obtain only urban classified NonPrimary C routes with mileage that should be counted and for resolution segments."
    MakeFeatureLayer_management(NonState, "NonStateCNP", "(LRS_KEY LIKE '%C%' OR LRS_ROUTE_PREFIX = 'C') AND (MILEAGE_COUNTED = 0) AND (LRS_DIR_OF_TRAVEL = 'S') and (COUNTY_NUMBER <> 0)")

    print "shared.Non_State_System has unique IDS that we desire to keep as persistent IDs for comparison with GeoMedia, so we are spatially intersecting the state boundary to keep them as is."
    Buffer_analysis(StateBnd, "State_Boundary_1Mile", "5280 Feet", "FULL", "ROUND", "NONE", "", "PLANAR")
    MakeFeatureLayer_management("State_Boundary_1Mile", "StateBnd" )
    Intersect_analysis("NonStateCP #;StateBnd #", "Non_State_Classified_Primary", "ALL", "-1 Unknown", "LINE")
    Intersect_analysis("NonStateCNP #;StateBnd #", "Non_State_Classified_NonPrimary", "ALL", "-1 Unknown", "LINE")

    NonStateCP_fx = r'Non_State_Classified_Primary'
    NonStateCNP_fx = r'Non_State_Classified_NonPrimary'

    MakeFeatureLayer_management(NonStateCP_fx, "Non_State_Classified_Primary" )
    MakeFeatureLayer_management(NonStateCNP_fx, "Non_State_Classified_NonPrimary" )

    CP_ET = 'CP_NON_STATE_EVENTS'
    CNP_ET = 'CNP_NON_STATE_EVENTS'

    MakeFeatureLayer_management(NUSYS, "Nusys_Extract", "NSEC_SUB_CLASS <> 'R'" )

    print "creating primary C Non_State_Routes by the Shape Length"
    MakeFeatureLayer_management("Non_State_Classified_Primary", "BackwardSegsCP", "LRS_BACKWARDS = -1 AND (MILEAGE_COUNTED = -1 OR (LRS_DIR_OF_TRAVEL = 'P' and SURFACE = 'Propose'))")
    FlipLine_edit("BackwardSegsCP")
    Dissolve_management("Non_State_Classified_Primary", "CPRouteShapeLength", "NQR_DESCRIPTION", "", "MULTI_PART", "DISSOLVE_LINES")
    AddField_management("CPRouteShapeLength", "BCM", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management("CPRouteShapeLength", "BCM", "0", "VB", "")
    AddField_management("CPRouteShapeLength", "ECM", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management("CPRouteShapeLength", "ECM", "!Shape.length@miles!", "Python")

    CreateRoutes_lr("CPRouteShapeLength", "NQR_DESCRIPTION", destdb+"\CP_ShapeLengthRoute", "TWO_FIELDS", "BCM", "ECM", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    #Flip them back to the original direction
    FlipLine_edit(in_features="BackwardSegsCP")
    LocateFeaturesAlongRoutes_lr("Non_State_Classified_Primary", "CP_ShapeLengthRoute", "NQR_DESCRIPTION", "0 Feet", "CP_NON_STATE_EVENTS", "RID LINE FMEAS TMEAS", "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    AddField_management("CP_NON_STATE_EVENTS", "AdjBegin", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CP_NON_STATE_EVENTS", "AdjEnd", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CP_NON_STATE_EVENTS", "CHG_BEGLOG","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CP_NON_STATE_EVENTS", "CHG_ENDLOG","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CP_NON_STATE_EVENTS", "NEW_BEGLOG","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CP_NON_STATE_EVENTS", "NEW_ENDLOG","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CP_NON_STATE_EVENTS", "AdjLength","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CP_NON_STATE_EVENTS", "CHANGE","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    CalculateField_management("CP_NON_STATE_EVENTS", "AdjBegin", "round( [FMEAS] , 3 )", "VB", code_block="")
    CalculateField_management("CP_NON_STATE_EVENTS", "AdjEnd", "round( [TMEAS] , 3 )", "VB", code_block="")
    CalculateField_management("CP_NON_STATE_EVENTS", "CHG_BEGLOG", "[AdjBegin] - [LRS_BEG_CNTY_LOGMILE]", "VB", code_block="")
    CalculateField_management("CP_NON_STATE_EVENTS", "CHG_ENDLOG", "[AdjEnd] - [LRS_END_CNTY_LOGMILE]", "VB", code_block="")
    CalculateField_management("CP_NON_STATE_EVENTS", "NEW_BEGLOG", "[AdjBegin]", "VB", code_block="")
    CalculateField_management("CP_NON_STATE_EVENTS", "NEW_ENDLOG", "[AdjEnd]", "VB", code_block="")
    CalculateField_management("CP_NON_STATE_EVENTS", "AdjLength", "[AdjEnd] - [AdjBegin]", "VB", code_block="")
    CalculateField_management("CP_NON_STATE_EVENTS", "CHANGE", "abs([LENGTH] - [AdjLength])", "VB", code_block="")

    MakeRouteEventLayer_lr("CP_ShapeLengthRoute", "NQR_DESCRIPTION", "CP_NON_STATE_EVENTS", "RID LINE FMEAS TMEAS", "CP_LRS_Review_Events", "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
    print "CP-Rte Builder script completed successfully"

    print "creating NonPrimary C Non_State_Routes by the Shape Length"
    MakeFeatureLayer_management("Non_State_Classified_NonPrimary", "BackwardSegsCNP", "LRS_BACKWARDS = -1 AND LRS_DIR_OF_TRAVEL = 'S' and COUNTY_NUMBER <> 0")
    FlipLine_edit("BackwardSegsCNP")
    Dissolve_management("Non_State_Classified_NonPrimary", "CNPRouteShapeLength", "LRS_KEY", "", "MULTI_PART", "DISSOLVE_LINES")
    AddField_management("CNPRouteShapeLength", "BCM", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management("CNPRouteShapeLength", "BCM", "0", "VB", "")
    AddField_management("CNPRouteShapeLength", "ECM", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management("CNPRouteShapeLength", "ECM", "!Shape.length@miles!", "Python")

    CreateRoutes_lr("CNPRouteShapeLength", "LRS_KEY", destdb+"\CNP_ShapeLengthRoute", "TWO_FIELDS", "BCM", "ECM", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    #Flip them back to the original direction
    FlipLine_edit(in_features="BackwardSegsCNP")
    LocateFeaturesAlongRoutes_lr("Non_State_Classified_NonPrimary", "CNP_ShapeLengthRoute", "LRS_KEY", "0 Feet", "CNP_NON_STATE_EVENTS", "RID LINE FMEAS TMEAS", "FIRST", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    AddField_management("CNP_NON_STATE_EVENTS", "AdjBegin", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CNP_NON_STATE_EVENTS", "AdjEnd", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CNP_NON_STATE_EVENTS", "CHG_BEGLOG","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CNP_NON_STATE_EVENTS", "CHG_ENDLOG","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CNP_NON_STATE_EVENTS", "NEW_BEGLOG","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CNP_NON_STATE_EVENTS", "NEW_ENDLOG","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CNP_NON_STATE_EVENTS", "AdjLength","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CNP_NON_STATE_EVENTS", "CHANGE","DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    CalculateField_management("CNP_NON_STATE_EVENTS", "AdjBegin", "round( [FMEAS] , 3 )", "VB", "")
    CalculateField_management("CNP_NON_STATE_EVENTS", "AdjEnd", "round( [TMEAS] , 3 )", "VB", "")
    CalculateField_management("CNP_NON_STATE_EVENTS", "CHG_BEGLOG", "[AdjBegin] - [LRS_BEG_CNTY_LOGMILE]", "VB", "")
    CalculateField_management("CNP_NON_STATE_EVENTS", "CHG_ENDLOG", "[AdjEnd] - [LRS_END_CNTY_LOGMILE]", "VB", "")
    CalculateField_management("CNP_NON_STATE_EVENTS", "NEW_BEGLOG", "[AdjBegin]", "VB", "")
    CalculateField_management("CNP_NON_STATE_EVENTS", "NEW_ENDLOG", "[AdjEnd]", "VB", "")
    
    CalculateField_management("CNP_NON_STATE_EVENTS", "AdjLength", "[AdjEnd] - [AdjBegin]", "VB", code_block="")
    CalculateField_management("CNP_NON_STATE_EVENTS", "CHANGE", "abs([LENGTH] - [AdjLength])", "VB", code_block="")

    MakeRouteEventLayer_lr("CNP_ShapeLengthRoute", "LRS_KEY", "CNP_NON_STATE_EVENTS", "RID LINE FMEAS TMEAS", "CNP_LRS_Review_Events", "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
    AddField_management("CNPRouteShapeLength", "PersistentID", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CNPRouteShapeLength", "Pbeg", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CNPRouteShapeLength", "Pend", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    CalculateField_management("CNPRouteShapeLength", "PersistentID", "!ID2!", "PYTHON_9.3", "")
    TableToTable_conversion("CNPRouteShapeLength", "in_memory", "CNP_Events", "")

    endpoints = ["beg", "end"]
    for pos in endpoints:
        out_event = "CNP_Events_"+pos
        print out_event
        out_lyr = "CNP_Events_Features_"+pos
        print out_lyr
    
        outfield = "P"+pos
        print outfield
        if pos == "beg":
            print "Will locate begin point"
            routesettings = "LRS_KEY POINT BCM"
        else:
            print "locating end point"
            routesettings = "LRS_KEY POINT ECM"
        MakeRouteEventLayer_lr("CNP_ShapeLengthRoute", "LRS_KEY", "CNP_Events", routesettings, out_event, "", "ERROR_FIELD", "ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
        LocateFeaturesAlongRoutes_lr(out_event, "CP_ShapeLengthRoute", "NQR_DESCRIPTION", "500 Feet", out_lyr, "RID POINT MEAS", "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
        AddJoin_management(out_lyr, "PersistentID", "CNPRouteShapeLength", "PersistentID", "KEEP_ALL")
        selexp = out_lyr+".RID <> CNPRouteShapeLength.LRS_KEY"
        print selexp
        SelectLayerByAttribute_management(out_lyr, "NEW_SELECTION", selexp)
        DeleteRows_management(out_lyr)
        RemoveJoin_management(out_lyr)
        AddJoin_management("CNPRouteShapeLength", "PersistentID", out_lyr, "PersistentID", "KEEP_ALL")
        #expression = "[CNP_Events_Features_Begin.MEAS]"
        expression = "["+out_lyr+".MEAS]"
        print expression
        calcfield  = "CNPRouteShapeLength."+outfield
        #CNPRouteShapeLength.Pbeg
        CalculateField_management("CNPRouteShapeLength", calcfield, expression, "VB", "")
        RemoveJoin_management("CNPRouteShapeLength", "")
    
    #test flipped routes and calculate mileage and flip flag    
    AddField_management("CNPRouteShapeLength", "FlipTest", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CNPRouteShapeLength", "Adj_Beg", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("CNPRouteShapeLength", "Adj_End", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    SelectLayerByAttribute_management("CNPRouteShapeLength", "NEW_SELECTION", '"Pbeg" > "Pend"')
    CalculateField_management("CNPRouteShapeLength", "FlipTest", "1", "VB", "")
    CalculateField_management("CNPRouteShapeLength", "Adj_Beg", "!Pend!", "Python", "")
    CalculateField_management("CNPRouteShapeLength", "Adj_End", "!Pbeg!", "Python", "")
    SelectLayerByAttribute_management("CNPRouteShapeLength", "NEW_SELECTION", '"Pbeg" < "Pend"')
    CalculateField_management("CNPRouteShapeLength", "FlipTest", "0", "VB", "")
    CalculateField_management("CNPRouteShapeLength", "Adj_Beg", "!Pbeg!", "Python", "")
    CalculateField_management("CNPRouteShapeLength", "Adj_End", "!Pend!", "Python", "")
    SelectLayerByAttribute_management("CNPRouteShapeLength", "NEW_SELECTION", '"Adj_Beg" <= 0.003')
    CalculateField_management("CNPRouteShapeLength", "Adj_Beg", "0", "Python", "")
    

    print "CNP-Rte Builder script completed successfully"

# add a function to write the adjusted beglog and end log back to the NON_STATE_SYSTEM FC in Oracle

def RouteCheck(RID):
    #when running this function, pass the RID/LRS KEY Value into the function to update the desired RID
    #RID is structured '030C0011800W0'
    #Class should be L, C, or RM
    print "what route number should be updated?"
    #RID = '030C0011800W0'
    Class = RID[3]
    if Class in ("R", "M"):
        Class = "RM"
    else:
        pass
    print RID
    RID_ = RID.replace('-', '_')
    RIDExp = "RID = '"+RID+"'"
    tablename = Class+RID_
    print RIDExp
    print "Updating route "+ str(RID) + " in table "+str(RID_)
    if Exists("UpdateGISPROD"):
        print "this exists"
        pass
    else:
        AddTable = Class+"P_NON_STATE_EVENTS"
        MakeTableView_management(r"in_memory/"+AddTable, tablename+"_view","#")
        MakeFeatureLayer_management(NonState, "NonStateUpdate", "((LRS_KEY LIKE '%C%' OR LRS_ROUTE_PREFIX = 'C') AND (MILEAGE_COUNTED = -1)) OR (LRS_DIR_OF_TRAVEL = 'P' and SURFACE = 'Propose')")

    TableToTable_conversion(tablename+"_view", "in_memory", tablename, RIDExp)
    if str(GetCount_management(tablename)) == '0':
        print "No Records to Calculate"
    else:
        try:
            RemoveJoin_management("NonStateUpdate")
        except:
            print "no NonStateUpdate, creating the NonStateSystem layer"
        MakeFeatureLayer_management(NonState, "NonStateUpdate", "(MILEAGE_COUNTED = -1 OR SURFACE = 'Propose')")
        AddJoin_management("NonStateUpdate", "ID2", tablename, "FID_NON_STATE_SYSTEM", "KEEP_COMMON")
        print "Check the numbers one more time, and review"
        print "start Edit session on NonStateUpdate now and type RouteCalc(RID) if it all looks good"
    print "RteChk script completed successfully"

def RouteCalc(RID):
    Class = RID[3]
    if Class in ("R", "M"):
        Class = "RM"
    else:
        pass
    print RID
    RID_ = RID.replace('-', '_')
    tablename = Class+RID_
    SelectLayerByAttribute_management("NonStateUpdate", "NEW_SELECTION", "1=1")
    CalculateField_management("NonStateUpdate", "SHARED.NON_STATE_SYSTEM.LRS_BEG_CNTY_LOGMILE", "["+tablename+".NEW_BEGLOG]", "VB", "")
    CalculateField_management("NonStateUpdate", "SHARED.NON_STATE_SYSTEM.LRS_END_CNTY_LOGMILE", "["+tablename+".NEW_ENDLOG]", "VB", "")
    CalculateField_management("NonStateUpdate", "SHARED.NON_STATE_SYSTEM.LENGTH", "["+tablename+".AdjLength]", "VB", "")
    print "adjusted begin and end logmiles were recalculated to the source GISPROD database"
    print "end your edit session"
    #Delete_management("in_memory/"+tablename)
    print "RteCalc script completed successfully"

# Need to call the specific UAB and/or LRS KEY to update
# ie Enter a Layer (restricted) to UPDATE to prevent update of the entire dataset
# need a node layer, with node ID, and a script to chain begin/end node IDs to segmentation.  Bill does this now.  Bill has node values in a table - ask bill about the "Nodes".

#--

def MapHPMS_Events():
    env.workspace = HPMS_DATA
    tableList = ListTables()
    
    for table in tableList:
        intable = HPMS_DATA+r"/"+table
        outname = str(table)
        print "table "+ table +" mapping"
        MakeRouteEventLayer_lr("C_Primary_Route", "NQR_DESCRIPTION", intable, "ROUTE_ID LINE END_POINT END_POINT", outname, "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
    
    


CRB()

#RouteCheck('RID')

#RouteCalc('RID')

#--

def RouteFix(RID):
    #when running this function, pass the RID/LRS KEY Value into the function to update the desired RID
    #RID is structured '030C0011800W0'
    #Class should be L, C, or RM
    
    print "what route number should be updated?"
    #RID = '030C0011800W0'
    Class = RID[3]
    if Class in ("R", "M"):
        Class = "RM"
    else:
        pass
    print RID
    RID_ = RID.replace('-', '_')
    tablename = Class+RID_
    
    if RID == "000C":
        RIDExp = "#"
    else:
        RIDExp = "RID = '"+RID+"'"
    
    print "Updating route "+ str(RID)
    if Exists("UpdateGISPROD"):
        pass
    else:
        AddTable = Class+"P_NON_STATE_EVENTS"
        MakeTableView_management("in_memory/"+AddTable, tablename+"_view","#")


    TableToTable_conversion(tablename+"_view", "in_memory", tablename, RIDExp)
    if str(GetCount_management(tablename)) == '0':
        print "No Records to Calculate"
    else:
        try:
            RemoveJoin_management("NonStateUpdate")
        except:
            print "no NonStateUpdate, creating the NonStateSystem layer"
        #AddIndex_management("updatetblh", "FID_NON_STATE_SYSTEM", "ID2", "UNIQUE", "ASCENDING")
        MakeFeatureLayer_management(NonState, "NonStateUpdate", "(MILEAGE_COUNTED = -1 OR SURFACE = 'Propose')")
        AddJoin_management("NonStateUpdate", "ID2", tablename, "FID_NON_STATE_SYSTEM", "KEEP_COMMON")
        print "Check the numbers one more time, and review"
        print "start Edit session on NonStateUpdate now and type RouteCalc(RID) if it all looks good"
    print "RteChk script completed successfully & RteCalc script starting..."

    Class = RID[3]
    if Class in ("R", "M"):
        Class = "RM"
    else:
        pass
    print RID
    tablename = Class+RID
    SelectLayerByAttribute_management("NonStateUpdate", "NEW_SELECTION", "1=1")
    CalculateField_management("NonStateUpdate", "SHARED.NON_STATE_SYSTEM.LRS_BEG_CNTY_LOGMILE", "["+tablename+".NEW_BEGLOG]", "VB", "")
    CalculateField_management("NonStateUpdate", "SHARED.NON_STATE_SYSTEM.LRS_END_CNTY_LOGMILE", "["+tablename+".NEW_ENDLOG]", "VB", "")
    CalculateField_management("NonStateUpdate", "SHARED.NON_STATE_SYSTEM.LENGTH", "["+tablename+".AdjLength]", "VB", "")
    print "adjusted begin and end logmiles were recalculated to the source GISPROD database"
    print "end your edit session"
    #Delete_management("in_memory/"+tablename)"
    print "RteFix script completed successfully"



