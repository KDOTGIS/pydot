'''
Created on Jan 14, 2014

@author: kyleg
'''
'''
Created on Aug 22, 2012
add PLSS township and range to polygon layers so they can be dynamic labels with DDP indexes 
@author: kyleg
'''

if __name__ == '__main__':
    pass
import arcpy
ws = r"//gisdata/arcgis/GISdata/KDOT/BTP/Projects/MAPINDEX/IndexProcess.mdb/KSLAM"
PLSS_IN = "DW_PLSS_MV"
PLSS_1 = "PLSS"
PLSS_2 = "PLSSTR1"
BndU = "Bnd_U"
BndUD = "Bnd_UD"
BndLyr = "CCL_ENV"
BndIndx = "CITYNO"
BndEnv = "CCL_ENV"
arcpy.env.overwriteOutput = True 


#Bnd Bounding Polygons
#arcpy.MakeRouteEventLayer_lr("SDE.CMLRS","LRS_KEY","SDE.Bnd_Lane","LRSKEY LINE BEGMILEPOST ENDMILEPOST","Bnd_LINES","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
arcpy.MinimumBoundingGeometry_management(BndLyr,BndEnv,"ENVELOPE","LIST",BndIndx,"MBG_FIELDS")
#City Limit Bounding Polygons

#Build PLSS SEctions for T&R
arcpy.env.workspace = ws
if arcpy.Exists(PLSS_1):
    print ("Using "+ PLSS_1 +" to merge township and range")
else:
    print ("MAking the Township and Range dissolve from PLSS")
    arcpy.FeatureClassToFeatureClass_conversion(PLSS_IN,ws,PLSS_1,"#","#")
    arcpy.Dissolve_management(PLSS_1,ws+"//"+PLSS_2,"TOWNSHIP;RANGE","#","MULTI_PART","DISSOLVE_LINES")
    arcpy.AddField_management(PLSS_2,"TWP_NO","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    arcpy.AddField_management(PLSS_2,"RNG_NO","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    arcpy.AddField_management(PLSS_2,"TWP_Dir","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    arcpy.AddField_management(PLSS_2,"RNG_Dir","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    arcpy.CalculateField_management(PLSS_2,"TWP_NO","Left([TOWNSHIP],2)","VB","#")
    arcpy.CalculateField_management(PLSS_2,"RNG_NO","Left([RANGE],2)","VB","#")
    arcpy.SelectLayerByAttribute_management(PLSS_2,"NEW_SELECTION","[TOWNSHIP] LIKE '*S'")
    arcpy.CalculateField_management(PLSS_2,"TWP_Dir","2","VB","#")
    arcpy.SelectLayerByAttribute_management(PLSS_2,"NEW_SELECTION","[TOWNSHIP] LIKE '*N'")
    arcpy.CalculateField_management(PLSS_2,"TWP_Dir","1","VB","#")
    arcpy.SelectLayerByAttribute_management(PLSS_2,"NEW_SELECTION","[RANGE] LIKE '*W'")
    arcpy.CalculateField_management(PLSS_2,"RNG_Dir","2","VB","#")
    arcpy.SelectLayerByAttribute_management(PLSS_2,"NEW_SELECTION","[RANGE] LIKE '*E'")
    arcpy.CalculateField_management(PLSS_2,"RNG_Dir","1","VB","#")
    arcpy.SelectLayerByAttribute_management(PLSS_2,"CLEAR_SELECTION")


#start thje union/dissolve/calculate as a function to add Township and Range info to index table
#def Indexmaker(Inboundary, indexfield):
arcpy.Union_analysis([BndEnv, PLSS_2],BndU,"ALL","#","GAPS")
# arcpy.SelectLayerByAttribute_management(BndU, "NEW_SELECTION","[FID_PLSSTR1] =-1") DOES NOT APPLY TO CCL
# arcpy.DeleteFeatures_management(BndU)

outpath = ws+"//"+BndUD
arcpy.Dissolve_management(BndU,outpath,BndIndx+";MBG_Width;MBG_Length","TWP_NO MIN;TWP_NO MAX;RNG_NO Min;RNG_NO Max;RNG_Dir Mean; TWP_Dir Min;TWP_Dir Max;RNG_Dir Min;RNG_Dir Max","MULTI_PART","DISSOLVE_LINES")
arcpy.AddField_management(BndUD,"TOWNSHIP","TEXT","12","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(BndUD,"RANGE","TEXT","12","#","#","#","NULLABLE","NON_REQUIRED","#")

#Calculate the Township label fields
arcpy.SelectLayerByAttribute_management(BndUD,"NEW_SELECTION","[MIN_TWP_NO] = [MAX_TWP_NO] AND [MIN_TWP_Dir] = 2 AND [MAX_TWP_Dir]=2")
arcpy.CalculateField_management(BndUD,"TOWNSHIP",'"T."&[MIN_TWP_NO]&" S"',"VB","#")
arcpy.SelectLayerByAttribute_management(BndUD,"NEW_SELECTION","[MIN_TWP_NO] <> [MAX_TWP_NO] AND [MIN_TWP_Dir] = 2 AND [MAX_TWP_Dir]=2")
arcpy.CalculateField_management(BndUD,"TOWNSHIP",'"T."&[MIN_TWP_NO]&"-"&[MAX_TWP_NO]&" S"',"VB","#")
arcpy.SelectLayerByAttribute_management(BndUD,"NEW_SELECTION","[MIN_TWP_NO] =0 AND [MAX_TWP_NO]>0 AND [MIN_TWP_Dir] = 0 AND [MAX_TWP_Dir]=2")
arcpy.CalculateField_management(BndUD,"TOWNSHIP",'"T."&[MAX_TWP_NO]&" S"',"VB","#")
#Calculate the Range label fields
#same range & dir
arcpy.SelectLayerByAttribute_management(BndUD,"NEW_SELECTION","[MIN_RNG_NO] = [MAX_RNG_NO] AND [MIN_RNG_Dir] = 2 AND [MAX_RNG_Dir]=2")
arcpy.CalculateField_management(BndUD,"RANGE",'"R."&[MIN_RNG_NO]&" W"',"VB","#")
arcpy.SelectLayerByAttribute_management(BndUD,"NEW_SELECTION","[MIN_RNG_NO] = [MAX_RNG_NO] AND [MIN_RNG_Dir] = 1 AND [MAX_RNG_Dir]=1")
arcpy.CalculateField_management(BndUD,"RANGE",'"R."&[MIN_RNG_NO]&" E"',"VB","#")
#same range, different dir r
arcpy.SelectLayerByAttribute_management(BndUD,"NEW_SELECTION","[MIN_RNG_NO] = [MAX_RNG_NO] AND [MIN_RNG_Dir] = 1 AND [MAX_RNG_Dir]=2")
arcpy.CalculateField_management(BndUD,"RANGE",'"R."&[MIN_RNG_NO]&" E -"&[MAX_RNG_NO]&" W"',"VB","#")
arcpy.SelectLayerByAttribute_management(BndUD,"NEW_SELECTION","[MIN_RNG_NO] <> [MAX_RNG_NO] AND [MIN_RNG_Dir] = 1 AND [MAX_RNG_Dir]=2 AND [MEAN_RNG_DIR]<1.5")
arcpy.CalculateField_management(BndUD,"RANGE",'"R."&[MIN_RNG_NO]&" W -"&[MAX_RNG_NO]&" E"',"VB","#") #this does wichita for city conn link
arcpy.SelectLayerByAttribute_management(BndUD,"NEW_SELECTION","[MIN_RNG_NO] <> [MAX_RNG_NO] AND [MIN_RNG_Dir] = 1 AND [MAX_RNG_Dir]=2 AND [MEAN_RNG_DIR]>1.5")
arcpy.CalculateField_management(BndUD,"RANGE",'"R."&[MIN_RNG_NO]&" E -"&[MAX_RNG_NO]&" W"',"VB","#") #this does wichita for city conn link

#harvey, cloud, McPherson, Ottawa, Republic, Saline, 

#same different ranges, same range dir
arcpy.SelectLayerByAttribute_management(BndUD,"NEW_SELECTION","[MIN_RNG_NO] <> [MAX_RNG_NO] AND [MIN_RNG_Dir] = 1 AND [MAX_RNG_Dir]=1")
arcpy.CalculateField_management(BndUD,"RANGE",'"R."&[MIN_RNG_NO]&"-"&[MAX_RNG_NO]&" E"',"VB","#")
arcpy.SelectLayerByAttribute_management(BndUD,"NEW_SELECTION","[MIN_RNG_NO] <> [MAX_RNG_NO] AND [MIN_RNG_Dir] = 2 AND [MAX_RNG_Dir]=2")
arcpy.CalculateField_management(BndUD,"RANGE",'"R."&[MIN_RNG_NO]&"-"&[MAX_RNG_NO]&" W"',"VB","#")

#same different ranges with range 0, same range dir
arcpy.SelectLayerByAttribute_management(BndUD,"NEW_SELECTION","[MIN_RNG_NO]=0 AND [MAX_RNG_NO]>0 AND [MIN_RNG_Dir] = 0 AND [MAX_RNG_Dir]=1")
arcpy.CalculateField_management(BndUD,"RANGE",'"R."&[MAX_RNG_NO]&" E"',"VB","#")
arcpy.SelectLayerByAttribute_management(BndUD,"NEW_SELECTION","[MIN_RNG_NO]=0 AND [MAX_RNG_NO]>0 AND [MIN_RNG_Dir] = 0 AND [MAX_RNG_Dir]=2")
arcpy.CalculateField_management(BndUD,"RANGE",'"R."&[MAX_RNG_NO]&" W"',"VB","#")

arcpy.SelectLayerByAttribute_management(BndUD,"NEW_SELECTION",BndIndx+"=0")
arcpy.DeleteFeatures_management(BndUD)


#if BndUD = "City":
#    arcpy.AddField_management(BndUD,"City","TEXT","120","#","#","#","NULLABLE","NON_REQUIRED","#")
#else:
#    print ("going ahead")
arcpy.AddField_management(BndUD,"CountyNum","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(BndUD,"City","TEXT","120","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(BndUD,"County","TEXT","120","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(BndUD,"District","TEXT","120","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(BndUD,"County_Abbr","TEXT","4","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(BndUD,"Orientation","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddField_management(BndUD,"Scale","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.AddJoin_management(BndUD,BndIndx,BndLyr,BndIndx,"KEEP_ALL")
#CCL ENV has no useful info, need to join it to CITY_LIMITS for next steps


#county
#arcpy.CalculateField_management(BndUD,"Bnd_UD.City","!SDE.DW_CITY_LIMITS_MV.CITY!","PYTHON","#")
arcpy.CalculateField_management(BndUD, BndUD+".CountyNum", "!SDE."+BndLyr+".COUNTY_NUMBER!","PYTHON","#")
arcpy.CalculateField_management(BndUD, BndUD+".County", "!SDE."+BndLyr+".COUNTY_NAME!","PYTHON","#")
arcpy.CalculateField_management(BndUD, BndUD+".District","!SDE."+BndLyr+".DISTRICT!","PYTHON","#")
arcpy.CalculateField_management(BndUD, BndUD+".County_Abbr","!SDE."+BndLyr+".COUNTY_ABBR!","PYTHON","#")
arcpy.CalculateField_management(BndUD, BndUD+".CountyNum", "!SDE."+BndLyr+".COUNTY_NUMBER!","PYTHON","#")

arcpy.RemoveJoin_management(BndUD,"SDE."+BndLyr)

arcpy.DeleteField_management(BndUD,"MIN_TWP_NO;MAX_TWP_NO;MIN_RNG_NO;MAX_RNG_NO;MIN_TWP_Dir;MAX_TWP_Dir;MIN_RNG_Dir;MAX_RNG_Dir;MEAN_RNG_Dir")

#CITY LIMITS
arcpy.MinimumBoundingGeometry_management("SDE.SDE.CITY_LIMITS","//gisdata/arcgis/GISdata/KDOT/BTP/Projects/MAPINDEX/IndexProcess.mdb/NAD83/CITYLIM","ENVELOPE","LIST","CITYNO","MBG_FIELDS")

#UAB Bounding Polygons
arcpy.MinimumBoundingGeometry_management("SDE.SDE.URBAN_BOUNDARIES","//gisdata/arcgis/GISdata/KDOT/BTP/Projects/MAPINDEX/IndexProcess.mdb/NAD83/UAB","ENVELOPE","LIST","CITYNO","MBG_FIELDS")
#County Limit Bounding Polygons
arcpy.MinimumBoundingGeometry_management("SDE.SDE.URBAN_BOUNDARIES","//gisdata/arcgis/GISdata/KDOT/BTP/Projects/MAPINDEX/IndexProcess.mdb/NAD83/CITYLIM","ENVELOPE","LIST","CITYNO","MBG_FIELDS")
#SubArea Bounding Polygons
arcpy.MinimumBoundingGeometry_management("SDE.SDE.URBAN_BOUNDARIES","//gisdata/arcgis/GISdata/KDOT/BTP/Projects/MAPINDEX/IndexProcess.mdb/NAD83/cOUNTYlIM","ENVELOPE","LIST","CITYNO","MBG_FIELDS")
#SNICE_Area Bounding Polygons

#DISTRICT Bounding Polygons

#assemble bounding polygons into map index

#create Quads and Quarter Quad Grids that match the FAA Sectionals
arcpy.GridIndexFeatures_cartography("F:/Cart/projects/Graticule/MKC15.shp","#","NO_INTERSECTFEATURE","NO_USEPAGEUNIT","#","0.25 DecimalDegrees","0.25 DecimalDegrees","-97 36","16","28","1","NO_LABELFROMORIGIN")
arcpy.GridIndexFeatures_cartography("F:/Cart/projects/Graticule/ICT15.shp","#","NO_INTERSECTFEATURE","NO_USEPAGEUNIT","#","0.25 DecimalDegrees","0.25 DecimalDegrees","-104 36","16","28","1","NO_LABELFROMORIGIN")
arcpy.GridIndexFeatures_cartography("F:/Cart/projects/Graticule/ICT75.shp","#","NO_INTERSECTFEATURE","NO_USEPAGEUNIT","#","0.125 DecimalDegrees","0.125 DecimalDegrees","-104 36","32","56","1","NO_LABELFROMORIGIN")
arcpy.GridIndexFeatures_cartography("F:/Cart/projects/Graticule/MKC75.shp","#","NO_INTERSECTFEATURE","NO_USEPAGEUNIT","#","0.125 DecimalDegrees","0.125 DecimalDegrees","-97 36","32","56","1","NO_LABELFROMORIGIN")