'''
Created on Aug 13, 2014
Truncate and Append LRS elements from the Gateway MXD to static features classes in the Gateway SQL server GEodatabase
Moved to Production on Aug 20 2014
@author: kyleg

modified on 11/25/2014 to handle metadata updating

'''


import arcpy
#Import arcpy module
import os, string
from arcpy import mapping, Append_management,TruncateTable_management, Exists, ClearWorkspaceCache_management, env, ListDatasets, ListFeatureClasses, XSLTransform_conversion, MetadataImporter_conversion, Delete_management

def RemoveGpHistory_fd(sdeconn,remove_gp_history_xslt,out_xml):
    ClearWorkspaceCache_management()
    for fd in ListDatasets():
        env.workspace = sdeconn + os.sep + fd
        for fc in arcpy.ListFeatureClasses():
            
            name_xml = out_xml + os.sep + str(fc) + ".xml"
            #Process: XSLT Transformation
            XSLTransform_conversion(sdeconn + os.sep + fd + os.sep + fc, remove_gp_history_xslt, name_xml, "")
            print "Completed xml coversion on {0} {1}".format(fd,fc)
            # Process: Metadata Importer
            MetadataImporter_conversion(name_xml,sdeconn + os.sep + fd + os.sep + fc)
            print "Imported XML on {0}".format(fc)
   
             
def RemoveGpHistory_fc(sdeconn,remove_gp_history_xslt,out_xml):
    ClearWorkspaceCache_management()
    env.workspace = sdeconn
    for fx in ListFeatureClasses():
        
        name_xml = out_xml + os.sep + str(fx) + ".xml"
        #Process: XSLT Transformation
        XSLTransform_conversion(sdeconn + os.sep + fx, remove_gp_history_xslt, name_xml, "")
        print "Completed xml coversion on {0}".format(fx)
        # Process: Metadata Importer
        MetadataImporter_conversion(name_xml,sdeconn + os.sep + fx)
        print "Imported XML on {0}".format(fx)

def TruncateAndAppend(mxd, TargetLT, TargetST):
	lyrs = mapping.ListLayers(mxd)

	print "Updating data for " +str(lyrs[0])
	TruncateTable_management(TargetST)
	Append_management(lyrs[0], TargetST, "NO_TEST", "#")

	print "Updating data for " +str(lyrs[1])
	TruncateTable_management(TargetLT)
	Append_management(lyrs[1], TargetLT, "NO_TEST", "#")
				
if __name__== "__main__":
	# Local variables:
	sdeconn = r'D:\HNTB_GATEWAY\ProductionMOT\SQL54_GATEWAY15.sde'
	env.OverwiteOutput = "True"
	mxd = mapping.MapDocument(r'D:\HNTB_GATEWAY\ProductionMOT\2014111401_GatewayExec.mxd')
	TargetLT = sdeconn+r"\Gateway2015.GATEWAY_SPATIAL.LongTermApproved"
	TargetST = sdeconn+r'\Gateway2015.Gateway_Spatial.ShortTermApproved'
	arcpy.env.workspace = sdeconn
	remove_gp_history_xslt = "D:\\Program Files (x86)\\ArcGIS\\Desktop10.1\\Metadata\\Stylesheets\\gpTools\\remove geoprocessing history.xslt"
	out_xml = "D:\\XML_out"
	if Exists(out_xml):
		Delete_management("D:/XML_out","Folder")
	os.mkdir(out_xml)
	RemoveGpHistory_fd(sdeconn,remove_gp_history_xslt,out_xml)
	RemoveGpHistory_fc(sdeconn,remove_gp_history_xslt,out_xml)
	TruncateAndAppend(mxd, TargetLT, TargetST)
