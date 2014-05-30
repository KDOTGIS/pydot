'''
Created on Oct 7, 2013

@author: kyleg
'''

#HARD SET A WORKSPACE ENVIRONMENT
ws = r'\\gisdata\arcgis\GISdata\KDOT\BTP\Projects\CCL'

#SET THE GEODATABASE CONNECTON FOR CCL PROCESSING
connection0 = r'Database Connections\SQL61_GEOADMIN_CCLtest.sde'

#SCHEMA.Owner.
schema = "CCL_TEST.DBO."

#SET THE GEODATABASE SCHEMA/DBO FOR CCL PROCESSING
connection1 =  connection0+'/'+schema

#SET THE GIS POLYGON LAYER FOR CITY LIMIT COMPARISON
citylimits = r'Database Connections\SDEDEV_GIS_DEV.sde\GIS_DEV.Administrative_Boundary\GIS_DEV.CITY_LIMITS'

#SET THE GIS STATE SYSTEM COUNTY LRS ROUTE LAYER FOR LINEAR REFERENCE
cntyroutelyr = r'Database Connections\SQL61_GIS_CANSYS_RO.sde\GIS_CANSYS.DBO.CMLRS'

#SET THE GIS STATE SYSTEM STATE LRS ROUTE LAYER FOR LINEAR REFERENCE
stateroutelyr = r'Database Connections\SQL61_GIS_CANSYS_RO.sde\GIS_CANSYS.DBO.SMLRS'

#SET THE LOCATION OF THE "LANE CLASS" POLYLINE FEATURE CLASS EXTRACTED FROM CANSYS
laneclass = r"Database Connections\SQL61_GIS_CANSYS_RO.sde\GIS_CANSYS.DBO.LNCL"

#SET THE LOCATION OF THE "INTERCHANGE" POINT FEATURE CLASS EXTRACTED FROM CANSYS
interchange = r"Database Connections\SQL61_GIS_CANSYS_RO.sde\GIS_CANSYS.DBO.V_INTR_SDO_V"

#NON STATE SYSTEM GIS LAYER  ### Nonstate layer in GISPROD will not work in ArcGIS until geodatabase is updated
nonstate = r"Database Connections\SDEDEV_GIS_DEV.sde\GIS_DEV.KDOT_ROADWAY_WORKSPACE\GIS_DEV.NON_STATE_SYSTEM"

#MAINTNENACE EVENT TABLE
maintenance = r"Database Connections\SQL61_GEOADMIN_CCLtest.sde\CCL_TEST.DBO.Maint_Segment"

#RESOULTION EVENT TABLE
resolve = connection1+"CCL_Resolution"

LineFeatureClass = connection1+"CITY_CONNECTING_LINK_STATE"
ReferenceRoute = stateroutelyr
ReferenceRouteKey = "LRS_ROUTE"
NewRouteKey = "CCL_LRS"
NewBeg = "CCL_BEGIN"
NewEnd = "CCL_END"
NewRoute = "CCL_LRS_ROUTE"

