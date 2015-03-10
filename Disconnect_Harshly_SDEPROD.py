'''
Created on Mar 12, 2013

@author: kyleg
'''
from arcpy import DisconnectUser, AcceptConnections, env, ListUsers
admin_workspace = r"Database Connections\SDEPROD_SDE.sde"
env.workspace = admin_workspace
users = ListUsers(admin_workspace) #
print users
DisconnectUser(admin_workspace, "All")
AcceptConnections(admin_workspace, True)