'''
Created on Sep 5, 2013

@author: kyleg
'''
import arcpy
ws = r"Database Connections/SDEDEV_SHARED.sde/"
arcpy.env.workspace = ws
schema = "SHARED"
fctest = "COUNTIES"
fd = "SHARED"
fclist = arcpy.ListFeatureClasses(schema+"."+fctest)

for fc in fclist:
    desc = arcpy.Describe(fc)
    print fc + "; " +desc.shapeType
        #arcpy.RegisterWithGeodatabase_management("Database Connections/SDEDEV_SHARED.sde/SHARED.COUNTIES")
    destdb = ws+schema+"."+fd
    fcn = str(fc)
    print fc
    if arcpy.Exists(fc):
        print fc.index(".")
        #arcpy.FeatureClassToFeatureClass_conversion("Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS","Database Connections/SDEDEV_SHARED.sde/SHARED.SHARED","AIRPORTS1","#","""STRARPT_ID "STRARPT_ID" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRARPT_ID,-1,-1;STRARPT_NAME "STRARPT_NAME" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRARPT_NAME,-1,-1;STRASSOCIATED_CITY "STRASSOCIATED_CITY" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRASSOCIATED_CITY,-1,-1;STRCOUNTY "STRCOUNTY" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRCOUNTY,-1,-1;STRKDOT_DIST "STRKDOT_DIST" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRKDOT_DIST,-1,-1;STRUS_CONGRESSIONAL_DIST "STRUS_CONGRESSIONAL_DIST" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRUS_CONGRESSIONAL_DIST,-1,-1;STRSTATE_SENATE_DIST "STRSTATE_SENATE_DIST" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRSTATE_SENATE_DIST,-1,-1;STROWNERSHIP "STROWNERSHIP" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STROWNERSHIP,-1,-1;STRSTATE_HOUSE_DIST "STRSTATE_HOUSE_DIST" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRSTATE_HOUSE_DIST,-1,-1;STRUSE "STRUSE" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRUSE,-1,-1;YSNNPIAS "YSNNPIAS" true true false 4 Long 0 10 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,YSNNPIAS,-1,-1;STRP_OR_NP "STRP_OR_NP" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRP_OR_NP,-1,-1;STRFAA_SITE_NBR "STRFAA_SITE_NBR" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRFAA_SITE_NBR,-1,-1;STRFAA_SVC_LEVEL "STRFAA_SVC_LEVEL" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRFAA_SVC_LEVEL,-1,-1;YSNFAR_PART_139 "YSNFAR_PART_139" true true false 4 Long 0 10 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,YSNFAR_PART_139,-1,-1;STRSTATE_SYSTEM_ROLE "STRSTATE_SYSTEM_ROLE" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRSTATE_SYSTEM_ROLE,-1,-1;YSNAIR_AMB_CAPABLE "YSNAIR_AMB_CAPABLE" true true false 4 Long 0 10 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,YSNAIR_AMB_CAPABLE,-1,-1;STRELEVATION "STRELEVATION" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRELEVATION,-1,-1;HPLLINK_TO_ARPT_DIR "HPLLINK_TO_ARPT_DIR" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,HPLLINK_TO_ARPT_DIR,-1,-1;STRLATITUDE "STRLATITUDE" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRLATITUDE,-1,-1;STRLONGITUDE "STRLONGITUDE" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRLONGITUDE,-1,-1;HPLLINK_TO_5010 "HPLLINK_TO_5010" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,HPLLINK_TO_5010,-1,-1;STRWXEQUIPMENT "STRWXEQUIPMENT" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRWXEQUIPMENT,-1,-1;STRFED_NON_FED "STRFED_NON_FED" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRFED_NON_FED,-1,-1;HPLHYPERLINK_TO_WX_DATA "HPLHYPERLINK_TO_WX_DATA" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,HPLHYPERLINK_TO_WX_DATA,-1,-1;STRWXFREQUENCY "STRWXFREQUENCY" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRWXFREQUENCY,-1,-1;STRWXPHONE "STRWXPHONE" true true false 255 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,STRWXPHONE,-1,-1;LATITUDE1 "LATITUDE1" true true false 15 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,LATITUDE1,-1,-1;LONGITUDE1 "LONGITUDE1" true true false 15 Text 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,LONGITUDE1,-1,-1;LATSECONDS1 "LATSECONDS1" true true false 8 Double 0 38 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,LATSECONDS1,-1,-1;LONGSECONDS1 "LONGSECONDS1" true true false 8 Double 0 38 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,LONGSECONDS1,-1,-1;SE_ANNO_CAD_DATA "SE_ANNO_CAD_DATA" true true false 0 Blob 0 0 ,First,#,Database Connections/SDEDEV_SHARED.sde/SHARED.AIRPORTS,SE_ANNO_CAD_DATA,-1,-1""","SDO_GEOMETRY")
        print destdb
        s = fc.index(".")+1
        destfc = "temp"+fc[s:]
        print destfc
        #arcpy.FeatureClassToFeatureClass_conversion(fc, destdb, destfc,"#", "#", "SDO_GEOMETRY")
        #arcpy.Delete_management(fc)
        renamed = destfc#[s+4:]
        print renamed
        #arcpy.Rename_management(destfc, "#", renamed)
    else:
        print "input fc has error"