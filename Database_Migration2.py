'''
Created on Jan 22, 2014
the first part of the migration (GISPROD 2014) is run in SAFE FME, exporting and projecting all desired data from GISPROD city, countymap, and shared schemas to a file geodatabase
the FME filters Oracle Spatial geometry types, and appends the geometry type (point, line, polygon) to the feature name
This script removes the appended part of the feature name

Hospitals did not export for some reason, had to move it over manually

This script works after the data has been imported into the Geodatabase, in the ST_Geomtetry type.

@author: kyleg
'''
from arcpy import env, ListFeatureClasses, DefineProjection_management, Describe, FeatureClassToFeatureClass_conversion, Exists, EnableEditorTracking_management, AddField_management, RegisterAsVersioned_management, ListFields
coor_system="PROJCS['NAD_83_Kansas_Lambert_Conformal_Conic_Feet',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['false_easting',1312333.333333333],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',-98.25],PARAMETER['standard_parallel_1',37.5],PARAMETER['standard_parallel_2',39.5],PARAMETER['scale_factor',1.0],PARAMETER['latitude_of_origin',36.0],UNIT['Foot_US',0.3048006096012192]]"

sourceGDB = r"C:/temp/SDEPROD.gdb"
print sourceGDB
OracleDB = r"Database Connections\SDEDEV_SHARED.sde"
env.workspace = sourceGDB

#disabling Z values on the output enables WFS_T editing capability on the server level
env.outputZFlag = "Disabled"

def MigrateFeatureClasses():
    fclist = ListFeatureClasses()

    for fc in fclist:
        if Exists(OracleDB+"/"+fc):
            print str(OracleDB+"/"+fc) + " Aleady exist"
            print
        else:
            print str(fc) + "... exporting to SDO in " + str(OracleDB)
            FeatureClassToFeatureClass_conversion(fc,OracleDB,str(fc), where_clause="#", config_keyword="SDO_GEOMETRY")

def TrackEditsAndVersion():
    env.workspace = OracleDB
    fclist = ListFeatureClasses()
    for fc in fclist:
            print fc
            if str(fc)[-2:]=='MV':
                print "no actions taken on a Materialized View"
                pass
            else:
                if ListFields(fc, "GlobalID"):
                    print "GlobalID Field already added"
                else:
                    AddField_management(OracleDB+"/"+fc, "GlobalID", "GUID", "#", "#", "#", "GlobalID", "NON_NULLABLE", "REQUIRED")
                    AddField_management(OracleDB+"/"+fc, "START_DATE", "DATE", "#", "#", "#", "Start_Date", "NULLABLE", "NON_REQUIRED")
                    AddField_management(OracleDB+"/"+fc, "END_DATE", "DATE", "#", "#", "#", "End_Date", "NULLABLE", "NON_REQUIRED")
                    EnableEditorTracking_management(OracleDB+"/"+fc,creator_field="Creator",creation_date_field="Created",last_editor_field="Editor",last_edit_date_field="Edited",add_fields="ADD_FIELDS",record_dates_in="UTC")
                    RegisterAsVersioned_management( OracleDB+"/"+fc, "NO_EDITS_TO_BASE")

def SetProjection():
    env.workspace = OracleDB
    fclist = ListFeatureClasses()
    for fc in fclist:
        if str(fc)[-2:]=='MV':
            print "no actions taken on a Materialized View"
            pass
        else:
            spatial_ref = Describe(fc).spatialReference
                # If the spatial reference is unknown
            if spatial_ref.name == "Unknown":
                print("{0} has an unknown spatial reference".format(fc))
                DefineProjection_management(OracleDB+"/"+fc,coor_system)
            # Otherwise, print out the feature class name and
            # spatial reference
            else:
                print("{0} : {1}".format(fc, spatial_ref.name))




def CreateVersionTree():
    defaultVersion = "shared.DEFAULT"
    WfsVersionName = "WFS_CURRENT"
    GISversionName = "ARC_CURRENT"
    WfsVersionName1 = "WFS_PLANNED"
    GISVersionName1 = "ARC_PLANNED"
    CreateVersion_management(inWorkspace, defaultVersion, WFSversionName, "PUBLIC")
    CreateVersion_management(inWorkspace, WFSversionName, WFSversionName1, "PUBLIC")
    CreateVersion_management(inWorkspace, defaultVersion, GISversionName, "PUBLIC")
    CreateVersion_management(inWorkspace, GISversionName, GISversionName1, "PUBLIC")

#MigrateFeatureClasses()
#TrackEditsAndVersion()
SetProjection()
