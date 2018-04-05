'''
@author: kyleg
reCreated on Mar 7, 2018 
integrated to KhubCode 25 pydev project
modified to work in python 3 environment using arcgis pro
also switched from _mssql to pyodbc using the system DSN connection
updated 3/14/2018 - happy birthday to me!
updated 3/15/2018 - I shouldn't use the workspace from UpdateFileGdb script, since we should calibrate before creating that, added "temp" to the name.  
updated 3/16/2018 - initially tested, working and run on production

the propy libs cannot connect to a sql 2008 database, so copy CMLRS into the working roads db

originally reCreated on Feb 7, 2017
Created from Eliminate Overlaps, modifided to work and populate non primary route key
This script prepares the conflation data for route creation
'''
def RM_Calibrate():
    import datetime
    startDateTime = datetime.datetime.now()
    print("starting SHS calibration at "+str(startDateTime)+", it should take about 10-30 minutes to calibration state system routes")
#Calibration process completed in 0:03:36.252839 hours, minutes, seconds
    from KhubCode25.KhubCode25Config import devorprod, dbname, dbownername, localProFileGDBWorkspace, KDOTConnections, Cmlrs, prodDataSourceSDE, devDataSourceSDE
    fileformatDateStr = startDateTime.strftime("%Y%m%d") 
    from arcpy import Exists, FeatureClassToFeatureClass_conversion, Delete_management, FeatureVerticesToPoints_management, LocateFeaturesAlongRoutes_lr, CreateFileGDB_management, env, MakeFeatureLayer_management, SelectLayerByAttribute_management, DeleteRows_management, MakeTableView_management  
 
    if Exists(localProFileGDBWorkspace+"KhubRoadCenterlinesTemp"+fileformatDateStr+".gdb"):
        print("local temp proc db exists"+localProFileGDBWorkspace+"/KhubRoadCenterlinesTemp"+fileformatDateStr)
    else:
        CreateFileGDB_management(localProFileGDBWorkspace, "KhubRoadCenterlinesTemp"+fileformatDateStr, "CURRENT")
        print("creating a local temp calibration processing file geodatabase at"+localProFileGDBWorkspace+"called KhubRoadCenterlinesTemp"+fileformatDateStr)
    

def StateHighwayCalibrate():
    import datetime
    startDateTime = datetime.datetime.now()
    print("starting SHS calibration at "+str(startDateTime)+", it should take about 10-30 minutes to calibration state system routes")
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
    sderoads = sdegdb+".All_Road_Centerlines"   
    MakeFeatureLayer_management(sderoads, "lyrStateSystemSource", "LRS_ROUTE_PREFIX IN ('I', 'K', 'U')", None, "")
    RoadCenterlines = localfilegdb+"/lyrStateSystemSource"
    #once there were two linear referencing methods we were going to use to calibrate the state highway system
    #for iteration 2, no source data should refer to the state LRM, so we're only doing the County LRM
    #if there were more we could use this LRM dictionary.  Since that's how the script was created, that's how it works still
    #it was nicely pythonic 
    #CMLRS are the GIS routes with measures extracted regularly from EXOR using the FME extraction and python route reference tools from DT00ar60
    CMLRS = sdegdb+"."+Cmlrs
    Lrm_Dict = {'COUNTY':CMLRS}
    
    #and this is the beginning and end of a line, for which we are going to create a vertex point
    End_List = ['START', 'END']
    
    # First,  create points at the begin and end of each road centerline segment using Vertices to Points.  
    for end in End_List:
        i_end_output = localfilegdb+"/CalibrationPoint"+str(end)
        try:
            FeatureVerticesToPoints_management(RoadCenterlines, i_end_output, str(end))
            #this works in Pro
        except:
            FeatureVerticesToPoints_management("lyrStateSystemSource", i_end_output, str(end))
            #this works in non-Pro script environment
    
    #Iterate through the LRMs to bring them into memory and do the processing for each segment begin and end point!  
    for key, value in Lrm_Dict.items():
        FeatureClassToFeatureClass_conversion(value, localfilegdb, "LRM"+str(key))
        for end in End_List:
            outtable = localfilegdb+r"/"+str(end)+"_"+str(key)
            outproperties = str(key)+"_LRS POINT MEAS_"+str(key)
            if key == "STATE":
                lrskey = str(key)+"_NQR_DESCRIPTION"
            else:
                lrskey = "NQR_DESCRIPTION"
            try:
                LocateFeaturesAlongRoutes_lr(localfilegdb+r"/CalibrationPoint"+str(end),"LRM"+str(key), lrskey, "500 Feet", outtable, outproperties, "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
                #this works in Pro
            except:
                LocateFeaturesAlongRoutes_lr(localfilegdb+"/CalibrationPoint"+str(end),localfilegdb+r"/LRM"+str(key), lrskey, "500 Feet", outtable, outproperties, "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
                #this works in non-Pro script environment
            
            #that LFAR function located begin/end segment points to ALL ROUTES within 500 feet of the segment endpoint
        
            #for calibrating, we are only interested in the points and LFAR Results that where this query is NOT true:
            qNotThisRoad  = '"COUNTY_LRS" <> "KDOT_LRS_KEY"'
            #so we will delete the records where this query is trye
            try:
                SelectLayerByAttribute_management(str(end)+"_"+str(key), "NEW_SELECTION", qNotThisRoad)
                DeleteRows_management(str(end)+"_"+str(key))
                #this works in Pro Environment
            except:
                #SelectLayerByAttribute_management(localfilegdb+"/"+str(end)+"_"+str(key), "NEW_SELECTION", qNotThisRoad)
                MakeTableView_management(localfilegdb+"/"+str(end)+"_"+str(key), "deleterows", qNotThisRoad, None, "")
                DeleteRows_management("deleterows")  
                #this works in non-Pro script environment    


def CalcUsingSQLserver():     
    #for ArcGIS Pro python 3.6
    #Propy will not load pymssql package for some reason
    #new plan on 3/13/2018 - use pyodbc and system DSN to connect to SQL Server, because it works.
    #another option to test someday might be http://desktop.arcgis.com/en/arcmap/latest/analyze/arcpy-classes/arcsdesqlexecute.htm
    import datetime
    startDateTime = datetime.datetime.now()
    print("starting SQL calculation at "+str(startDateTime)+", it should take about 10-30 minutes to calibration state system routes")
    #Calibration process completed in 0:03:36.252839 hours, minutes, seconds
    import getpass
    fileformatDateStr = startDateTime.strftime("%Y%m%d")
    from KhubCode25.KhubCode25Config import devorprod, dbname, dbownername, localProFileGDBWorkspace, devDataSourceSDE, prodDataSourceSDE, KDOTConnections, devSqlDSN, prodSqlDSN

    username = dbownername
    password = getpass.getpass("Enter Password for "+str(username)+":")
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
    connectionstring = 'DSN='+dsn+';UID='+username+';PWD='+ password
    print(connectionstring)
    sdegdb = KDOTConnections+r'\\'+database+r'\\'+dbname+"."+dbownername
    if Exists(sdegdb+".END_COUNTY"):
        Delete_management(sdegdb+".END_COUNTY")
    else:
        pass
    TableToTable_conversion(localfilegdb+"\\END_COUNTY", KDOTConnections+r'\\'+database, "END_COUNTY")
    
    if Exists(sdegdb+".START_COUNTY"):
        Delete_management(sdegdb+".START_COUNTY")
    else:
        pass
    TableToTable_conversion(localfilegdb+"\\START_COUNTY", KDOTConnections+r'\\'+database, "START_COUNTY")
    print("connecting...")
    cnxn = pyodbc.connect(connectionstring)
    cursor = cnxn.cursor()
    querystringSetStateSystemMiles = """
        update [sde].[All_Road_Centerlines]
            set [county_log_begin] = bm.[MEAS_COUNTY]
            from [sde].[All_Road_Centerlines] r
            JOIN (select distinct [KDOT_STATIC_ID1], [COUNTY_LRS], [MEAS_COUNTY], [KDOT_LRS_KEY]
                from [sde].[START_COUNTY] bm
                where 1=1
                and substring([COUNTY_LRS],0,15) =substring([KDOT_LRS_KEY],0,15)) bm 
                on r.[KDOT_STATIC_ID1] = bm.[KDOT_STATIC_ID1]

        update [sde].[All_Road_Centerlines]
            set [county_log_end] = em.[MEAS_COUNTY]
            from [sde].[All_Road_Centerlines] r
            JOIN (select distinct [COUNTY_LRS], [MEAS_COUNTY], [KDOT_STATIC_ID1], [KDOT_LRS_KEY]
                from [sde].[END_COUNTY] em
                where 1=1
                and substring([COUNTY_LRS],0,15) = substring([KDOT_LRS_KEY],0,15)) em 
                on r.[KDOT_STATIC_ID1] = em.[KDOT_STATIC_ID1]

        """

    cursor.execute(querystringSetStateSystemMiles) 
    cursor.execute("COMMIT")
    cursor.close()
    del cursor
            #  F:\Cart\projects\Conflation\SQL\SQLServer\Conflation2012\KHUB  is where that SQL query lives, its the State System Calibration 2 SQL file
    
    print("calculated using sql server")
    
def main():
    StateHighwayCalibrate()
    CalcUsingSQLserver()
    
if __name__ == '__main__':
    import datetime
    startDateTime = datetime.datetime.now()
    print("starting calibration at "+str(startDateTime)+", it should take about 5 minutes to calibrate state system routes")
#Calibration process completed in 0:03:36.252839 hours, minutes, seconds
    main()
    #print(datetime.datetime.now())
    print('Calibration process completed in {} hours, minutes, seconds.'.format(datetime.datetime.now()-startDateTime))
else:
    print("this is the else section")