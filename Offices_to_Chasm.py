import arcpy
PRODDC = r'Database Connections\sdeprod_GIS.sde'
PRODUSER = 'GIS'
ABYSS = r'Database Connections\CHASM.sde\KDOT.KDOT_SHARED'
Offices = 'KDOT_OFFICES'
inFC = PRODDC+'\\'+PRODUSER+'.'+Offices
arcpy.FeatureClassToFeatureClass_conversion(inFC, ABYSS, Offices)