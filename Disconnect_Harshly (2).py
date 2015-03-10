'''
Created on Mar 12, 2013

@author: kyleg
'''
import arcpy
#admin_workspace = r"Database Connections\SQL61_AVIATION_DB.sde"
#admin_workspace = r"Database Connections\SDEDev-sde.sde"
admin_workspace = r"Database Connections\SDEPROD_sde.sde"
arcpy.env.workspace = admin_workspace
users = arcpy.ListUsers(admin_workspace) #
print users
arcpy.DisconnectUser(admin_workspace, "All")
arcpy.AcceptConnections(admin_workspace, True)