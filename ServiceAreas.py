'''
Created on Jun 28, 2016

@author: kyleg
'''
from arcpy import (FeatureClassToFeatureClass_conversion, AddField_management, CalculateField_management, Clip_analysis,
                   gp, RasterToPolygon_conversion, Dissolve_management, FeatureToPoint_management, SpatialJoin_analysis, env)

env.overwriteOutput = 1
MASA = r'\\gisdata\arcgis\GISdata\Connection_files\ArcGIS103\sql2008\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.MASA'
FeatureClassToFeatureClass_conversion(MASA, "in_memory", "DAS1", "", "#", config_keyword="")
AddField_management("DAS1", "DAS", "Text", "#", "#", "4" )
CalculateField_management("DAS1", "DAS", "[MAINT_DISTRICT] & [MAINT_AREA] & [MAINT_SUB_AREA]", "VB", code_block="")
gp.EucAllocation_sa("DAS1", "in_memory/EucAllo_Subarea", "", "", "1E-03", "DAS", "", "")
RasterToPolygon_conversion("EucAllo_Subarea", "in_Memory/DAS_Poly", "SIMPLIFY", "Value")
Dissolve_management("DAS1", "in_memory/DAS_Dissolve", "DAS", "", "SINGLE_PART", "DISSOLVE_LINES")
FeatureToPoint_management("DAS_Dissolve", "in_memory/DAS_Dissolve_FeatureToPoint", "INSIDE")
SpatialJoin_analysis("DAS_Poly", "DAS_Dissolve_FeatureToPoint", "in_memory/MAINTENANCE_AREA", "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CONTAINS", "", "")
#this is the time to look at the in memory process and edit any null DAS values, and review the changes


Clip_analysis("in_memory/MAINTENANCE_AREA", "Database Connections/GISPROD_Shared.sde/SHARED.STATE_BOUNDARY", "in_memory/MAINTENANCE_AREA_CLIP", "")

AddField_management("MAINTENANCE_AREA_CLIP", "D", "Text", "#", "#", "1" )
AddField_management("MAINTENANCE_AREA_CLIP", "A", "Text", "#", "#", "1" )
AddField_management("MAINTENANCE_AREA_CLIP", "S", "Text", "#", "#", "1" )

CalculateField_management("MAINTENANCE_AREA_CLIP", "D", "Left( [DAS],1)", "VB", "")
CalculateField_management("MAINTENANCE_AREA_CLIP", "A", "Mid( [DAS],2, 1)", "VB", "")
CalculateField_management("MAINTENANCE_AREA_CLIP", "S", "Right( [DAS], 1)", "VB", "")



Dissolve_management("MAINTENANCE_AREA_CLIP", "in_memory/KDOT_Maint_District", "D", "", "MULTI_PART", "DISSOLVE_LINES")
Dissolve_management("MAINTENANCE_AREA_CLIP", "in_memory/KDOT_Maint_Area", "D;A", "", "MULTI_PART", "DISSOLVE_LINES")

