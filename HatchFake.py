'''
Created on Jul 14, 2015
This script will create route events as points along the route features at specific increments
the points can be symbolically displayed as route hatches for web mapping
@author: Kyle Gonterwitz with, as always the amazing help from Dirk Talley
@contact: Kyleg@Ksdot.org
'''

#import arcpy
from arcpy import (AddField_management, MakeFeatureLayer_management, CreateTable_management,da, 
TruncateTable_management, Append_management, MakeRouteEventLayer_lr, Delete_management, FeatureClassToFeatureClass_conversion, env)
#set the geodatabase parameters for the input route data
env.overwriteOutput = True
wsPath = r"Database Connections\shared@sqlgisprod_GIS_cansys.sde" #enter the workspace path that has the data owner login
StatefcRoutes = r"\\gisdata\arcgis\GISdata\Connection_files\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.SMLRS"
CountyfcRoutes = r"\\gisdata\arcgis\GISdata\Connection_files\RO@sqlgisprod_GIS_cansys.sde\GIS_CANSYS.SHARED.CMLRS"
StateOutTable = "SMHatch"
CountyOutTable=  "CMHatch"
StateFields = ["LRS_Route", "BEG_STATE_LOGMILE", "END_STATE_LOGMILE"]
CountyFields = ["LRS_KEY", "BEG_CNTY_LOGMILE", "END_CNTY_LOGMILE"]
#this field sets the hatch separation/spacing.  For a hatch point every 1/10 of a mile, enter 0.1.  For a hatch every 1/100th of a mile, choose 0.01.  
#for mapping in KanPlan 1/10 mile seems plenty sufficient, and will create about 108,000 points for each LRM.  
#1/100 would create 1,080,000 points which might suffer from use of in-memory processing, already this script takes a few minutes to run for each LRM 
HatchSep = 0.1
mem_point = "HatchPt"
mem_table = "HatchEvents"

countyLRM = [CountyfcRoutes, CountyOutTable, CountyFields]
stateLRM = [StatefcRoutes, StateOutTable, StateFields]
LRMethod = [countyLRM, stateLRM]

for method in LRMethod:
    print "creating hatches for " + str(method[1])
    #add route table as feature layer
    MakeFeatureLayer_management(method[0], "RouteLyr", "DIRECTION in (  1 ,  2 )")
    #create event table in memory
    mem_tbl = CreateTable_management("in_memory", mem_table)
    mem_table = r"in_memory/"+mem_table
    AddField_management(mem_table, "RouteID", "TEXT")
    AddField_management(mem_table, "LogMile", "Double")
        #add the route ID and event logmile fields
    
    #first, serach cursor through each LRS Key in the route layer
    #with da.SearchCursor("RouteLyr", (fields)) as search:  # @UndefinedVariable
    
    for row in sorted(da.SearchCursor("RouteLyr", (method[2]))): # @UndefinedVariable
        LRSKEY = row[0]
        if LRSKEY == (LRSKEY):  
            # use this loop to test the script against a single route
            iter0 = row[1]
            #print row[0]+ ' from '+str(row[1])+' to '+str(row[2])  #print the current LRS Key
            #set the begin and end parameters from which to create incremental values
            if HatchSep == 0.1:
                round_dec = 1
            elif HatchSep == 0.01:
                round_dec = 2
            else:    
                round_dec = 0
                print "check hatch separation value"
            minlog = round(row[1], round_dec)
            if minlog > row[1]:
                minlog = minlog - HatchSep
            else:
                pass
            maxlog = round(row[2], round_dec)
            if maxlog < row[2]:
                maxlog = maxlog + HatchSep
            else:
                pass
            #set the starting point for the route segment
            itermile = minlog 
            #now loop between the start and end logmiles for each route segment, and insert the step increment into the event table in memory
            while itermile <= maxlog and itermile >= minlog:
                #print str(itermile) 
                with da.InsertCursor(mem_table, ("RouteID", "LogMile")) as insert:# @UndefinedVariable
                    insertfields = [LRSKEY, itermile]
                    insert.insertRow(insertfields)
                itermile = itermile + HatchSep
            del minlog
            del maxlog
        
    MakeRouteEventLayer_lr("RouteLyr", method[2][0], mem_table, "RouteID POINT LogMile", "HatchPoints_events", "", "ERROR_FIELD", "ANGLE_FIELD", "NORMAL", "COMPLEMENT", "LEFT", "POINT")
    
    try:
        Delete_management(wsPath+'//'+method[1])
        FeatureClassToFeatureClass_conversion("HatchPoints_events", wsPath, method[1], "LOC_ERROR = 'NO ERROR'")
    except:
        TruncateTable_management(wsPath+'//'+method[1])
        Append_management("HatchPoints_events", wsPath+'//'+method[1])
    cleanup = [mem_table, "RouteLyr", "HatchPoints_events"]
    for layer in cleanup:
        Delete_management(layer)