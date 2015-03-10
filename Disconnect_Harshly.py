'''
Created on Mar 12, 2013

@author: kyleg
'''
import arcpy
import ListUsersProd
ListUsersProd.main()

admin_workspace = r"Database Connections\SDEPROD_SDE.sde"
#admin_workspace = r"Database Connections\SDEDEV_SDE.sde"

arcpy.env.workspace = admin_workspace

users = arcpy.ListUsers(admin_workspace) #

arcpy.DisconnectUser(admin_workspace, "All")
        
arcpy.AcceptConnections(admin_workspace, True)

