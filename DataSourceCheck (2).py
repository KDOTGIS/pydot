'''
Created on July 10, 2014

@author: kyleg
'''
import arcpy, os
#workspace to search for MXDs
startplace = r"F:\Cart\projects\KanPlan\MXD\Public"
arcpy.env.workspace = startplace
Workspaces = arcpy.ListWorkspaces("*", "Folder")
for Workspace in Workspaces:
    arcpy.env.workspace = Workspace
    print str(Workspace)
    #list map documents in folder
    mxdList = arcpy.ListFiles("*.mxd")
    #set relative path setting for each MXD in list.
    for mapdoc in mxdList:
        #print the mapdocument name
        print "   "
        print "MAPDOCUMENT   "+str(mapdoc)
        mapdocu = Workspace+"/"+mapdoc
        mxd = arcpy.mapping.MapDocument(mapdocu)
        
        #Print the layer name of each layer in each mapdocument, and the layer properties of each layer
        
        for lyr in arcpy.mapping.ListLayers(mxd):
            if lyr.supports("SERVICEPROPERTIES"):
                servProp = lyr.serviceProperties
                print "    Layer name:" + lyr.name +" at " + servProp.get('Connection', 'N/A')
                #print "        Service Type: " + servProp.get('ServiceType', 'N/A')
                print "        Service Type: " + servProp.get('Database', 'N/A')
                #print "        Service Type: " + servProp.get('Server', 'N/A')
                print "        Service:        " + servProp.get('Service', 'N/A')
                print "        Version:        " + servProp.get('Version', 'N/A')
                print "        User name:      " + servProp.get('UserName', 'N/A')
                #print "        Authentication: " + servProp.get('AuthenticationMode', 'N/A')
                #print "        Workspace path: "+ lyr.workspacePath       
                #print "        Feature Dataset: "+ lyr.datasetName
                print "------------------------------------------------"
            else:
                pass
    
