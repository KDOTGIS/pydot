'''
Created on Sep 26, 2013
udpated on Oct 10, 2013
@author: kyleg
'''
from config import sdeCDRS, stageDB, sdeCDRSWZ, sdeWichwayCDRS

import datetime
print str(datetime.datetime.now()) + " starting arcpy function imports"
from arcpy import DefineProjection_management, CreateFileGDB_management, Append_management, TruncateTable_management, AddJoin_management, Project_management, CalculateField_management, MakeTableView_management, Exists, Delete_management, MakeFeatureLayer_management, env, FeatureClassToFeatureClass_conversion, AddField_management

print str(datetime.datetime.now()) + " setting variables"
env.overwriteOutput= True
labmertCC = "PROJCS['NAD_83_Kansas_Lambert_Conformal_Conic_Meters',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['false_easting',0.0],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',-98.0],PARAMETER['standard_parallel_1',38.0],PARAMETER['standard_parallel_2',39.0],PARAMETER['scale_factor',1.0],PARAMETER['latitude_of_origin',38.5],UNIT['Meter',1.0]]"

stagews = stageDB + "\\CDRS.gdb"

print str(datetime.datetime.now()) + " refreshing the staging geodatabase"
if Exists(stagews):
    Delete_management(stagews)
CreateFileGDB_management(stageDB, "CDRS.gdb")
env.workspace = stagews

print str(datetime.datetime.now()) + " manipulating the Oracle CDRS layers"
MakeFeatureLayer_management(sdeCDRS, "Construction", '#') 
FeatureClassToFeatureClass_conversion("Construction",stagews,"CDRS_RAW", "#","""CDRS_ALERT_ROUTE_ID "CDRS_ALERT_ROUTE_ID" true false false 8 Double 10 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,CDRS_ALERT_ROUTE_ID,-1,-1;AlertID "AlertID" true true false 8 Double 10 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,ALERT_ID,-1,-1;AlertDate "AlertDate" true true false 36 Date 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,ALERT_DATE,-1,-1;AlertStatus "AlertStatus" true true false 8 Double 10 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,ALERT_STATUS,-1,-1;FeaClosed "FeaClosed" true true false 8 Double 10 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,FEA_CLOSED,-1,-1;District "District" true true false 8 Double 10 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,DISTRICT,-1,-1;Area "Area" true true false 8 Double 10 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,AREA,-1,-1;LRSKey "LRSKey" true true false 19 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,BEG_LRS_KEY,-1,-1;LRSRoute "LRSRoute" true true false 12 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,BEG_LRS_ROUTE,-1,-1;County "County" true true false 20 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,BEG_COUNTY_NAME,-1,-1;CountyNumber "CountyNumber" true true false 8 Double 10 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,BEG_COUNTY_NUMBER,-1,-1;AlertType "AlertType" true true false 50 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,ALERT_TYPE_TXT,-1,-1;AlertDescription "AlertDescription" true true false 50 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,ALERT_DESC_TXT,-1,-1;BeginMP "BeginMP" true true false 8 Double 0 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,BEG_STATE_LOGMILE,-1,-1;BegRP "BegRP" true true false 8 Double 0 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,BEG_REF_POST,-1,-1;EndMP "EndMP" true true false 8 Double 0 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,END_STATE_LOGMILE,-1,-1;EndRP "EndRP" true true false 8 Double 10 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,END_REF_POST,-1,-1;Direction "Direction" true true false 12 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,ALERT_DIREC_TXT,-1,-1;StartDate "StartDate" true true false 36 Date 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,START_DATE,-1,-1;CompDate "CompDate" true true false 36 Date 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,COMP_DATE,-1,-1;ExpireDate "ExpireDate" true true false 36 Date 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,EXPIRE_DATE,-1,-1;TimeDelay "TimeDelay" true true false 30 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,TIME_DELAY_TXT,-1,-1;WZDetailId "WZDetailId" true true false 8 Double 10 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,CDRS_WZ_DETAIL_ID,-1,-1;WidthLimit "WidthLimit" true true false 8 Double 0 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,WIDTH_RESTRICTION,-1,-1;HeightLimit "HeightLimit" true true false 8 Double 0 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,VERT_RESTRICTION,-1,-1;WeightLimit "WeightLimit" true true false 8 Double 0 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,WEIGHT_RESTRICTION,-1,-1;SpeedLimit "SpeedLimit" true true false 8 Double 0 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,SPEED_RESTRICTION,-1,-1;INTERNAL_COMMENT "INTERNAL_COMMENT" true true false 4000 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,INTERNAL_COMMENT,-1,-1;Comments "Comments" true true false 4000 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,PUBLIC_COMMENT,-1,-1;PUBLIC_VIEW "PUBLIC_VIEW" true true false 8 Double 10 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,PUBLIC_VIEW,-1,-1;RPT_BY_NAME "RPT_BY_NAME" true true false 50 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,RPT_BY_NAME,-1,-1;RPT_BY_PHONE "RPT_BY_PHONE" true true false 15 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,RPT_BY_PHONE,-1,-1;RPT_BY_EMAIL "RPT_BY_EMAIL" true true false 40 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,RPT_BY_EMAIL,-1,-1;ContactName "ContactName" true true false 50 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,CONTACT_NAME,-1,-1;ContactPhone "ContactPhone" true true false 15 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,CONTACT_PHONE,-1,-1;ContactEmail "ContactEmail" true true false 30 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,CONTACT_EMAIL,-1,-1;OfficeName "OfficeName" true true false 30 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,OFFICE_NAME,-1,-1;NEW_NOTIFICATION "NEW_NOTIFICATION" true true false 8 Double 10 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,NEW_NOTIFICATION,-1,-1;ALERT_INSERT_DT "ALERT_INSERT_DT" true true false 36 Date 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,ALERT_INSERT_DT,-1,-1;WebLink "WebLink" true true false 500 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,ALERT_HYPERLINK,-1,-1;SITE_CR "SITE_CR" true true false 18 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,SITE_CR,-1,-1;LINE_COLOR "LINE_COLOR" true true false 8 Double 0 32 ,First,#,KANROAD.CDRS_ALERT_ROUTE,LINE_COLOR,-1,-1;GIS_VIEW "GIS_VIEW" true true false 2 Short 0 2 ,First,#,KANROAD.CDRS_ALERT_ROUTE,GIS_VIEW,-1,-1;DCAM_COMMENT "DCAM_COMMENT" true true false 1024 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,DCAM_COMMENT,-1,-1;DCAM_DATE "DCAM_DATE" true true false 12 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,DCAM_DATE,-1,-1;DISPLAY_MAP "DISPLAY_MAP" true true false 2 Short 0 1 ,First,#,KANROAD.CDRS_ALERT_ROUTE,DISPLAY_MAP,-1,-1;OBJECTID "OBJECTID" true false false 4 Long 0 38 ,First,#,KANROAD.CDRS_ALERT_ROUTE,OBJECTID,-1,-1;ROUTE "ROUTE" true true false 10 Text 0 0 ,First,#,KANROAD.CDRS_ALERT_ROUTE,ROUTE,-1,-1""","DEFAULTS")
MakeTableView_management(sdeCDRSWZ,"detail","#","#")
MakeFeatureLayer_management(stagews+"//CDRS_RAW", "ConstructionJoin")

print str(datetime.datetime.now()) + " Joining the Oracle CDRS WZ table"

AddJoin_management("ConstructionJoin","CDRS_WZ_DETAIL_ID","detail","CDRS_WZ_DETAIL_ID","KEEP_ALL")
FeatureClassToFeatureClass_conversion("ConstructionJoin",stagews,"CDRS_DETAIL", "CDRS_RAW.ALERT_STATUS <>  3") #EDIT to remove Alert Status = 3 to remove suspended projects from CDRS 2013/11/13 - has to be here to be queryable
                                      
print str(datetime.datetime.now()) + " reformatting the Route name for US routes"
AddField_management("CDRS_DETAIL", "RouteName", "TEXT", "#", "10")
routenamed = '!BEG_LRS_ROUTE![0:1] +str(!BEG_LRS_ROUTE![3:6]).lstrip("0")'  # calculation expression
CalculateField_management("CDRS_DETAIL","RouteName",routenamed,"PYTHON_9.3","#") 
AddField_management("CDRS_DETAIL", "STATUS", "TEXT", "#", "10")
AddField_management("CDRS_DETAIL", "Alert_Status_I", "LONG", "#", "#")
CalculateField_management("CDRS_DETAIL","Alert_Status_I", '!ALERT_STATUS!' ,"PYTHON_9.3","#") 

print str(datetime.datetime.now()) + " reprojection processing"
DefineProjection_management("CDRS_DETAIL", labmertCC)
Project_management("CDRS_DETAIL","CDRS_Project","PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]","WGS_1984_(ITRF00)_To_NAD_1983","PROJCS['NAD_83_Kansas_Lambert_Conformal_Conic_Meters',GEOGCS['GCS_North_American_1983',DATUM['D_North_American_1983',SPHEROID['GRS_1980',6378137.0,298.257222101]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Lambert_Conformal_Conic'],PARAMETER['false_easting',0.0],PARAMETER['false_northing',0.0],PARAMETER['central_meridian',-98.0],PARAMETER['standard_parallel_1',38.0],PARAMETER['standard_parallel_2',39.0],PARAMETER['scale_factor',1.0],PARAMETER['latitude_of_origin',38.5],UNIT['Meter',1.0]]")

MakeFeatureLayer_management(stagews+"\CDRS_Project", "ACTIVERoutes", '"ALERT_STATUS" =  2' )
CalculateField_management("ACTIVERoutes","STATUS",'"Active"',"PYTHON_9.3","#") 

#something right here is corrupting the file geodatabase... changed stagews+"//CDRS_Project" to stagews+"\CDRS_Project"

MakeFeatureLayer_management(stagews+"\CDRS_Project", "ClosedRoutes", '"ALERT_STATUS" =  2 AND "FEA_CLOSED" =  1')
CalculateField_management("ClosedRoutes","STATUS",'"Closed"',"PYTHON_9.3","#") 

MakeFeatureLayer_management(stagews+"\CDRS_Project", "PlannedRoutes", '"ALERT_STATUS" =  1' )
CalculateField_management("PlannedRoutes","STATUS",'"Planned"',"PYTHON_9.3","#") 

print str(datetime.datetime.now()) + " truncating CDRS segments in WICHWAY SPATIAL"

TruncateTable_management(sdeWichwayCDRS)

print str(datetime.datetime.now()) + " appending CDRS segments"
Append_management("CDRS_Project",sdeWichwayCDRS,"NO_TEST","""RouteName "RouteName" true true false 50 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,RouteName,-1,-1;BeginMP "BeginMP" true true false 8 Double 8 38 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,BEG_STATE_LOGMILE,-1,-1;EndMP "EndMP" true true false 8 Double 8 38 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,END_STATE_LOGMILE,-1,-1;County "County" true true false 50 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,BEG_COUNTY_NAME,-1,-1;StartDate "StartDate" true true false 36 Date 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,ALERT_DATE,-1,-1,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,COMP_DATE,-1,-1;CompDate "CompDate" true true false 36 Date 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,COMP_DATE,-1,-1;AlertType "AlertType" true true false 50 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,ALERT_TYPE_TXT,-1,-1;AlertDescription "AlertDescription" true true false 50 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,ALERT_DESC_TXT,-1,-1;HeightLimit "HeightLimit" true true false 50 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,VERT_RESTRICTION,-1,-1;WidthLimit "WidthLimit" true true false 50 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,WIDTH_RESTRICTION,-1,-1;TrafficRouting "TrafficRouting" true true false 50 Text 0 0 ,First,#;TimeDelay "TimeDelay" true true false 50 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,TIME_DELAY_TXT,-1,-1;Comments "Comments" true true false 4000 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,PUBLIC_COMMENT,-1,-1;DetourType "DetourType" true true false 50 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,KANROAD_CDRS_WZ_DETAIL_DETOUR_TYPE_TXT,-1,-1;DetourDescription "DetourDescription" true true false 1500 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,KANROAD_CDRS_WZ_DETAIL_DETOUR_DESC,-1,-1;ContactName "ContactName" true true false 50 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,CONTACT_NAME,-1,-1;ContactPhone "ContactPhone" true true false 50 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,CONTACT_PHONE,-1,-1;ContactEmail "ContactEmail" true true false 50 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,CONTACT_EMAIL,-1,-1;WebLink "WebLink" true true false 500 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,ALERT_HYPERLINK,-1,-1;X "X" true true false 8 Double 8 38 ,First,#;Y "Y" true true false 8 Double 8 38 ,First,#;AlertStatus "AlertStatus" true true false 4 Long 0 10 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,Alert_Status_I,-1,-1;FeaClosed "FeaClosed" true true false 4 Long 0 10 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,FEA_CLOSED,-1,-1;Status "Status" true true false 50 Text 0 0 ,First,#,D:/wichway/harvesters/python/CDRS.gdb/CDRS_Project,STATUS,-1,-1;LoadDate "LoadDate" true true false 36 Date 0 0 ,First,#;SHAPE_STLength__ "SHAPE_STLength__" true false false 8 Double 8 38 ,First,#;Shape.STLength() "Shape.STLength()" false false true 0 Double 0 0 ,First,#""","#")

try:
    MakeFeatureLayer_management(sdeWichwayCDRS, "loaded", "#")
    CalculateField_management("loaded","LoadDate","datetime.datetime.now( )","PYTHON_9.3","#") 
    print str(datetime.datetime.now()) + " It Ran, time for lunch"
except:
    print str(datetime.datetime.now()) + " It Ran, but didn't calc the LoadDate field"
