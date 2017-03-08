'''
Created on Aug 24, 2016

@author: kyleg
'''

if __name__ == '__main__':
    pass
    from arcpy import env
    env.overwriteOutput = 1
    gdbname = "RefpostLocate"
    fcname = "ReferencePosts"
    GDB_In = r"C:/temp/"+gdbname
    gdbin = GDB_In+".gdb"

def GetRefposts():
    from arcpy import WFSToFeatureClass_conversion, CreateFileGDB_management, Delete_management
    input_WFS_server = r"http://wfs.ksdot.org/arcgis_web_adaptor/services/Structures/Reference_Post_Signs/MapServer/WFSServer?request=GetCapabilities&service=WFS"
    gdbin = GDB_In+".gdb"
    try:
        CreateFileGDB_management(r"C:/temp", gdbname, "CURRENT")
        print "new created " + gdbin
    except:
        Delete_management(gdbin, "Workspace")
        CreateFileGDB_management(r"C:/temp", gdbname, "CURRENT")
        print "refreshed " + gdbin
    WFSToFeatureClass_conversion(input_WFS_server, fcname, gdbin, fcname)
    
def FormatGeocoding():
    fcname = "ReferencePosts"
    fcnameout = "CardinalRefposts"
    cardfcfull = gdbin+r"/"+fcnameout
    print cardfcfull
    from arcpy import AddField_management, CalculateField_management, FeatureClassToFeatureClass_conversion
    try:
        FeatureClassToFeatureClass_conversion(gdbin+r"/"+fcname, gdbin, fcnameout, """DIRECTION in (1, 3)""")
        AddField_management(cardfcfull, "Address", "TEXT", "", "", "55", "", "NULLABLE", "NON_REQUIRED", "")
        AddField_management(cardfcfull, "CountyNum", "TEXT", "", "", "3", "", "NULLABLE", "NON_REQUIRED", "")
    except:
        print "stuff exists"

    address="""Int([REFPOST]) &" "& [LRS]"""
    print address
    countynum = 'Left( [LRS_KEY],3)'
    CalculateField_management(cardfcfull, "CountyNum", countynum, "VB")
    CalculateField_management(cardfcfull, "Address", address, "VB")
GetRefposts()
FormatGeocoding()