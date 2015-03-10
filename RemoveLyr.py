'''
Created on Mar 21, 2012

@author: kyleg
'''

class MyClass(object):
    '''
    classdocs
    '''

#RemoveLayer - doesnt seem to work
#for df in arcpy.mapping.ListDataFrames(mxd):
#    for lyr in arcpy.mapping.ListLayers(mxd, "", df):
#        if lyr.name.lower() == "DS_*":
#            arcpy.mapping.AddLayer(df, lyr)
#mxd.save()
#arcpy.RefreshTOC()
#arcpy.RefreshActiveView()


    def __init__(selfparams):
        '''
        Constructor
        '''
        