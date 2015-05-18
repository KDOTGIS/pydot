'''
Created on Apr 23, 2015

This script is designed to dissolve all feature classes exported from CANSYS spatial views in EXOR to a File Geodatabase on the server.  
When FME runs, it should recreate that geodatabase, and all of it's tables
This geodatabase contains CANSYS items for roadway attributes that apply items with cross sectional positions
The script goes through each feature class, dissolves the linear segments around common attribute values, and 
first attempts to truncate and append the dissolved data from in_memory workspace to the destination geodatabase, 
if that fails, the script will attempt to drop and create a new dataset (need to reset permissions in that case)
if the dataset does not already exist, it will be created.  

@author: kyleadm
'''
from arcpy import (ListFields, Dissolve_management,
                   env, Exists, Delete_management,
                   TruncateTable_management, Append_management,
                   ExecuteError, ListFeatureClasses,
                   ChangePrivileges_management, DisconnectUser,
                   AcceptConnections)

from EXOR_GIS_CONFIG import OpEnvironment

def DissolveXSPItems(OpEnvironmentMode):
        
    OpRunIn= OpEnvironment.OpRunInXSum  # @UndefinedVariable
    OpRunOut= OpEnvironment.OpRunOut  # @UndefinedVariable
    adm=OpEnvironment.adm  # @UndefinedVariable
    Owner=OpEnvironment.Owner  # @UndefinedVariable
    DB=OpEnvironment.DB  # @UndefinedVariable
    
    env.workspace = OpRunIn
    env.overwriteOutput = True
    print OpRunIn
    
    #combine the connection, db, and owner to the destination path for enterprise geodatabase output
    OpRunFullOut = OpRunOut+"/"+DB+"."+Owner+"."
    print OpRunFullOut
    
    FCList = ListFeatureClasses()
    print "dissolving items in the primary direction"
    FCGlobalFieldsDissolve = ["LRS_KEY", "COUNTY_CD", "COUNTY_NAME", "DISTRICT"]
    FCGlobalFieldsSummarize = "BSMP MIN;ESMP MAX;BCMP MIN;ECMP MAX"
    FCFieldsIgnore = ["OBJECTID", "CRND_RTE", "SHAPE", "SHAPE.STLength()",
                      "BSMP", "ESMP", "BCMP", "ECMP", "OLD_FUN_CLASS", "FUN_DT"]
    for Item in FCList:
        ItemOut = Item[2:]
        ItemDissolveFields = []
        print ItemOut
        fields = ListFields(Item)
        for field in fields:
            if field.name not in FCFieldsIgnore:
                #print " "+field.name
                ItemDissolveFields.append(field.name)
        dissolvelist = ItemDissolveFields+FCGlobalFieldsDissolve
        DissolveFields = ';'.join(dissolvelist)
        if Exists(OpRunFullOut+ItemOut):  
            try:
                print "feature class "+str(ItemOut) + " exists and will be updated"
                Dissolve_management(Item, "in_memory/"+ItemOut, DissolveFields, FCGlobalFieldsSummarize, "MULTI_PART", "DISSOLVE_LINES")
                TruncateTable_management(OpRunFullOut+ItemOut)
                Append_management("in_memory/"+ItemOut, OpRunFullOut+ItemOut, "NO_TEST", "#")
                Delete_management("in_memory/"+ItemOut)
                print "feature class "+str(ItemOut) + " was successfully updated"
            except ExecuteError:
                print "update failed because the schema has changed from what existed"
                #need to add locking
                DisconnectUser(adm, "readonly")
                AcceptConnections(adm, True)
                Delete_management(OpRunFullOut+ItemOut)
                print "recreating the dissolved feature class for "+str(ItemOut)
                Dissolve_management(Item, OpRunFullOut+ItemOut, DissolveFields, FCGlobalFieldsSummarize, "MULTI_PART", "DISSOLVE_LINES")
                ChangePrivileges_management(OpRunFullOut+ItemOut, "readonly", "GRANT", "AS_IS")
            except:
                print "another error happened on updating the feature class"
        else:
            print "feature class "+str(ItemOut) + " will be created or overwritten"
            DisconnectUser(adm, "readonly")
            AcceptConnections(adm, True)
            Dissolve_management(Item, OpRunFullOut+ItemOut, DissolveFields, FCGlobalFieldsSummarize, "MULTI_PART", "DISSOLVE_LINES")
            ChangePrivileges_management(OpRunFullOut+ItemOut, "readonly", "GRANT", "AS_IS")
        try:
            Delete_management("in_memory/"+Item)
        except:
            pass
    
if __name__== "__main__":
    DissolveXSPItems(OpEnvironment)
