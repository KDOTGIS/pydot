'''
Created on Mar 7, 2018
this script uses the pyodbc cursor to update the LRSKEY in Microsoft Sql Server
it utilizes a system DSN at this time to connect to SQL server because I got that to work!
pyodbc is working in python 3.6 for ArcGIS Pro2.xx, I can't say the same for pymssql and _mssql. 
seems like pyodbc works almost exactly the same as _mssql other than the actual connection string  
@author: kyleg
'''

import datetime
startDateTime = datetime.datetime.now()


def SqlUpdateLRSKeys():
    import pyodbc  # @UnresolvedImport for pydev/eclipse
    import getpass
    from KhubCode25.KhubCode25Config import devorprod, dbownername, devSqlDSN, prodSqlDSN
    if devorprod == 'prod':
        database = prodSqlDSN
        print("running on "+devorprod)
    else: 
        database = devSqlDSN
        print("running on "+devorprod)
    username = dbownername
    password = getpass.getpass("Enter Password for "+str(username)+":")
    connectionstring = 'DSN='+database+';UID='+username+';PWD='+ password
    print(connectionstring)
    cnxn = pyodbc.connect(connectionstring)
    cursor = cnxn.cursor()
    querystringLRSKEY = """
        USE ROADS
        UPDATE [Roads].[sde].[ALL_ROAD_CENTERLINES]
            SET [KDOT_LRS_KEY] = CONCAT([LRS_COUNTY_PRE], [LRS_ROUTE_PREFIX], [LRS_ROUTE_NUM],[LRS_ROUTE_SUFFIX],[LRS_UNIQUE_IDENT], '-',[LRS_DIRECTION]) 
                WHERE 1=1
                AND LRS_ROUTE_PREFIX in ('I', 'U', 'K')
                AND [KDOT_LRS_KEY]<> CONCAT([LRS_COUNTY_PRE], [LRS_ROUTE_PREFIX], [LRS_ROUTE_NUM],[LRS_ROUTE_SUFFIX],[LRS_UNIQUE_IDENT], '-',[LRS_DIRECTION])

        UPDATE [Roads].[sde].[ALL_ROAD_CENTERLINES]
            SET [Target_LRSKEY_Temp1]= SUBSTRING([LRS_ROUTE_NUM_TARGET], PATINDEX('%[^0]%', [LRS_ROUTE_NUM_TARGET]+'.'), LEN([LRS_ROUTE_NUM_TARGET]))
                WHERE 1=1
                AND [ROUTE_PREFIX_TARGET] in ('1', '2', '3')
                AND LEFT(LRS_ROUTE_NUM_TARGET,1)='0'
                
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
        """

    cursor.execute(querystringLRSKEY) 
    cursor.execute("COMMIT")
    cursor.close()
    del cursor
  
def main():
    #UpdateLRSKeyFieldsSQL()
    SqlUpdateLRSKeys()
    
if __name__ == '__main__':
    #print(datetime.datetime.now())
    #print("this is the main section")
    main()
    #print(datetime.datetime.now())
    print('SQL update query completed in {} hours, minutes, seconds.'.format(datetime.datetime.now()-startDateTime))
else:
    print("this is the else section")