'''
Created on Nov 16, 2015

@author: kyleg
'''
from arcpy import FeatureClassToFeatureClass_conversion, MakeFeatureLayer_management, FlipLine_edit, CreateRoutes_lr, MakeRouteEventLayer_lr

Non_State_Roads = r"\\gisdata\arcgis\GISdata\Connection_files\shared@sdeprod.sde\SHARED.NON_STATE_SYSTEM"
Non_State_Sections = r"\\gisdata\arcgis\GISdata\Connection_files\shared@sdeprod.sde\SHARED.NON_STATE_SECTIONS"

#import cx_Oracle
#con = cx_Oracle.connect('shared/gis@sdeprod')
# here, explore using cx_Oracle to run/commit the following SQL Query

#update  NON_STATE_SECTIONS S
#set S.END_MP = S.milepost+ S.length
#where (ABS(S.END_MP - (S.MILEPOST+ S.LENGTH))) >= 0.001 or S.END_MP is null

#print con.version
#con.close()

FeatureClassToFeatureClass_conversion(Non_State_Roads, "in_memory", "Rural_Major_Collectors", "LRS_KEY like '%R%'")
MakeFeatureLayer_management("Rural_Major_Collectors", "Rural_Major_Collectors_Flips", """"LRS_BACKWARDS" <0""")
FlipLine_edit("Rural_Major_Collectors_Flips")
CreateRoutes_lr("Rural_Major_Collectors", "LRS_KEY", "in_memory/RMC_Routes", "TWO_FIELDS", "LRS_BEG_CNTY_LOGMILE", "LRS_END_CNTY_LOGMILE", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
MakeRouteEventLayer_lr("RMC_Routes", "LRS_KEY", Non_State_Sections, "LRS_KEY LINE MILEPOST END_MP", "NON_STATE_SECTIONS", "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
MakeFeatureLayer_management("NON_STATE_SECTIONS", "HP_Colls", "HPMS is not null AND SUPERCEDEDASOF IS NULL")
