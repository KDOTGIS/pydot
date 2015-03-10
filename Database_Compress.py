'''
Created on Mar 12, 2013

@author: kyleg
'''

if __name__ == '__main__':
    pass

import arcpy

# Set Admin workspace variable
admin_workspace = r"Database Connections\SDEPROD_SDE.sde"

# Block connections
arcpy.AcceptConnections(admin_workspace, False)

# Disconnect users
arcpy.DisconnectUser(admin_workspace, 'ALL')

# Reconcile/Post using default parameters.
arcpy.ReconcileVersions_management(admin_workspace, 'ALL_VERSIONS',
                                   'sde.DEFAULT', with_post='POST')

# Compress the geodatabase
#arcpy.Compress_management(admin_workspace)

# Allow connections.
arcpy.AcceptConnections(admin_workspace, True)