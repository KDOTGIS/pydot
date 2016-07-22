'''
Created on Jul 19, 2016

@author: kyleg
'''

#source information:
#this is the path to the Conflation road centerlines - all of them
ConflationDatabase  = r"Database Connections/Conflation2012_sde.sde"
Roads = ConflationDatabase + r"\Conflation.SDE.NG911\Conflation.SDE.RoadCenterlines"

#there are 25443 segments at this time

#here are the GIS routes with measures extracted regularly from EXOR using the FME extraction and python route reference tools from DT00ar60
Smlrs = r'Database Connections\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.SMLRS'
Cmlrs = r'Database Connections\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.CMLRS'

from arcpy import FeatureClassToFeatureClass_conversion, FeatureVerticesToPoints_management, LocateFeaturesAlongRoutes_lr, DeleteField_management, TableToTable_conversion
from arcpy import env
env.overwriteOutput=1
# Let's Start by loading NG911 aggregated, conflated road centerlines to an in-memory feature class

FeatureClassToFeatureClass_conversion(Roads, "in_memory", "RoadCenterlines", "StateKey1 IS NOT NULL ")

#these are the two linear referencing networks we're going to use to calibrate the state highway system
Lrm_Dict = {'STATE':Smlrs, 'COUNTY':Cmlrs}

#and this is the beginning and end of a line, for which we are going to create a vertex point
End_List = ['START', 'END']

# First, lets create points at the beginning of each centerline segment using Vertices to Points.  
for end in End_List:
    i_end_output = "in_memory/CalibrationPoint"+str(end)
    FeatureVerticesToPoints_management("in_memory/RoadCenterlines", i_end_output, str(end))

#Iterate through the LRMs to bring them into memory and do the processing for each segment begin and end point!  
for key, value in Lrm_Dict.items():
    FeatureClassToFeatureClass_conversion(value, "in_memory", "LRM"+str(key))
    for end in End_List:
        outtable = "in_memory/"+str(end)+"_"+str(key)
        outstore = ConflationDatabase+r"/"+str(end)+"_"+str(key)
        outproperties = str(key)+"_LRS POINT MEAS_"+str(key)
        if key == "STATE":
            lrskey = str(key)+"_NQR_DESCRIPTION"
        else:
            lrskey = "NQR_DESCRIPTION"
        LocateFeaturesAlongRoutes_lr("in_memory/CalibrationPoint"+str(end), "in_memory/LRM"+str(key), lrskey, "500 Feet", outtable, outproperties, "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
        
        #there is a bug here between hte LFAR, DeleteField_management, TableToTable_conversion code
        #delete field - the tables are corrupt in memory upon running deletefield management
        #DeleteField_management(outtable, "STEWARD;L_UPDATE;EFF_DATE;EXP_DATE;SEGID;STATE_L;STATE_R;COUNTY_L;COUNTY_R;MUNI_L;MUNI_R;L_F_ADD;L_T_ADD;R_F_ADD;R_T_ADD;PARITY_L;PARITY_R;POSTCO_L;POSTCO_R;ZIP_L;ZIP_R;ESN_L;ESN_R;MSAGCO_L;MSAGCO_R;PRD;STP;RD;STS;POD;POM;SPDLIMIT;ONEWAY;RDCLASS;UPDATEBY;LABEL;ELEV_F;ELEV_T;ESN_C;SURFACE;STATUS;TRAVEL;LRSKEY;UNINC_L;UNINC_R;EXCEPTION_;SUBMIT;NOTES;COUNTY_BEGIN_MP;COUNTY_END_MP;STATE_BEGIN_MP;STATE_END_MP;NON_STATE_BEGIN_MP;NON_STATE_END_MP;STATE_FLIP_FLAG;STATE_MILEAGE_FLAG;NON_STATE_FLIP_FLAG;NON_STATE_MILEAGE_FLAG;State_System_LRSKey;Non_State_System_LRSKey;Ramps_LRSKey;BEG_NODE;END_NODE;Con_Surface;KDOT_BEG_LOGMILE;KDOT_END_LOGMILE;KDOT_LRS_KEY;KDOT_DIRECTION_CALC;RID;FMEAS;TMEAS;LRS_COUNTY_PRE;LRS_URBAN_PRE;LRS_ROUTE_PREFIX;LRS_ROUTE_SUFFIX;LRS_UNIQUE_IDENT;LRS_ADMO;LRS_SUBCLASS;LRS_DIRECTION;MILEAGE_COUNTED;LRS_ROUTE_NUM;KDOT_QA;RouteID;FromDate;ToDate;LRS_ROUTE_NUM1;LRS_UNIQUE_IDENT1;LRS_PRIMARY_DIR;LRS_RdNm_Soundex;RouteID2;KDOT_RAMP_CRASH_ID;KDOT_COUNTY_L;KDOT_COUNTY_R;KDOT_MUNI_L;KDOT_MUNI_R;created_user;created_date;last_edited_user;last_edited_date;CountyKey1;StateKey1;F_CNTY_1;T_CNTY_1;F_STAT_1;T_STAT_1;Shape_STLength__;ORIG_FID")
        #tableto table conversion from in memory to SQL server throws unhandled error
        #TableToTable_conversion(outtable, ConflationDatabase, outstore)

print "Done!!!"
# At this point, all the values we need to calculate the calibrated begin/end mileage of a segment are stored in SQL server
# to wrap this up, I will use SQL Server Management Studio to join and set the calibrated begin/end values for the segments

#  F:\Cart\projects\Conflation\SQL\SQLServer\Conflation2012\KHUB  is where that SQL query lives, its the State System Calibration 2 SQL file

