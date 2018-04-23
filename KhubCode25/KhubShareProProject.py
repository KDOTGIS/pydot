'''
Created on Mar 7, 2018
share the designated ArcGIS Pro project to ArcGIS online

https://pro.arcgis.com/en/pro-app/tool-reference/data-management/share-package.htm

This tool may have limited use in a Python script outside of ArcGIS applications 
when sharing a package to a portal that uses OAUTH2 authentication. The ArcGIS Online 
for example, uses this authentication method. To authenticate, you must connect directly 
to the portal from the application. You will only be able to use this tool in a Python 
script if the application is open and connected to the portal, or you're connecting to a 
portal which uses traditional authentication mechanisms and allow the user name and 
password to be passed in.

reporting a bug, the python PackageProject_management function will not work with a non-basemap map service, such as valtus imagery or 
an editable feature service from ArcGIS server.  To accomodate this script, those layers have been removed from the project.


@author: kyleg
'''
   
def ShareProToOnline(onlinepassword):
    import datetime
    startDateTime = datetime.datetime.now()
    print ("this script takes about 8 minutes")


    from arcpy import PackageProject_management, SharePackage_management, os, env
    env.overwriteOutput = True
    #import getpass
    from KhubCode25.KhubCode25Config import localProProjectPath, localProProjectName, AGOUser
    localproject = os.path.join(localProProjectPath,localProProjectName)
    print(localproject)
    print ("logging in as"+AGOUser)
    try:
        username = AGOUser
        password = onlinepassword
        fileformatDateStr = startDateTime.strftime("%Y%m%d")
        summary = "This project contains maps that link to KDOT SQL Server databases AR58 gdb_prod, AR68 gdb_Dev, and a local file geodatabase copied from DT00ar58 gdb_prod for use on Amazon Servers or otherwise outside the KDOT network. The schema presentation matches the schema for the 1spatial extension.  For the local geodatabse copy, there is one map displaying highway symbols based on the source LRS network route prefix and direction, and another map displaying highway symbols based on the target network classification and direction"
    
        PackageProject_management(localproject, r"C:\temp\KhubDataCleanup25_"+fileformatDateStr+".ppkx", "INTERNAL", "PROJECT_PACKAGE", "DEFAULT", "ALL", None, summary, "Khub", "CURRENT", "NO_TOOLBOXES", "NO_HISTORY_ITEMS", "READ_WRITE")
        #SharePackage_management(SharePackage_management (localProProjectName, "KanDOT", password, summary, "Khub, 1spatial, Roads, Centerlines, LRS, Highways", "KANSAS DOT Restricted Use - 23 U.S.C. 409", "MYGROUPS", "Data Quality Assurance and Quality Control Group", "MYORGANIZATION"))
        print("package created, now sharing")
        SharePackage_management(r"C:\temp\KhubDataCleanup25_"+fileformatDateStr+".ppkx", username, password, summary, r"Khub,Project Package,ppkx,2D,ArcGIS Pro", "KDOT", "MYGROUPS", "Data Quality Assurance and Quality Control Group", "MYORGANIZATION")
    except:
        import getpass
        username = "kyle.gonterwitz_KSDOT"
        password = getpass.getpass("Enter Password for "+str(username)+":")
        print("logging in as "+username )
        #p = mp.ArcGISProject(localproject)
        fileformatDateStr = startDateTime.strftime("%Y%m%d")
        summary = "This project contains maps that link to KDOT SQL Server databases AR58 gdb_prod, AR68 gdb_Dev, and a local file geodatabase copied from DT00ar58 gdb_prod for use on Amazon Servers or otherwise outside the KDOT network. The schema presentation matches the schema for the 1spatial extension.  For the local geodatabse copy, there is one map displaying highway symbols based on the source LRS network route prefix and direction, and another map displaying highway symbols based on the target network classification and direction"
    
        PackageProject_management(localproject, r"C:\temp\KhubDataCleanup25_"+fileformatDateStr+".ppkx", "INTERNAL", "PROJECT_PACKAGE", "DEFAULT", "ALL", None, summary, "Khub", "CURRENT", "NO_TOOLBOXES", "NO_HISTORY_ITEMS", "READ_WRITE")
        #SharePackage_management(SharePackage_management (localProProjectName, "KanDOT", password, summary, "Khub, 1spatial, Roads, Centerlines, LRS, Highways", "KANSAS DOT Restricted Use - 23 U.S.C. 409", "MYGROUPS", "Data Quality Assurance and Quality Control Group", "MYORGANIZATION"))
        print("package created, now sharing")
        SharePackage_management(r"C:\temp\KhubDataCleanup25_"+fileformatDateStr+".ppkx", username, password, summary, r"Khub,Project Package,ppkx,2D,ArcGIS Pro", "KDOT", "MYGROUPS", "Data Quality Assurance and Quality Control Group", "MYORGANIZATION")

def main():
    ShareProToOnline()
    
if __name__ == '__main__':
    import datetime
    startDateTime = datetime.datetime.now()
    main()
    print('project packaged and shared in {} hours, minutes, seconds.'.format(datetime.datetime.now()-startDateTime))
else:
    print("functions from KhubShareProProject imported to main script")