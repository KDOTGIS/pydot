'''
Created on Jan 29, 2013

@author: kyleg
'''

if __name__ == '__main__':
    pass
import arcpy, datetime, os
ws = r'\\gisdata\arcgis\GISdata\KDOT\BTP\Projects\CCL'  #change this path from CANSYSTEST
CCLUpdate = "Lyons"
now = datetime.datetime.now()
tempdb = CCLUpdate+str(now.year)+"_"+str(now.month)+"_"+str(now.day)+".gdb"
arcpy.env.workspace = ws
wsouttbl = ws+"\\"+tempdb
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
arcpy.MakeTableView_management(r"Database Connections\SDEDEV.sde\SDE.CCL_Lane", "Lane_tview")
arcpy.MakeTableView_management(r"Database Connections\SDEDEV.sde\SDE.Maint_Segment", "Maint_tview")
routelyr = "kdot_sde:oracle10g:SDE.KDOT_ROADWAYS\SDE.CMLRS"
clim = arcpy.mapping.Layer(r"\\gisdata\arcgis\GISdata\Layers\City Limits.lyr")
countylrs = arcpy.mapping.Layer(r"\\gisdata\arcgis\GISdata\Layers\County Linear Reference System.lyr")

arcpy.mapping.AddLayer(df,clim)
arcpy.mapping.AddLayer(df,countylrs)
clrs = "County Linear Reference System"
smlrs = "Database Connections\SDEDEV.sde\SDE.KDOT_ROADWAY\SDE.SMLRS"
arcpy.DisconnectUser("Database Connections\\kdot_sde.sde", "ALL")

arcpy.LocateFeaturesAlongRoutes_lr("City Limits","County Linear Reference System","LRS_KEY","0 Feet","Database Connections/KDOT_SDE.sde/SDE.GIS_CCL_Extents","LRS_KEY LINE Beg_CMP End_CMP","FIRST","DISTANCE","NO_ZERO","FIELDS","M_DIRECTON")

arcpy.MakeRouteEventLayer_lr(clrs,"LRS_KEY","Lane_tview","LRSKEY LINE BEGMILEPOST ENDMILEPOST","Lane_Events_ln","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
arcpy.MakeRouteEventLayer_lr(clrs,"LRS_KEY","Maint_tview","LRSKEY LINE BEGMILEPOST END_MP","Maint_Events_ln","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")

arcpy.MakeRouteEventLayer_lr(clrs,"LRS_KEY","SDE.GIS_CCL_Extents","LRS_KEY LINE BEG_CMP END_CMP","GIS_CCL","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")

arcpy.OverlayRouteEvents_lr("SDE.CCL_Resolution","LRS_KEY LINE BEG_CNTY_LOGMILE END_CNTY_LOGMILE","Database Connections\SDEDEV.sde\SDE.LNCL_EVENT","LRS_KEY LINE Beg_Cnty_Logmile End_Cnty_Logmile","INTERSECT",wsouttbl+"//CCL_LANES","LRS_KEY LINE BEG_CNTY_LOGMILE END_CNTY_LOGMILE","NO_ZERO","FIELDS","INDEX")
arcpy.OverlayRouteEvents_lr("Database Connections/SDEDEV.sde/SDE.CCL_Resolution","LRS_KEY LINE BEG_CNTY_LOGMILE END_CNTY_LOGMILE","Database Connections/SDEDEV.sde/SDE.LNCL_EVENT","LRS_KEY LINE BEG_CNTY_LOGMILE END_CNTY_LOGMILE","INTERSECT","Database Connections/SDEDEV.sde/SDE.CCL_Lanes","LRS_KEY LINE BEG_CNTY_LOGMILE END_CNTY_LOGMILE","NO_ZERO","FIELDS","INDEX")
#create Route Layer specific to City Connecting Link locations
ws = r"\\gisdata\arcgis\GISdata\KDOT\BTP\Projects\CCL"
tempdb = "LyonCCL2013_1_10.gdb"
CCLRS = "LRS_KEY" + "CITY"

#split line parts to account for inconsistent route lengths from CANSYS

arcpy.MakeRouteEventLayer_lr(clrs,"LRS_KEY","Database Connections\SDEDEV.sde\SDE.CCL_Resolution","LRS_KEY LINE BEG_CNTY_LOGMILE END_CNTY_LOGMILE","CCL_Resolution_Events","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
arcpy.FeatureClassToGeodatabase_conversion("CCL_Resolution_Events", "Database Connections\SDEDEV.sde\SDE.KDOT_CCL_WORKSPACE")
arcpy.SplitLine_management("Database Connections\SDEDEV.sde\SDE.KDOT_CCL_WORKSPACE\SDE.CCL_Resolution_Events","Database Connections\SDEDEV.sde\SDE.KDOT_CCL_WORKSPACE\CCL_LN_SPEC")
#locate resolution mileage along state route to cross counties
arcpy.LocateFeaturesAlongRoutes_lr("Database Connections\SDEDEV.sde\SDE.KDOT_CCL_WORKSPACE\SDE.CCL_LN_SPEC","Database Connections\SDEDEV.sde\SDE.KDOT_ROADWAY\SDE.SMLRS","LRS_ROUTE","0 Meters","Database Connections\SDEDEV.sde\CCL_ROUTE_CALIBRATE_SM","LRS_ROUTE LINE BEG_STATE_LOGMILE END_STATE_LOGMILE","FIRST","DISTANCE","ZERO","FIELDS","M_DIRECTON")
#Make the route event line layer matching hte state routes
arcpy.MakeRouteEventLayer_lr(smlrs, "LRS_ROUTE","SDE.CCL_ROUTE_CALIBRATE_SM","LRS_ROUTE LINE BEG_STATE_LOGMILE END_STATE_LOGMILE","CCL_ROUTE_SM_Events","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
#dissolve the state route events to find the begin logmile in the city
arcpy.Dissolve_management("CCL_ROUTE_SM_Events","Database Connections\SDEDEV.sde\SDE.KDOT_CCL_WORKSPACE\CCL_BEG_OFFSET_DISSOLVE","LRS_ROUTE;CITY","BEG_STATE_LOGMILE MIN;END_STATE_LOGMILE MAX","MULTI_PART","DISSOLVE_LINES")

## processes to Create the layer that will be used to create a new LRS for city connecting links 
CCLBegin = 0
CCLEnd = "!MAX_END_STATE_LOGMILE!- !MIN_BEG_STATE_LOGMILE!"
CCLLRS = '!LRS_KEY![3:14]+"_"+!CITY!'
CCLLRS_ST = '!LRS_ROUTE![0:11]+"_"+!CITY!'
#resln = "Database Connections\SDEDEV.sde\SDE.CCL_Resolution"
#arcpy.AddField_management(resln,"CCL_BEGIN", "DOUBLE", 12, 3)
#arcpy.AddField_management(resln,"CCL_END", "DOUBLE", 12, 3)
#arcpy.AddField_management(resln,"CCL_LRS", "TEXT", "#", "#", "120")
#arcpy.CalculateField_management(resln, "CCL_BEGIN", "0", "PYTHON")
#arcpy.CalculateField_management(resln, "CCL_END", CCLEnd, "PYTHON")
#arcpy.CalculateField_management(resln, "CCL_LRS", CCLLRS, "PYTHON")

arcpy.AddField_management("SDE.CCL_BEG_OFFSET_DISSOLVE","CCL_BEGIN", "DOUBLE", 12, 3)
arcpy.AddField_management("SDE.CCL_BEG_OFFSET_DISSOLVE","CCL_END", "DOUBLE", 12, 3)
arcpy.AddField_management("SDE.CCL_BEG_OFFSET_DISSOLVE","CCL_LRS", "TEXT", "#", "#", "120")
arcpy.CalculateField_management("SDE.CCL_BEG_OFFSET_DISSOLVE", "CCL_BEGIN", "0", "PYTHON")
arcpy.CalculateField_management("SDE.CCL_BEG_OFFSET_DISSOLVE", "CCL_END", CCLEnd, "PYTHON")
arcpy.CalculateField_management("SDE.CCL_BEG_OFFSET_DISSOLVE", "CCL_LRS", CCLLRS_ST, "PYTHON")

arcpy.AddField_management("CCL_ROUTE_SM_Events","CCL_BEGIN", "DOUBLE", 12, 3)
arcpy.AddField_management("CCL_ROUTE_SM_Events","CCL_END", "DOUBLE", 12, 3)
arcpy.AddField_management("CCL_ROUTE_SM_Events","CCL_LRS", "TEXT", "#", "#", "120")
arcpy.CalculateField_management("CCL_ROUTE_SM_Events", "CCL_LRS", CCLLRS_ST, "PYTHON")

## create the CCL LRM beinning from 0 using the state route mileage, offsetting the minimum state route mileage from the city limit 
arcpy.AddJoin_management("CCL_ROUTE_SM_Events","CCL_LRS","SDE.CCL_BEG_OFFSET_DISSOLVE","CCL_LRS","KEEP_ALL")
CCLPartBegin = "!SDE.CCL_ROUTE_CALIBRATE_SM_Features.BEG_STATE_LOGMILE!-!SDE.CCL_BEG_OFFSET_DISSOLVE.MIN_BEG_STATE_LOGMILE!"
CCLPartEnd = "!SDE.CCL_ROUTE_CALIBRATE_SM_Features.END_STATE_LOGMILE!- !SDE.CCL_BEG_OFFSET_DISSOLVE.MIN_BEG_STATE_LOGMILE!"
arcpy.CalculateField_management("CCL_ROUTE_SM_Events", "SDE.CCL_ROUTE_CALIBRATE_SM_Features.CCL_BEGIN", CCLPartBegin, "PYTHON")
arcpy.CalculateField_management("CCL_ROUTE_SM_Events", "SDE.CCL_ROUTE_CALIBRATE_SM_Features.CCL_END", CCLPartEnd, "PYTHON")
arcpy.RemoveJoin_management("CCL_ROUTE_SM_Events")
#create the routes with the cansys mileage
arcpy.env.MResolution = 0.00001
arcpy.env.MTolerance = 0.00001  # set the M tolerance below the default reduces the errors in the arc file 
#create the routes, in the temp DB.  As CCL issues get ironed out, consider outputting this in SDE
arcpy.CreateRoutes_lr("CCL_ROUTE_SM_Events","CCL_LRS","Database Connections\SDEDEV.sde\SDE.KDOT_CCL_WORKSPACE\CCLLRM","TWO_FIELDS","CCL_BEGIN","CCL_END","UPPER_LEFT","1","0","IGNORE","INDEX")

# for now, should produce an error file, setting the tolerance to 0.0001 results in one warning for a zero length section
# review the error file - there should be C:\Users\kyleg\AppData\Local\Temp\arc5163\CCL_RESOLUTION_ROUTE0.txt
# import os
os.startfile(r"C:\Users\kyleg\AppData\Local\Temp\arc41E3\SDE.CCLLRM2.txt") #shortcut to open the warning file through py interface, change the file name as needed

#intersect non-state routes
nsul = arcpy.mapping.Layer(r"\\gisdata\arcgis\GISdata\Layers\Non State System Urban Low.lyr")
arcpy.mapping.AddLayer(df,nsul)
arcpy.Intersect_analysis("SDE.CCLLRM #;'Non State System Urban Low' #","Database Connections\SDEDEV.sde\SDE.KDOT_CCL_WORKSPACE\Intersect_NONSTATE","ALL","5 Feet","POINT")
arcpy.LocateFeaturesAlongRoutes_lr("SDE.Intersect_NONSTATE","SDE.CCLLRM","CCL_LRS","5 Feet","Database Connections\SDEDEV.sde\INTR_CCL_NS","CCL_LRS POINT CCL_MEAS","ALL","DISTANCE","ZERO","FIELDS","M_DIRECTON")
arcpy.MakeRouteEventLayer_lr("SDE.CCLLRM","CCL_LRS","SDE.INTR_CCL_NS","CCL_LRS POINT CCL_MEAS","INTR_CCL_NS Events","#","ERROR_FIELD","ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")

#add intersect intersection points that are state - state intersections
arcpy.MakeFeatureLayer_management(r'Database Connections\SDEDEV.sde\SDE.CANSYS\SDE.INTR', 'INTR', "ON_STATE_NONSTATE = 'S'")
arcpy.LocateFeaturesAlongRoutes_lr("INTR","SDE.CCLLRM","CCL_LRS","5 Feet","Database Connections\SDEDEV.sde\INTR_CCL","CCL_LRS POINT CCL_MEAS","ALL","DISTANCE","ZERO","FIELDS","M_DIRECTON")
arcpy.MakeRouteEventLayer_lr("SDE.CCLLRM","CCL_LRS","SDE.INTR_CCL","CCL_LRS POINT CCL_MEAS","INTR_CCL Events","#","ERROR_FIELD","ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")

#show lane classification referenced to city connecting link LRS
arcpy.DisconnectUser("Database Connections\\kdot_sde.sde", "ALL")
arcpy.TransformRouteEvents_lr("SDE.CCL_Lanes","LRS_KEY LINE BEG_CNTY_LOGMILE END_CNTY_LOGMILE",clrs,"LRS_KEY","SDE.CCLLRM","CCL_LRS","Database Connections\SDEDEV.sde\CCLRS_LANES","LRS_KEY LINE BEG_CCL_LOGMILE END_CCL_LOGMILE","0 Feet","FIELDS")
arcpy.MakeRouteEventLayer_lr("SDE.CCLLRM", "CCL_LRS","SDE.CCLRS_LANES","LRS_KEY LINE BEG_CCL_LOGMILE END_CCL_LOGMILE","CCL_LANE_Events","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
# make route event layer


