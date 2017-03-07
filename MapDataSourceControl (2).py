'''
Created on Sep 18, 2013

@author: kyleg
'''

import arcpy
print "imported arcpy lib"
connection = r'\\gisdata\arcgis\GISdata\Connection_files\Conflation2012_RO.sde'
oldpath = r'C:\Users\kyleg\AppData\Roaming\ESRI\Desktop10.3\ArcCatalog\conflation_sqlgis_geo.sde'

newFD = r'Conflation.sde.RoadCenterlines'
oldFD = r"Conflation.GEO.RoadCenterlines"

mxd = arcpy.mapping.MapDocument(r"G:\GISdata\MXD\2016010601_ConflationIIAggregationReviewer06a.mxd")
#connection = r'//gisdata/arcgis/GISdata/MXD/services/sdedev.sde'

#if arcpy.Exists(connection):
#    arcpy.Delete_management(connection)

#arcpy.CreateArcSDEConnectionFile_management(r'//gisdata/arcgis/GISdata/MXD/services', "sdedev", "sdedev", "sde:Oracle11g:sdedev", "#", "DATABASE_AUTH", "gis_dev", "gis", "SAVE_USERNAME", "SDE.DEFAULT", "SAVE_VERSION")

#fromcon = r'Database Connections/SDEPROD_GIS.sde'

for lyr in arcpy.mapping.ListLayers(mxd):
    if lyr.supports("SERVICEPROPERTIES"):
        servProp = lyr.serviceProperties
        print "Layer name:" + lyr.name +" at " + servProp.get('Connection', 'N/A')
        print "-----------------------------------------------------"
        #if lyr.serviceProperties["ServiceType"] != "SDE":
        #    print lyr.name +" at " + lyr.workspacePath 
        #else:
        print "Service Type: " + servProp.get('ServiceType', 'N/A')
        print "    Service:        " + servProp.get('Service', 'N/A')
        print "    Version:        " + servProp.get('Version', 'N/A')
        print "    User name:      " + servProp.get('UserName', 'N/A')
        print "    Authentication: " + servProp.get('AuthenticationMode', 'N/A')
        print "    Workspace path: "+ lyr.workspacePath       
        print "    Feature Dataset: "+ lyr.datasetName
        if lyr.workspacePath == oldpath and lyr.datasetName == 'Conflation.GEO.RoadCenterlines':
            #lyr.findAndReplaceWorkspacePath(oldpath, connection, False)
            lyr.replaceDataSource(connection, 'SDE_WORKSPACE', newFD)
        print "    new Workspace path: "+ lyr.workspacePath  
    else:
        print "Layer name:" + lyr.name + "doesnt support service properties"   
mxd.saveACopy(r'G:\GISdata\MXD\2016010601_ConflationIIAggregationReviewer06b.mxd')            
del mxd

