'''
Created on Jun 9, 2015

@author: kyleg
'''
from NG911_Config import currentPathSettings
from arcpy import ListWorkspaces, env, ListDatasets, ListFeatureClasses, ListTables, Exists, MakeTableView_management, DeleteRows_management, Append_management
from NGfLRSMethod import CalledUpon

def main():
    #crawlFinal()
    #Restart(), with no args will clear out the target geodatabase completely by deleting all rows in all tables
    Restart()
    #the loadfile, loadfeatureclass, and load table can be used to isolate the input datasets.  
    #to load all datasets, enter '*'

    ProcFile = '*Roadchecks*'
    ProcFeatureclass = 'RoadCenterline'
    ProcTable = 'RoadAlias'
    #ProcessFMLRS will perform tasks to prepare the NG911 data for KDOT accident geocoding and linear referencing
    #ProcessFMLRS(ProcFile, ProcFeatureclass, ProcTable)
    #LoadFinalStreets will pass the road alias and road centerline data to the target from files and features provided in the args
    LoadFinalStreets(ProcFile, ProcFeatureclass, ProcTable)
    
def LoadFinalStreets(inFile, inFeatureclass, inTable):
    LoadThis = inFeatureclass
    FromThis = inFile
    LoadTable = inTable
    targetpath = currentPathSettings.EntDB+'/'+currentPathSettings.EDBName+'.'+currentPathSettings.EDBO
    env.workspace = currentPathSettings.FinalPath
    print str(currentPathSettings.FinalPath)
    #list the file gebdatabases in the final directory
    workspace = ListWorkspaces(FromThis, "FileGDB")
    for ws in workspace:
        print ws
        env.workspace = ws
        #print the tables in the geodatabase
        tablelist = ListTables(LoadTable)
        print "tables"
        for table in tablelist:
            print "   "+table
            print "loading "+ws+"/"+table +" to "+ targetpath+table
            #CalledUpon(ws)
            #Try to load/append the rows i nthe alias table  the aggregated geodatabase
            try:
                Append_management(ws+"/"+table, targetpath+"."+table, "NO_TEST", "#" )
            except:
                print 'there was a problem loading alias table for'+ws
            
        #print the features classes stored in feature datasets
        Datasets = ListDatasets("*")
        for fd in Datasets:
            #print fd
            #print "feature classes - Polygon"
            #FCListPoly = ListFeatureClasses("*", "Polygon", fd)
            #for fc in FCListPoly:
            #    print "    "+fc
            #print "feature classes - Lines"
            FCListLine = ListFeatureClasses(LoadThis, "Polyline", fd)
            for fc in FCListLine:
                #print "    "+fc   
                print "loading "+ws+"/"+fc +" to "+ targetpath+'.'+currentPathSettings.EFD +"." + fc
                try:
                    Append_management(fc, targetpath+'.'+currentPathSettings.EFD +"/" + fc, "NO_TEST", "#" )
                except:
                    print 'there was a problem loading centerlines for'+ws
            #print "feature classes - points"
            #FCListPoint = ListFeatureClasses("*", "Point", fd)
            #for fc in FCListPoint:
            #    print "    "+fc 

    
def Restart():
    print ""
    targetpath = currentPathSettings.EntDB+'/'+currentPathSettings.EDBName+'.'+currentPathSettings.EDBO+'.'+currentPathSettings.EFD
    print targetpath
    env.workspace = targetpath
    fclist = ListFeatureClasses()
    for fc in fclist:
        print fc
        #DeleteRows_management(fc)
    targetpath = currentPathSettings.EntDB
    env.workspace = targetpath
    tablelist = ListTables()
    for table in tablelist:
        print table
        DeleteRows_management(table)

def crawlFinal():
    env.workspace = currentPathSettings.FinalPath
    print str(currentPathSettings.FinalPath)
    #list the file gebdatabases in the final directory
    workspace = ListWorkspaces("*", "FileGDB")
    for ws in workspace:
        print ws
        env.workspace = ws
        #print the tables in the geodatabase
        tablelist = ListTables()
        print "tables"
        for table in tablelist:
            print "   "+table
        #print the features classes stored in feature datasets
        Datasets = ListDatasets("*")
        for fd in Datasets:
            print fd
            print "feature classes - Polygon"
            FCListPoly = ListFeatureClasses("*", "Polygon", fd)
            for fc in FCListPoly:
                print "    "+fc
            print "feature classes - Lines"
            FCListLine = ListFeatureClasses("*", "Polyline", fd)
            for fc in FCListLine:
                print "    "+fc   
            print "feature classes - points"
            FCListPoint = ListFeatureClasses("*", "Point", fd)
            for fc in FCListPoint:
                print "    "+fc   

def ProcessFMLRS(inFile, inFeatureclass, inTable):
    LoadThis = inFeatureclass
    FromThis = inFile
    LoadTable = inTable
    targetpath = currentPathSettings.EntDB+'/'+currentPathSettings.EDBName+'.'+currentPathSettings.EDBO
    print targetpath
    env.workspace = currentPathSettings.FinalPath
    print str(currentPathSettings.FinalPath)
    #list the file gebdatabases in the final directory
    workspace = ListWorkspaces(FromThis, "FileGDB")
    for ws in workspace:
        print ws
        env.workspace = ws
        #print the tables in the geodatabase
        tablelist = ListTables(LoadTable)
        print "tables"
        for table in tablelist:
            print "   "+table
            print "loading "+ws+"/"+table +" to "+ targetpath+table
            CalledUpon(ws)

if __name__ == '__main__':
    main()