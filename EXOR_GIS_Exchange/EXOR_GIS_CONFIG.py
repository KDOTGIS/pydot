'''
Created on May 7, 2015

The Configuration file for EXOR to GIS operations
FME Batch Files export spatial and non-spatial views to several geodatabases in a directory of AR60 D:/SCHED
This config class defines the target source and operational parameters for several other functions to process the info FME extracts from EXOR
By dividing the processes in FME and Python we can take advantage of multiple simultaneous processes to expedite the data transfer operations
 
@author: kyleadm
'''

class EXOR_CONFIG(object):
    '''
    This class describes the parameters, sources, and targets for the EXOR to GIS operations
    
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.FME_NET = r"D:\SCHED\FME_CANSYS_TEST\FME_NET.gdb"
        self.FME_ITEM_SUM = r"D:\SCHED\FME_CANSYS_TEST\FME_ITEM_SUM.gdb"
        self.FME_ITEM_DIRSUM = r"D:\SCHED\FME_CANSYS_TEST\FME_ITEM_DIRSUM.gdb"
        self.FME_ITEM_DIRXSP = r"D:\SCHED\FME_CANSYS_TEST\FME_ITEM_DIRXSP.gdb"
        self.GIS_TARGET_CONN_DEV = r"D:\SCHED\shared@GIS_CANSYS_TEST.sde"
        self.GIS_TARGET_CONN_PROD = r"D:\SCHED\shared@sqlprod_GIS_CANSYS.sde"
        self.GIS_TARGET_CONN_DEV_ADMIN = r"D:\SCHED\sde@GIS_CANSYS_TEST.sde"
        self.GIS_TARGET_CONN_PROD_ADMIN = r"D:\SCHED\sde@sqlprod_GIS_CANSYS.sde"
        self.GIS_TARGET_DB_OWNER_DEV = "SHARED"
        self.GIS_TARGET_DB_OWNER_PROD = "SHARED"
        self.GIS_TARGET_DB_DEV = "CANSYS_GIS_DEV"
        self.GIS_TARGET_DB_PROD = "GIS_CANSYS"
        
        
OpEnvironment = EXOR_CONFIG()