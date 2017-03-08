'''
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


roadcenterlines  ="Database Connections/Conflation2012_ADuser.sde/Conflation.SDE.NG911/Conflation.SDE.RoadCenterlines"
#roadcenterlines = r"\\gisdata\planning\Cart\projects\Conflation\GIS_DATA\GEO_COMM\STATEWIDE_20170212\STATEWIDE_20170212.gdb\NG911\RoadCenterlines"

SSoutput = r"Database Connections\Conflation_KHUBI2_sde.sde\KHUB_I2.SDE.KANSAS_DOT\KHUB_I2.SDE.County2Dissolve"
ClassOutput = r"Database Connections\Conflation_KHUBI2_sde.sde\KHUB_I2.sde.KANSAS_DOT\KHUB_I2.SDE.RMC2Dissolve"
RouteOutput = r"Database Connections/Conflation_KHUBI2_sde.sde/KHUB_I2.SDE.KHubI2/KHUB_I2.SDE."


def main():
    #StateHighwaySystemDissolve()
    #FederalAidSystemDissolve()
    RouteMaker()
    
    
def RouteMaker():
    from arcpy import CreateRoutes_lr, Append_management
    CreateRoutes_lr(SSoutput+"Unsplit", "CountyKey1", RouteOutput+"CountyRoute", "TWO_FIELDS", "MIN_F_CNTY_2", "MAX_T_CNTY_2", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    CreateRoutes_lr(ClassOutput+"Unsplit", "CountyKey1", "in_memory/RMCRoute", "TWO_FIELDS", "MIN_F_CNTY_2", "MAX_T_CNTY_2", "UPPER_LEFT", "1", "0", "IGNORE", "INDEX")
    Append_management("RMCRoute", RouteOutput+"CountyRoute", "TEST", "", "")


def StateHighwaySystemDissolve():
    from arcpy import FeatureClassToFeatureClass_conversion,FlipLine_edit,SelectLayerByAttribute_management,CalculateField_management
    print "Up now, the state highway system"
    from arcpy import AddField_management, Dissolve_management, Delete_management
    print "The state highways are a little over 10,000 miles these days"
    print "That's right arnie, they've been dominating transportation in Kansas since about 1936."
    print "stepping up to the ladder now"
    # Create an in-memory copy of state highay system routes based on LRS Route Prefix
    FeatureClassToFeatureClass_conversion(roadcenterlines, "in_memory", "State_System", "LRS_ROUTE_PREFIX in ('I', 'U', 'K')")
    #about 941 records in Southwest Kansas had reverse mileages and need to be flipped
    #this should be corrected in the final conflation delivery
    #if it is not corrected, these route segments should be explored in more detail
    print "and we're off"
    #print "ready, set, go!"
    SelectLayerByAttribute_management("State_System", "NEW_SELECTION", """("COUNTY_BEGIN_MP" > "COUNTY_END_MP" OR "STATE_BEGIN_MP" > "STATE_END_MP") AND "STATE_FLIP_FLAG" IS NULL""")
    CalculateField_management("State_System", "STATE_FLIP_FLAG", """'Y'""", "PYTHON_9.3", "")
    
    SelectLayerByAttribute_management("State_System", "NEW_SELECTION", """"STATE_FLIP_FLAG" = 'Y' """)
    
    print "here comes a 180 whirly-doo"
    FlipLine_edit("State_System")
    
    #need to flip mileages where geometry was flipped so add fields
    AddField_management("State_System", "F_CNTY_2", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("State_System", "T_CNTY_2", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("State_System", "F_STAT_2", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    AddField_management("State_System", "T_STAT_2", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
        
    #check if there are any state system segments where the to is greater than the from and flag them for review
    AddField_management("State_System", "MileFlipCheck", "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    print "with a twist"
    CalculateField_management("State_System", "F_CNTY_2", "!COUNTY_END_MP!", "PYTHON_9.3", "")
    CalculateField_management("State_System", "T_CNTY_2", "!COUNTY_BEGIN_MP!", "PYTHON_9.3", "")
    CalculateField_management("State_System", "F_STAT_2", "!STATE_END_MP!", "PYTHON_9.3", "")
    CalculateField_management("State_System", "T_STAT_2", "!STATE_BEGIN_MP!", "PYTHON_9.3", "")
    
    # Switch selection and calculate mileages
    print "then a spin"
    SelectLayerByAttribute_management("State_System", "SWITCH_SELECTION", "")

    CalculateField_management("State_System", "F_CNTY_2", "!COUNTY_BEGIN_MP!", "PYTHON_9.3", "")
    CalculateField_management("State_System", "T_CNTY_2", "!COUNTY_END_MP!", "PYTHON_9.3", "")
    CalculateField_management("State_System", "F_STAT_2", "!STATE_BEGIN_MP!", "PYTHON_9.3", "")
    CalculateField_management("State_System", "T_STAT_2", "!STATE_END_MP!", "PYTHON_9.3", "")
    #KDOT Direction should already be calculated, by running "DualCarriagweayIdentity.py" and updating the KDOT_DIRECTION_CALC to 1 where dual carriagway is found
    #Validation_CheckOverlaps can also help do identify sausage link/parallel geometries that may indicate dual carriagway, but that script does not yet 
    #identify and calculate the KDOT_DIRECTION_CALC flag.  It probably could with more development
    # Select the EB routes and change the LRS_Direction to WB
    
    print "...changing directions here, now going the other way.."
    SelectLayerByAttribute_management("State_System", "NEW_SELECTION", """"KDOT_DIRECTION_CALC" = '1' AND "LRS_DIRECTION" = 'EB'""")
    CalculateField_management("State_System", "LRS_DIRECTION", "'WB'", "PYTHON_9.3", "")
    #Select the SB routes to chante hte LRS direction to SB
    SelectLayerByAttribute_management("State_System", "NEW_SELECTION", """"KDOT_DIRECTION_CALC" = '1' AND "LRS_DIRECTION" = 'NB'""")
    CalculateField_management("State_System", "LRS_DIRECTION", "'SB'", "PYTHON_9.3", "")
    # Clear the selections
    SelectLayerByAttribute_management("State_System", "CLEAR_SELECTION", "")

    #Calculate County LRS Key in CountyKey1 field for State Highway system
    #Need to add CountyKey2 for iteration 2, also go ahead and add new LRS Key format
    CalculateField_management("State_System", "CountyKey1", """[LRS_COUNTY_PRE] + [LRS_ROUTE_PREFIX] + [LRS_ROUTE_NUM] + [LRS_ROUTE_SUFFIX] + [LRS_UNIQUE_IDENT] +"-" + [LRS_DIRECTION]""", "VB")
    CalculateField_management("State_System", "StateKey1", """[LRS_ROUTE_PREFIX] + [LRS_ROUTE_NUM] + [LRS_ROUTE_SUFFIX] + [LRS_UNIQUE_IDENT] +"-" + [LRS_DIRECTION]""", "VB")
    
    print "here comes the big finish, a triple lindy"
    #this is the dissolve - the output of this is a feature class which is clean for route creation of the state highway system
    Dissolve_management("State_System", SSoutput+"dissolve", "CountyKey1;LRS_COUNTY_PRE;LRS_ROUTE_PREFIX;LRS_ROUTE_NUM;LRS_ROUTE_SUFFIX;LRS_UNIQUE_IDENT;LRS_DIRECTION", "F_CNTY_2 MIN;T_CNTY_2 MAX", "SINGLE_PART", "DISSOLVE_LINES")
    Dissolve_management("State_System", SSoutput+"Unsplit" , "CountyKey1;LRS_COUNTY_PRE;LRS_ROUTE_PREFIX;LRS_ROUTE_NUM;LRS_ROUTE_SUFFIX;LRS_UNIQUE_IDENT;LRS_DIRECTION", "F_CNTY_2 MIN;T_CNTY_2 MAX", "SINGLE_PART", "UNSPLIT_LINES")
    #Once dissolved, delete the in memory dataset to free up resources
    #review the dissolve output, go back and flag the input data 
    print "...and hardly a splash!"
    Delete_management("State_System")
    
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