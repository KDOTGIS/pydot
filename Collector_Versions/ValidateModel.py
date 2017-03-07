'''
Created on Jun 22, 2016
use this when you have an issue importing from Sparx EA
first pass validation
next, see if you can do this.  
You might have to use it a lot it you are learning sparx.
things to look for:
domain values have the correct field type for the values

dont be tempted to go changing all the xml around in one session without frequently using this script

@author: kyleg
'''

if __name__ == '__main__':
    pass

def ValidatetoFileGDB():
    from arcpy import ImportXMLWorkspaceDocument_management, Exists, CreateFileGDB_management, Delete_management


    xmlIn = r"C:\temp\ValidateThis.xml"
    gdbname = "Validate"
    GDB_In = r"C:/temp/"+gdbname
    gdbin = GDB_In+".gdb"
    if Exists(gdbin):
        Delete_management(gdbin, "Workspace")
        CreateFileGDB_management(r"C:/temp", gdbname, "CURRENT")
        print "new geodatabase created"

    ImportXMLWorkspaceDocument_management(gdbin, xmlIn, import_type="SCHEMA_ONLY")
ValidatetoFileGDB()
print "validated"