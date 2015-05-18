'''
Created on May 11, 2015

@author: kyleadm
'''
from arcpy import env, ClearWorkspaceCache_management, Exists, MetadataImporter_conversion, ListFeatureClasses, XSLTransform_conversion, Delete_management
import os
from EXOR_GIS_CONFIG import OpEnvironment
from TargetEnvironment import ChooseTargetEnv

def RemoveGpHistory_fc(remove_gp_history_xslt,out_xml, OpEnvironment):
    env.workspace = OpEnvironment.OpRunOut
    sdeconn = OpEnvironment.OpRunOut
    env.overwriteOutput = True
    print sdeconn
    ClearWorkspaceCache_management()
    for fx in ListFeatureClasses():
        try:
            name_xml = out_xml + os.sep + str(fx) + ".xml"
            #Process: XSLT Transformation
            XSLTransform_conversion(sdeconn + os.sep + fx, remove_gp_history_xslt, name_xml, "")
            print "Completed xml conversion on {0}".format(fx)
            # Process: Metadata Importer
            MetadataImporter_conversion(name_xml,sdeconn + os.sep + fx)
            print "Imported XML on {0}".format(fx)
        except:
            print "could not complete xml conversion on {0}".format(fx)

if __name__== "__main__":

    #ProdEnv = True
    #DevEnv = False
    OpEnvironmentVar = ChooseTargetEnv(OpEnvironment, False)
    remove_gp_history_xslt = "D:\\Program Files (x86)\\ArcGIS\\Desktop10.3\\Metadata\\Stylesheets\\gpTools\\remove geoprocessing history.xslt"
    out_xml = r"D:\SCHED\FME_CANSYS_TEST\Metadata_Refresh"
    if Exists(out_xml):
        Delete_management(r"D:\SCHED\FME_CANSYS_TEST\Metadata_Refresh","Folder")
        print 'folder deleted'
    os.mkdir(out_xml)
    print 'metadata folder created'
    RemoveGpHistory_fc(remove_gp_history_xslt,out_xml, OpEnvironmentVar)
    print 'gp history deleted'
