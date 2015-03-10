'''
Created on Jan 29, 2013

@author: kyleg
'''

class MyClass(object):
    '''
    classdocs
    '''
# Import arcpy module
#What city are we mapping?
import arcpy, os, datetime
CCLUpdate = "Lyons"
CCLtemplate = r"\\gisdata\ArcGIS\GISdata\MXD\templates\CCL_template_dec2012.mxd"
CClWorking = r"\\gisdata\ArcGIS\GISdata\MXD\\"+str(now.year)+str(now.month)+str(now.day)+CCLUpdate+".mxd"
arcpy.env.MResolution = 0.0005
arcpy.env.MTolerance = 0.0005  # set the M tolerance below the default 

ws = r'\\gisdata\arcgis\GISdata\KDOT\BTP\Projects\CCL'  #change this path from CANSUSTEST

now = datetime.datetime.now()
tempdb = CCLUpdate+str(now.year)+"_"+str(now.month)+"_"+str(now.day)+".gdb"
try:
    arcpy.CreateFileGDB_management(ws,tempdb)
    print 'created temp db '+ ws, tempdb
except:
    print 'temp db already exists for today as '+ str(ws) +"\"+ str(tempdb)
    pass
arcpy.env.workspace = ws
wsouttbl = ws+"\\"+tempdb


mxd = arcpy.mapping.MapDocument(CCLtemplate)
df = arcpy.mapping.ListDataFrames(mxd, "Layers")[0]
for df in arcpy.mapping.ListDataFrames(mxd):
    mxd.title = "CCL "+CCLUpdate
    mxd.saveACopy(CClWorking)
del mxd

os.startfile(CClWorking)


#    def __init__(selfparams):self
#        '''
#        Constructor

        