'''
Created on Jun 25, 2012

@author: kyleg
'''
# ---------------------------------------------------------------------------
#Codewritten by KMG @ KDOT 2012-07-26
# ---------------------------------------------------------------------------


import arcpy
#import math
#import string

#Set Variables
tblBridgeData = "BridgeData"
fdBridgeData = "KS_FEET"
lyrDWBridge = "STATE_BRIDGES"
BridgeDB = "\\\\gisdata\\arcgis\\ESRI\\ArcGIS10\\pyWorkspace\\Bridge\\BridgePackage\\BridgeData.mdb"
tblFldBridKey = "BRKEY" 
tblFldStrucKey = "STR_NAME"
lyrFldStrucKey = "STR_NAME"
calcStrucKey = "'0'+!BRKEY![0:3]+'-B0'+!BRIDGE_NUMBER!"
calcBRKey = "!STR_NAME![1:4]+!STR_NAME![7:10]"
fldLyrBridBuf = "LENGTH_FT"
fldLyrBridWid = "WIDTH_FT"
ddpMapIndexPt = "BridgeIndexPt"
ddpMapIndex = "StateBridgeIndex"
ddpFldMapScale = "BridgeScale"
selLen1 = "[BridgeData_LENGTH_FT] IS NULL"
selLen2 = "[BridgeData_LENGTH_FT] IS NOT NULL"
selLen3 = "[BridgeData_LENGTH_FT] < [BridgeData_WIDTH_FT]"
calcLen2 = "!BridgeData_LENGTH_FT!"
calcLen3 = "!BridgeData_WIDTH_FT!"

arcpy.env.workspace = BridgeDB
arcpy.env.overwriteOutput = True 
#arcpy.Compact_management(BridgeDB)
print ("Workspace set to "+BridgeDB)

#add bridge Structure Name field to bridge data table
#arcpy.AddField_management(tblBridgeData, tblFldStrucKey, "TEXT", "", "", "14", "", "NULLABLE", "NON_REQUIRED", "")

#use SHARED Schema Bridges for best geometry.  Copied to Geodatabase, need to export manually from query layer, reproject in FEET, then add BRKEY 
arcpy.AddField_management(lyrDWBridge, tblFldBridKey, "TEXT", "", "", "14", "", "NULLABLE", "NON_REQUIRED", "")
#calculate BRKEY from STRUCT_NAME.  
#remove query layer prior to this step if it is called STATE_BRIDGES
arcpy.CalculateField_management(lyrDWBridge, tblFldBridKey, calcBRKey, "Python", "")

#try:
#    arcpy.CalculateField_management(tblBridgeData, tblFldStrucKey, calcStrucKey, "Python", "")
#    print ("Unique Structure ID updated")
#except (RuntimeError):
#    print "calculation problem"
#    pass

#calculate the longest dimension of the bridge in to a new field

#join shapes to data
arcpy.AddJoin_management(lyrDWBridge, lyrFldStrucKey, tblBridgeData, tblFldStrucKey)
#save in workspace
arcpy.FeatureClassToFeatureClass_conversion(lyrDWBridge, BridgeDB+"\\"+fdBridgeData, ddpMapIndexPt)
arcpy.AddField_management(ddpMapIndexPt, ddpFldMapScale, "LONG", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.SelectLayerByAttribute_management(ddpMapIndexPt, "NEW_SELECTION", selLen1)
arcpy.CalculateField_management(ddpMapIndexPt, ddpFldMapScale, '1200', "Python", "")
arcpy.SelectLayerByAttribute_management(ddpMapIndexPt, "NEW_SELECTION", selLen2)
arcpy.CalculateField_management(ddpMapIndexPt, ddpFldMapScale, calcLen2, "Python", "")
arcpy.SelectLayerByAttribute_management(ddpMapIndexPt, "NEW_SELECTION", selLen3)
arcpy.CalculateField_management(ddpMapIndexPt, ddpFldMapScale, calcLen3, "Python", "")
arcpy.SelectLayerByAttribute_management(ddpMapIndexPt, "CLEAR_SELECTION")
#buffer by the longest dimension of the bridge to create the index layer
arcpy.Buffer_analysis(ddpMapIndexPt, ddpMapIndex, ddpFldMapScale, "FULL", "ROUND", "NONE" )



