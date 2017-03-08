'''
Created on Jan 27, 2017
a test to find road centerlines that are overlapping
also extended to find road centerlines either in a dual carriageway or a sausage link configuration
dual carriageways should be attributed with singular way operations, and a travel direction
Sausage links should be isolated to one road, with the other ghosted or flagged for mileage not counted
Overlapping roads should be isolated to one road, or otherwise checked

Ideally, overlapping roadways and sausage links would be resolved 
by using a single road centerline and an alias record by the data steward or with 
KDOT will process a singular road centerline to a singular route, 
and overlaps will process to overlapping  NG911 events on the singular route of KDOT choice

 ideally start with:
  simplified lines where county boundaries have been resolved in statewide aggregation
      or else every county boundary in the aggregated layer will have overlaps
  no line segments having length of less than 10 feet
      or else false positives will appear, especially when evaluating carriageways and sausages

@author: kyleg
'''

from arcpy import MakeFeatureLayer_management, FeatureVerticesToPoints_management, SpatialJoin_analysis, FeatureClassToFeatureClass_conversion, Delete_management

#modeling this code using file geodatabase road centerlines
roadcenterlines = r'C:\temp\New File Geodatabase (2).gdb\RoadCenterlinesS3'

def FindOverlapsSausages():
    '''KDOT Checks are already simplifying lines
    technically this is an unnecessary step 
    and it is a time consuming, resource intensive process
    KDOT will run this script on lines that have already been simplified
    Data stewards are encouraged to simplify lines to improve their data quality and system performance
    using a tool or the following command, which is commented out'''
    #SimplifyLine_cartography(inroadcenterlines, ", algorithm="POINT_REMOVE", tolerance="3 Feet", error_resolving_option="RESOLVE_ERRORS", collapsed_point_option="NO_KEEP", error_checking_option="CHECK")
    
    #Check to Make sure that Shape_Length is the appropriate geometry column length in all geodatabases
    MakeFeatureLayer_management(roadcenterlines, "RoadCenterlinesS3_L10", "Shape_Length>=10")
    #test overlapping with a centerline midpoint
    FeatureVerticesToPoints_management("RoadCenterlinesS3_L10", "in_memory/RoadCenterlinesS3_L10_Mid", point_location="MID")
    #Get the count of roads within a distance of the centerline midpoint
    SpatialJoin_analysis("RoadCenterlinesS3_L10_Mid", roadcenterlines, "in_memory/ValidateOverlaps2", "JOIN_ONE_TO_ONE", "KEEP_ALL", '#', "INTERSECT", "2 Feet", "Distance")
    #return the midpoints with a count greater than 1 - indicating possible overlaps
    #output this next line into validation geodatabase and add to arcmap for user interface
    FeatureClassToFeatureClass_conversion("in_memory/ValidateOverlaps2", r"C:\temp\New File Geodatabase (2).gdb", "ValidateOverlaps",""""Join_Count" > 1""")
    #may need to dev code to test for endpoints
    #clean up in memory artifact
    Delete_management("ValidateOverlaps2")
    #In aggregated data, county boundary overlaps are expected.  It's also assumed that county bound left right should be coded correctly.  
    #the following feature layer are the most important overlaps for review
    MakeFeatureLayer_management("ValidateOverlaps", "ValidateOverlaps_Non_County_Boundary", "COUNTY_L = COUNTY_R")
    #now using same midpoints look for sausages, midpoints less than 60 feet apart, might explore different distances under 60 feet
    #it might help and also hurt to lengthen the minimum segment length to longer than 10 feet for this, test a little more
    SpatialJoin_analysis("RoadCenterlinesS3_L10_Mid", roadcenterlines, "in_memory/ValidateSausages60", "JOIN_ONE_TO_ONE", "KEEP_ALL", '#', "INTERSECT", "120 Feet", "Distance")
    
    FeatureClassToFeatureClass_conversion("in_memory/ValidateSausages60", r"C:\temp\New File Geodatabase (2).gdb", "ValidateSausages_60ft",""""Join_Count" > 1""")
    Delete_management("ValidateSausages60")
    MakeFeatureLayer_management("ValidateSausages_60ft", "ValidateSausages_Non_County_Boundary", "COUNTY_L = COUNTY_R")
    
    
def main():
    FindOverlapsSausages()
    
main()