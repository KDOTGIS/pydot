from arcpy import MakeFeatureLayer_management, CalculateField_management, AddField_management
fc = r'//gisdata/arcgis/GISdata/DASC/NG911/KDOTReview/KDOT_HPMS_2014.gdb/RM_SectionData'
MakeFeatureLayer_management(fc, "RM_SectionData_Layer", where_clause="", workspace="")



AddField_management("RM_SectionData_Layer", field_name="HPPA_SURF", field_type="TEXT", field_precision="", field_scale="", field_length="24", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
AddField_management("RM_SectionData_Layer", field_name="HPPA_CODE", field_type="LONG", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")


MakeFeatureLayer_management(fc, exp, "SURF BETWEEN 0 AND 40", "#", "#")
expression = '"'+exp+'"'
CalculateField_management(exp, "HPPA_SURF", expression, "PYTHON")
CalculateField_management(exp, "HPPA_CODE", "1", "PYTHON")

exp = "bituminous"
MakeFeatureLayer_management(fc, exp, "SURF BETWEEN 41 AND 61", "#", "#")
expression = '"'+exp+'"'
CalculateField_management(exp, "HPPA_SURF", expression, "PYTHON")
CalculateField_management(exp, "HPPA_CODE", "2", "PYTHON")

exp = "AC Overlay over PCC"
MakeFeatureLayer_management(fc, exp, "SURF = 62", "#", "#")
expression = '"'+exp+'"'
CalculateField_management(exp, "HPPA_SURF", expression, "PYTHON")
CalculateField_management(exp, "HPPA_CODE", "7", "PYTHON")

exp = "JPCP"
MakeFeatureLayer_management(fc, exp, "SURF = 71", "#", "#")
expression = '"'+exp+'"'
CalculateField_management(exp, "HPPA_SURF", expression, "PYTHON")
CalculateField_management(exp, "HPPA_CODE", "3", "PYTHON")

exp = "JRCP"
MakeFeatureLayer_management(fc, exp, "SURF = 72", "#", "#")
expression = '"'+exp+'"'
CalculateField_management(exp, "HPPA_SURF", expression, "PYTHON")
CalculateField_management(exp, "HPPA_CODE", "4", "PYTHON")

exp = "CRCP"
MakeFeatureLayer_management(fc, exp, "SURF = 73", "#", "#")
expression = '"'+exp+'"'
CalculateField_management(exp, "HPPA_SURF", expression, "PYTHON")
CalculateField_management(exp, "HPPA_CODE", "5", "PYTHON")
#73 and 74 DNE in data

exp = "PCC"
MakeFeatureLayer_management(fc, exp, "SURF = 80", "#", "#")
expression = '"'+exp+'"'
CalculateField_management(exp, "HPPA_SURF", expression, "PYTHON")
CalculateField_management(exp, "HPPA_CODE", "10", "PYTHON")