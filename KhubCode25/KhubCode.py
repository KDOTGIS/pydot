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
    KhubCode25.KhubUpdateLRSKeyFields()
    KhubCode25.KhubCalibrateSourceToControl()
    KhubCode25.KhubUpdateFileGDB()
    KhubCode25.KhubShareProProject()
    
if __name__ == '__main__':
    pass