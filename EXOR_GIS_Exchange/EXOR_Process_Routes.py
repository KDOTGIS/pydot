'''
Created on May 7, 2015

@author: kyleadm
'''
from arcpy import (MakeTableView_management, MakeFeatureLayer_management, MakeRouteEventLayer_lr,
                   TruncateTable_management, Append_management, env,
                   GetCount_management, FeatureClassToFeatureClass_conversion)




def MakeRouteLayers(OpEnvironmentMode):
    from EXOR_GIS_CONFIG import OpEnvironment
    OpRunIn= OpEnvironment.OpRunInRoutes  # @UndefinedVariable
    OpRunOut= OpEnvironment.OpRunOut  # @UndefinedVariable
    #adm=OpEnvironment.adm  # @UndefinedVariable
    Owner=OpEnvironment.Owner  # @UndefinedVariable
    DB=OpEnvironment.DB  # @UndefinedVariable
    
    env.workspace = OpRunIn
    env.overwriteOutput = True
    print OpRunIn
    
    #combine the connection, db, and owner to the destination path for enterprise geodatabase output
    OpRunFullOut = OpRunOut+r"/"+DB+"."+Owner+"."
    
    print "Updating CRND"
    #add the Map Extract Event Table limited to primary direction into memory
    TruncateTable_management(OpRunFullOut+"CRND")
    Append_management("CRND", OpRunFullOut+"CRND", "NO_TEST")
    print "Updating SRND"
    TruncateTable_management(OpRunFullOut+"SRND")
    Append_management("SRND", OpRunFullOut+"SRND", "NO_TEST")
    print "Updating NSND"
    TruncateTable_management(OpRunFullOut+"NSND")
    Append_management("NSND", OpRunFullOut+"NSND", "NO_TEST")  
        
    if GetCount_management("MAP_EXTRACT")>0:
        MakeTableView_management("MAP_EXTRACT", "V_MV_MAP_EXTRACT", "DIRECTION < 3")
    
        #Add the CRND CANSYS rotue layer, dynseg the event table, truncate and load to CMLRS
        MakeFeatureLayer_management("CRND", "CRND")
        MakeRouteEventLayer_lr("CRND", "NE_UNIQUE", "MAP_EXTRACT", "NQR_DESCRIPTION LINE BEG_CNTY_LOGMILE END_CNTY_LOGMILE", "CMLRS1", "", "ERROR_FIELD", "NO_ANGLE_FIELD", "NORMAL", "ANGLE", "LEFT", "POINT")
        try:
            print "truncation and appending the CMLRS"
            TruncateTable_management(OpRunFullOut+"CMLRS")
            Append_management("CMLRS1", OpRunFullOut+"CMLRS", "NO_TEST")
        except:
            print "could not truncate, overwriting CMLRS"
            FeatureClassToFeatureClass_conversion("CMLRS1", OpRunOut, "CMLRS","#", "#", "#")
        #except:
        #    print "could not update the CMLRS"
        
        MakeFeatureLayer_management("SRND", "SRND")
        MakeRouteEventLayer_lr("SRND", "NE_UNIQUE", "MAP_EXTRACT", "STATE_NQR_DESCRIPTION LINE BEG_STATE_LOGMILE END_STATE_LOGMILE", out_layer="SMLRS1", offset_field="", add_error_field="ERROR_FIELD", add_angle_field="NO_ANGLE_FIELD", angle_type="NORMAL", complement_angle="ANGLE", offset_direction="LEFT", point_event_type="POINT")
        try:
            print "truncation and appending the SMLRS"
            TruncateTable_management(OpRunFullOut+"SMLRS")
            Append_management("SMLRS1", OpRunFullOut+"SMLRS", "NO_TEST")
        except:
            print "could not truncate, overwriting SMLRS"
            FeatureClassToFeatureClass_conversion("SMLRS1", OpRunOut, "SMLRS","#", "#", "#")
        #except:
        #    print "could not update the SMLRS" 
        
        print "Route Layers Updated"
    else: 
        print "the map extract is unreliable and was not exported"

if __name__== "__main__":        
    
    OpRunIn = OpEnvironment.FME_NET
    OpRunOut = OpEnvironment.GIS_TARGET_CONN_DEV
    adm = OpEnvironment.GIS_TARGET_CONN_DEV_ADMIN
    
    env.workspace = OpRunIn
    env.overwriteOutput = True
    print OpRunIn
    
    #combine the connection, db, and owner to the destination path for enterprise geodatabase output
    OpRunFullOut = OpRunOut+"/"+OpEnvironment.GIS_TARGET_DB_DEV+"."+OpEnvironment.GIS_TARGET_DB_OWNER_DEV+"."
    
    print OpRunFullOut
    MakeRouteLayers(OpEnvironment)
