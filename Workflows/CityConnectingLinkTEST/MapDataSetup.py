'''
Created on Oct 7, 2013
udpated 5/1/2014
@author: kyleg
'''
#import data paths from config file.  If testing in ArcMap, run config first to set up environments
try:
    from config import ws, connection0, connection1, citylimits, stateroutelyr, cntyroutelyr, laneclass, maintenance, resolve, LineFeatureClass, NewRouteKey, NewBeg, NewEnd, NewRoute, schema
except:
    pass


from arcpy import env, Intersect_analysis, SelectLayerByAttribute_management, DissolveRouteEvents_lr, DeleteRows_management, CreateRoutes_lr, ChangePrivileges_management, CalibrateRoutes_lr, DeleteIdentical_management, Exists, AddJoin_management, Delete_management, FeatureClassToFeatureClass_conversion, MakeFeatureLayer_management, MakeTableView_management, Dissolve_management, AddField_management, CalculateField_management, LocateFeaturesAlongRoutes_lr, MakeRouteEventLayer_lr, OverlayRouteEvents_lr
import datetime
env.workspace = ws
env.overwriteOutput = True
env.MResolution = 0.0001
env.MTolerance = 0.0002 

def setupEnv():
    print "run at "+ str(datetime.datetime.now())
    rsel = "ENDDATE IS NULL"
    MakeTableView_management(resolve, "CCL_Resolution_tbl", rsel)
    CalculateField_management("CCL_Resolution_tbl", "CCL_LRS",  'str(!CITYNUMBER!)+str(!LRS_KEY![3:14])', "PYTHON" )
    MakeTableView_management(connection1+"CCL_Resolution", "CCL_Resolution_tbl10", 'CITYNUMBER<100')
    CalculateField_management("CCL_Resolution_tbl10", "CCL_LRS", '"0"+str(!CITYNUMBER!)+str(!LRS_KEY![3:14])', "PYTHON")
    MakeFeatureLayer_management(cntyroutelyr, "cmlrs")
    MakeFeatureLayer_management(stateroutelyr, "smlrs")
    MakeFeatureLayer_management(citylimits, "CityLimits", "TYPE IN ( 'CS', 'ON')")
    LocateFeaturesAlongRoutes_lr(citylimits,"cmlrs","LRS_KEY","0 Feet",connection1+"GIS_CITY","LRS_KEY LINE Beg_CMP End_CMP","FIRST","DISTANCE","NO_ZERO","FIELDS","M_DIRECTON")
    MakeRouteEventLayer_lr("cmlrs","LRS_KEY","CCL_Resolution_tbl","LRS_KEY LINE BEG_CNTY_LOGMILE END_CNTY_LOGMILE","City_Connecting_Links","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
    MakeTableView_management(connection1+"GIS_CITY", "GIS_CITY")
    MakeTableView_management(laneclass, "LaneClass")
    MakeRouteEventLayer_lr("cmlrs","LRS_KEY","GIS_CITY","LRS_KEY LINE BEG_CMP END_CMP","GIS_BASED_CCL","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
    OverlayRouteEvents_lr(connection1+"CCL_Resolution","LRS_KEY LINE BEG_CNTY_LOGMILE END_CNTY_LOGMILE",laneclass,"LRS_KEY LINE BCMP ECMP","INTERSECT",connection1+"CCL_LANE_CLASS_OVERLAY","LRS_KEY LINE BEG_CNTY_LOGMILE END_CNTY_LOGMILE","NO_ZERO","FIELDS","INDEX")
    print "create Route Layer specific to City Connecting Link locations"    
    FeatureClassToFeatureClass_conversion("City_Connecting_Links", connection0, "CITY_CONNECTING_LINK_CENTERLINE")
    LocateFeaturesAlongRoutes_lr(connection1+"CITY_CONNECTING_LINK_CENTERLINE",stateroutelyr,"LRS_ROUTE","0 Meters",connection1+"CCL_STATE_LRS_tbl","LRS_ROUTE LINE BEG_STATE_LOGMILE END_STATE_LOGMILE","FIRST","DISTANCE","ZERO","FIELDS","M_DIRECTON")
    MakeRouteEventLayer_lr("smlrs", "LRS_ROUTE",connection1+"CCL_STATE_LRS_tbl","LRS_ROUTE LINE BEG_STATE_LOGMILE END_STATE_LOGMILE","CCL_STATE_LRS","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
    FeatureClassToFeatureClass_conversion("CCL_STATE_LRS", connection0, "CITY_CONNECTING_LINK_STATEREF")
    if Exists(connection1+"CITY_CONNECTING_LINK_STATE"):
        Delete_management(connection1+"CITY_CONNECTING_LINK_STATE")
    Dissolve_management(connection1+"CITY_CONNECTING_LINK_STATEREF",connection1+"CITY_CONNECTING_LINK_STATE","LRS_ROUTE;CITY;CITYNUMBER;DESCRIPTION;CCL_LRS","BEG_STATE_LOGMILE MIN;END_STATE_LOGMILE MAX","MULTI_PART","UNSPLIT_LINES")
    Dissolve_management(connection1+"CITY_CONNECTING_LINK_STATEREF",connection1+"CITY_CONNECTING_LINK_STATE_D","CCL_LRS","BEG_STATE_LOGMILE MIN;END_STATE_LOGMILE MAX","MULTI_PART","DISSOLVE_LINES")
    
    print "processes to Create the layer that will be used to create a new LRS for city connecting links"

def calibrationCCL():
    
    print "deriving CCL LRS starting points and calibrations"
    CCLEnd = "!"+schema+"CITY_CONNECTING_LINK_STATE.MAX_END_STATE_LOGMILE!- !"+schema+"CITY_CONNECTING_LINK_STATE_D.MIN_BEG_STATE_LOGMILE!"
    CCLBeg = "!"+schema+"CITY_CONNECTING_LINK_STATE.MIN_BEG_STATE_LOGMILE! - !"+schema+"CITY_CONNECTING_LINK_STATE_D.MIN_BEG_STATE_LOGMILE!"
    MakeFeatureLayer_management(LineFeatureClass, "CITY_CONNECTING_LINK_RESET")
    resln = "CITY_CONNECTING_LINK_RESET"
    AddField_management(resln,"CCL_BEGIN", "DOUBLE", 12, 3)
    AddField_management(resln,"CCL_END", "DOUBLE", 12, 3)
    AddJoin_management("CITY_CONNECTING_LINK_RESET","CCL_LRS",connection1+"CITY_CONNECTING_LINK_STATE_D","CCL_LRS","KEEP_ALL")
    CalculateField_management(resln, "CCL_BEGIN", CCLBeg, "PYTHON")
    CalculateField_management(resln, "CCL_END", CCLEnd, "PYTHON")
    print "calibrating LRS - point calibration method"
    statecalpoints = stateroutelyr+"_Point"
    print statecalpoints
    MakeFeatureLayer_management(statecalpoints, "smlrs_pt")
    print connection1+"CITY_CONNECTING_LINK_STATE_D"
    MakeFeatureLayer_management(connection1+"CITY_CONNECTING_LINK_STATE_D", "dissolved_res_sects")
    intersects = ["dissolved_res_sects", "smlrs_pt"]
    Intersect_analysis(intersects,connection0+"CALIBRATION_POINTS_CCL","ALL","#","POINT")
    print connection1+"CALIBRATION_POINTS_CCL"
    MakeFeatureLayer_management(connection1+"CALIBRATION_POINTS_CCL", "Calibrators")
    querystr = "Substring( CCL_LRS,4, 12)<> LRS_ROUTE"  
    SelectLayerByAttribute_management("Calibrators","NEW_SELECTION",querystr)
    DeleteRows_management("Calibrators")
    MakeFeatureLayer_management(connection1+"CITY_CONNECTING_LINK_STATE", "CCL_sections")
    DeleteIdentical_management("Calibrators","LRS_KEY;POINT_X;POINT_Y;POINT_M","#","0")
    AddField_management("CCL_sections","CCL_BEGIN","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    AddField_management("CCL_sections","CCL_BEGIN","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    AddJoin_management("CCL_sections","CCL_LRS","dissolved_res_sects","CCL_LRS","KEEP_ALL")
    CalculateField_management("CCL_sections",schema+"CITY_CONNECTING_LINK_STATE.CCL_BEGIN","!"+schema+"CITY_CONNECTING_LINK_STATE.MIN_BEG_STATE_LOGMILE!- !"+schema+"CITY_CONNECTING_LINK_STATE_D.MIN_BEG_STATE_LOGMILE!","PYTHON","#")
    CalculateField_management("CCL_sections",schema+"CITY_CONNECTING_LINK_STATE.CCL_END","!"+schema+"CITY_CONNECTING_LINK_STATE.MAX_END_STATE_LOGMILE!- !"+schema+"CITY_CONNECTING_LINK_STATE_D.MIN_BEG_STATE_LOGMILE!","PYTHON","#")
    AddField_management(connection1+"CALIBRATION_POINTS_CCL","CCL_MEASURE", "DOUBLE", 12, 3)
    CalculateField_management("Calibrators","CCL_MEASURE","!POINT_M!- !MIN_BEG_STATE_LOGMILE!","PYTHON","#")
    CreateRoutes_lr(LineFeatureClass,NewRouteKey,connection1+NewRoute+"base","TWO_FIELDS",NewBeg, NewEnd,"UPPER_LEFT","1","0","IGNORE","INDEX")
    CalibrateRoutes_lr(connection0+"/"+schema+"CCL_LRS_ROUTEbase","CCL_LRS",connection1+"CALIBRATION_POINTS_CCL","CCL_LRS","CCL_MEASURE",connection1+"CCL_LRS_ROUTE","DISTANCE","1 Feet","BETWEEN","NO_BEFORE","NO_AFTER","IGNORE","KEEP","INDEX")
    AddField_management(connection1+NewRoute, "NETWORKDATE", "DATE")
    CalculateField_management(connection1+NewRoute,"NETWORKDATE","datetime.datetime.now( )","PYTHON_9.3","#")
    MakeFeatureLayer_management(connection1+"CCL_LRS_ROUTE", NewRoute)
    
def Maintenance():
    print "reference maintenance agreement table"
    MakeTableView_management(maintenance, "Maint_tview")
    MakeRouteEventLayer_lr(cntyroutelyr,"LRS_KEY", "Maint_tview","LRSKEY LINE BEGMILEPOST END_MP","Maintenance_Events_CNTY","#","ERROR_FIELD","ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
    if Exists(connection1+"MAINTENANCE_CCL"):
        Delete_management(connection1+"MAINTENANCE_CCL")
    LocateFeaturesAlongRoutes_lr("Maintenance_Events_CNTY",connection1+"CCL_LRS_ROUTE",NewRouteKey,"1 Feet",connection1+"MAINTENANCE_CCL","CCL_LRS LINE CCL_BEGIN CCL_END","ALL","DISTANCE","ZERO","FIELDS","M_DIRECTON")
    print "show lane classification referenced to city connecting link LRS"
    
def LaneClass():    
    MakeFeatureLayer_management(laneclass, 'LNCL', "LANE_DIRECTION in ( 'EB' , 'NB' )")
    LocateFeaturesAlongRoutes_lr("LNCL",connection1+"CCL_LRS_ROUTE",NewRouteKey,"0.1 FEET",connection1+"LANECLASS_CCL","CCL_LRS LINE CCL_BEGIN CCL_END","ALL","DISTANCE","ZERO","FIELDS","M_DIRECTON")
    AddField_management(connection1+"LANECLASS_CCL", "Lanes", "LONG")
    MakeTableView_management(laneclass, "LANECLASS_CCL_tbl", "LANE_DIRECTION in ( 'EB' , 'NB' )")
    CalculateField_management(connection1+"LANECLASS_CCL","Lanes", 'Left([LNCL_CLS_ID_DESC],1)', "VB" )

def Report():
    OverlayRouteEvents_lr(connection1+"MAINTENANCE_CCL","CCL_LRS LINE CCL_BEGIN CCL_END",connection1+"LANECLASS_CCL","CCL_LRS LINE CCL_BEGIN CCL_END","UNION",connection1+"CCL_Report_M","CCL_LRS LINE CCL_MA_BEGIN CCL_MA_END","NO_ZERO","FIELDS","INDEX")
    DissolveRouteEvents_lr(connection1+"CCL_Report_M","CCL_LRS LINE CCL_MA_BEGIN CCL_MA_END","CITYNO;MAINT_DESC;CITY_NAME;Lanes",connection1+"CCL_Report_D","CCL_LRS LINE CCL_MA_BEGIN CCL_MA_END","CONCATENATE","INDEX")
    #cleanup border errors - make feature layers based on City, city number, and CCLLRS and delete where they are not consistent between Maintenance and Resolution sections
    if Exists(connection1+"CCL_Report"):
        MakeTableView_management(connection1+"CCL_Report", "Report_Clean1", "CCL_LRS2 <> CCL_LRS")
        DeleteRows_management("Report_Clean1")
    LocateFeaturesAlongRoutes_lr(LineFeatureClass, connection1+"CCL_LRS_ROUTE",NewRouteKey,"#",connection1+"RES_SECTION_CCL","CCL_LRS LINE CCL_BEGIN CCL_END","ALL","DISTANCE","ZERO","FIELDS","M_DIRECTON")
    OverlayRouteEvents_lr(connection1+"RES_SECTION_CCL","CCL_LRS LINE CCL_BEGIN CCL_END",connection1+"CCL_Report_D","CCL_LRS LINE CCL_MA_BEGIN CCL_MA_END","INTERSECT",connection1+"CCL_Report","CCL_LRS LINE CCL_BEGIN CCL_END","NO_ZERO","FIELDS","INDEX")   
    MakeRouteEventLayer_lr(connection1+"CCL_LRS_ROUTE", "CCL_LRS",connection1+"CCL_Report","CCL_LRS LINE CCL_BEGIN CCL_END","City Connecting Links Mapping","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
    print "add mapping fields for lane miles"
    AddField_management("City Connecting Links Mapping", "CenterlineMiles", "DOUBLE")
    CalculateField_management("City Connecting Links Mapping","CenterlineMiles", '[CCL_END]-[CCL_BEGIN]', "VB" )
    AddField_management("City Connecting Links Mapping", "LaneMiles", "DOUBLE")
    CalculateField_management("City Connecting Links Mapping","LaneMiles", '([CCL_END]-[CCL_BEGIN])*[Lanes]', "VB" )
    AddField_management(connection1+"CITY_CONNECTING_LINK_CENTERLINE", "CenterlineMiles", "DOUBLE")
    MakeFeatureLayer_management(connection1+"CITY_CONNECTING_LINK_CENTERLINE", 'Res_centerline')
    CalculateField_management("Res_centerline","CenterlineMiles", '[END_CNTY_LOGMILE]-[BEG_CNTY_LOGMILE]', "VB" )
    Dissolve_management("Res_centerline",connection1+"CCL_LEGEND","CITY;LRS_KEY;CITYNUMBER;CCL_LRS","CenterlineMiles SUM","MULTI_PART","DISSOLVE_LINES")
    AddField_management(connection1+"CCL_LEGEND", "CCL_LEGEND", "TEXT", "#", "#", "50")
    legendexp = 'str(!CCL_LRS![3]) +"-" + str(!CCL_LRS![6:9]).lstrip("0")+"........"+ str(!SUM_CenterlineMiles!)'
    MakeFeatureLayer_management(connection1+"CCL_LEGEND", 'LegendCalc')
    CalculateField_management("LegendCalc","CCL_LEGEND",legendexp,"PYTHON_9.3","#")
    
def ROPrivs():
    ChangePrivileges_management(connection1+"CCL_Report", "Readonly", "GRANT")
    ChangePrivileges_management(connection1+"MAINTENANCE_CCL", "Readonly", "GRANT")
    ChangePrivileges_management(connection1+"CCL_Resolution", "Readonly", "GRANT")
    ChangePrivileges_management(connection1+"CCL_LANE_CLASS_OVERLAY", "Readonly", "GRANT")
    ChangePrivileges_management(connection1+"CCL_LEGEND", "Readonly", "GRANT")
    

if __name__ == '__main__':
#    CityConnectingLink()
    setupEnv()
    calibrationCCL()
    Maintenance()
    LaneClass()
    Report()
    print "ended at "+ str(datetime.datetime.now())
    