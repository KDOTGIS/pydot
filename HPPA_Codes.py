'''
Created on Jul 9, 2015

@author: kyleg
'''
from arcpy import MakeFeatureLayer_management, CalculateField_management, AddField_management, Delete_management
fc = r'\\gisdata\arcgis\GISdata\DASC\NG911\KDOTReview\KDOT_HPMS_2014.gdb\NUSYS_NAMES_PAVEMENT'
MakeFeatureLayer_management(fc, "PavementCode", where_clause="", workspace="")

try:
    AddField_management("PavementCode", field_name="HPPA_SURF", field_type="TEXT", field_precision="", field_scale="", field_length="24", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
    AddField_management("PavementCode", field_name="SURFACE", field_type="TEXT", field_precision="", field_scale="", field_length="24", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
except:
    print "could not add those fields"

dictHPPA_CODES =  {"1":"Unpaved", "2": "Bituminous", "3":"JPCP", "4":"JRCP", "5":"CRCP", "6":"AC OVER AC", "7":"AC OVER JCP", "8":"AC over CRCP", "9":"JC on PCC, Unbonded", "10": "Bonded PCC on PCC", "11":"Other"}
dictStupidCodes = {"1":"Unpaved", "2": "Paved", "3":"Paved", "4":"Paved", "5":"Paved", "6":"Paved", "7":"Paved", "8":"Paved", "9":"Paved", "10": "Paved", "11":"Paved"}


for code in dictStupidCodes:

    codesel = int(code)
    codename = dictStupidCodes[code]
    try:
        Delete_management("Layer", "Paved")
    except:
        print "do nothing"
    fullselect = "HPPA_HPMS_SURFACE_TYPE = "+str(codesel)
    print fullselect
    MakeFeatureLayer_management(fc, codename, fullselect, "#", "#")
    print "Made feature layer %r" % codename
    calcexp = "'"+codename+"'"
    print calcexp
    CalculateField_management(codename, "SURFACE", calcexp, "PYTHON")
    Delete_management("Layer", codename)
    print "calculated Codename"

for code in dictHPPA_CODES:
    codesel = int(code)
    codename = dictHPPA_CODES[code]
    fullselect = "HPPA_HPMS_SURFACE_TYPE = "+str(codesel)
    print fullselect
    MakeFeatureLayer_management(fc, codename, fullselect, "#", "#")
    print "Made feature layer %r" % codename
    calcexp = "'"+codename+"'"
    print calcexp
    CalculateField_management(codename, "HPPA_SURF", calcexp, "PYTHON")
    Delete_management("Layer", codename)
    print "calculated Codename"

    


"""    
fullselect = '"HPPA_HPMS_SURFACE_TYPE = "'+ codesel+'"'

    
    
exp = "1"
selection = '"HPPA_HPMS_SURFACE_TYPE = "'+ exp+'"'
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
"""