'''
Created on Mar 4, 2013

@author: kyleg
'''
import arcpy
from arcpy import env
arcpy.env.OverwriteOutput=True
mxd = arcpy.mapping.MapDocument(r"\\gisdata\ArcGIS\GISdata\MXD\2013030401_AllLayersReset.mxd")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
ws = r"\\gisdata\arcgis\GISdata\Layers"
env.workspace = ws
slayer=arcpy.ListFiles("*.lyr")
lcount=len(slayer)
print lcount
for filelay in slayer:
    mxd = arcpy.mapping.MapDocument(r"\\gisdata\ArcGIS\GISdata\MXD\2013030401_AllLayersReset.mxd")
    lyrFile=arcpy.mapping.Layer(ws+"\\"+filelay)
    print lyrFile
    arcpy.mapping.AddLayer(df, lyrFile, "AUTO_ARRANGE")
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()
    del mxd
    del lyrFile
    
import arcpy, os, glob

# Set Workspace
base_Folder = r"\\gisdata\arcgis\GISdata\Layers"
arcpy.env.Workspace = base_Folder
arcpy.env.OverwriteOutput = True

# User input for NTS mapsheet name.  This variable is also used to search for the correct mapsheet.
# map_No = arcpy.GetParameterAsText(0)
#map_No = "031L33"
# arcpy.AddMessage("Map Number: " + map_No)

# Canvec data is stored in folders, broken down by 1:50000 mapsheet number (eg: 031, 001, 045, etc).
# This variable extracts the folder name to be used when finding the correct folder
# folder_Name = map_No[0:3]
# arcpy.AddMessage("Folder Name: " + folder_Name)
# print folder_Name

#Established the correct folder to look in when loading the specified layers.
# search_Folder = base_Folder + "\\" + folder_Name + "\\" + map_No
# arcpy.AddMessage("Search Folder: " + search_Folder)
# print search_Folder

##mxd = arcpy.mapping.MapDocument("CURRENT")
##dataFrame = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
lyr_List = glob.glob(str(base_Folder) + "\*.lyr")
arcpy.AddMessage("lyr List: ")
for lyr in lyr_List:
    arcpy.AddMessage(lyr)
print shp_List


for layer in shp_List:
    mxd = arcpy.mapping.MapDocument("CURRENT")
    dataFrame = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
    
    addLayer = arcpy.mapping.Layer(layer)
    arcpy.mapping.AddLayer(dataFrame, addLayer, "BOTTOM")
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()
    del addLayer, mxd