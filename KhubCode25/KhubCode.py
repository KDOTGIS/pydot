'''
Created on Mar 15, 2018
this script combines the individual scripts in to the appropriate run order
first update key fields
next update calibrations
next update local files and the pro project
next package and share the pro project to the online group
run 1spatial from the server.
updated 3/28/2018

@author: kyleg
'''
import KhubCode25.KhubUpdateLRSKeyFields
import KhubCode25.KhubCalibrateSourceToControl
import KhubCode25.KhubUpdateFileGDB
import KhubCode25.KhubShareProProject


def CollectPasswords():
    from KhubCode25.KhubCode25Config import AGOUser
    import getpass
    username = AGOUser
    password = getpass.getpass("Enter Password for "+str(username)+":")
    print("logging in as "+username )
    dbpassword = getpass.getpass("Enter Password for SDE user on the Geodatabase:")
    return password, dbpassword

def main():
    thesecret = CollectPasswords()
    KhubCode25.KhubUpdateLRSKeyFields.SqlUpdateLRSKeys(thesecret[1])
    KhubCode25.KhubCalibrateSourceToControl.StateHighwayCalibrate()
    KhubCode25.KhubCalibrateSourceToControl.CalcUsingSQLserver(thesecret[1])
    KhubCode25.KhubUpdateFileGDB.UpdateLocalFileGDB()
    KhubCode25.KhubUpdateFileGDB.UpdateProjectDataSources()
    KhubCode25.KhubShareProProject.ShareProToOnline(thesecret[0])
    print ("all done")
    
main()
    
if __name__ == '__main__':
    pass