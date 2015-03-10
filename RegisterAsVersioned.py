'''
Created on Mar 12, 2013

@author: kyleg
'''
# Import system modules
import arcpy

# Set local variables
datasetName = r"Database Connections/SDEPROD_GIS.sde/GIS.KDOT_RAIL"

# Execute RegisterAsVersioned
arcpy.RegisterAsVersioned_management( datasetName, "NO_EDITS_TO_BASE")