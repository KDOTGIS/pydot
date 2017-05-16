'''
process described in general by KyleG
testd by TimB
developed by DirkT, and implemented in DirkT code.

'''

def KDOTOverlappingRoutesFlaggingFix():
    # conflationCountyBoundary = r'\\gisdata\ArcGIS\GISdata\Connection_files\Conflation2012_RO.sde\Conflation.SDE.NG911\Conflation.SDE.CountyBoundary'
    # Copy the "Conflation.SDE.CountyBoundary" layer to the FGDB.
    
    if Exists(routesSourceIntermediate):
        Delete_management(routesSourceIntermediate)
    else:
        pass
    
    CopyFeatures_management(dissolvedFlippedOutput, routesSourceIntermediate)
    
    tempDesc = Describe(routesSourceIntermediate)
    print("Calculating values for new LRS and measure fields in " + returnFeatureClass(tempDesc.catalogPath) + ".")
    
    currentFields = [x.name for x in tempDesc.fields]
    
    try:
        del tempDesc
    except:
        pass
    
    fieldsNeeded = ['OverlapStatus']
    
    fieldsToAdd = [x for x in fieldsNeeded if x not in currentFields]
    
    if 'OverlapStatus' in fieldsToAdd:
        AddField_management(routesSourceIntermediate, "OverlapStatus", "TEXT", "", "", 1, "OverlapStatus", nullable)
    else:
        pass
    
    fcAsFeatureLayerRSCFL = 'routesSourceIntermediateFL'
    fcAsFeatureLayerRSCFL_FCName = returnFeatureClass(routesSourceIntermediate)
    countyBoundary_FCName = returnFeatureClass(conflationCountyBoundary)
    
    joinField1 = 'STEWARD'
    indexFieldList = [joinField1]
    selectionQuery2 = "NOT (COUNTY_L = COUNTY_R)"
    MakeFeatureLayer_management(routesSourceIntermediate, fcAsFeatureLayerRSCFL, selectionQuery2)
    
    countResult = GetCount_management(fcAsFeatureLayerRSCFL)
    intCount = int(countResult.getOutput(0))
    
    print(str(intCount) + " records were added to the feature layer defined by the query, " + str(selectionQuery2) +  ".")
    
    try:
        RemoveIndex_management(fcAsFeatureLayerRSCFL, stewardIndexNameRSC)
    except:
        print("The attribute index " + stewardIndexNameRSC + " could not be removed, or it may not have existed to begin with.")
    try:
        RemoveIndex_management(conflationCountyBoundary, stewardIndexNameCB)
    except:
        print("The attribute index " + stewardIndexNameCB + " could not be removed, or it may not have existed to begin with.")
    
    print("Adding attribute indexes...")
    # Then, add an index on the "Steward" field to both of them.
    AddIndex_management(routesSourceIntermediate, indexFieldList, stewardIndexNameRSC)
    AddIndex_management(conflationCountyBoundary, indexFieldList, stewardIndexNameCB)
    
    # Join the tables based on their "STEWARD" fields.
    AddJoin_management(fcAsFeatureLayerRSCFL, joinField1, conflationCountyBoundary, joinField1)
    print("Attribute indexes added and join created.")
    # Select by Attributes from said table where "CountyLRSPrefix" field == "Conflation.SDE.CountyBoundary"."KDOT_CountyNumStr" field
    # Then, reverse the selection.
    # These are the "zombie routes".
    
    # ----------------------------------------------------------------------- #
    # "NOT (RoutesSource.LRS_COUNTY_PRE = CountyBoundary.KDOT_CountyNumStr)"
    # causes Python and ArcMap to both crash when passed to
    # SelectLayerByAttribute_management for this layer.
    # Instead, use RoutesSource.LRS_COUNTY_PRE = CountyBoundary.KDOT_CountyNumStr, then
    # invert the selection.
    
    fieldNameToFind1 = fcAsFeatureLayerRSCFL_FCName + '.LRS_COUNTY_PRE'
    fieldNameToFind2 = countyBoundary_FCName + '.KDOT_CountyNumStr'
    
    listedFields = ListFields(fcAsFeatureLayerRSCFL)
    
    for fieldObject in listedFields:
        if fieldObject.aliasName == 'LRS_COUNTY_PRE' or fieldObject.aliasName == fieldNameToFind1:
            print 'LRS_COUNTY_PRE found!'
            fieldNameToFind1 = fieldObject.name 
        else:
            pass
        if fieldObject.aliasName == 'KDOT_CountyNumStr' or fieldObject.aliasName == fieldNameToFind2:
            print 'KDOT_CountyNumStr found!'
            fieldNameToFind2 = fieldObject.name 
        else:
            pass
    
    selectionQuery3 = fieldNameToFind1 + ''' <> ''' + '''''' + fieldNameToFind2
    
    print(str(selectionQuery3) + " is being used as the selection query.")
    
    
    SelectLayerByAttribute_management(fcAsFeatureLayerRSCFL, "NEW_SELECTION", selectionQuery3)
    #getCount, then Print the results.
    countResult = GetCount_management(fcAsFeatureLayerRSCFL)
    intCount = int(countResult.getOutput(0))
    print(str(intCount) + " records were selected by the query, " + str(selectionQuery3) +  ".")
    
    # Clean-up try/excepts.
    print ('Removing joins and indexes.')
    try:
        RemoveJoin_management(fcAsFeatureLayerRSCFL)
    except:
        print("The join could not be removed, or it may not have existed to begin with.")
    try:
        RemoveIndex_management(fcAsFeatureLayerRSCFL, stewardIndexNameRSC)
    except:
        print("The attribute index " + stewardIndexNameRSC + " could not be removed, or it may not have existed to begin with.")
    try:
        RemoveIndex_management(conflationCountyBoundary, stewardIndexNameCB)
    except:
        print("The attribute index " + stewardIndexNameCB + " could not be removed, or it may not have existed to begin with.")
    
    countResult = GetCount_management(fcAsFeatureLayerRSCFL)
    intCount = int(countResult.getOutput(0))
    
    # Then, calculate the field for the Zombie Suffix.
    print("Setting the OverlapStatus for " + str(intCount) + " records to 'Z'.")
    expressionText = "'Z'"
    CalculateField_management(fcAsFeatureLayerRSCFL, "OverlapStatus", expressionText, "PYTHON_9.3")
    
    # Instead of just excluding these, could calculate the LRS Key to a modified verison that
    # includes the Z.