'''
Created on Sep 3, 2013

@author: kyleg
'''
import arcpy
ws = r"Database Connections/SDEDEV_SHARED.sde/"
arcpy.env.workspace = ws
fclist = arcpy.ListFeatureClasses("SHARED.*")

for fc in fclist:
    desc = arcpy.Describe(fc)
    print fc + "; " +desc.shapeType
        #arcpy.RegisterWithGeodatabase_management("Database Connections/SDEDEV_SHARED.sde/SHARED.COUNTIES")

