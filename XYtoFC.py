'''
Created on Aug 21, 2013
references database connections at \\gisdata\arcgis\GISdata\Layers\connection_files
make sure these sde connection files have the passwords stored.
@author: kyleg
'''
#import arcpy

if __name__ == '__main__':
    pass
import datetime, os, shutil
from arcpy import Exists, Delete_management, MakeTableView_management, MakeXYEventLayer_management, CalculateField_management, Append_management, TruncateTable_management
#mxd = arcpy.mapping.MapDocument(r'\\gisdata\arcgis\GISdata\MXD\CIIMS_PROCESS_DEV.mxd')
now = datetime.datetime.now()
apd = os.getenv('APPDATA')
conns = r'\\gisdata\arcgis\GISdata\Layers\connection_files'
ArcVersion = '10.2'
DCL = apd + r'\\ESRI\\Desktop'+ArcVersion+'\\ArcCatalog'

##################################################################
#####Define the function that creates a point layer from X, Y coordinates in event table ######
##################################################################

def XYFC(source, dst, Lat, Long, GCS, loaded):
    if Exists("FCtbl"):
        Delete_management("FCtbl")
    else:    
        pass
    if Exists("FC_Layer"):
        Delete_management("FC_Layer")
    else:
        pass
    print "start XYFC "+ str(datetime.datetime.now())
    MakeTableView_management(source, 'FCtbl', "#", "#", "")
    MakeXYEventLayer_management("FCtbl",Long, Lat,"FC_Layer", GCS,"#")
    TruncateTable_management(dst)
    Append_management("FC_Layer",dst,"NO_TEST","#","#")
    CalculateField_management(dst, loaded,"datetime.datetime.now( )","PYTHON_9.3","#")
    print "XYFC complete for " +str(dst)+ " at " + str(datetime.datetime.now())

############################################################################
#class object for CIIMS loader into SDEDev from SDEDEV view into CANSYS 
############################################################################

class CIIMSDev(object):
    srcdb =r'sdedev_ciims.sde'

    if Exists(r'Database Connections/'+srcdb):
        Delete_management(DCL+r'\\Database Connections\\'+srcdb)
       
    shutil.copy(conns+"/"+srcdb, DCL+"/"+srcdb)
    srcschema = 'CIIMS'
    srctbl ='CIIMS_VWCROSSINGGIS3'
    source = r'Database Connections/'+srcdb +'/'+srcschema+'.'+srctbl
    Lat = "CROSSINGLATITUDE"
    Long = "CROSSINGLONGITUDE"
    loaded = "LOADDATE"
    dstdb = r'sdedev_ciims.sde'
    if Exists(r'Database Connections/'+dstdb):
        pass
    else:
        shutil.copy(conns+"/"+dstdb, DCL+"/"+dstdb)
    dstschema = 'CIIMS'
    dstfd = 'CIIMS'
    dstfc = 'Static_Crossings'
    dst = r'Database Connections/'+dstdb+'/'+dstschema+'.'+dstfd+'/'+dstschema+'.'+dstfc
      
    GCS = "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision"
    XYFC(source, dst, Lat, Long, GCS, loaded)
    
############################################################################
#class object for CIIMS loader into SDEDev from SDEDEV view into CANSYS 
############################################################################

class CIIMSProd(object):
    srcdb =r'sdeprod_CIIMS.sde'
    if Exists(r'Database Connections/'+srcdb):
        Delete_management(DCL+r'\\Database Connections\\'+srcdb)
    shutil.copy(conns+"/"+srcdb, DCL+"/"+srcdb)
    srcschema = 'CIIMS'
    srctbl ='CIIMS_VWCROSSINGGIS3'
    source = r'Database Connections/'+srcdb +'/'+srcschema+'.'+srctbl
    Lat = "CROSSINGLATITUDE"
    Long = "CROSSINGLONGITUDE"
    loaded = "LOADDATE"
    dstdb = r'sdeprod_CIIMS.sde'
    if Exists(r'Database Connections/'+dstdb):
        pass
    else:
        shutil.copy(conns+"/"+dstdb, DCL+"/"+dstdb)
    dstschema = 'CIIMS'
    dstfd = 'CIIMS'
    dstfc = 'Static_Crossings'
    dst = r'Database Connections/'+dstdb+'/'+dstschema+'.'+dstfd+'/'+dstschema+'.'+dstfc
      
    GCS = "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision"
    XYFC(source, dst, Lat, Long, GCS, loaded)    
    
############################################################################
#class object for ACCESS Points loader into GISTest from AtlasPRD materialized view
############################################################################

class ACCESSPERMDev(object):
    print "access permit points: GO "+ str(datetime.datetime.now())
    srcdb =r'ATLASPROD.odc'
    if Exists(r'Database Connections/'+srcdb):
        Delete_management(DCL+r'\\Database Connections\\'+srcdb)
    shutil.copy(conns+"/"+srcdb, DCL+"/"+srcdb)
    srcschema = 'KDOT'
    srctbl ='KGATE_ACCESSPOINTS_TEST'
    source = r'Database Connections/'+srcdb +'/'+srcschema+'.'+srctbl
    print source
    Lat = "GPS_LATITUDE"
    Long = "GPS_LONGITUDE"
    loaded = "LOAD_DATE"
    dstdb = 'GISTEST.sde'
    if Exists(r'Database Connections/'+dstdb):
        print dstdb +" exists"
        pass
    else:
        shutil.copy(conns+"/"+dstdb, DCL+"/"+dstdb)
    dstschema = 'SHARED'
    dstfc = 'ACCESS_POINTS'
    dst = r'Database Connections/'+dstdb+'/'+dstschema+'.'+dstfc
    print source
    print dst
      
    GCS = "GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119521E-09;0.001;0.001;IsHighPrecision"
    XYFC(source, dst, Lat, Long, GCS, loaded)

