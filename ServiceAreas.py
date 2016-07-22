'''
Created on Jun 28, 2016

@author: kyleg
'''
import arcpy
MASA = r'\\gisdata\AGSserver\Connections\a103\mssql\read\GIS_Cansys.sde\GIS_CANSYS.SHARED.MASA'
arcpy.FeatureClassToFeatureClass_conversion(MASA, "in_memory", "DAS1", "", "#", config_keyword="")
arcpy.AddField_management("DAS1", "DAS", "Text", "#", "#", "4" )
arcpy.CalculateField_management("DAS1", field="DAS", expression="[DISTRICT] & [MAINT_AREA] & [MAINT_SUB_AREA]", expression_type="VB", code_block="")
arcpy.gp.EucAllocation_sa("DAS1", "in_memory/EucAllo_Subarea2", "", "", "1E-03", "DAS", "", "")
arcpy.RasterToPolygon_conversion(in_raster="EucAllo_Subarea2", out_polygon_features="in_Memory/DAS_Poly3", simplify="SIMPLIFY", raster_field="Value")