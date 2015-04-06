'''
Created on July 10, 2014

@author: kyleg
'''
import arcpy, os
#workspace to search for MXDs
startplace = r"\\GISDATA\Planning\Cart\projects\KanPlan\MXD\Public"
arcpy.env.workspace = startplace
Workspaces = arcpy.ListWorkspaces("*", "Folder")
print "MXDPATH, MXD, Layer, Database, DB_Connection, Version, User"
for Workspace in Workspaces:
    arcpy.env.workspace = Workspace
    
    #list map documents in folder
    mxdList = arcpy.ListFiles("*.mxd")
    #set relative path setting for each MXD in list.
    for mapdoc in mxdList:
        #print the mapdocument name
        #print str(mapdoc)+","
        mapdocu = Workspace+"/"+mapdoc
        mxd = arcpy.mapping.MapDocument(mapdocu)
        
        #Print the layer name of each layer in each mapdocument, and the layer properties of each layer
        
        for lyr in arcpy.mapping.ListLayers(mxd):
            if lyr.supports("SERVICEPROPERTIES"):
                servProp = lyr.serviceProperties
                print str(Workspace)+", "+str(mapdoc)+", "+lyr.name +" at " + servProp.get('Connection', 'N/A') + ", "+servProp.get('Database', 'N/A')+", " + servProp.get('Service', 'N/A')+", " + servProp.get('Version', 'N/A')+", " + servProp.get('UserName', 'N/A')
            else:
                pass
    
