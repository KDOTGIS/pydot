'''
Created on Aug 25, 2014

@author: kyleg
'''
#import arcpy
from arcpy import env, GetCount_management, DeleteRows_management, SetLogHistory, da, Intersect_analysis, SelectLayerByAttribute_management, Append_management, LocateFeaturesAlongRoutes_lr, Dissolve_management, MakeFeatureLayer_management, MakeRouteEventLayer_lr, MakeTableView_management, Exists, AddJoin_management, Union_analysis, Delete_management

FMIS_PROJ = r"D:\SCHED\CANT_CPMS.sde\CPMS.CPMS_STAGING_TMP"
FMIS_LOAD = r"D:\SCHED\CANT_CPMS.sde\CPMS.CPMS_HPMS_FMIS_DATA"

#2/24/2015 Terri created views that identify added and deleted rows for regular processing
FMIS_ADD = r"D:\SCHED\CANT_CPMS.sde\CPMS.CPMS_FMIS_GIS_INS_ROWS"
FMIS_DEL = r"D:\SCHED\CANT_CPMS.sde\CPMS.CPMS_FMIS_GIS_DEL_ROWS"



ProjectID = "Project_ID"

ws = r"\\gisdata\arcgis\GISdata\FHWA\HPMS2012\kansas2012\Process.gdb"

env.overwriteOutput=1
env.outputMFlag = 'Disabled'

CountyLyr = r'D:\SCHED\SDEPROD_SHARED.sde\SHARED.Counties'
MPOLyr = r'D:\SCHED\SDEPROD_SHARED.sde\SHARED.MPO_Boundaries'
CONGDistlyr =r'D:\SCHED\GATEPROD.sde\GATE.GATE_US_CONG_2012' 
CPMSlyr =r"D:\SCHED\SQL61_GIS_CANSYS_RO.sde\GIS_CANSYS.DBO.CPMS"
HPMSlyr = r"\\gisdata\arcgis\GISdata\FHWA\HPMS2012\kansas2012\Kansas2012.shp"

#Do this Annually
def Annually():
    #arcpy.MakeFeatureLayer_management(CPMSlyr, 'CPMS', ProjectSelect)
    MakeFeatureLayer_management(CPMSlyr, 'CPMS')
    MakeFeatureLayer_management(CountyLyr, 'County')
    MakeFeatureLayer_management(HPMSlyr, 'HPMS')
    MakeFeatureLayer_management(MPOLyr, 'MPO')
    MakeFeatureLayer_management(CONGDistlyr, 'CONG')
    
    #make the polygon analysis layer for Districts, Counties, and MPOs 
    Union_analysis("CONG #;MPO #;County #",ws+"/Polygons","ALL","1 feet","GAPS")

def FIMS_GIS(FMIS_ADD):
    #arcpy.MakeFeatureLayer_management(CPMSlyr, 'CPMS', ProjectSelect)
    #only process the new rows in FMIS_ADD
    
    MakeFeatureLayer_management(CPMSlyr, 'CPMS')
    MakeFeatureLayer_management(CountyLyr, 'County')
    MakeFeatureLayer_management(HPMSlyr, 'HPMS')
    MakeFeatureLayer_management(MPOLyr, 'MPO')
    MakeFeatureLayer_management(CONGDistlyr, 'CONG')
    MakeFeatureLayer_management(ws+"/Polygons", 'Polygons')
    #make the polygon analysis layer for Districts, Counties, and MPOs 
    #arcpy.Union_analysis("CONG #;MPO #;County #",ws+"/Polygons","ALL","1 feet","GAPS")
    
    MakeTableView_management(FMIS_ADD, 'CPMS_STAGING_TMP')
    AddJoin_management("CPMS","PROJECT_ID","CPMS_STAGING_TMP","PROJECT_NUMBER","KEEP_COMMON")
    
    Output_Event_Table_Properties = 'RID LINE CNTY_BEG CNTY_END'
    
    outtblP = ws+"/FIMS_EventTableAreas"
    outtblH = ws+"/FIMS_EventTableLines"
    
    if Exists(outtblP):
        Delete_management(outtblP)
    
    #consider/testing running "in memory"
    LocateFeaturesAlongRoutes_lr('CPMS', 'HPMS', "Route_ID", "30 Feet", outtblH, Output_Event_Table_Properties, "FIRST", "DISTANCE", "NO_ZERO", "FIELDS", "M_DIRECTON")
    MakeRouteEventLayer_lr("HPMS","Route_ID","FIMS_EventTableLines","rid LINE CNTY_BEG CNTY_END","FIMS_EventTableLineLyr","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
    Intersect_analysis("FIMS_EventTableLineLyr #;HPMS #;Polygons #",ws+"/FMIS_Data","ALL","#","LINE")
    
    Dissolve_management("FMIS_Data",ws+r"/HPMS_Data","PROJECT_ID;F_SYSTEM_V;NHS_VN;DISTRICT_1;COUNTY_NUMBER;ID_1","#","MULTI_PART","UNSPLIT_LINES")
    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
    LocateFeaturesAlongRoutes_lr("HPMS_Data","HPMS","Route_ID","0 Feet",ws+"/FIMS_EventTable","RID LINE CNTY_BEG CNTY_END","FIRST","DISTANCE","NO_ZERO","FIELDS","M_DIRECTON")
    
    # to rerun at this time, we would need to truncate the table FMIS_LOAD
    # we will now run this with the append code incorporated from KTRIPS
    # investigate a method to incorporate delete, updates


def AppendAddedRows():
    #separating append into a separate function may be a good idea, 
    #but now hte function doesn't know what the 'FMIS event table' is
    #altered the append to incorporate the SYSTEM CODE, we are now appending the NHS_VN code to the table as NHS_VN, derive SYSTEM_CODE in Oracle
    Append_management("FIMS_EventTable",FMIS_LOAD,"NO_TEST","""
    ROUTE_ID "ROUTE_ID" true true false 14 Text 0 0 ,First,#,FIMS_EventTable,RID,-1,-1;
    BEG_CNTY_MP "BEG_CNTY_MP" true true false 8 Double 10 38 ,First,#,FIMS_EventTable,CNTY_BEG,-1,-1;
    END_CNTY_MP "END_CNTY_MP" true true false 8 Double 10 38 ,First,#,FIMS_EventTable,CNTY_END,-1,-1;
    CONGRESSIONAL_DISTRICT "CONGRESSIONAL_DISTRICT" true true false 50 Text 0 0 ,First,#,FIMS_EventTable,DISTRICT_1,-1,-1;
    URBAN_ID "URBAN_ID" true true false 10 Text 0 0 ,First,#,FIMS_EventTable,ID_1,-1,-1;
    FUN_CLASS "FUN_CLASS" true true false 3 Text 0 0 ,First,#,FIMS_EventTable,F_SYSTEM_V,-1,-1;
    NHS_VN "NHS_VN" true true false 10 Text 0 0 ,First,#,FIMS_EventTable,NHS_VN,-1,-1;
    PROJECT_NUMBER "PROJECT_NUMBER" true true false 15 Text 0 0 ,First,#,FIMS_EventTable,PROJECT_ID,-1,-1;
    COUNTY "COUNTY" true true false 3 Text 0 0 ,First,#,FIMS_EventTable,COUNTY_NUMBER,-1,-1""","#")
    
def DeleteDeletedRows(FMIS_DEL, FMIS_LOAD):
    #delete rows from the FMIS table programmed to be deleted according to the CPMS view
    MakeTableView_management(FMIS_DEL, "RowstoDelete")
    MakeTableView_management(FMIS_LOAD, "DeleteThese")
    delcount = GetCount(FMIS_DEL)
    #delete rows from SDE CIIMS that are removed from CANSYS CIIMS
    #search cursor to match the crossing ID in the delete view
    SetLogHistory(False)
    DeleteList =[]
    with da.SearchCursor("RowstoDelete", "PROJECT_NUMBER") as delcur:  # @UndefinedVariable
        for row in delcur:
            DelXID=  ("{0}".format(row[0]))
            DeleteList.append(DelXID)
    print "list completed"
    for record in DeleteList:
        #print DelXID + " is being deleted from the FMIS table"
        #add the the crossing ID for the row to be deleted to a selection set
        delsel = "PROJECT_NUMBER LIKE '%s'" %record
        #print delsel
        SelectLayerByAttribute_management("DeleteThese","ADD_TO_SELECTION",delsel)
    #delete the selected rows
    DeleteRows_management("DeleteThese")
    del FMIS_DEL, FMIS_LOAD, delsel
    print "Delete function completed"

    #delete rows 
    
#Need some error handling - need to (just look for errors or place errors in testing)
#Maybe locate routes to add begin/end or other LRS errors
#Need to join and delete rows prior to appending, if the project exists in the output table, need to delete those rows before appending them back in
#Consider adding a process date, it might be helpful in the future.  (oracle side or GP?)
    
#add logging script
    
#FIMS_GIS()
#DeleteDeletedRows(FMIS_DEL, FMIS_LOAD)
#FIMS_GIS(FMIS_ADD)
AppendAddedRows()
