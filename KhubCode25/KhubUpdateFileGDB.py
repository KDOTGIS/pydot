'''
Created on Mar 6, 2018
The script creates a new file geodatabase in ArcGIS Pro from the data in dt00ar58 - roads
Then, it updates the file sources in the master project to use that new file geodatabase
after running this, you can run the scipt "Share Pro Project" to package and share the project and file geodatabase to the QAQC group
@author: kyleg
'''

def UpdateLocalFileGDB():
    import datetime, time
    fDateTime = datetime.datetime.now()
    from arcpy import FeatureClassToFeatureClass_conversion, CreateFileGDB_management, Exists, Delete_management
    from KhubCode25.KhubCode25Config import (
    localProProjectPath, localProFileGDBWorkspace, prodDataSourceSDE, devDataSourceSDE, dbname, dbownername, countylines, devorprod)
    if devorprod == 'prod':
        database = prodDataSourceSDE
        print("running on "+devorprod)
    else: 
        database = devDataSourceSDE
        print("running on "+devorprod)
    fileformatDateStr = fDateTime.strftime("%Y%m%d")
    localfilegdb = localProFileGDBWorkspace+'\\'+'KhubRoadCenterlines'+fileformatDateStr+'.gdb'
    #print(fileformatDateStr)
    if Exists(localfilegdb):
        print(localfilegdb +" exists and will be deleted")
        Delete_management(localfilegdb)
        time.sleep(1)
    CreateFileGDB_management(localProFileGDBWorkspace, "KhubRoadCenterlines"+fileformatDateStr, "CURRENT")
    FeatureClassesUsed = ['All_Road_Centerlines', 'All_Road_Centerlines_D1', 'MARKUP_POINT', 'All_Roads_Stitch_Points', 'Videolog_CURRENT_LANETRACE', 'Videolog_CURRENT_RAMPTRACE', 'HPMS_RAMPS']
    for FeatureClass in FeatureClassesUsed:
        loopFC = localProProjectPath+'/'+database+"/"+dbname+"."+dbownername+"."+FeatureClass
        FeatureClassToFeatureClass_conversion(loopFC, localfilegdb, FeatureClass)
    FeatureClassToFeatureClass_conversion(localProProjectPath+'/'+countylines, localfilegdb, "SHARED_COUNTY_LINES")
    
def UpdateProjectDataSources():
    import datetime
    from KhubCode25.KhubCode25Config import localProProjectPath, localProProjectName, localProFileGDBWorkspace
    from arcpy import mp
    fDateTime = datetime.datetime.now()
    fileformatDateStr = fDateTime.strftime("%Y%m%d")
    localfilegdb = localProFileGDBWorkspace+'\\'+'KhubRoadCenterlines'+fileformatDateStr+'.gdb'
    aprx = mp.ArcGISProject(localProProjectPath+'/'+localProProjectName)
    LocalMaps = aprx.listMaps("1SpatialLocal*")
    for Localmap in LocalMaps:
        #print(Localmap)
        lyrlist =  Localmap.listLayers("*")
        #for layer in lyrlist:
            #conprops= layer.connectionProperties
            #if conprops != None:
                #print(conprops)
        #use the first layer to as the file geodatabase name to update the source file geodatabse for each local map
        conprops = (lyrlist[0].connectionProperties)      
        #print(conprops)
        #print(conprops['connection_info']['database'])  
        firstdb = conprops['connection_info']['database']
        aprx.updateConnectionProperties(firstdb, localfilegdb)
    aprx.save()

def main():
    import datetime
    startDateTime = datetime.datetime.now()
    print("File update started at "+ str(startDateTime)+ ", it usually takes about 5 minutes")
    UpdateLocalFileGDB()
    UpdateProjectDataSources()
    print('program executed in {} hours, minutes, seconds.'.format(datetime.datetime.now()-startDateTime))
    print("but that time calculation seems way off for this script")
    
if __name__ == '__main__':
    #formattedDateStr = startDateTime.strftime("%m-%d-%Y")
    main()
    #print(datetime.datetime.now())

else:
    print("Functions from KhubFileGDB imported to main script")
    #this take usually takes about 5-7 minutes to complete.
