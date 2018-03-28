'''
Created on Mar 15, 2018
this script combines the individual scripts in to the appropriate run order
first update key fields
next update calibrations
next update local files and the pro project
next package and share the pro project to the online group
run 1spatial from the server.


@author: kyleg
'''
import KhubCode25.KhubUpdateLRSKeyFields
import KhubCode25.KhubCalibrateSourceToControl
import KhubCode25.KhubUpdateFileGDB
import KhubCode25.KhubShareProProject

def main():
    KhubCode25.KhubUpdateLRSKeyFields.SqlUpdateLRSKeys()
    KhubCode25.KhubCalibrateSourceToControl.StateHighwayCalibrate()
    KhubCode25.KhubCalibrateSourceToControl.CalcUsingSQLserver()
    KhubCode25.KhubUpdateFileGDB.UpdateLocalFileGDB()
    KhubCode25.KhubUpdateFileGDB.UpdateProjectDataSources()
    KhubCode25.KhubShareProProject.ShareProToOnline()
    
if __name__ == '__main__':
    pass