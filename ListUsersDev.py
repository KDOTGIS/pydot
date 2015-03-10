'''
Created on Feb 28, 2013

@author: kyleg
'''




import arcpy

users = arcpy.ListUsers("Database Connections/SDEDEV_SDE.sde")
for user in users:
    print("Username: {0}, Connected at: {1}".format(
        user.Name, user.ConnectionTime))
