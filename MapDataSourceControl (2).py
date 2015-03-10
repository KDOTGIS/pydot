'''
Created on Sep 18, 2013

@author: kyleg
'''

import arcpy
mxd = arcpy.mapping.MapDocument(r"//gisdata/arcgis/GISdata/MXD/services/DevServices.mxd")
connection = r'//gisdata/arcgis/GISdata/MXD/services/sdedev.sde'

if arcpy.Exists(connection):
    arcpy.Delete_management(connection)

arcpy.CreateArcSDEConnectionFile_management(r'//gisdata/arcgis/GISdata/MXD/services', "sdedev", "sdedev", "sde:Oracle11g:sdedev", "#", "DATABASE_AUTH", "gis_dev", "gis", "SAVE_USERNAME", "SDE.DEFAULT", "SAVE_VERSION")

fromcon = r'Database Connections/SDEPROD_GIS.sde'

for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("SERVICEPROPERTIES"):
        servProp = lyr.serviceProperties
        print "Layer name:" + lyr.name +" at " + servProp.get('Connection', 'N/A')
        print "-----------------------------------------------------"
        if lyr.serviceProperties["ServiceType"] != "SDE":
            print lyr.name +" at " + lyr.workspacePath 
        else:
            print "Service Type: " + servProp.get('ServiceType', 'N/A')
            print "    Service:        " + servProp.get('Service', 'N/A')
            print "    Version:        " + servProp.get('Version', 'N/A')
            print "    User name:      " + servProp.get('UserName', 'N/A')
            print "    Authentication: " + servProp.get('AuthenticationMode', 'N/A')
            print "    Workspace path: "+ lyr.workspacePath       
            print "    Feature Dataset: "+ lyr.datasetName
            lyr.findAndReplaceWorkspacePath(r'C:\Users\nickh\AppData\Roaming\ESRI\Desktop10.2\ArcCatalog\sdedev_gis_dev.sde', connection,False)
            print "    new Workspace path: "+ lyr.workspacePath       
mxd.save()            
del mxd

