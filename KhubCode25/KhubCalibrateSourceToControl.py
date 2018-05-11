'''
@author: kyleg
reCreated on Mar 7, 2018 
integrated to KhubCode 25 pydev project
modified to work in python 3 environment using arcgis pro
also switched from _mssql to pyodbc using the system DSN connection
updated 3/14/2018 
updated 3/15/2018 - I shouldn't use the workspace from UpdateFileGdb script, since we should calibrate before creating that, added "temp" to the name.  
updated 3/16/2018 - initially tested, working and run on production
updated 4/5/2018 - state system calibrate adjusted to handle iterations of output from 1spatial processing including dissolves, named "..._D1"
updated 5/10/2018 - adding non-state system classified urban and rural spatial calibration
                    need to add flagging to D1 layer in order to identify the routes that flip post calibration
                    
originally reCreated on Feb 7, 2017
Created from Eliminate Overlaps, modifided to work and populate non primary route key
This script prepares the conflation data for route creation
'''
from arcpy.conversion import FeatureClassToFeatureClass
def RM_Calibrate():
    import datetime
    startDateTime = datetime.datetime.now()
    print("starting SHS calibration at "+str(startDateTime)+", it should take about 20 minutes to calibrate non-state system urban and rural classified routes")

    from KhubCode25.KhubCode25Config import devorprod, dbname, dbownername, localProFileGDBWorkspace, KDOTConnections, prodDataSourceSDE, devDataSourceSDE, RuralClassifiedRoutes, UrbanClassifiedRoutes
    
    if devorprod == 'prod':
        database = prodDataSourceSDE

        print("running on "+devorprod)
    else: 
        database = devDataSourceSDE

        print("running on "+devorprod)
    fileformatDateStr = startDateTime.strftime("%Y%m%d") 
    from arcpy import (MakeFeatureLayer_management,
                       FeatureVerticesToPoints_management, LocateFeaturesAlongRoutes_lr, MakeRouteEventLayer_lr, 
                       Dissolve_management, Exists)
                       
    localfilegdb = localProFileGDBWorkspace+'\\'+'KhubRoadCenterlinesTemp'+fileformatDateStr+'.gdb'
    print (localfilegdb)
    sdegdb = KDOTConnections+r'\\'+database+r'\\'+dbname+"."+dbownername
    CalibrateD1 = sdegdb+".All_Road_Centerlines_D1"
    RMRoute = sdegdb+"."+RuralClassifiedRoutes
    Croutes = sdegdb+"."+UrbanClassifiedRoutes
    FeatureClassToFeatureClass(RMRoute, localfilegdb, "RM_Routes")
    nusysprimary = "DIRECTION IN ('EB', 'NB') Or (DIVIDED_UNDIVIDED = 'U' And DIRECTION IN ('SB', 'WB'))"
    FeatureClassToFeatureClass(Croutes, localfilegdb, "C_Routes", nusysprimary)
    
    
    RMRoute = localfilegdb+"."+r"/RM_Routes"
    Croutes = localfilegdb+"."+r"/C_Routes"
    
    MakeFeatureLayer_management(CalibrateD1, "D1_NUSYS", "LRS_ROUTE_PREFIX = 'C'", None, "#")
    MakeFeatureLayer_management(CalibrateD1, "D1_RM", "LRS_ROUTE_PREFIX IN ('M', 'R')", None, "")
    
    print("making endpoints for nusys")
    FeatureVerticesToPoints_management("D1_NUSYS", localfilegdb+r"\Nusys_END", "END")
    FeatureVerticesToPoints_management("D1_NUSYS", localfilegdb+r"\Nusys_START", "START")
    print("making endpoints for rural")
    FeatureVerticesToPoints_management("D1_RM", localfilegdb+r"\RM_END", "END")
    FeatureVerticesToPoints_management("D1_RM", localfilegdb+r"\RM_START", "START")

    print ("Exporting rural event tables")
    LocateFeaturesAlongRoutes_lr(localfilegdb+r"\RM_START", RMRoute, "LRS_KEY", "250 Feet", localfilegdb+r"\START_D1_RM", "LRS_KEY Point RM_MEAS", "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    LocateFeaturesAlongRoutes_lr(localfilegdb+r"\RM_END", RMRoute, "LRS_KEY", "250 Feet", localfilegdb+r"\END_D1_RM", "LRS_KEY Point RM_MEAS", "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    print ("Exporting urban event tables")
    
    print ("starting start c" )
    
    LocateFeaturesAlongRoutes_lr(localfilegdb+r"\Nusys_START", Croutes, "Route", "250 Feet", localfilegdb+r"\START_D1_C", "LRS_KEY Point C_MEAS", "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    print ("starting end c" )
    LocateFeaturesAlongRoutes_lr(localfilegdb+r"\Nusys_END", Croutes, "Route", "250 Feet", localfilegdb+r"\END_D1_C", "LRS_KEY Point C_MEAS", "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
    
    
    MakeRouteEventLayer_lr(RMRoute, "LRS_KEY", localfilegdb+r"\START_D1_RM", "LRS_KEY Point RM_MEAS", "START_D1_RM Events", None, "ERROR_FIELD", "ANGLE_FIELD", "NORMAL", "COMPLEMENT", "LEFT", "POINT")
    MakeRouteEventLayer_lr(RMRoute, "LRS_KEY", localfilegdb+r"\END_D1_RM", "LRS_KEY Point RM_MEAS", "END_D1_RM Events", None, "ERROR_FIELD", "ANGLE_FIELD", "NORMAL", "COMPLEMENT", "LEFT", "POINT")
    
    MakeRouteEventLayer_lr(Croutes, "Route", localfilegdb+r"\START_D1_C", "LRS_KEY Point C_MEAS", "START_D1_C Events", None, "ERROR_FIELD", "ANGLE_FIELD", "NORMAL", "COMPLEMENT", "LEFT", "POINT")
    MakeRouteEventLayer_lr(Croutes, "Route", localfilegdb+r"\END_D1_C", "LRS_KEY Point C_MEAS", "END_D1_C Events", None, "ERROR_FIELD", "ANGLE_FIELD", "NORMAL", "COMPLEMENT", "LEFT", "POINT")
    
    Dissolve_management("START_D1_RM Events", localfilegdb+r"\START_D1_RM_DX", "LRS_KEY;RM_MEAS;KDOT_LRS_KEY", "Distance MIN;Distance MAX;KDOT_STATIC_ID2 FIRST;OBJECTID COUNT;RM_MEAS MIN;RM_MEAS MAX", "MULTI_PART", "DISSOLVE_LINES")
    FeatureClassToFeatureClass(localfilegdb+r"\START_D1_RM_DX", localfilegdb, "START_D1_RM_D", "KDOT_LRS_KEY = LRS_KEY", "#")
    print ("START_D1_RM_D")
    
    Dissolve_management("END_D1_RM Events", localfilegdb+r"\END_D1_RM_DX", "LRS_KEY;RM_MEAS;KDOT_LRS_KEY", "Distance MIN;Distance MAX;KDOT_STATIC_ID2 FIRST;OBJECTID COUNT;RM_MEAS MIN;RM_MEAS MAX", "MULTI_PART", "DISSOLVE_LINES")
    FeatureClassToFeatureClass(localfilegdb+r"\END_D1_RM_DX", localfilegdb, "END_D1_RM_D", "KDOT_LRS_KEY = LRS_KEY", "#")
    print ("END_D1_RM_D")
    
    Dissolve_management("START_D1_C Events", localfilegdb+r"\START_D1_C_DX", "LRS_KEY;C_MEAS;KDOT_LRS_KEY", "Distance MIN;Distance MAX;KDOT_STATIC_ID2 FIRST;OBJECTID COUNT;C_MEAS MIN;C_MEAS MAX", "MULTI_PART", "DISSOLVE_LINES")
    FeatureClassToFeatureClass(localfilegdb+r"\START_D1_C_DX", localfilegdb, "START_D1_C_D", "KDOT_LRS_KEY = LRS_KEY", "#")
    print ("START_D1_C_D")
    
    Dissolve_management("END_D1_C Events", localfilegdb+r"\END_D1_C_DX", "LRS_KEY;C_MEAS;KDOT_LRS_KEY", "Distance MIN;Distance MAX;KDOT_STATIC_ID2 FIRST;OBJECTID COUNT;C_MEAS MIN;C_MEAS MAX", "MULTI_PART", "DISSOLVE_LINES")
    FeatureClassToFeatureClass(localfilegdb+r"\END_D1_C_DX", localfilegdb, "END_D1_C_D", "KDOT_LRS_KEY = LRS_KEY", "#")
    print ("END_D1_C_D")

    print('Calibration process completed in {} hours, minutes, seconds.'.format(datetime.datetime.now()-startDateTime))


def StateHighwayCalibrate():
    import datetime
    startDateTime = datetime.datetime.now()
    print("starting SHS calibration at "+str(startDateTime)+", it should take about 15 minutes to calibrate state system routes")
#Calibration process completed in 0:03:36.252839 hours, minutes, seconds
    from KhubCode25.KhubCode25Config import devorprod, dbname, dbownername, localProFileGDBWorkspace, KDOTConnections, Cmlrs, prodDataSourceSDE, devDataSourceSDE
    fileformatDateStr = startDateTime.strftime("%Y%m%d")
    #theStateHighwaySegments is defined as the roadway segments intended for calibration to the EXOR measures
    if devorprod == 'prod':
        database = prodDataSourceSDE

        print("running on "+devorprod)
    else: 
        database = devDataSourceSDE

        print("running on "+devorprod)
    from arcpy import FeatureClassToFeatureClass_conversion, Delete_management, FeatureVerticesToPoints_management, LocateFeaturesAlongRoutes_lr, CreateFileGDB_management, env, MakeFeatureLayer_management, SelectLayerByAttribute_management, DeleteRows_management, MakeTableView_management  
    env.overwriteOutput=1
    try:
        CreateFileGDB_management(localProFileGDBWorkspace, "KhubRoadCenterlinesTemp"+fileformatDateStr, "CURRENT")
    except:
        Delete_management(localProFileGDBWorkspace, "KhubRoadCenterlinesTemp"+fileformatDateStr)
        CreateFileGDB_management(localProFileGDBWorkspace, "KhubRoadCenterlinesTemp"+fileformatDateStr, "CURRENT")

    #stopped using in_memory after the upgrade to arcgis pro, it doesn't work like it used to do.
    #consider using in memory for not in non-pro script environment, but for this process, probably will not make much difference

    localfilegdb = localProFileGDBWorkspace+'\\'+'KhubRoadCenterlinesTemp'+fileformatDateStr+'.gdb'
    sdegdb = KDOTConnections+r'\\'+database+r'\\'+dbname+"."+dbownername
    firstCut = sdegdb+".All_Road_Centerlines"
    NextIter = "_D1"
    nextCut = firstCut+NextIter
    RoadsToCalibrate = [firstCut, nextCut]

    CMLRS = sdegdb+"."+Cmlrs
    Lrm_Dict = {'COUNTY':CMLRS}
    for sderoads in RoadsToCalibrate:
        if sderoads[-3:] == "_D1":
            MakeFeatureLayer_management(sderoads, "lyrStateSystemSource"+NextIter, "LRS_ROUTE_PREFIX IN ('I', 'U', 'K') And LRS_ROUTE_SUFFIX NOT IN ('Z', 'G')", None, "")
            RoadCenterlines = localfilegdb+"/lyrStateSystemSource"+NextIter
            End_List = ['START', 'END']
                    # First,  create points at the begin and end of each road centerline segment using Vertices to Points.  
            for end in End_List:
                end_name = end+NextIter
                i_end_output = localfilegdb+"/CalibrationPoint"+end_name
                try:
                    FeatureVerticesToPoints_management(RoadCenterlines, i_end_output, str(end))
                    #this works in Pro
                except:
                    FeatureVerticesToPoints_management("lyrStateSystemSource"+NextIter, i_end_output, str(end))
        #and this is the beginning and end of a line, for which we are going to create a vertex point
        #Iterate through the LRMs to bring them into memory and do the processing for each segment begin and end point!  
                for key, value in Lrm_Dict.items():
                    FeatureClassToFeatureClass_conversion(value, localfilegdb, "LRM"+str(key))
                    for end in End_List:
                        outtable = localfilegdb+r"/"+str(end_name)+"_"+str(key)
                        outproperties = str(key)+"_LRS POINT MEAS_"+str(key)
                        if key == "STATE":
                            lrskey = str(key)+"_NQR_DESCRIPTION"
                        else:
                            lrskey = "NQR_DESCRIPTION"
                        try:
                            LocateFeaturesAlongRoutes_lr(localfilegdb+r"/CalibrationPoint"+str(end_name),"LRM"+str(key), lrskey, "500 Feet", outtable, outproperties, "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
                            #this works in Pro
                        except:
                            LocateFeaturesAlongRoutes_lr(localfilegdb+"/CalibrationPoint"+str(end_name),localfilegdb+r"/LRM"+str(key), lrskey, "500 Feet", outtable, outproperties, "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
                            #this works in non-Pro script environment
                        
                        #that LFAR function located begin/end segment points to ALL ROUTES within 500 feet of the segment endpoint
                    
                        #for calibrating, we are only interested in the points and LFAR Results that where this query is NOT true:
                        qNotThisRoad  = 'SUBSTRING("COUNTY_LRS",0,10) <> SUBSTRING("KDOT_LRS_KEY",0,10)'
                        #so we will delete the records where this query is trye
                        try:
                            SelectLayerByAttribute_management(str(end_name)+"_"+str(key), "NEW_SELECTION", qNotThisRoad)
                            DeleteRows_management(str(end_name)+"_"+str(key))
                            #this works in Pro Environment
                        except:
                            #SelectLayerByAttribute_management(localfilegdb+"/"+str(end)+"_"+str(key), "NEW_SELECTION", qNotThisRoad)
                            MakeTableView_management(localfilegdb+"/"+str(end_name)+"_"+str(key), "deleterows", qNotThisRoad, None, "")
                            DeleteRows_management("deleterows")  
                            #this works in non-Pro script environment                        
                #this works in non-Pro script environment
        else:
            MakeFeatureLayer_management(sderoads, "lyrStateSystemSource", "LRS_ROUTE_PREFIX IN ('I', 'U', 'K') And LRS_ROUTE_SUFFIX NOT IN ('Z', 'G')", None, "")
            RoadCenterlines = localfilegdb+"/lyrStateSystemSource"
            End_List = ['START', 'END']
            for end in End_List:
                end_name = end
                print(end_name)
                i_end_output = localfilegdb+"/CalibrationPoint"+str(end)
                try:
                    FeatureVerticesToPoints_management(RoadCenterlines, i_end_output, str(end))
                    #this works in Pro
                except:
                    FeatureVerticesToPoints_management("lyrStateSystemSource", i_end_output, str(end))
        #and this is the beginning and end of a line, for which we are going to create a vertex point
        #Iterate through the LRMs to bring them into memory and do the processing for each segment begin and end point!  
                for key, value in Lrm_Dict.items():
                    FeatureClassToFeatureClass_conversion(value, localfilegdb, "LRM"+str(key))
                    for end in End_List:
                        outtable = localfilegdb+r"/"+str(end_name)+"_"+str(key)
                        outproperties = str(key)+"_LRS POINT MEAS_"+str(key)
                        if key == "STATE":
                            lrskey = str(key)+"_NQR_DESCRIPTION"
                        else:
                            lrskey = "NQR_DESCRIPTION"
                        try:
                            LocateFeaturesAlongRoutes_lr(localfilegdb+r"/CalibrationPoint"+str(end_name),"LRM"+str(key), lrskey, "500 Feet", outtable, outproperties, "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
                            #this works in Pro
                        except:
                            LocateFeaturesAlongRoutes_lr(localfilegdb+"/CalibrationPoint"+str(end_name),localfilegdb+r"/LRM"+str(key), lrskey, "500 Feet", outtable, outproperties, "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
                            #this works in non-Pro script environment
                        
                        #that LFAR function located begin/end segment points to ALL ROUTES within 500 feet of the segment endpoint
                    
                        #for calibrating, we are only interested in the points and LFAR Results that where this query is NOT true:
                        qNotThisRoad  = 'SUBSTRING("COUNTY_LRS",0,10) <> SUBSTRING("KDOT_LRS_KEY",0,10)'
                        #so we will delete the records where this query is true
                        #It is possible that there will be multiple rows where this query is true, this result
                        #will calculate one value, not conditional on distance, min/max, just takes the first true result I guess
                        #in situations where there are multiple results, consider dissolving these points and keeping some stats
                        #then review stats to determine appropriate value, probably the closest result
                        try:
                            SelectLayerByAttribute_management(str(end_name)+"_"+str(key), "NEW_SELECTION", qNotThisRoad)
                            DeleteRows_management(str(end_name)+"_"+str(key))
                            #this works in Pro Environment
                        except:
                            #SelectLayerByAttribute_management(localfilegdb+"/"+str(end)+"_"+str(key), "NEW_SELECTION", qNotThisRoad)
                            MakeTableView_management(localfilegdb+"/"+str(end_name)+"_"+str(key), "deleterows", qNotThisRoad, None, "")
                            DeleteRows_management("deleterows")  
                            #this works in non-Pro script environment    
    print('Calibration process completed in {} hours, minutes, seconds.'.format(datetime.datetime.now()-startDateTime))

def CalcUsingSQLserver(DBPassword):     
    #for ArcGIS Pro python 3.6
    #Propy will not load pymssql package for some reason
    #new plan on 3/13/2018 - use pyodbc and system DSN to connect to SQL Server, because it works.
    #another option to test someday might be http://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy-classes/arcsdesqlexecute.htm
    import datetime
    startDateTime = datetime.datetime.now()
    print("starting SQL calculation at "+str(startDateTime)+", it should take a couple minutes to refresh tables and calculate measures")
    #Calibration process completed in 0:03:36.252839 hours, minutes, seconds
    import getpass
    fileformatDateStr = startDateTime.strftime("%Y%m%d")
    from KhubCode25.KhubCode25Config import devorprod, dbname, dbownername, localProFileGDBWorkspace, devDataSourceSDE, prodDataSourceSDE, KDOTConnections, devSqlDSN, prodSqlDSN
    from arcpy import SelectLayerByAttribute_management, FlipLine_edit
    username = dbownername
    #use Collect Password upfront so we dont need to wait for the sequence to run before entering this password
    dbpassword = DBPassword
    if devorprod == 'prod':
        database = prodDataSourceSDE
        dsn = prodSqlDSN
        print("running on "+devorprod)
    else: 
        database = devDataSourceSDE
        dsn = devSqlDSN
        print("running on "+devorprod)

    import pyodbc  # @UnresolvedImport for pydev/eclipse
    from arcpy import Delete_management, TableToTable_conversion, Exists
    localfilegdb = localProFileGDBWorkspace+'\\'+'KhubRoadCenterlinesTemp'+fileformatDateStr+'.gdb'
    connectionstring = 'DSN='+dsn+';UID='+username+';PWD='+ dbpassword
    print(connectionstring)
    sdegdb = KDOTConnections+r'\\'+database+r'\\'+dbname+"."+dbownername
    CalTables = ["START_COUNTY", "END_COUNTY", "END_D1_COUNTY", "START_D1_COUNTY", "START_D1_C_D", "END_D1_C_D", "START_D1_RM_D", "END_D1_RM_D"]
    for table in CalTables:
        if Exists(sdegdb+"."+table):
            Delete_management(sdegdb+"."+table)
        else:
            pass
        print ("copying table "+str(table))
        TableToTable_conversion(localfilegdb+"\\"+table, KDOTConnections+r'\\'+database, table)

    print("connecting to SQL server...")
    cnxn = pyodbc.connect(connectionstring)
    cursor = cnxn.cursor()
    querystringSetStateSystemMiles = """
    

            update [sde].[All_Road_Centerlines]
                set [county_log_begin] = bm.[MEAS_COUNTY]
                from [sde].[All_Road_Centerlines] r
                JOIN (select distinct [KDOT_STATIC_ID1], [COUNTY_LRS], [MEAS_COUNTY], [KDOT_LRS_KEY]
                    from [sde].[START_COUNTY] bm
                    where 1=1
                    and substring([COUNTY_LRS],0,10) =substring([KDOT_LRS_KEY],0,10)) bm 
                    on r.[KDOT_STATIC_ID1] = bm.[KDOT_STATIC_ID1]
    
            update [sde].[All_Road_Centerlines]
                set [county_log_end] = em.[MEAS_COUNTY]
                from [sde].[All_Road_Centerlines] r
                JOIN (select distinct [COUNTY_LRS], [MEAS_COUNTY], [KDOT_STATIC_ID1], [KDOT_LRS_KEY]
                    from [sde].[END_COUNTY] em
                    where 1=1
                    and substring([COUNTY_LRS],0,10) = substring([KDOT_LRS_KEY],0,10)) em 
                    on r.[KDOT_STATIC_ID1] = em.[KDOT_STATIC_ID1]
            
            update [sde].[All_Road_Centerlines_D1]
                set [county_log_begin] = bm.[MEAS_COUNTY]
                from [sde].[All_Road_Centerlines_D1] r
                JOIN (select distinct [KDOT_STATIC_ID2], [COUNTY_LRS], [MEAS_COUNTY], [KDOT_LRS_KEY]
                    from [sde].[START_D1_COUNTY] bm
                    where 1=1
                    and substring([COUNTY_LRS],0,10) =substring([KDOT_LRS_KEY],0,10)) bm 
                    on r.[KDOT_STATIC_ID2] = bm.[KDOT_STATIC_ID2]
    
            update [sde].[All_Road_Centerlines_D1]
                set [county_log_end] = em.[MEAS_COUNTY]
                from [sde].[All_Road_Centerlines_D1] r
                JOIN (select distinct [COUNTY_LRS], [MEAS_COUNTY], [KDOT_STATIC_ID2], [KDOT_LRS_KEY]
                    from [sde].[END_D1_COUNTY] em
                    where 1=1
                    and substring([COUNTY_LRS],0,10) = substring([KDOT_LRS_KEY],0,10)) em 
                    on r.[KDOT_STATIC_ID2] = em.[KDOT_STATIC_ID2]

            update [sde].[All_Road_Centerlines_D1]
                set [county_log_begin] = bm.[C_MEAS]
                from [sde].[All_Road_Centerlines_D1] r
                JOIN (select distinct [KDOT_STATIC_ID2], [LRS_KEY], [C_MEAS], [KDOT_LRS_KEY]
                    from [sde].[START_D1_C_D]bm
                    where 1=1
                    and [LRS_ROUTE_PREFIX] = 'C'
                    and substring([LRS_KEY],0,9) =substring([KDOT_LRS_KEY],0,9)) bm
                    on r.[KDOT_STATIC_ID2] = bm.[KDOT_STATIC_ID2]

            update [sde].[All_Road_Centerlines_D1]
                set [county_log_end] = em.[C_MEAS]
                from [sde].[All_Road_Centerlines_D1] r
                JOIN (select distinct [KDOT_STATIC_ID2], [LRS_KEY], [C_MEAS], [KDOT_LRS_KEY]
                    from [sde].[END_D1_C_D]em
                    where 1=1
                    and [LRS_ROUTE_PREFIX] = 'C'
                    and substring([LRS_KEY],0,9) =substring([KDOT_LRS_KEY],0,9)) em
                    on r.[KDOT_STATIC_ID2] = em.[KDOT_STATIC_ID2]

            update [sde].[All_Road_Centerlines_D1]
                set [county_log_begin] = bm.[RM_MEAS]
                from [sde].[All_Road_Centerlines_D1] r
                JOIN (select distinct [KDOT_STATIC_ID2], [LRS_KEY], [RM_MEAS], [KDOT_LRS_KEY]
                    from [sde].[START_D1_RM_D]bm
                    where 1=1
                    and [LRS_ROUTE_PREFIX] in ('R', 'M')
                    and substring([LRS_KEY],0,9) =substring([KDOT_LRS_KEY],0,9)) bm
                    on r.[KDOT_STATIC_ID2] = bm.[KDOT_STATIC_ID2]

            update [sde].[All_Road_Centerlines_D1]
                set [county_log_end] = em.[RM_MEAS]
                from [sde].[All_Road_Centerlines_D1] r
                JOIN (select distinct [KDOT_STATIC_ID2], [LRS_KEY], [RM_MEAS], [KDOT_LRS_KEY]
                    from [sde].[END_D1_RM_D]em
                    where 1=1
                    and [LRS_ROUTE_PREFIX] in ('R', 'M')
                    and substring([LRS_KEY],0,9) =substring([KDOT_LRS_KEY],0,9)) em
                    on r.[KDOT_STATIC_ID2] = em.[KDOT_STATIC_ID2]
        
        
        """
        
        
        
    cursor.execute(querystringSetStateSystemMiles) 
    cursor.execute("COMMIT")
    cursor.close()
    del cursor
                #  F:\Cart\projects\Conflation\SQL\SQLServer\Conflation2012\KHUB  is where that SQL query lives, its the State System Calibration 2 SQL file
    print('Calibration process completed in {} hours, minutes, seconds.'.format(datetime.datetime.now()-startDateTime))
    print("calculated using sql server, need to incorporate flipping directions based on D1 calibration")
    #SelectLayerByAttribute_management("All_Road_Centerlines_D1", "NEW_SELECTION", "county_log_begin > county_log_end And LRS_ROUTE_PREFIX IN ('I', 'K', 'U')", None)
    
    #FlipLine_edit("All_Road_Centerlines_D1")
    
    #CalculateField_management("All_Road_Centerlines_D1", "Mileage_Logmile", "!county_log_begin!", "PYTHON3", None)
    #CalculateField_management("All_Road_Centerlines_D1", "county_log_begin", "!county_log_end!", "PYTHON3", None)
    #CalculateField_management("All_Road_Centerlines_D1", "county_log_end", "!Mileage_Logmile!", "PYTHON3", None)
   
    
def main():
    StateHighwayCalibrate()
    #RM_Calibrate()
    #CalcUsingSQLserver()
    
if __name__ == '__main__':
    #import datetime
    #startDateTime = datetime.datetime.now()
    #print("starting calibration at "+str(startDateTime)+", it should take about 5 minutes to calibrate state system routes")
#Calibration process completed in 0:03:36.252839 hours, minutes, seconds
    main()
    #print(datetime.datetime.now())
    #print('Calibration process completed in {} hours, minutes, seconds.'.format(datetime.datetime.now()-startDateTime))
else:
    print("Functions from Calibrate Source to Control imported to main script")