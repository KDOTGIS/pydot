'''
Created on Jun 17, 2013

@author: kyleg
'''
import arcpy
mxd = arcpy.mapping.MapDocument("CURRENT")
for lyr in arcpy.mapping.ListLayers(mxd):
    print lyr.name
    try:
        arcpy.AddField_management(lyr, "URL_link", "TEXT", "#", "#", "255", "#", "NULLABLE", "NON_REQUIRED")
    except:
        "this is probably a grouped layer"
        pass

URLBase = "http://kdotdev/KDOTOrg/BurTransPlan/GeneratedReports/Planningmaps/Gateway_GIS/"
URLCalc = """"http://kdotdev/KDOTOrg/BurTransPlan/GeneratedReports/Planningmaps/Gateway_GIS/"+Mid([Hyperlink_],3,150)"""
URLCalc2 = """"http://kdotdev/KDOTOrg/BurTransPlan/GeneratedReports/Planningmaps/Gateway_GIS/"+Mid([Hyperlink],3,150)"""
for lyr in arcpy.mapping.ListLayers(mxd, "*"):
    print lyr.name
    try:
        arcpy.CalculateField_management(lyr, "URL_link", URLCalc, "VB","#")
        arcpy.CalculateField_management(lyr, "URL_link", URLCalc2, "VB","#")
    except:
        "this is probably didn't work for a reason"
        pass
    
SpaceCalc = """!URL_link!.replace(" ", "%20")"""
for lyr in arcpy.mapping.ListLayers(mxd, "*"):
    print lyr.name
    try:
        arcpy.CalculateField_management(lyr, "URL_link", SpaceCalc, "PYTHON_9.3","#")
    except:
        "this is probably didn't work for a reason"
        pass
