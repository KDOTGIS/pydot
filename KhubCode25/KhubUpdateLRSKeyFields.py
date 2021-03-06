'''
Created on Mar 7, 2018
this script uses the pyodbc cursor to update the LRSKEY in Microsoft Sql Server
it utilizes a system DSN at this time to connect to SQL server because I got that to work!
pyodbc is working in python 3.6 for ArcGIS Pro2.xx, I can't say the same for pymssql and _mssql. 
seems like pyodbc works almost exactly the same as _mssql other than the actual connection string  
@author: kyleg
'''

def SqlUpdateLRSKeys(DBPassword):
    # Add if exists LocalRoadNumbering
    import datetime
    startDateTime = datetime.datetime.now()
    import pyodbc  # @UnresolvedImport for pydev/eclipse
    import getpass
    print('Updating LRS Keys with SQL, it should take a few seconds...starting at {}'.format(datetime.datetime.now()))
    from KhubCode25.KhubCode25Config import devorprod, dbownername, devSqlDSN, prodSqlDSN
    if devorprod == 'prod':
        database = prodSqlDSN
        print("running on "+devorprod)
    else: 
        database = devSqlDSN
        print("running on "+devorprod)
    username = dbownername
    try:
        dbpassword = DBPassword
    except:
        dbpassword = getpass.getpass("Enter Password for "+str(username)+":")
    
    connectionstring = 'DSN='+database+';UID='+username+';PWD='+ dbpassword
    print(connectionstring)
    cnxn = pyodbc.connect(connectionstring)
    cursor = cnxn.cursor()
    querystringLRSKEY = """
        USE ROADS
        
        select [LRS_COUNTY_PRE],  
        RTRIM([RD]) as RD_TRIMMED, 
        RTRIM([STS]) AS STS_TRIMMED, 
        Count([OBJECTID]) as NAMECOUNT, ROW_NUMBER() over (order by [RD] ASC, STS ASC) AS STATEROWNUM,  
        ROW_NUMBER() over (PARTITION BY [LRS_COUNTY_PRE] order by [RD] ASC, STS ASC) AS COUNTYROWNUM
        /*into LOCAL_ROAD_NUMBERING*/
        from [sde].[ALL_ROAD_CENTERLINES]
        where [LRS_ROUTE_PREFIX] = 'L' OR [ROUTE_PREFIX_TARGET] in ('6','7','8')
        group by LRS_COUNTY_PRE, [STS], [RD]
        order by LRS_COUNTY_PRE ASC, rd ASC, STS ASC

            
        /*#this update query took 16 seconds to reset all local route numbers*/
        
        update [ALL_ROAD_CENTERLINES]
        set [LRS_ROUTE_NUM_TARGET] = L.COUNTYROWNUM
        from [ALL_ROAD_CENTERLINES] r
        inner join LOCAL_ROAD_NUMBERING L
        ON r.[LRS_COUNTY_PRE] = L.LRS_COUNTY_PRE  
        AND RTRIM(r.[RD])= L.RD_TRIMMED
        AND RTRIM(r.[STS])=L.STS_TRIMMED
        where r.[ROUTE_PREFIX_TARGET] in ('6','7','8')
        and r.[LRS_ROUTE_NUM_TARGET] != L.COUNTYROWNUM


        UPDATE [Roads].[sde].[ALL_ROAD_CENTERLINES]
            SET [KDOT_LRS_KEY] = CONCAT([LRS_COUNTY_PRE], [LRS_ROUTE_PREFIX], [LRS_ROUTE_NUM],[LRS_ROUTE_SUFFIX],[LRS_UNIQUE_IDENT], '-',[LRS_DIRECTION]) 
                WHERE 1=1
                AND LRS_ROUTE_PREFIX in ('I', 'U', 'K')
                AND [KDOT_LRS_KEY]<> CONCAT([LRS_COUNTY_PRE], [LRS_ROUTE_PREFIX], [LRS_ROUTE_NUM],[LRS_ROUTE_SUFFIX],[LRS_UNIQUE_IDENT], '-',[LRS_DIRECTION])

        UPDATE [Roads].[sde].[ALL_ROAD_CENTERLINES]
            SET [Target_LRSKEY_Temp1] = CONCAT([LRS_COUNTY_PRE],[ROUTE_PREFIX_TARGET],REPLICATE('0',5-LEN(RTRIM([LRS_ROUTE_NUM_TARGET]))) + RTRIM([LRS_ROUTE_NUM_TARGET]),[LRS_ROUTE_SUFFIX],[KDOT_DIRECTION_CALC],[LRS_UNIQUE_TARGET])
                WHERE 1=1
                AND [Target_LRSKEY_Temp1] <> CONCAT([LRS_COUNTY_PRE],[ROUTE_PREFIX_TARGET],REPLICATE('0',5-LEN(RTRIM([LRS_ROUTE_NUM_TARGET]))) + RTRIM([LRS_ROUTE_NUM_TARGET]),[LRS_ROUTE_SUFFIX],[KDOT_DIRECTION_CALC],[LRS_UNIQUE_TARGET])

        UPDATE [Roads].[sde].[ALL_ROAD_CENTERLINES]
            SET [KDOT_LRS_KEY] = CONCAT([LRS_COUNTY_PRE], [LRS_ROUTE_PREFIX], [LRS_ROUTE_NUM],[LRS_ROUTE_SUFFIX],[LRS_UNIQUE_IDENT],[LRS_ADMO],[KDOT_DIRECTION_CALC]) 
                WHERE 1=1
                AND LRS_ROUTE_PREFIX in ('R', 'M')
                AND [KDOT_LRS_KEY]<> CONCAT([LRS_COUNTY_PRE], [LRS_ROUTE_PREFIX], [LRS_ROUTE_NUM],[LRS_ROUTE_SUFFIX],[LRS_UNIQUE_IDENT],[LRS_ADMO],[KDOT_DIRECTION_CALC])
        
        UPDATE [Roads].[sde].[ALL_ROAD_CENTERLINES]
            SET  [KDOT_LRS_KEY] = CONCAT([LRS_URBAN_PRE], [LRS_ROUTE_PREFIX], [LRS_ROUTE_NUM],[LRS_ROUTE_SUFFIX],[LRS_UNIQUE_IDENT],[LRS_ADMO],[KDOT_DIRECTION_CALC])
                WHERE 1=1
                AND LRS_ROUTE_PREFIX in ('C')
                AND [KDOT_LRS_KEY]<> CONCAT([LRS_URBAN_PRE], [LRS_ROUTE_PREFIX], [LRS_ROUTE_NUM],[LRS_ROUTE_SUFFIX],[LRS_UNIQUE_IDENT],[LRS_ADMO],[KDOT_DIRECTION_CALC])
       
        UPDATE [sde].[ALL_ROAD_CENTERLINES_D1]
            set [KDOT_STATIC_ID2] = [OBJECTID]
        """

    cursor.execute(querystringLRSKEY) 
    cursor.execute("COMMIT")
    cursor.close()
    del cursor
    print('SQL update query completed in {} hours, minutes, seconds.'.format(datetime.datetime.now()-startDateTime))
  
def main():
    #UpdateLRSKeyFieldsSQL()
    SqlUpdateLRSKeys()
    
if __name__ == '__main__':
    #print(datetime.datetime.now())
    #print("this is the main section")
    main()
    #print(datetime.datetime.now())
    
else:
    print("Functions from UpdateLRSKey fields script imported to main script")
    