'''
Created on Jan 22, 2014
the first part of the migration (GISPROD 2014) is run in SAFE FME, exporting and projecting all desired data from GISPROD city, countymap, and shared schemas to a file geodatabase
the FME filters Oracle Spatial geometry types, and appends the geometry type (point, line, polygon) to the feature name
This script removes the appended part of the feature name

Hospitals did not export for some reason, had to move it over manually



@author: kyleg
'''
import arcpy

ws = r"C:\temp\SDEPROD.gdb"
arcpy.env.workspace = ws
print ws
        
points = arcpy.ListFeatureClasses("*_point")
for fc in points:
    namestring = str(fc)
    newname = namestring.replace("_point", "")
    print namestring +" changed to "+ newname
    arcpy.Rename_management(fc,newname)
    
lines = arcpy.ListFeatureClasses("*_line")

for fc in lines:
    namestring = str(fc)
    print namestring
    newname = namestring.replace("_line", "")
    print namestring +" changed to "+ newname
    arcpy.Rename_management(fc,newname)
    
polys = arcpy.ListFeatureClasses("*_polygon")
    
for fc in polys:
    namestring = str(fc)
    print namestring
    newname = namestring.replace("_polygon", "")
    print namestring +" changed to "+ newname
    arcpy.Rename_management(fc,newname)


#arcpy.ExportXMLWorkspaceDocument_management(ws, r"C:\temp\SDEPROD_dataset.xml" )