'''
Created on Jan 10, 2013

@author: kyleg
'''

class MyClass(object):
    '''
    classdocs
    def __init__ (self):
    '''


    def __init__(self):
        '''
        Constructor
        '''
import arcpy, sys, datetime
ws = r'\\gisdata\arcgis\GISdata\KDOT\BTP\Projects\CCL'
now = datetime.datetime.now()
tempdb = "LyonCCL"+str(now.year)+"_"+str(now.month)+"_"+str(now.day)+".gdb"
try:
    arcpy.CreateFileGDB_management(ws,tempdb)
    #    arcpy.CreatePersonalGDB_management(ws,tempdb,"9.1")
    print 'created temp db '+ ws, tempdb
except:
    print 'temp db already exists for today'
    pass
arcpy.env.workspace = ws+"\\"+tempdb

        