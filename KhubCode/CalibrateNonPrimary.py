'''
Created from Eliminate Overlaps, modivided to work and populate non primary route key



Created on Feb 7, 2017
This script prepares the conflation data for route creation
conflation road data representing the state highway system is copied toin-memory for fast processing 
field are formatted for route creating based on the LRS flagging for flips and non-primary directions
make all changes in the source conflation data

LRS Keys are structured in the source format and can also be outputted in the destination LRS key format 
The dissolve settings should eliminate overlapping geometries

The results table can be sorted and reviewed to find additional non-primary directions, bad conflation route keys, ghost routes, and other issues

Feb 13, 2017 added Classified_System function





@author: kyleg
'''

if __name__ == '__main__':
    pass

                    #the roads geodatabase for road centerline editing
                    
roadcenterlines = r"\\gisdata\arcgis\GISdata\KDOT\BTP\Projects\KHUB Cleanup\i2_NonPrimaryExor.gdb\Highway_NonCardinalDirection2"
                    
#roadcenterlines = r"\\gisdata\ArcGIS\GISdata\KDOT\BTP\Projects\KHUB Cleanup\NetworkQCErrors\Data_Mirroring_17D_AllRegions_Source_Exor_Calibration.gdb\RoutesSource_State_Exor"


#roadcenterlines = r"\\gisdata\arcgis\GISdata\Connection_files\Roads\prod\Roads_geo.sde\Roads.GEO.NG\Roads.GEO.RoadCenterlines"

                    #centerlines submitted by GeoComm, statewide final
#roadcenterlines = r"\\gisdata\planning\Cart\projects\Conflation\GIS_DATA\GEO_COMM\STATEWIDE_20170212\STATEWIDE_20170212.gdb\NG911\RoadCenterlines"

                    #centerline edits made by KDOT staff
#roadcenterlines = r"\\gisdata\arcgis\GISdata\KDOT\BTP\Projects\KHUB Cleanup\Manual_Edit_Support\Manual_Edit_Aggregation\2017-03-08\MidifiedRoadCenterlinesManual_roads.gdb\NG\RoadCenterlines"

SSoutput = r"Database Connections\Conflation_KHUBI2_sde.sde\KHUB_I2.SDE.KANSAS_DOT\KHUB_I2.SDE.County2Dissolve"
ClassOutput = r"Database Connections\Conflation_KHUBI2_sde.sde\KHUB_I2.sde.KANSAS_DOT\KHUB_I2.SDE.RMC2Dissolve"
RouteOutput = r"Database Connections/Conflation_KHUBI2_sde.sde/KHUB_I2.SDE.KHubI2/KHUB_I2.SDE."

spam = r"C:\temp"
spamdata = "KHub_Process1.gdb" 
import os
spampath = os.path.join(spam, spamdata)
spampathfd = os.path.join(spampath, "NG")
xmlpath = r"\\gisdata\arcgis\GISdata\KDOT\BTP\Projects\KHUB Cleanup\RoadsGeo.xml"
#\\gisdata\arcgis\GISdata\Connection_files\Roads\dev\Roads_Dev_aduser.sde


def main():
    SpamData()
    StateHighwaySystemDissolve()
    #FederalAidSystemDissolve()
    #RouteMaker()
    
def SpamData():
    print "refreshing processing file geodatabase in C:/temp"
    from arcpy import CreateFileGDB_management, Exists, Delete_management, ImportXMLWorkspaceDocument_management
    if Exists(spampath):
        try:
            Delete_management(spampath)
            print "deleted existing temp geodatabase"
        except:
            print "there may be a lock on your temporary processing geodatabase"
          
    else:
        print "no existing temp geodatabase to delete"
    try:
        CreateFileGDB_management(spam, spamdata)
        ImportXMLWorkspaceDocument_management(spampath, xmlpath, import_type="SCHEMA_ONLY", config_keyword="MAX_FILE_SIZE_4GB")
    except:
        print "start a new arcmap instance"
        

def RouteMaker():
    from arcpy import CreateRoutes_lr, Append_management
    CreateRoutes_lr(SSoutput+"Unsplit", "CountyKey1", RouteOutput+"CountyRoute", "TWO_FIELDS", "MIN_F_CNTY_2", "MAX_T_CNTY_2", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    CreateRoutes_lr(ClassOutput+"Unsplit", "CountyKey1", "in_memory/RMCRoute", "TWO_FIELDS", "MIN_F_CNTY_2", "MAX_T_CNTY_2", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    Append_management("RMCRoute", RouteOutput+"CountyRoute", "TEST", "", "")

def SuperSimpleSimplify(thePolylineLayer):
    from arcpy import SimplifyLine_cartography
    SimplifyLine_cartography(thePolylineLayer, os.path.join(spampathfd, "Simplified"), "POINT_REMOVE", "3 Feet", "FLAG_ERRORS", "KEEP_COLLAPSED_POINTS", "CHECK")
    
def NetworkingTopology(thePolylineLayer):
    from arcpy import CreateGeometricNetwork_management, VerifyAndRepairGeometricNetworkConnectivity_management
    CreateGeometricNetwork_management(r"C:/temp/KHub_Process1.gdb/NG", "NG_Net", "Simplified1_Pnt SIMPLE_JUNCTION YES;Simplified1 COMPLEX_EDGE NO", "10", "", "", "", "PRESERVE_ENABLED")
    VerifyAndRepairGeometricNetworkConnectivity_management(r"C:/temp/KHub_Process1.gdb/NG/NG_Net", r"C:/temp/KHub_Process1netlog", "VERIFY_AND_REPAIR", "NO_EXHAUSTIVE_CHECK", "DEFAULT")
    print "test"
    
def StateHighwayCalibrate(theStateHighwaySegments):
    #theStateHighwaySegments is defined as the roadway segments intended for calibration to the EXOR measures
    #this function is being called by 
      
    #here are the GIS routes with measures extracted regularly from EXOR using the FME extraction and python route reference tools from DT00ar60
    #these routes contain the current exor measures 
    #Smlrs = r'Database Connections\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.SMLRS'
    
    #need to define a route source represntative of the correct network year, about 2015
    #should have K-10 on 23rd street still
    
    Cmlrs = r'Database Connections\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.CMLRS_2015'
    
    from arcpy import FeatureClassToFeatureClass_conversion, FeatureVerticesToPoints_management, LocateFeaturesAlongRoutes_lr, CalculateField_management
    from arcpy import env, MakeFeatureLayer_management, SelectLayerByAttribute_management, DeleteRows_management, AddJoin_management, AddField_management, RemoveJoin_management
    env.overwriteOutput=1
    # Start by loading NG911 aggregated, conflated road centerlines to an in-memory feature class
    
    #FeatureClassToFeatureClass_conversion(Roads, "in_memory", "RoadCenterlines", "StateKey1 IS NOT NULL ")
    #FeatureClassToFeatureClass_conversion(Roads, "in_memory", "RoadCenterlines", "StateKey1 IS NOT NULL ")
    
    
    MakeFeatureLayer_management(theStateHighwaySegments, "CalibrateRoadCenterlines")
    RoadCenterlines = "CalibrateRoadCenterlines"
    #these are the two linear referencing networks we're going to use to calibrate the state highway system
    #for iteration 2, no source data should refer to the state LRM, so we're only doing the County LRM
    Lrm_Dict = {'COUNTY':Cmlrs}
    
    #and this is the beginning and end of a line, for which we are going to create a vertex point
    End_List = ['START', 'END']
    
    # First,  create points at the begin and end of each road centerline segment using Vertices to Points.  
    for end in End_List:
        i_end_output = "in_memory/CalibrationPoint"+str(end)
        FeatureVerticesToPoints_management(RoadCenterlines, i_end_output, str(end))
    
    #Iterate through the LRMs to bring them into memory and do the processing for each segment begin and end point!  
    for key, value in Lrm_Dict.items():
        FeatureClassToFeatureClass_conversion(value, "in_memory", "LRM"+str(key))
        for end in End_List:
            outtable = "in_memory/"+str(end)+"_"+str(key)
            outstore = spampathfd+r"/"+str(end)+"_"+str(key)
            outproperties = str(key)+"_LRS POINT MEAS_"+str(key)
            if key == "STATE":
                lrskey = str(key)+"_NQR_DESCRIPTION"
            else:
                lrskey = "NQR_DESCRIPTION"
            LocateFeaturesAlongRoutes_lr("in_memory/CalibrationPoint"+str(end), "in_memory/LRM"+str(key), lrskey, "500 Feet", outtable, outproperties, "ALL", "DISTANCE", "ZERO", "FIELDS", "M_DIRECTON")
            
            #that LFAR function located begin/end segment points to ALL ROUTES within 500 feet of the segment endpoint
        
            #for calibrating, we are only interested in the points and LFAR Results that where this query is NOT true:
            qNotThisRoad  = '"COUNTY_LRS" <> "KDOT_LRS_KEY"'
            #so we will delete the records where this query is trye
            SelectLayerByAttribute_management(str(end)+"_"+str(key), "NEW_SELECTION", qNotThisRoad)
            DeleteRows_management(str(end)+"_"+str(key))
            #DeleteField_management(outtable, "Mileage_Length;Mileage_Logmile;ROUTE_PREFIX_TARGET;LRS_ROUTE_NUM_TARGET;LRS_UNIQUE_TARGET;Non_State_System_OBJECTID;LRS_BACKWARD;F_CNTY_2;T_CNTY_2;F_STAT_2;T_STAT_2;CountyKey2;MileFlipCheck;InLine_FID;SimLnFLag")
            
            #TableToTable_conversion(outtable, ConflationDatabase, outstore)
            #One Method, if using SQL Server, is to use table to table conversion to export to SQL server, then run these query in #CalcUsingSQLserver()
            #If not using SQL server this will suffice, although if there are multiple orig FID's to the original data source FID, there's no logic or handling to discern between the many to one relationship.  
            #In the case of hte many to one, or duplicate Orig_FID in the measure table, it might be desirable to choose the closest result
            #A few of the duplicates I reviewed had identical measure values, if that's always the case, then handling the duplicates is unnecessary
            measfield = str(end)+"_"+str(key)+"_meas"
            try:
                AddField_management(theStateHighwaySegments, measfield, "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED")
            except:
                print "could not add the field for calibrated measures"
            jointable = str(end)+"_"+str(key)
            AddJoin_management(theStateHighwaySegments, "OBJECTID", jointable, "ORIG_FID", "KEEP_ALL")
            exp = "!"+jointable+".MEAS_"+str(key)+"!"
            measfieldcalc = theStateHighwaySegments+"."+measfield
            CalculateField_management(theStateHighwaySegments, measfieldcalc, exp, "PYTHON")
            RemoveJoin_management(theStateHighwaySegments)
        
        # NEed to now test for direction again based on begin < end, handle flipping and assemble the routes
    from arcpy import CreateRoutes_lr
    CreateRoutes_lr("CalibrateRoadCenterlines", "KDOT_LRS_KEY", "in_memory/Simplified_CreateRoutes_test1", "TWO_FIELDS", "START_COUNTY_meas", "END_COUNTY_meas", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    
    #the dissolve method does not help, it hurts with the accuracy of the calibration process
    #CreateRoutes_lr(SSoutput+"Unsplit", "CountyKey2", "in_memory/Simplified_CreateRoutes_test2", "TWO_FIELDS", "MIN_F_CNTY_2", "MAX_T_CNTY_2", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")

    
def CalcUsingSQLserver():    
    import _mssql
    print "enter the sde password to your sql server instance:"
    conn = _mssql.connect(server = 'dt00ar65\gdb_dev', user = 'sde', password = "secret", database = 'KHUB_i2')

    querystring1 = """
        update [sde].[STATE_SYSTEM_CALIBRATED]
            set [Exor_Beg_MP] = m.[MEAS_COUNTY]
            from [sde].[STATE_SYSTEM_CALIBRATED] r
            JOIN (select distinct [GCID], [COUNTY_LRS], [MEAS_COUNTY], [CountyKey2]
                from [sde].[START_COUNTY]
                where 1=1
                and substring([COUNTY_LRS],0,12) =substring([CountyKey2],0,12)) m on r.[GCID] = m.[GCID]
            where 1=1
            
        
        
        update [sde].[STATE_SYSTEM_CALIBRATED]
        set [EXOR_End_Mp] = m.[MEAS_COUNTY]
        from [sde].[STATE_SYSTEM_CALIBRATED] r
        JOIN (select distinct [COUNTY_LRS], [MEAS_COUNTY], [GCID], [CountyKey2]
            from [sde].[END_COUNTY]
            where 1=1
            and substring([COUNTY_LRS],0,12) = substring([CountyKey2],0,12)) m on r.[GCID] = m.[GCID]
        where 1=1
        
        """

    
    conn.execute_query(querystring1)

    
    conn.close
            #  F:\Cart\projects\Conflation\SQL\SQLServer\Conflation2012\KHUB  is where that SQL query lives, its the State System Calibration 2 SQL file
        
def StateHighwaySystemDissolve():
    from arcpy import FeatureClassToFeatureClass_conversion,FlipLine_edit,SelectLayerByAttribute_management,CalculateField_management
    print "processing the state highway system"
    from arcpy import AddField_management, Dissolve_management, Delete_management

    # Create an in-memory copy of state highway system routes based on LRS Route Prefix
    FeatureClassToFeatureClass_conversion(roadcenterlines, "in_memory", "State_System", "LRS_ROUTE_PREFIX in ('I', 'U', 'K')")

    #this happens in memory, only do this in memory, and don't do it twice or the flipping logic will break
    #Many records have state system flip flags that are falsely identified as yes.
    #The flip flag by definition tells you about the nature of the geometry direction accumulation of vertices compared to the direction accummulation of measures.
    #If the measures are backwards, ie the end measure is less than the begin measure, that is the defining indicator 
    #that the centerline vertex accumulation is opposite the measure accumulation. 
    #to be consistent, this processing will orient all vertices in the direction of measure accumulation, 
    #and at the attribute level,  ensure all begin measures are less than the end measures for all segments to be processed  
    
    #two lines here correct false positive flip flags
    SelectLayerByAttribute_management("State_System", "NEW_SELECTION", """("COUNTY_BEGIN_MP" > "COUNTY_END_MP") AND "STATE_FLIP_FLAG" = """"'Y'""")
    CalculateField_management("State_System", "STATE_FLIP_FLAG", """''""", "PYTHON_9.3", "")
    
    #about 941 records in Southwest Kansas had reverse mileages and need to be flipped  
    #two lines here correct null flip flags
    SelectLayerByAttribute_management("State_System", "NEW_SELECTION", """("COUNTY_BEGIN_MP" > "COUNTY_END_MP") AND "STATE_FLIP_FLAG" IS NULL""")
    CalculateField_management("State_System", "STATE_FLIP_FLAG", """'Y'""", "PYTHON_9.3", "")
    
    #flip the lines using the flip flag
    SelectLayerByAttribute_management("State_System", "NEW_SELECTION", """"STATE_FLIP_FLAG" = 'Y' """)
    FlipLine_edit("State_System")
    
    #need to flip mileages where geometry was flipped so add fields
    AddField_management("State_System", "F_CNTY_2", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("State_System", "T_CNTY_2", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("State_System", "F_STAT_2", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("State_System", "T_STAT_2", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("State_System", "CountyKey2", "TEXT", "15", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        
    #check if there are any state system segments where the to measure is less than the from measure and flag them for review
    AddField_management("State_System", "MileFlipCheck", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    CalculateField_management("State_System", "F_CNTY_2", "!COUNTY_END_MP!", "PYTHON_9.3", "")
    CalculateField_management("State_System", "T_CNTY_2", "!COUNTY_BEGIN_MP!", "PYTHON_9.3", "")
    CalculateField_management("State_System", "F_STAT_2", "!STATE_END_MP!", "PYTHON_9.3", "")
    CalculateField_management("State_System", "T_STAT_2", "!STATE_BEGIN_MP!", "PYTHON_9.3", "")
    
    #Switch selection and calculate mileages
    SelectLayerByAttribute_management("State_System", "SWITCH_SELECTION", "")
    
    CalculateField_management("State_System", "F_CNTY_2", "!COUNTY_BEGIN_MP!", "PYTHON_9.3", "")
    CalculateField_management("State_System", "T_CNTY_2", "!COUNTY_END_MP!", "PYTHON_9.3", "")
    CalculateField_management("State_System", "F_STAT_2", "!STATE_BEGIN_MP!", "PYTHON_9.3", "")
    CalculateField_management("State_System", "T_STAT_2", "!STATE_END_MP!", "PYTHON_9.3", "")
    
    #KDOT Direction should already be calculated, by running "DualCarriagweayIdentity.py" and updating the KDOT_DIRECTION_CALC to 1 where dual carriageway is found
    #Validation_CheckOverlaps can also help identify sausage link/parallel geometries that may indicate dual carriageway
    #identify and calculate the KDOT_DIRECTION_CALC flag by whatever means necessary - script, manual editing
    #Select the EB routes and change the LRS_Direction to WB
    
    SelectLayerByAttribute_management("State_System", "NEW_SELECTION", """"KDOT_DIRECTION_CALC" = '1' AND "LRS_DIRECTION" = 'EB'""")
    CalculateField_management("State_System", "LRS_DIRECTION", "'WB'", "PYTHON_9.3", "")
    #Select the SB routes to change the LRS direction to SB
    
    SelectLayerByAttribute_management("State_System", "NEW_SELECTION", """"KDOT_DIRECTION_CALC" = '1' AND "LRS_DIRECTION" = 'NB'""")
    CalculateField_management("State_System", "LRS_DIRECTION", "'SB'", "PYTHON_9.3", "")
    
    #Clear the selections
    SelectLayerByAttribute_management("State_System", "CLEAR_SELECTION", "")
    
    #Calculate County LRS Key in CountyKey1 field for State Highway system
    #Need to add CountyKey2 for iteration 2, also go ahead and add new LRS Key format
    CalculateField_management("State_System", "CountyKey2", """[LRS_COUNTY_PRE] + [LRS_ROUTE_PREFIX] + [LRS_ROUTE_NUM] + [LRS_ROUTE_SUFFIX] + [LRS_UNIQUE_IDENT] +"-" + [LRS_DIRECTION]""", "VB")
    #CalculateField_management("State_System", "StateKey2", """[LRS_ROUTE_PREFIX] + [LRS_ROUTE_NUM] + [LRS_ROUTE_SUFFIX] + [LRS_UNIQUE_IDENT] +"-" + [LRS_DIRECTION]""", "VB")

    SuperSimpleSimplify("State_System")
    
    StateHighwayCalibrate("Simplified")
    
    
    #this is the dissolve - the output of this is a feature class which is "clean" for route creation of the state highway system
    #looking at the dissolve output, you can easily identify multipart issues due to KDOT_DIRECTION_CALC settings and/or ghost routes 
    #Dissolve_management("State_System", SSoutput+"dissolve", "CountyKey2;LRS_COUNTY_PRE;LRS_ROUTE_PREFIX;LRS_ROUTE_NUM;LRS_ROUTE_SUFFIX;LRS_UNIQUE_IDENT;LRS_DIRECTION", "F_CNTY_2 MIN;T_CNTY_2 MAX", "SINGLE_PART", "DISSOLVE_LINES")
    #Dissolve_management("State_System", SSoutput+"Unsplit" , "CountyKey2;LRS_COUNTY_PRE;LRS_ROUTE_PREFIX;LRS_ROUTE_NUM;LRS_ROUTE_SUFFIX;LRS_UNIQUE_IDENT;LRS_DIRECTION", "F_CNTY_2 MIN;T_CNTY_2 MAX", "SINGLE_PART", "UNSPLIT_LINES")
    #Once dissolved, delete the in memory dataset to free up resources
    #review the dissolve output, go back and flag the input data 
    
    print "...and hardly a splash!"
    
    #Delete_management("State_System")
    
def FederalAidSystemDissolve():
    from arcpy import FeatureClassToFeatureClass_conversion,FlipLine_edit,SelectLayerByAttribute_management,CalculateField_management

    from arcpy import AddField_management, Dissolve_management, Delete_management
    print "hang on a minute, let me stretch..."
    FeatureClassToFeatureClass_conversion(roadcenterlines, "in_memory", "Classified_System", "LRS_ROUTE_PREFIX in ('R', 'M', 'C')")
    print "RMC Routes here"
    CalculateField_management("Classified_System", "CountyKey1", "!Non_State_System_LRSKey![:-1]+ !KDOT_DIRECTION_CALC!", "PYTHON_9.3", "")
    #select lines that need to be flipped - this query should include them all, and not result in any double flips
    print "they went that way"
    SelectLayerByAttribute_management("Classified_System", "NEW_SELECTION", """("NON_STATE_FLIP_FLAG" = 'Y'  AND( "LRS_BACKWARD" IS NULL OR "LRS_BACKWARD" = 0)) OR ("LRS_BACKWARD" IN( -1 , 1 ) AND "NON_STATE_FLIP_FLAG" IS NULL)""")
    #editorial note:  as of 2/13/2017, draft statewide conflation deliverable, there are 41782 of 93600 segments in the above queries for flips on the classified networks
    #there are 38525 segments where the non_state begin logmile is greater than the non state end logmile
    #flip geometry and calculate begin/end miles
    print "doing cartwheels"
    FlipLine_edit("Classified_System")
    AddField_management("Classified_System", "F_CNTY_2", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("Classified_System", "T_CNTY_2", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("Classified_System", "F_STAT_2", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("Classified_System", "T_STAT_2", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        
    CalculateField_management("Classified_System", "F_CNTY_2", "!NON_STATE_END_MP!", "PYTHON_9.3", "")
    CalculateField_management("Classified_System", "T_CNTY_2", "!NON_STATE_BEGIN_MP!", "PYTHON_9.3", "")
    
    print "now a somersault"
    #calculate mileages for non flip segments
    SelectLayerByAttribute_management("Classified_System", "SWITCH_SELECTION", "")
    CalculateField_management("Classified_System", "F_CNTY_2", "!NON_STATE_BEGIN_MP!", "PYTHON_9.3", "")
    CalculateField_management("Classified_System", "T_CNTY_2", "!NON_STATE_END_MP!", "PYTHON_9.3", "")

    #check for increasing logmiles

    SelectLayerByAttribute_management("Classified_System", "NEW_SELECTION", '"F_CNTY_2" > "T_CNTY_2"')
    #as of 2/13/2017, draft statewide conflation deliverable at this point there are 5206 segments meeting this criteria
    #upon initial review, lots of variables... need to review what's going on here more
    
    #There is 1 segment flagged with KDOT_DIRECTION_CALC = 1
    #Also, the Non-State_System was conflated with the GIS_LRS_KEY, not the NSND NE_Unique which MAY be preferable for data migration.
    #based on discussion with Kevin K, there shouldnt be any unique information keyed to the non-primary direction
    #The NSND NE_Unique key should be calculate-able from the LRS Key parts we have once we calculate the appropriate direction code
    #The NSND does not follow Even/East Odd/North rule 100%
    SelectLayerByAttribute_management("Classified_System", "NEW_SELECTION", """"KDOT_DIRECTION_CALC" = '1'""")
    #We are also going to need to refer to the NSND or NUSYS layer from CANSYS to determine whether a route is EB or NB, logically

    SelectLayerByAttribute_management("Classified_System", "CLEAR_SELECTION", "")
    
    print "here comes the landing..."
    
    Dissolve_management("Classified_System", ClassOutput+"dissolve", "CountyKey1;LRS_COUNTY_PRE;LRS_ROUTE_PREFIX;LRS_ROUTE_NUM;LRS_ROUTE_SUFFIX;LRS_UNIQUE_IDENT;KDOT_DIRECTION_CALC", "F_CNTY_2 MIN;T_CNTY_2 MAX", "SINGLE_PART", "DISSOLVE_LINES")
    Dissolve_management("Classified_System", ClassOutput+"Unsplit" , "CountyKey1;LRS_COUNTY_PRE;LRS_ROUTE_PREFIX;LRS_ROUTE_NUM;LRS_ROUTE_SUFFIX;LRS_UNIQUE_IDENT;KDOT_DIRECTION_CALC", "F_CNTY_2 MIN;T_CNTY_2 MAX", "SINGLE_PART", "UNSPLIT_LINES")
    #Once dissolved, delete the in memory dataset to free up resources
    #review the dissolve output, go back and flag the input data 
    print "..Stuck it beautifully!"
    Delete_management("Classified_System")

    print "I've seen it go better, let's see what the judges say..."
    

main()


'''
notes from the route creation processes

1040, At least one of the route location's measure values is invalid, KHUB_I2.SDE.County2DissolveUnsplit
1041, At least one of the route location's measure values is invalid, KHUB_I2.SDE.County2DissolveUnsplit
1042, At least one of the route location's measure values is invalid, KHUB_I2.SDE.County2DissolveUnsplit
1043, At least one of the route location's measure values is invalid, KHUB_I2.SDE.County2DissolveUnsplit
1048, At least one of the route location's measure values is invalid, KHUB_I2.SDE.County2DissolveUnsplit
1049, At least one of the route location's measure values is invalid, KHUB_I2.SDE.County2DissolveUnsplit
1050, At least one of the route location's measure values is invalid, KHUB_I2.SDE.County2DissolveUnsplit
1053, At least one of the route location's measure values is invalid, KHUB_I2.SDE.County2DissolveUnsplit
1054, At least one of the route location's measure values is invalid, KHUB_I2.SDE.County2DissolveUnsplit
1055, At least one of the route location's measure values is invalid, KHUB_I2.SDE.County2DissolveUnsplit


27, The route location's route ID is invalid (NULL, empty or invalid value), KHUB_I2.SDE.RMC2DissolveUnsplit
28, The route location's route ID is invalid (NULL, empty or invalid value), KHUB_I2.SDE.RMC2DissolveUnsplit
29, The route location's route ID is invalid (NULL, empty or invalid value), KHUB_I2.SDE.RMC2DissolveUnsplit


'''


