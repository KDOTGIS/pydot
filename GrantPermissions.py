'''
Created on Feb 28, 2013

@author: kyleg
'''

import arcpy

GISusername = "KDOT_GIS"

SYSPROD = r"Database Connections/SDEPROD_GIS.sde"  #PROD DB OWNER
SYSDEV = r"Database Connections/SDEDEV_GISDEV.sde"  #DEV DB OWNER
ViewPerm = "GRANT"
EditPerm = "GRANT"   #options are GRANT, AS_IS, REVOKE

#Grant Dev permissions to everything
arcpy.env.workspace = SYSDEV
datasets = arcpy.ListDatasets("*", "Feature")

for dataset in datasets:
    try:
        arcpy.ChangePrivileges_management(SYSDEV+"//"+dataset,GISusername, ViewPerm, EditPerm)
    except:
        print SYSDEV+" "+dataset + "!!!"
        pass
#PROD
arcpy.env.workspace = SYSPROD
datasets = arcpy.ListDatasets("*", "Feature")

for dataset in datasets:
    try:
        arcpy.ChangePrivileges_management(SYSPROD+"//"+dataset,GISusername, ViewPerm, EditPerm)
    except:
        print SYSPROD+" "+dataset + "!!!"
        pass