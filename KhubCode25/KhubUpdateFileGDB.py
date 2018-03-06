'''
Created on Mar 6, 2018
this script creates a new file geodatabase in ArcGIS Pro from the data in dt00ar68 - roads
@author: kyleg
'''

import datetime, time
from KhubCode25.KhubCode25Config import countylines
startDateTime = datetime.datetime.now()
#print(currentDateTime)
#formattedDateStr = startDateTime.strftime("%m-%d-%Y")

def UpdateLocalFileGDB():
    from arcpy import FeatureClassToFeatureClass_conversion, CreateFileGDB_management, Exists, Delete_management
    from KhubCode25.KhubCode25Config import (
    localProProjectPath, 
    localProFileGDBWorkspace, 
    prodDataSourceSDE, 
    devDataSourceSDE, 
    dbname, 
    dbownername, 
    countylines)
    fileformatDateStr = startDateTime.strftime("%Y%m%d")
    localfilegdb = localProFileGDBWorkspace+'\\'+'KhubRoadCenterlines'+fileformatDateStr+'.gdb'
    #print(fileformatDateStr)
    if Exists(localfilegdb):
        print(localfilegdb +" exists and will be deleted")
        Delete_management(localfilegdb)
        time.sleep(1)
    CreateFileGDB_management(localProFileGDBWorkspace, "KhubRoadCenterlines"+fileformatDateStr, "CURRENT")
    FeatureClassesFromProd = ['All_Road_Centerlines', 'All_Roads_Stitch_Points', 'Videolog_CURRENT_LANETRACE', 'Videolog_CURRENT_RAMPTRACE', 'HPMS_RAMPS']
    for FeatureClass in FeatureClassesFromProd:
        loopFC = localProProjectPath+'/'+prodDataSourceSDE+"/"+dbname+"."+dbownername+"."+FeatureClass
        FeatureClassToFeatureClass_conversion(loopFC, localfilegdb, FeatureClass)
    FeatureClassToFeatureClass_conversion(localProProjectPath+'/'+countylines, localfilegdb, "Shared_County_Lines")
    
def UpdateProjectDataSources():
    from KhubCode25.KhubCode25Config import localProProjectPath, localProProjectName, localProFileGDBWorkspace
    from arcpy import mp
    fileformatDateStr = startDateTime.strftime("%Y%m%d")
    localfilegdb = localProFileGDBWorkspace+'\\'+'KhubRoadCenterlines'+fileformatDateStr+'.gdb'
    aprx = mp.ArcGISProject(localProProjectPath+'/'+localProProjectName)
    LocalMaps = aprx.listMaps("1SpatialLocal*")
    for Localmap in LocalMaps:
        print(Localmap)
        lyrlist =  Localmap.listLayers("*")
        #for layer in lyrlist:
            #conprops= layer.connectionProperties
            #if conprops != None:
                #print(conprops)
        #use the first layer to as the file geodatabase name to update the source file geodatabse for each local map
        conprops = (lyrlist[0].connectionProperties)      
        print(conprops)
        print(conprops['connection_info']['database'])  
        firstdb = conprops['connection_info']['database']
        aprx.updateConnectionProperties(firstdb, localfilegdb)
        
    aprx.save()

def main():
    #UpdateLocalFileGDB()
    UpdateProjectDataSources()
    
if __name__ == '__main__':
    #print(datetime.datetime.now())
    #print("this is the main section")
    main()
    #print(datetime.datetime.now())
    print('program executed in {} hours, minutes, seconds.'.format(datetime.datetime.now()-startDateTime))
else:
    print("this is the else section")
