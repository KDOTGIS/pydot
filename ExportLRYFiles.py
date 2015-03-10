'''
Created on Oct 31, 2012

@author: kyleg
'''
import arcpy
mxd = arcpy.mapping.MapDocument("CURRENT")
from arcpy import env
arcpy.env.OverwriteOutput=True
ws = r"\\gisdata\arcgis\GISdata\Layers\SHARED"
env.workspace = ws

for lyr in arcpy.mapping.ListLayers(mxd):
    print lyr
    lyr.saveACopy(ws+"\\"+lyr.name + ".lyr")
