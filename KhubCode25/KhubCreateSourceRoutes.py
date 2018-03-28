'''
Created on Mar 7, 2018

@author: kyleg
'''
import datetime, time
startDateTime = datetime.datetime.now()

def createSourceRoutes123():
    from arcpy import CreateRoutes_lr, FlipLine_edit, AddField_management, FeatureClassToFeatureClass_conversion, SelectLayerByAttribute_management, CalculateField_management
    from KhubCode25.KhubCode25Config import localProFileGDBWorkspace
    
    fileformatDateStr = startDateTime.strftime("%Y%m%d")
    localfilegdb = localProFileGDBWorkspace+'\\'+'KhubRoadCenterlines'+fileformatDateStr+'.gdb'
    FeatureClassToFeatureClass_conversion(localfilegdb+"\\All_Road_Centerlines", "in_memory", "SourceRoadCenterlines123", "LRS_ROUTE_SUFFIX in ( '0' , 'A' , 'B' , 'C' , 'Y' , 'S' ) AND LRS_ROUTE_PREFIX in ( 'I' , 'K' , 'U' )")
    
    #flip backward routes
    #selecting by End less than begin mileage: 3/7/2018, 14948 routes need flipped
    #Selection by State Flip Flag = "Y" 3/7/2018, 14752 routes need flipped
    #for county_log_end < county_log_begin AND STATE_FLIP_FLAG NOT LIKE 'Y' there are 5 records, all 5 are K-14 on the mitchell/jewell county line
    #flip flag has become unreliable, do not use, just use mileage relationship

    AddField_management("SourceRoadCenterlines123", "TmpDblVal", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
    SelectLayerByAttribute_management("SourceRoadCenterlines123", "NEW_SELECTION", "county_log_end < county_log_begin")
    
    CalculateField_management("SourceRoadCenterlines123", "TmpDblVal", "!county_log_begin!", "PYTHON")
    CalculateField_management("SourceRoadCenterlines123", "county_log_begin", "!county_log_end!", "PYTHON", "")
    CalculateField_management("SourceRoadCenterlines123", "county_log_end", "!TmpDblVal!", "PYTHON", "")
    FlipLine_edit("SourceRoadCenterlines123")
    #once these lines have been flipped, we will flag them with an F in the state flip flag field
    CalculateField_management("SourceRoadCenterlines123", "STATE_FLIP_FLAG", "'F'", "PYTHON")
    


def main():

    createSourceRoutes123()

if __name__ == '__main__':
    main()
    
    pass