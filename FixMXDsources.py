'''
Created on Mar 4, 2013

@author: kyleg
'''
import arcpy
mxd = arcpy.mapping.MapDocument("CURRENT")
from arcpy import env
layerws = r'\\gisdata\arcgis\GISdata\Layers'
env.workspace = layerws
arcpy.env.OverwriteOutput=True
ProdDS = r'Database Connections\SDEPROD_GIS.sde'
ProdUser = 'GIS'
DestDS = r'Database Connections\SDEPROD_KDOT_GIS.sde'
DestUser = 'KDOT_GIS'

#replace data sources
mxd.findAndReplaceWorkspacePaths(ProdDS+"."+ProdUser,DestDS+"."+DestUser, "True")
arcpy.RefreshActiveView
arcpy.RefreshTOC

layerws = r'\\gisdata\arcgis\GISdata\Layers'
for lyr in arcpy.mapping.ListLayers(mxd): 
    lyr.findAndReplaceWorkspacePath(find_workspace_path=lyr.dataSource, replace_workspace_path=r"C:\Newpath\To\SDE_ConnectionFile.sde")
    lyr.saveACopy(layerws+"\\"+lyr.name + ".lyr")
    print lyr

arcpy.RefreshCatalog
    

