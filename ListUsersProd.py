'''
Created on Feb 28, 2013

@author: kyleg
'''




import arcpy

def main():
    users = arcpy.ListUsers("Database Connections/SDEPROD_SDE.sde")
    for user in users:
        print("Username: {0}, Connected at: {1}".format(user.Name, user.ConnectionTime))

if __name__ == "__main__":
    main()