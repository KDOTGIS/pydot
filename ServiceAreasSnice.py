'''
Created on Jun 28, 2016

@author: kyleg

'''
def main():
    MakeSniceBoundaries()
    #UpdateSniceBoundaries()
    

def MakeSniceBoundaries():
    from arcpy import (FeatureClassToFeatureClass_conversion, AddField_management, CalculateField_management, Clip_analysis, SelectLayerByAttribute_management,
                       gp, RasterToPolygon_conversion, Dissolve_management, FeatureToPoint_management, SpatialJoin_analysis, env, Union_analysis, DeleteRows_management)
    
    env.overwriteOutput = 1
    SNIC = r'\\gisdata\arcgis\GISdata\Connection_files\ArcGIS103\sql2008\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.SNIC'
    FeatureClassToFeatureClass_conversion(SNIC, "in_memory", "DAS1", "", "#", config_keyword="")
    AddField_management("DAS1", "DAS", "Text", "#", "#", "4" )
    CalculateField_management("DAS1", "DAS", "[SNICE_DISTRICT] & [SNICE_AREA] & [SNICE_SUB_AREA]", "VB", code_block="")
    gp.EucAllocation_sa("DAS1", "in_memory/EucAllo_Subarea", "", "", "1E-03", "DAS", "", "")
    RasterToPolygon_conversion("EucAllo_Subarea", "in_Memory/DAS_Poly", "SIMPLIFY", "Value")
    Dissolve_management("DAS1", "in_memory/DAS_Dissolve", "DAS", "", "SINGLE_PART", "DISSOLVE_LINES")
    FeatureToPoint_management("DAS_Dissolve", "in_memory/DAS_Dissolve_FeatureToPoint", "INSIDE")
    SpatialJoin_analysis("DAS_Poly", "DAS_Dissolve_FeatureToPoint", "in_memory/SNICE_AREA", "JOIN_ONE_TO_ONE", "KEEP_ALL", "", "CONTAINS", "", "")
    #this is the time to look at the in memory process and edit any null DAS values, and review the changes
    
    #for some reason, SNICE boudary will not clip, it results in no values.  May be a projection issue or a extent issue
    Clip_analysis(r"in_memory/SNICE_AREA", r"Database Connections/GISPROD_Shared.sde/SHARED.STATE_BOUNDARY", r"in_memory/SNICE_AREA_CLIP")
    #for workaround Union the Euclidean Allocation areas and the state boundary, then select results outside state boundary and delete them
    
    Union_analysis("in_memory/SNICE_AREA #;'Database Connections/SDEPROD_SHARED.sde/SHARED.STATE_BOUNDARY' #", "in_memory/SNICE_AREA_Union", "ALL", "", "GAPS")
    SelectLayerByAttribute_management("SNICE_AREA_Union", "NEW_SELECTION", """"FID_STATE_BOUNDARY" = -1 OR "FID_SNICE_AREA" = -1""")
    DeleteRows_management("SNICE_AREA_Union")
    
    
    AddField_management("SNICE_AREA_Union", "D", "Text", "#", "#", "1" )
    AddField_management("SNICE_AREA_Union", "A", "Text", "#", "#", "1" )
    AddField_management("SNICE_AREA_Union", "S", "Text", "#", "#", "1" )
    
    CalculateField_management("SNICE_AREA_Union", "D", "Left( [DAS],1)", "VB", "")
    CalculateField_management("SNICE_AREA_Union", "A", "Mid( [DAS],2, 1)", "VB", "")
    CalculateField_management("SNICE_AREA_Union", "S", "Right( [DAS], 1)", "VB", "")
    
    
    Dissolve_management("SNICE_AREA_Union", "in_memory/KDOT_SNICE_District", "D", "", "MULTI_PART", "DISSOLVE_LINES")
    Dissolve_management("SNICE_AREA_Union", "in_memory/KDOT_SNICE_Area", "D;A", "", "MULTI_PART", "DISSOLVE_LINES")
    Dissolve_management("SNICE_AREA_Union", "in_memory/KDOT_SNICE_SubArea", "D;A;S", "", "MULTI_PART", "DISSOLVE_LINES")

def UpdateSniceBoundaries():
    from arcpy import TruncateTable_management, Append_management
    subarea = r'Database Connections\GISPROD_Shared.sde\SHARED.KDOT_SNICE_SUBAREA'
    area = r'Database Connections\GISPROD_Shared.sde\SHARED.KDOT_SNICE_AREAS'
    district = r'Database Connections\GISPROD_Shared.sde\SHARED.KDOT_SNICE_Districts'
    #TruncateTable_management(subarea)
    TruncateTable_management(area)
    TruncateTable_management(district)
    #Append_management("in_memory/KDOT_SNICE_SubArea", subarea, "NO_TEST")
    Append_management("in_memory/KDOT_SNICE_Area", area, "NO_TEST")
    Append_management("in_memory/KDOT_SNICE_District", district, "NO_TEST")
    
    
main()