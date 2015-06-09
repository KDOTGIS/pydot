'''
Script will monthly copy shapefiles from KTRIPS FTP site to folder on network, and append data to KTRIPS enterprise database
checked and plaved to production in 2015-6-13 by Kyleg - changes include:
environment change from inter*modal to dedicated KTRIPS database
added function to reverse spatial join to segment routes for BI (Route Segments table)
changed all temporary processing environments from the server to "in memory" with appends to enterprise db
The KTRIPS Routes and intersection polygons were cleaned, tested, and updated in the KTRIPS database in 4/2015
All previous KTRIPS processing needs to be truncated and re-run to avoid polygons that resulted in double counts
added the FileChecker function to prevent summarized duplicates from being processed and loaded into summary tables

@author: kyleg
'''

print "main function"
from ftplib import FTP
from arcpy import (Exists, env, TruncateTable_management, GetCount_management, AddFieldDelimiters, ListFields,
                   AddJoin_management, AddIndex_management, RemoveJoin_management, Append_management,
                   Statistics_analysis, Delete_management, FeatureClassToFeatureClass_conversion,
                   AddField_management, MakeRouteEventLayer_lr, CalculateField_management, Generalize_edit,
                   MakeTableView_management, TableToTable_conversion, FeatureToPoint_management,
                   MakeFeatureLayer_management, SpatialJoin_analysis, SelectLayerByAttribute_management,
                   DeleteFeatures_management, RebuildIndexes_management,
    ListFeatureClasses)
from arcpy.da import SearchCursor  # @UnresolvedImport
#from arcpy.sa import *
import time, os


try:
    from KTRIPSconfig import repo, cansys, gdb, db, schema

    #from config_localtest import repo, ftpHost, ftpUser, ftpPass, cansys, gdb, monthdb, yeardb
except:
    print "doing it in ArcMap? Get a compiler!"
os.chdir(repo)
gdboutpath = gdb+'/'+db+"."+schema
print gdboutpath

def main():
    ShapeFileDate = RunRealTimeMode()

    #ShapeFileDate = dateOverideMode('2015', '04')
    TheMonth = ShapeFileDate[13:15]
    TheYear = ShapeFileDate[16:20]
    if TheMonth == '01':
        print str(TheMonth)+" is the month"
        print str(TheYear)+" is the Year"
        print "Since it is the first of the year, the current year will be annualized and reset"
        AnnualizeData(TheYear)
        
    else:
        print TheMonth +" is the month"
        print TheYear +" is the Year"
        
    
    FileTransfer(ShapeFileDate)
    modeler(ShapeFileDate)
    runnext = FileChecker(ShapeFileDate, gdb+r"\KTRIPS.SDE.KTRIPS_ROUTES")
    if runnext == True:
        appender_NEW(ShapeFileDate)
    else:
        print "not running Appender New"
        
    runnext = FileChecker(ShapeFileDate, gdb+r"\KTRIPS.SDE.KTRIPS_ROUTE_Segments")
    if runnext == True:
        appender_DWBI_OLD(ShapeFileDate)
    else:
        print "not running DWBI Appender"    
    
    runnext = FileChecker(ShapeFileDate, gdb+"\KTRIPS.SDE.KTRIPS_MonthlySum")
    if runnext == True:
        MonthlyStats(ShapeFileDate)
        LoadMonthlyStats(ShapeFileDate)
        AnnualStats(ShapeFileDate)
    else:
        print "not running summaries"   
    Delete_management("in_memory")
    

        
    RebuildIndexes_management(gdb, "SYSTEM", "KTRIPS.SDE.IntrCounter2014;KTRIPS.SDE.KTRIPS_MonthlySum;KTRIPS.SDE.KTRIPS_MonthlySumIntr;KTRIPS.SDE.KTRIPS_ROUTES;KTRIPS.SDE.KTRIPS_ROUTE_Segments;KTRIPS.SDE.Ktrips_Annual;KTRIPS.SDE.Ktrips_CurrentYear;KTRIPS.SDE.RouteCounter2014", "ALL")
    
def AnnualizeData(YearToAnnualize):
    annualLayer = gdb+"\KTRIPS.SDE.Ktrips_Annual"
    currentyYear = gdb+"\KTRIPS.SDE.Ktrips_CurrentYear"
    SelectYear = YearSelTest
    CalcYear = str(int(YearSelTest-1))
    YearSelTest = "TripYear = '"+SelectYear+"'"
    if Exists("Check1"):
        Delete_management("Check1")
    MakeFeatureLayer_management(annualLayer, "Check1", YearSelTest)
    CheckExistence = GetCount_management("Check1")
    print CheckExistence
    if int(str(CheckExistence)) > 0:
        print "This source file info  is already in the target feature"
        runnext = False
    elif int(str(CheckExistence)) == 0:
        print 'the information is new for this source file and will be added.'
        runnext = True
        Append_management(currentyYear, annualLayer, "NO_TEST", "#" )
        CalculateField_management(annualLayer, "TripYear", CalcYear, "PYTHON_9.3")
        TruncateTable_management(currentyYear)
    else:
        print 'something isnt working here'
    print runnext
    pass
        

def RunRealTimeMode():
    thismonth = time.strftime("%m")
    lastmonth = str(int(thismonth)-1).zfill(2)
    thisyear = time.strftime("%Y")
    lastyear = str(int(thisyear)-1)
    if thismonth == '01':
        #print lastyear
        monthlyfile = "KTRIPSRoutes-12-"+lastyear
        loadfile = lastyear+lastmonth
        fileyear = lastyear
    else:
        monthlyfile = "KTRIPSRoutes-"+lastmonth+'-'+thisyear
        fileyear = thisyear
        loadfile = thisyear+lastmonth
    filename = monthlyfile+".shp"
    print "Running dates using realtime mode"
    print filename
    return filename
    

def dateOverideMode(yearToRun, monthToRun):
    #yearToRun = '2014'
    #monthToRun = '02'
    lastmonth = monthToRun
    thisyear = yearToRun
    monthlyfile = "KTRIPSRoutes-"+lastmonth+'-'+thisyear
    fileyear = thisyear
    loadfile = thisyear+lastmonth
    filename = monthlyfile+".shp"
    print "Running dates using date override mode"
    print filename
    return filename  


def modeler(ShapeFileDate):
    env.workspace = repo
    filename1 = repo+r"/"+ShapeFileDate
    SourceFileTxt = str(ShapeFileDate.replace("-", "_"))
    print "modeling the data schema"
    if Exists(filename1):
        Generalize_edit(filename1,"60 Feet")
        AddIndex_management(filename1, "PRMT_ID", "", "NON_UNIQUE", "NON_ASCENDING")
        AddField_management(filename1, "SourceFile", "TEXT")
        AddField_management(filename1, "Tonnage", "Double")
        AddField_management(filename1, "WidthFt", "Double")
        AddField_management(filename1, "HeightFt", "Double")
        AddField_management(filename1, "LengthFt", "Double")
        MakeTableView_management(filename1,"Ton_Calc","#","#","#")
        CalculateField_management("Ton_Calc","SourceFile","'"+SourceFileTxt+"'","PYTHON_9.3","#")
        CalculateField_management("Ton_Calc", "Tonnage", "40","PYTHON_9.3","#")
        CalculateField_management("Ton_Calc","LengthFt","Round([LENGTH] /12,2)","VB","#")
        CalculateField_management("Ton_Calc","HeightFt","Round([HEIGHT] /12,2)","VB","#")
        CalculateField_management("Ton_Calc","WidthFt","Round([WIDTH] /12,2)","VB","#")
        MakeTableView_management(filename1,"ActualTon_Calc",""""GVW" >80000""","#","#")
        CalculateField_management("ActualTon_Calc", "Tonnage", "!GVW!/2000","PYTHON_9.3","#")


def appender_OLD(ShapeFileDate):
    env.workspace = repo
    filename1 = repo+r"\\"+ShapeFileDate
    enterprisedbRoutes = gdb+"\KTRIPS.SDE.KTRIPS_ROUTES"
    Append_management(filename1, enterprisedbRoutes, "NO_TEST", "#")
    '''if Exists(filename1):
        MakeTableView_management(filename1,"AppendCheck","#","#","#")
        #AddJoin_management("AppendCheck", "PRMT_ID", enterprisedbRoutes, "PRMT_ID", join_type="KEEP_COMMON")
        #recordsTest = str(GetCount_management("AppendCheck"))
        #RemoveJoin_management("AppendCheck")
        if recordsTest =='0':
            print recordsTest +" records existed, and will be appended right now"
            Append_management(filename1, enterprisedbRoutes, "NO_TEST", "#")
        else:
            print recordsTest+" records already have been appended"
    else:
        print "there was a problem, "+str(filename1) + " could not be found"
        pass'''
def appender_DWBI_OLD(ShapeFileDate):
    print "appending the modeled data"
    env.workspace = repo
    filename1 = r"DWBI_SEGS"
    #C:\Workspace\pydot\sde_connections_10.3\sde@KTRIPS_sqlgiprod.sde\KTRIPS.SDE.KTRIPS_ROUTES
    enterprisedbRoutes = gdb+r"\KTRIPS.SDE.KTRIPS_ROUTE_Segments"
    print enterprisedbRoutes
    #Append_management(filename1, enterprisedbRoutes, "NO_TEST", "#")
    if Exists(filename1):
        MakeTableView_management(filename1,"AppendCheck","#","#","#")
        AddJoin_management("AppendCheck", "PRMT_ID", enterprisedbRoutes, "PRMT_ID", join_type="KEEP_COMMON")
        recordsTest = str(GetCount_management("AppendCheck"))
        RemoveJoin_management("AppendCheck")
        if recordsTest =='0':
            print recordsTest +" of these records exist, appending now"
            Append_management(filename1, enterprisedbRoutes, "NO_TEST", "#")
        else:
            print recordsTest+" records already have been appended"
    else:
        print "there was a problem, "+str(filename1) + " could not be found"
        pass

def appender_NEW(ShapeFileDate):
    print "appending the modeled data"
    env.workspace = repo
    filename1 = repo+r"\\"+ShapeFileDate
    #C:\Workspace\pydot\sde_connections_10.3\sde@KTRIPS_sqlgiprod.sde\KTRIPS.SDE.KTRIPS_ROUTES
    enterprisedbRoutes = gdb+r"\KTRIPS.SDE.KTRIPS_ROUTES"
    print enterprisedbRoutes
    ##enterprisedbRoutes = gdb+"\KTRIPS_ROUTES"
    if Exists(filename1):
        shapeRouteDict = dict()
        # Create a searchCursor here to build a dictionary
        # of tuples from the filename1 shapefile.
        newCursor = SearchCursor(filename1, ["FID", "PRMT_ID", "LEG_NO"])
        for newRow in newCursor:
            shapeRouteDict[newRow[0]] = (newRow[1], newRow[2])
        
        try:
            del newCursor
        except:
            pass
        
        existingRouteTupleList = list()
        
        # Then, create another searchCursor here to
        # get another list of tuples from the enterprisedbRoutes
        # feature class so that you can compare the two
        # and select the routes in filename1 which
        # do not exist in enterprisedbRoutes.
        newCursor = SearchCursor(enterprisedbRoutes, ["PRMT_ID", "LEG_NO"])
        for newRow in newCursor:
            existingRouteTupleList.append(newRow)
        
        try:
            del newCursor
        except:
            pass
        
        listContainer = list()
        featureIDList = list()
        featureIDListCounter = 0
        
        # This next part is a bit difficult to follow.
        # So, here is an explanation of what it does:
        # It takes the list of the dictionary keys in
        # the shaperoutedict and uses them to retrieve
        # each tuple in the shaperoutedict. Then, it
        # compares it to the list of tuples
        # in the existingRouteTupleList.
        # If it is not found, then we need to append
        # it into the target dataset.
        # To get it in there, we'll have to select
        # the correct featureID. The featureID in question
        # is also the dictionary key for the current
        # tuple, so append that to a list.
        # If the list gets too big, our select
        # statement might fail, so we keep them
        # to a manageable size by testing and
        # incrementing the value of the featureIDListCounter.
        # The lists that get created go into a
        # bigger list that holds them, so we that
        # we can do cool stuff like
        # for list in listOfLists:
        #     for listItem in list:
        #        doThingsRelatedToEachListItem(listItem)
        
        for featureIDAsKey in shapeRouteDict.keys():
            if shapeRouteDict[featureIDAsKey] not in existingRouteTupleList and featureIDListCounter <= 998:
                featureIDList.append(featureIDAsKey)
                featureIDListCounter += 1
            elif shapeRouteDict[featureIDAsKey] not in existingRouteTupleList and featureIDListCounter > 998:
                featureIDListCounter = 0
                listContainer.append(featureIDList)
                featureIDList = list()
                featureIDList.append(featureIDAsKey)
                featureIDListCounter += 1
            else:
                pass
        
        listContainer.append(featureIDList)
        
        try:
            del shapeRouteDict, existingRouteTupleList, featureIDList
        except:
            pass
        
        print "The List Container has " + str(len(listContainer)) + " list(s) within it."
        
        shapefileAsLyr = 'loadedShapefileAsLyr'
        
        MakeFeatureLayer_management(filename1, shapefileAsLyr)
        
        # Each sublist in the container list is 
        # used to create a whereClause and select
        # from the features, then append the
        # selected features to the target feature class.
        try:
            for featureIDList in listContainer:
                if len(featureIDList) > 0:
                    selectionClause = '"FID" IN ( '
                    for featureID in featureIDList:
                        selectionClause += str(featureID) + ','
                    selectionClause = selectionClause[:-1] + ')' # Remove the last comma
                    SelectLayerByAttribute_management(shapefileAsLyr, "NEW_SELECTION", selectionClause)
                    selectionCount = GetCount_management(shapefileAsLyr)
                    if selectionCount > 0:
                        print str(selectionCount) + " new records found, and will be appended right now."
                        Append_management(shapefileAsLyr, enterprisedbRoutes, "NO_TEST", "#")
                    else:
                        pass
                # This elif is only true when nothing has been added any of the featureIDLists.
                elif len(listContainer) == 1 and len(featureIDList) == 0:
                    print "All available records have already been appended."
                else:
                    pass
        except:
            print "The selectionClause that may be causing the failure: " + selectionClause
            raise # Reraises the previous exception
    else:
        print "There was a problem. " + str(filename1) + " could not be found."
    
    try:
        del listContainer, shapefileAsLyr
    except:
        pass


def DWBIappender(ShapeFileDate):
    print "appending the modeled data"
    env.workspace = repo
    filename1 = r"DWBI_SEGS"
    #C:\Workspace\pydot\sde_connections_10.3\sde@KTRIPS_sqlgiprod.sde\KTRIPS.SDE.KTRIPS_ROUTES
    enterprisedbRoutes = gdb+r"\KTRIPS.SDE.KTRIPS_ROUTE_Segments"
    print enterprisedbRoutes
    ##enterprisedbRoutes = gdb+"\KTRIPS_ROUTES"
    if Exists(filename1):
        shapeRouteDict = dict()
        # Create a searchCursor here to build a dictionary
        # of tuples from the filename1 shapefile.
        newCursor = SearchCursor(filename1, ["OBJECTID", "PRMT_ID", "LEG_NO"])
        for newRow in newCursor:
            shapeRouteDict[newRow[0]] = (newRow[1], newRow[2])
        
        try:
            del newCursor
        except:
            pass
        
        existingRouteTupleList = list()
        
        # Then, create another searchCursor here to
        # get another list of tuples from the enterprisedbRoutes
        # feature class so that you can compare the two
        # and select the routes in filename1 which
        # do not exist in enterprisedbRoutes.
        newCursor = SearchCursor(enterprisedbRoutes, ["PRMT_ID", "LEG_NO"])
        for newRow in newCursor:
            existingRouteTupleList.append(newRow)
        
        try:
            del newCursor
        except:
            pass
        
        listContainer = list()
        featureIDList = list()
        featureIDListCounter = 0
        
        # This next part is a bit difficult to follow.
        # So, here is an explanation of what it does:
        # It takes the list of the dictionary keys in
        # the shaperoutedict and uses them to retrieve
        # each tuple in the shaperoutedict. Then, it
        # compares it to the list of tuples
        # in the existingRouteTupleList.
        # If it is not found, then we need to append
        # it into the target dataset.
        # To get it in there, we'll have to select
        # the correct featureID. The featureID in question
        # is also the dictionary key for the current
        # tuple, so append that to a list.
        # If the list gets too big, our select
        # statement might fail, so we keep them
        # to a manageable size by testing and
        # incrementing the value of the featureIDListCounter.
        # The lists that get created go into a
        # bigger list that holds them, so we that
        # we can do cool stuff like
        # for list in listOfLists:
        #     for listItem in list:
        #        doThingsRelatedToEachListItem(listItem)
        
        for featureIDAsKey in shapeRouteDict.keys():
            if shapeRouteDict[featureIDAsKey] not in existingRouteTupleList and featureIDListCounter <= 998:
                featureIDList.append(featureIDAsKey)
                featureIDListCounter += 1
            elif shapeRouteDict[featureIDAsKey] not in existingRouteTupleList and featureIDListCounter > 998:
                featureIDListCounter = 0
                listContainer.append(featureIDList)
                featureIDList = list()
                featureIDList.append(featureIDAsKey)
                featureIDListCounter += 1
            else:
                pass
        
        listContainer.append(featureIDList)
        
        try:
            del shapeRouteDict, existingRouteTupleList, featureIDList
        except:
            pass
        
        print "The DWBI Segment List Container has " + str(len(listContainer)) + " list(s) within it."
        
        shapefileAsLyr = 'loadedShapefileAsLyr'
        
        MakeTableView_management(filename1, shapefileAsLyr)
        
        # Each sublist in the container list is 
        # used to create a whereClause and select
        # from the features, then append the
        # selected features to the target feature class.
        try:
            for featureIDList in listContainer:
                if len(featureIDList) > 0:
                    selectionClause = '"OBJECTID" IN ( '
                    for featureID in featureIDList:
                        selectionClause += str(featureID) + ','
                    selectionClause = selectionClause[:-1] + ')' # Remove the last comma
                    SelectLayerByAttribute_management(shapefileAsLyr, "NEW_SELECTION", selectionClause)
                    selectionCount = GetCount_management(shapefileAsLyr)
                    if selectionCount > 0:
                        print str(selectionCount) + " new records found, and will be appended right now."
                        Append_management(shapefileAsLyr, enterprisedbRoutes, "NO_TEST", "#")
                    else:
                        pass
                # This elif is only true when nothing has been added any of the featureIDLists.
                elif len(listContainer) == 1 and len(featureIDList) == 0:
                    print "All available records have already been appended."
                else:
                    pass
        except:
            print "The selectionClause that may be causing the failure: " + selectionClause
            raise # Reraises the previous exception
    else:
        print "There was a problem. " + str(filename1) + " could not be found."
    
    try:
        del listContainer, shapefileAsLyr
    except:
        pass



def FileTransfer(ShapeFileDate):
    import os, sys
    try:
        from SECURE_FILES.KTRIPS_FTP_config import (ftpHost, ftpUser, ftpPass)
    except:
        pass
    print ftpHost, ftpPass, ftpUser
    ftp = FTP(ftpHost)                      # connect to host, default port
    ftp.login(ftpUser, ftpPass)  
    monthlyfile = ShapeFileDate[:-4]
    filename1 = repo+r"/"+ShapeFileDate                   # user, passwd @
    ftp.retrlines('LIST')                            # list directory contents
    suffixtypes = ['.dbf', '.prj','.shx', '.shp']
    for filetype in suffixtypes:
        filename1 = monthlyfile+filetype
        print filename1
        if Exists(repo+"/"+filename1):
            print "file already transferred"
            exist = "yes"
        else:
            exist = "newload"
            with open(filename1, "wb") as newfile:
                ftp.retrbinary('RETR %s' % filename1, newfile.write)
    ftp.quit()
    print "File Transfer Completed"


def MonthlyStats(ShapeFileDate):
    env.overwriteOutput = 1
    qyear = ShapeFileDate[16:20]
    qmonth = ShapeFileDate[13:15]
    print "summarizing month " + str(qmonth) + " of year " +str(qyear)
    lyrQuery = 'DATEPART("YYYY", START_DT) = '+str(qyear)+' AND DATEPART("MM", START_DT) = '+str(qmonth)
    outlyr = "KTRIPS"+str(qyear)+str(qmonth).zfill(2)
    lyr = gdboutpath+".KTRIPS_ROUTES"
    if Exists(outlyr):
        Delete_management(outlyr)
    else:
        pass
    
    MakeFeatureLayer_management(lyr, outlyr, lyrQuery)
    IntersectSum = 'in_memory/Intsum'+outlyr
    IntersectPt  = "in_memory/Intpt"+outlyr
    #TripSum = monthdb+'\Seg'+outlyr
    TripSum2 = 'in_memory\Seg'+outlyr
    BISum2 = 'in_memory\BI'+outlyr
    infc = outlyr
    #config the intersection path
    Intersections = gdb+"\KTRIPS.SDE.IntrCounter2014"
    Routes = gdb+"\KTRIPS.SDE.RouteCounter2014"
    field_mapping1='SourceFile "SourceFile" true true false 50 Text 0 0 ,Last,#,'+infc+',SourceFile,-1,-1; Tonnage "Tonnage" true true false 8 Double 0 0 ,Sum,#,'+infc+',Tonnage,-1,-1'
    SpatialJoin_analysis(Intersections,infc,IntersectSum,"JOIN_ONE_TO_ONE","KEEP_COMMON",field_mapping1,"INTERSECT","#","#")
    field_mapping2='LRS_KEY "LRS_KEY" true true false 13 Text 0 0 ,First,#,'+Routes+',LRS_KEY,-1,-1;BEG_CNTY_LOGMILE "BEG_CNTY_LOGMILE" true true false 8 Double 3 9 ,Min,#,'+Routes+',BEG_CNTY_LOGMILE,-1,-1;END_CNTY_LOGMILE "END_CNTY_LOGMILE" true true false 8 Double 3 9 ,Max,#,'+Routes+',END_CNTY_LOGMILE,-1,-1;SourceFile "SourceFile" true true false 50 Text 0 0 ,Last,#,'+infc+',SourceFile,-1,-1;Tonnage "Tonnage" true true false 8 Double 0 0 ,Sum, #,'+infc+',Tonnage,-1,-1'
    SpatialJoin_analysis(Routes,infc,TripSum2,"JOIN_ONE_TO_ONE","KEEP_COMMON",field_mapping2,"INTERSECT","#","#")
    AddField_management(TripSum2,"TonMile","DOUBLE","#","1","#","Tons Per Mile","NULLABLE","NON_REQUIRED","#")
    CalculateField_management(TripSum2,"TonMile","!Tonnage! /( !END_CNTY_LOGMILE!- !BEG_CNTY_LOGMILE!)","PYTHON_9.3","#")
    AddField_management(TripSum2,"START_DATE","DATE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    AddField_management(IntersectSum,"START_DATE","DATE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    dateexpress = "'"+qmonth +"/"+qyear+"'"
    CalculateField_management(TripSum2,"START_DATE",dateexpress,"PYTHON_9.3","#")
    CalculateField_management(IntersectSum,"START_DATE",dateexpress,"PYTHON_9.3","#")
    # Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "KTRIPS.SDE.KTRIPS_ROUTES", "KTRIPS.SDE.RouteCounter2014"
    SpatialJoin_analysis(outlyr, Routes, r"in_memory\DWBI_SEGS_SPATIAL", "JOIN_ONE_TO_MANY", "KEEP_ALL", "#", match_option="INTERSECT", search_radius="", distance_field_name="")
    MakeTableView_management(r"in_memory\DWBI_SEGS_SPATIAL", "DWBI_SEGS")
    #Delete_management(r"in_memory\DWBI_SEGS_SPATIAL")
    #Add BI segmentation here
    #SpatialJoin_analysis(Routes,infc,TripSum2,"JOIN_ONE_TO_ONE","KEEP_COMMON",field_mapping2,"INTERSECT","#","#")
    
    #outtbl = "tbl"+str(qyear)+str(qmonth).zfill(2)
    #TableToTable_conversion(TripSum2,"in_memory",outtbl,"#","#","#")
    outtbl = TripSum2
    MakeRouteEventLayer_lr(cansys,"LRS_KEY",outtbl,"LRS_KEY LINE BEG_CNTY_LOGMILE END_CNTY_LOGMILE","LRS","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
    FeatureClassToFeatureClass_conversion("LRS", "in_memory", "LRS"+str(qmonth)+str(qyear).zfill(2))
    FeatureToPoint_management(IntersectSum,IntersectPt,"CENTROID")
    print "monthly summary complete"
    #convert units for width/length/height to feet+decimals


def BuildWhereClause(table, field, value):
    """Constructs a SQL WHERE clause to select rows having the specified value
    within a given field and table."""
    # Add DBMS-specific field delimiters
    fieldDelimited = AddFieldDelimiters(table, field)
    # Determine field type
    fieldType =ListFields(table, field)[0].type
    #set the value to look for
    #expression = "KTRIPSRoutes_"+ShapeFileDate[:2]+"_"+ShapeFileDate[2:8]
    expression = value
    # Add single-quotes for string field values
    if str(fieldType) == 'String':
        expression = "'%s'" % expression
    # Format WHERE clause
    whereClause = "%s = %s" % (fieldDelimited, expression)
    return whereClause


def BuildWhereClauseLike(table, field, value):
    """Constructs a SQL WHERE clause to select rows having the specified value
    within a given field and table."""
    # Add DBMS-specific field delimiters
    fieldDelimited = AddFieldDelimiters(table, field)
    # Determine field type
    fieldType =ListFields(table, field)[0].type
    #set the value to look for
    #expression = "KTRIPSRoutes_"+ShapeFileDate[:2]+"_"+ShapeFileDate[2:8]
    expression = "%"+value+"%"
    # Add single-quotes for string field values
    if str(fieldType) == 'String':
        expression ="'%s'" % expression
    # Format WHERE clause
    whereClauseLike =  "%s like %s" % (fieldDelimited, expression)
    return whereClauseLike


def LoadMonthlyStats(ShapeFileDate):
    env.overwriteOutput = 1
    SourceFileFGB = str(ShapeFileDate[12:-4].replace("-", ""))
    SourceFileINT= SourceFileFGB[2:6]+SourceFileFGB[0:2]
    infileMonthly = "in_memory\LRS"+SourceFileFGB
    IntersectionMonthly = "in_memory\IntptKTRIPS"+SourceFileINT
    SourceFileTxt = str(ShapeFileDate[:-4].replace("-", "_"))
    MakeTableView_management(infileMonthly,"AppendCheckMo","#","#","#")
    #Config this
    enterpriseDBMonthly= gdb+"\KTRIPS.SDE.KTRIPS_MonthlySum"
    #enterpriseDBMonthly = gdb+r"\INTERMODAL.DBO.KTRIPS_MonthlySum"
    #inputfc = r"C:\input.shp"
    outputView = "AppendCheckMonthly"
    fieldname = "SourceFile"
    fieldvalue = SourceFileTxt
    whereclause = str(BuildWhereClause(enterpriseDBMonthly, fieldname, fieldvalue))
    MakeTableView_management(enterpriseDBMonthly, outputView, whereclause)
    recordsTest = str(GetCount_management(outputView))
    if recordsTest =='0':
        print recordsTest+" of these records existed and will be appended right now"
        Append_management(infileMonthly, enterpriseDBMonthly, schema_type="NO_TEST", field_mapping="#", subtype="")
        Append_management(IntersectionMonthly, enterpriseDBMonthly+"Intr", schema_type="NO_TEST", field_mapping="#", subtype="")
    else:
        print recordsTest+" records already have been appended"

   
def AnnualStats(ShapeFileDate):
    env.overwriteOutput = 1
    #SourceFileTxt = str(ShapeFileDate[12:-4].replace("-", ""))
    #infileMonthly = yeardb+r"\Kansas\LRS"+SourceFileTxt
    qyear = ShapeFileDate[16:20]
    #try:
    #    Delete_management(yeardb+"/KTRIPS_MonthlySum_Statistics")
    #    Delete_management(yeardb+"/RunningTotal")
    #except:
    #    print "nothing deleted"
    #sumfile = gdb+"\INTERMODAL.DBO.KTRIPS_MonthlySum"
    sumfile = gdb+"\KTRIPS.SDE.KTRIPS_MonthlySum"
    whereclause = str(BuildWhereClauseLike(sumfile, "SourceFile", qyear))    
    if Exists("ThisYearMonthly"):
        Delete_management("ThisYearMonthly")
    MakeFeatureLayer_management(sumfile, "ThisYearMonthly", whereclause, "#", "#")
    Statistics_analysis("ThisYearMonthly","in_memory/KTRIPS_MonthlySum_Statistics","Join_Count SUM;Tonnage SUM","LRS_KEY;BEG_CNTY_LOGMILE;END_CNTY_LOGMILE")
    AddField_management("in_memory/KTRIPS_MonthlySum_Statistics","TonMiles","DOUBLE","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    CalculateField_management("in_memory/KTRIPS_MonthlySum_Statistics","TonMiles","!SUM_Tonnage! /(!END_CNTY_LOGMILE! - !BEG_CNTY_LOGMILE!)","PYTHON_9.3","#")
    if Exists("KTRIPS_RunningTotal_CurentYear"):
        Delete_management("KTRIPS_RunningTotal_CurentYear")
    MakeRouteEventLayer_lr(cansys,"LRS_KEY","in_memory/KTRIPS_MonthlySum_Statistics","LRS_KEY LINE BEG_CNTY_LOGMILE END_CNTY_LOGMILE","KTRIPS_RunningTotal_CurentYear","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
    CurrentYrStat = gdb+"\KTRIPS.SDE.Ktrips_CurrentYear"
    TruncateTable_management(CurrentYrStat)
    Append_management("KTRIPS_RunningTotal_CurentYear", CurrentYrStat, "NO_TEST", "#", "")
    print "annual Stats have been recalculated from the latest Monthly Statistics"
    Delete_management("in_memory/KTRIPS_MonthlySum_Statistics")
    
def delForTesting():
    env.workspace = repo
    whereClause = "ObjectID = 91783"
    enterprisedbRoutes = gdb+"\INTERMODAL.DBO.KTRIPS_ROUTES"
    loadedRoutesLayer = 'routesAsLyr'
    MakeFeatureLayer_management(enterprisedbRoutes, loadedRoutesLayer, "#", "#")
    SelectLayerByAttribute_management(loadedRoutesLayer, "NEW_SELECTION", whereClause)
    currentCount = GetCount_management(loadedRoutesLayer)
    print "Selected " + str(currentCount)+ " rows to delete."
    # Probably have to disconnect users before the next part will work. =(
    if int(str(currentCount)) > 0:
        print 'Deleting selected rows...'
        DeleteFeatures_management(loadedRoutesLayer)
    else:
        print 'Will not delete as there are no rows selected.'

def FileChecker(ShapeFileDate, CheckLayer):
    #runnext = False
    SourceFileTxt = str(ShapeFileDate.replace("-", "_"))
    print ShapeFileDate
    selectdate = "Sourcefile = '"+SourceFileTxt+"'"
    print selectdate
    print CheckLayer
    if Exists("Check1"):
        Delete_management("Check1")
    try:
        MakeFeatureLayer_management(CheckLayer, "Check1", selectdate)
    except:
        MakeTableView_management(CheckLayer, "Check1", selectdate)
    CheckExistence = GetCount_management("Check1")
    print CheckExistence
    if int(str(CheckExistence)) > 0:
        print "This source file info  is already in the target feature"
        runnext = False
    elif int(str(CheckExistence)) == 0:
        print 'the information is new for this source file and will be added.'
        runnext = True
    else:
        print 'something isnt working here'
    print runnext           
    return runnext 



main()
##delForTesting()
##ShapeFileDate = dateOverideMode('2014', '01')
##appender_NEW(ShapeFileDate)