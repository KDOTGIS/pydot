'''
Created on May 11, 2015

list feature classes in the output and apply read only privledges to all feature classes

@author: kyleadm
'''

from arcpy import ListFeatureClasses, ChangePrivileges_management, env

from EXOR_GIS_CONFIG import OpEnvironment

#from the config, import the workspace variables for which to operate this script        
OpRunOut = OpEnvironment.GIS_TARGET_CONN_DEV
adm = OpEnvironment.GIS_TARGET_CONN_DEV_ADMIN

def AddROPrivs(OpRunOut):
    env.workspace = OpRunOut
    env.overwriteOutput = True
    print OpRunOut
    DissolvedFCList = ListFeatureClasses()
    for FC in DissolvedFCList:
        print FC
        ChangePrivileges_management(FC, "readonly", "GRANT", "AS_IS")

if __name__== "__main__":
    AddROPrivs(OpRunOut)