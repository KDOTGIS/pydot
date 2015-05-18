'''
Created on May 12, 2015
This script calls functions from the other scripts and executes them in-line
To run this script in Development, the OpEnvironmentVar = ChooseTargetEnv(OpEnvironment, False)
To run this script in Production, the OpEnvironmentVar = ChooseTargetEnv(OpEnvironment, True)
As of this date  May 12, 2015 the source environment (geodatabases from FME) is the same for DEV and PROD
The Production environment will be the SQLGISPROD geodatabase
Moving to production will require inspection of services already published to ArcGIS server

@author: kyleadm
'''

from EXOR_GIS_CONFIG import OpEnvironment
from TargetEnvironment import ChooseTargetEnv
from EXOR_Process_Routes import MakeRouteLayers
from EXOR_Process_Dir import DissolveDirectionalItems
from EXOR_Process_DirXSP import DissolveXSPItems
from EXOR_Process_AllDir import DissolveNonDirectionalItems

#ProdEnv = True
#DevEnv = False

if __name__ == '__main__':
    OpEnvironmentVar = ChooseTargetEnv(OpEnvironment, True)
    
    #the mode Operational Environment Variable is returned from the function, and passed to these functions
    
    MakeRouteLayers(OpEnvironmentVar)
    DissolveDirectionalItems(OpEnvironmentVar)
    DissolveXSPItems(OpEnvironmentVar)
    DissolveNonDirectionalItems(OpEnvironmentVar)
    
    
    