'''
Created on Mar 12, 2013

@author: kyleg
'''


import arcpy, os
from arcpy import env

# set workspace
workspace = r'Database Connections\SDEPROD_GIS.sde\GIS.KDOT_RAIL'

# set the workspace environment
env.workspace = workspace

# Use a list comprehension to get a list of version names where the owner
# is the current user and make sure sde.default is not selected.
verList = [ver.name for ver in arcpy.da.ListVersions() if ver.isOwner== True and ver.name.lower() != 'sde.default']

arcpy.ReconcileVersions_management(workspace,"ALL_VERSIONS","SDE.Default",verList,"LOCK_AQUIRED","NO_ABORT","BY_OBJECT","FAVOR_TARGET_VERSION","NO_POST","KEEP_VERSION","c:\RecLog.txt")
print 'Reconciling Complete'

        