'''
Created on Feb 28, 2013

@author: kyleg
'''
import arcpy
SDEUsername = "KDOT_GIS"
DevRole = "GIS_VIEWER"  #Options are GIS_ADMIN, GIS_DEVELOPER, GIS_EDITOR, GIS_VIEWER, GIS_AVIATION
ProdRole = "GIS_VIEWER"  #Options are GIS_ADMIN, GIS_DEVELOPER, GIS_EDITOR, GIS_VIEWER, GIS_AVIATION
SYSProd = "Database Connections/SDEPROD-SYS.sde"
SYSDev = "Database Connections/SDEDEV-SYS.sde"

arcpy.CreateDatabaseUser_management(SYSDev,"DATABASE_USER",SDEUsername,SDEUsername,DevRole,"GISDATA")
arcpy.CreateDatabaseUser_management(SYSProd,"DATABASE_USER",SDEUsername,SDEUsername,ProdRole,"GISDATA")

