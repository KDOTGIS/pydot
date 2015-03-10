'''
Created on Oct 31, 2012

@author: kyleg
'''
import arcpy
mxd = arcpy.mapping.MapDocument("CURRENT")
for lyr in arcpy.mapping.ListLayers(mxd):
    lyr.saveACopy(lyr.name + ".lyr")
