'''
Created on Feb 9, 2017

#select a county in the map

@author: kyleg
'''

if __name__ == '__main__':
    pass

import arcpy
from arcpy.management import SelectLayerByLocation as SELECT, CopyFeatures as COPY, CalculateField as CALCULATE
'''   '''
localpath = r"C:\Users\kyleg\Documents\ArcGIS\Projects\RailCrossing1.4.1"
tempdb = "Staging_Workforce_Assignments"
def LocalStagingDatabase():
    #CreateFileGDB(localpath, tempdb, "CURRENT")
    SelectLayerByLocation("RailCrossing", "WITHIN", "SHARED.COUNTIES", None, "NEW_SELECTION", "NOT_INVERT")
    CalculateField("Assignments_Staging", "status", 1, "PYTHON_9.3", None)
    
    



def pyversion():
    #this script requires arcgis pro librarires of python 3.5x, which run from conda
    import sys
    print (sys.version)
        
def main():
    pyversion()
    
    