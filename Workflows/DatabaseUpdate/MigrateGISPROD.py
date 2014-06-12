'''
Created on May 13, 2014

@author: kyleg
'''
import arcpy, datetime, cx_Oracle
#provide the database connection as the SDE user
NewDB = "Database Connections/SDETEST_SDE.sde" 

DBC = ["city.sde", "shared.sde", "countymaps.sde", "videolog.sde", "osm.sde"]

def esrify():
    #enable ESRI Geodatabase on the converted spatial database
    arcpy.EnableEnterpriseGeodatabase_management(NewDB,"T:/Program Files/ESRI/License10.2/sysgen/keycodes")

def SetEncoding():
    #this is not working  - use DBTune
    SDEconnection = cx_Oracle.connect('sde/gisadmin@sdetest')
    cursor = SDEconnection.cursor()
    SQLCode = "INSERT INTO SDE.DBTUNE (KEYWORD,PARAMETER_NAME,CONFIG_STRING) VALUES ('DEFAULTS', 'UNICODE_STRING ', 'FALSE')"
    cursor.execute(SQLCode)
    SDEconnection.commit() 
    SDEconnection.close()    
    print "database encoding set to unicode = false"
    

def DBConns():
    #schemae is a list of the connection strings for the database owner user/password.  The db owner should match the first part of the DBC connection name.sde variable
    schemae = ["redacted"]
    for schema in schemae:
        pwd =  schema.split(" ")[1] 
        usr = schema.split(" ")[0]
        #this is the user name
        #print usr 
        #this is the password
        #print pwd
        dbname = usr+".sde"
        arcpy.env.overwriteOutput = 1
        #this .sde file goes your APPDATA roaming ESRI database connections
        arcpy.CreateDatabaseConnection_management("Database Connections",dbname,"ORACLE","SDETEST","DATABASE_AUTH", usr, pwd)
        
        
def DBinfo():
    #check the GeoDB version, as enabled
    isCurrent = arcpy.Describe(NewDB).currentRelease

    print "database is current? "+isCurrent

    
def ListFCsde():  
    #list feature classes viewable by the SDE admin conection
    arcpy.env.workspace = NewDB
    featureclasses = arcpy.ListFeatureClasses()
    try:
        for fc in featureclasses:
            print fc
    except:        
        # If an error occurred while running a tool print the messages
        print arcpy.GetMessages()
        
def ListFCdb():  
    #list feature classes viewable by the DB owner for each DB connection.  this is how we will perform our actions
    for db in DBC:
        arcpy.env.workspace = "Database Connections/"+db
        featureclasses = arcpy.ListFeatureClasses()
        try:
            for fc in featureclasses:
                print fc
        except:        
        # If an error occurred while running a tool print the messages
            print arcpy.GetMessages()        

def ShowRegistered():
    connection = cx_Oracle.connect('sde/gisadmin@sdetest')
    cursor = connection.cursor()
    #cursor.execute("select c.f_table_schema, c.f_table_name, c.storage_type from SDE.geometry_columns c Where c.f_table_schema = 'SHARED'")
    cursor.execute("select f_table_name from SDE.geometry_columns Where f_table_schema = 'SHARED'")
    global GDBReg 
    GDBReg = []
    for row in cursor:
        print row[0]
        GDBReg.append("SHARED."+row[0])
    connection.close()
    return GDBReg

def DescribeFCdb():  
    #provides a basic description of FC's viewable by the DB owner for each DB connection.  
    #his will give us an indicator of any problems we will have with feature classes
    
    #for db will look at all databases
    
    #for db in DBC:
    
    db = "shared.sde"
    arcpy.env.workspace = "Database Connections/"+db
    featureclasses = arcpy.ListFeatureClasses()
    try:
        for fc in featureclasses:
            
            print fc
            print datetime.datetime.now()
            desc = arcpy.Describe(fc)
            print "data Type:  " + desc.dataType       
            print "Feature Type:  " + desc.featureType
            print "Shape Type :   " + desc.shapeType
            print "Spatial Index: " + str(desc.hasSpatialIndex)
            print "Geometry Column" + str(desc.shapeFieldName)
            print("Spatial reference name: {0}:".format(desc.spatialReference.name))
            if desc.hasOID:
                print "OIDFieldName: " + desc.OIDFieldName
            print ""
    except:        
    # If an error occurred while running a tool print the messages
        print arcpy.GetMessages()   
        print fc
        pass
    del db
    
def reGIStration():
    DBCr = ["city.sde", "shared.sde", "countymaps.sde", "osm.sde"]
    for db in DBCr:
        arcpy.env.workspace = "Database Connections/"+db
        featureclasses = arcpy.ListFeatureClasses()
        try:
            for fc in featureclasses:
                print fc
                arcpy.RegisterWithGeodatabase_management(fc)
                print fc + " registered"
        except:        
        # If an error occurred while running a tool print the messages
            print fc + " failed to register"
            print arcpy.GetMessages()   
            pass
        
def reGIStrationShared():
    db = "shared.sde"
    arcpy.env.workspace = "Database Connections/"+db
    showredistered()
    reglist = ["SHARED.FUTURE_NETWORK", "SHARED.INTERCHANGE_RAMPS", "SHARED.GIS_BRIDGE_DETAILS_LOC", "SHARED.KDOT_AREAS","SHARED.KDOT_DISTRICTS",
"SHARED.KDOT_MAINT_SUBAREAS", "SHARED.KDOT_SNICE", "SHARED.KDOT_SUBAREAS", "SHARED.MPO_BOUNDARIES", "SHARED.NHDAREA", "SHARED.NHDFLOWLINE",
"SHARED.NHDWATERBODY", "SHARED.NON_STATE_BRIDGES", "SHARED.NON_STATE_BRIDGE_GRID", "SHARED.NON_STATE_BR_JOIN_MV",
"SHARED.NON_STATE_NODE", "SHARED.NON_STATE_SYSTEM", "SHARED.PAVED_RS_SEGMENTS", "SHARED.PLSS", "SHARED.PLSS_RNG", "SHARED.PLSS_TWP",
"SHARED.RAILROADS", "SHARED.REFPOSTS", "SHARED.RIDER_ROUTE", "SHARED.SHIELD_ALL", "SHARED.STATE_BOUNDARY", "SHARED.STATE_BOUNDARY_LINES",
"SHARED.STATE_PHYSIO_PROVINCES", "SHARED.STATE_SYSTEM", "SHARED.STATE_SYSTEM_LANE", "SHARED.TOWERS", "SHARED.TOWNSHIPS", "SHARED.URBAN_BOUNDARIES"]
    
    waitlist = [ "SHARED.NON_STATE_MEASURED", "SHARED.NON_STATE_BR_JOIN_MV", "SHARED.NON_STATE_NODE", "SHARED.PAVED_RS_SEGMENTS"]
    
    skiplist = waitlist + GDBReg

    #print reglist
    for fc in reglist:
        print fc
        if fc in skiplist:
            print "layer already registered or skipped"
        else:
            fcdb = "Database Connections/"+db+"/"+fc
            print fcdb
            arcpy.RegisterWithGeodatabase_management(fcdb)
        print fc + " registered"


def cleanup():
    #Steve is dropping these user/schemas from SDETEST:
    """ANONYMOUS
    CBRUNSON
    DennisB
    Dexter
    DIP
    Farolw
    FranMC
    Janette
    Jill
    KathyH
    Kyleg
    MGMT_VIEW
    MitchS
    NickK
    ShawnH
    SCOTT
    """
          
if __name__ == '__main__':
    
    #reGIStration()
    #SetEncoding()
    #DBinfo()
    #DBConns()
    #ListFCdb()
    #ShowRegistered()
    #DescribeFCdb()
    #reGIStration()

    reGIStrationShared()
    
    pass
