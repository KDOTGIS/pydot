'''
Created on Sep 11, 2016

@author: kyleg
'''

class MyClass(object):
    

    KCARS = r'Database Connections\kcarsprd_readonly.sde\KCARS.ACCIDENTS'
'''Data Type: XY Event Source
'''
def __init__(self, params):
    KCARS = r'Database Connections\kcarsprd_readonly.sde\KCARS.ACCIDENTS'
    NewLocation = r'Database Connections\CrashLocationProd.sde\crashlocation.SDE.Crashes_160511_gc_M92_47'
    '''
    
    
        Constructor
        '''
            
'''
    SDE Feature Class 
Database Platform:    SQL Server
Server:    dt00ar56
Connection Properties:    dt00ar56\gdb_prod
Authentication Type:    Database authentication
User name:    sde
Database:    crashlocation
Version:    sde.DEFAULT
Description:    Instance default version.
Feature Class:    crashlocation.SDE.Crashes_160511_gc_M92_47
Feature Type:    Simple
Geometry Type:    Point
Coordinates have Z values:    No 
    '''
        
        
'''Data Type: XY Event Source
Server: kcarsprd
User:  readonly
Instance: sde:oracle11g:kcarsprd
Table: READONLY.%ACCIDENTS
X Field: LONGITUDE
Y Field: LATITUDE
Has Object-ID Field: Yes

Geographic Coordinate System:    GCS_NAD_1983_2011
Datum:     D_NAD_1983_2011
Prime Meridian:     Greenwich
Angular Unit:     Degree
'''