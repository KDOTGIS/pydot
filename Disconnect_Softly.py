'''
Created on Mar 12, 2013

@author: kyleg
'''
import arcpy 
import ListUsersProd
ListUsersProd.main()

admin_workspace = r"Database Connections\SDEPROD_SDE.sde"
arcpy.env.workspace = admin_workspace
user_name = "GIS"
users = arcpy.ListUsers(admin_workspace) #

for item in users:
    if item.Name == user_name:
        print (item.ID, item.Name, item.ClientName, item.IsDirectConnection)
        arcpy.DisconnectUser(admin_workspace, item.ID)
        
arcpy.AcceptConnections(admin_workspace, True)