'''
Created on Jan 14, 2014

@author: kyleg
'''
import arcpy
outws = r'//gisdata/arcgis/GISdata/Layers/CCL/2014/CCL_INTERCHANGE/'
mxd = arcpy.mapping.MapDocument("CURRENT")
for lyr in arcpy.mapping.ListLayers(mxd):
    print lyr.name
    lyr.saveACopy(outws+lyr.name + ".lyr")
