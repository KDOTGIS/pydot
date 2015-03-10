'''
Created on Aug 12, 2013

@author: kyleg
'''
import arcpy

inws = r"//gisdata/arcgis/GISdata/KDOT/BTP/Projects/CCL/CCL20130812.gdb"
produser = "GIS"
prodpath = r"Database Connections\SDEPROD_GIS.sde"+"\\"+produser
fd = "Administrative_Boundary"
mod_lyr = prodpath+"fd"+"\\"+produser+".CITY_LIMITS_MODS"
kdor_cl = prodpath+"fd"+"\\"+produser+".CITY_LIMITS_KDOR"

arcpy.MakeFeatureLayer_management(mod_lyr,"CITY_LIMITS_MODS_ADD","MODTYPE = 'ADD'","#","#")
arcpy.MakeFeatureLayer_management(mod_lyr,"CITY_LIMITS_MODS_SUBTRACT","MODTYPE = 'SUBTRACT'","#","#")

arcpy.Erase_analysis(kdor_cl,"CITY_LIMITS_MODS_SUBTRACT",inws+"//CITY_LIMITS_KDOT","#")
arcpy.Append_management("CITY_LIMITS_MODS_ADD",inws+"//CITY_LIMITS_KDOT","NO_TEST", "#")

