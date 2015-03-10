'''
Created on Aug 22, 2012

@author: kyleg
'''

if __name__ == '__main__':
    pass
import arcpy
LRS = "SDE.CMLRS"
ws = r"//gisdata/arcgis/GISdata/KDOT/BTP/Projects/MAPINDEX/IndexProcess.mdb/NAD83"
iCCL = "CCL_ENV"
PLSS_IN = "DW_PLSS_MV"
PLSS_1 = "PLSS"
PLSS_2 = "PLSSTR1"
cclU = "CCL_U"
cclUD = "CCL_UD"

#CCL Bounding Polygons
arcpy.MakeRouteEventLayer_lr("SDE.CMLRS","LRS_KEY","SDE.CCL_Lane","LRSKEY LINE BEGMILEPOST ENDMILEPOST","CCL_LINES","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
arcpy.MinimumBoundingGeometry_management("SDE.CCL_Lane Events","//gisdata/arcgis/GISdata/KDOT/BTP/Projects/MAPINDEX/IndexProcess.mdb/NAD83/CCL","ENVELOPE","LIST","CITYNO; ","MBG_FIELDS")
#City Limit Bounding Polygons

#Build PLSS SEctions for T&R
arcpy.env.workspace = ws

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
def Indexmaker(Inboundary, indexfield):
    arcpy.Union_analysis("CCL_ENV #;PLSSTR1 #","//gisdata/arcgis/GISdata/KDOT/BTP/Projects/MAPINDEX/IndexProcess.mdb/NAD83/CCL_U","ALL","#","GAPS")
    outpath = ws+"//"+cclUD
    arcpy.Dissolve_management(cclU,outpath,"CITYNO;MBG_Width;MBG_Length;MAPINDEX;MAP_TYPE","TWP_NO MIN;TWP_NO MAX;RNG_NO Min;RNG_NO Max;TWP_Dir Min;TWP_Dir Max;RNG_Dir Min;RNG_Dir Max","MULTI_PART","DISSOLVE_LINES")
    arcpy.AddField_management(cclUD,"TOWNSHIP","TEXT",
                              
                              "12","#","#","#","NULLABLE","NON_REQUIRED","#")
    arcpy.AddField_management(cclUD,"RANGE","TEXT","12","#","#","#","NULLABLE","NON_REQUIRED","#")

#Calculate the Township label fields
    arcpy.SelectLayerByAttribute_management(cclUD,"NEW_SELECTION","[MIN_TWP_NO] = [MAX_TWP_NO] AND [MIN_TWP_Dir] = 2 AND [MAX_TWP_Dir]=2")
    arcpy.CalculateField_management(cclUD,"TOWNSHIP",'"T."&[MIN_TWP_NO]&" S"',"VB","#")
    arcpy.SelectLayerByAttribute_management(cclUD,"NEW_SELECTION","[MIN_TWP_NO] <> [MAX_TWP_NO] AND [MIN_TWP_Dir] = 2 AND [MAX_TWP_Dir]=2")
    arcpy.CalculateField_management(cclUD,"TOWNSHIP",'"T."&[MIN_TWP_NO]&"-"&[MAX_TWP_NO]&" S"',"VB","#")
    arcpy.SelectLayerByAttribute_management(cclUD,"NEW_SELECTION","[MIN_TWP_NO] =0 AND [MAX_TWP_NO]>0 AND [MIN_TWP_Dir] = 0 AND [MAX_TWP_Dir]=2")
    arcpy.CalculateField_management(cclUD,"TOWNSHIP",'"T."&[MAX_TWP_NO]&" S"',"VB","#")
#Calculate the Range label fields
#same range & dir
    arcpy.SelectLayerByAttribute_management(cclUD,"NEW_SELECTION","[MIN_RNG_NO] = [MAX_RNG_NO] AND [MIN_RNG_Dir] = 2 AND [MAX_RNG_Dir]=2")
    arcpy.CalculateField_management(cclUD,"RANGE",'"R."&[MIN_RNG_NO]&" W"',"VB","#")
    arcpy.SelectLayerByAttribute_management(cclUD,"NEW_SELECTION","[MIN_RNG_NO] = [MAX_RNG_NO] AND [MIN_RNG_Dir] = 1 AND [MAX_RNG_Dir]=1")
    arcpy.CalculateField_management(cclUD,"RANGE",'"R."&[MIN_RNG_NO]&" E"',"VB","#")
#same range, different dir r
    arcpy.SelectLayerByAttribute_management(cclUD,"NEW_SELECTION","[MIN_RNG_NO] = [MAX_RNG_NO] AND [MIN_RNG_Dir] = 1 AND [MAX_RNG_Dir]=2")
    arcpy.CalculateField_management(cclUD,"RANGE",'"R."&[MIN_RNG_NO]&" E -"&[MAX_RNG_NO]&" W"',"VB","#")
    arcpy.SelectLayerByAttribute_management(cclUD,"NEW_SELECTION","[MIN_RNG_NO] <> [MAX_RNG_NO] AND [MIN_RNG_Dir] = 1 AND [MAX_RNG_Dir]=2")
    arcpy.CalculateField_management(cclUD,"RANGE",'"R."&[MIN_RNG_NO]&" W -"&[MAX_RNG_NO]&" E"',"VB","#") #this is wichita

#same different ranges, same range dir
    arcpy.SelectLayerByAttribute_management(cclUD,"NEW_SELECTION","[MIN_RNG_NO] <> [MAX_RNG_NO] AND [MIN_RNG_Dir] = 1 AND [MAX_RNG_Dir]=1")
    arcpy.CalculateField_management(cclUD,"RANGE",'"R."&[MIN_RNG_NO]&"-"&[MAX_RNG_NO]&" E"',"VB","#")
    arcpy.SelectLayerByAttribute_management(cclUD,"NEW_SELECTION","[MIN_RNG_NO] <> [MAX_RNG_NO] AND [MIN_RNG_Dir] = 2 AND [MAX_RNG_Dir]=2")
    arcpy.CalculateField_management(cclUD,"RANGE",'"R."&[MIN_RNG_NO]&"-"&[MAX_RNG_NO]&" W"',"VB","#")

#same different ranges with range 0, same range dir
    arcpy.SelectLayerByAttribute_management(cclUD,"NEW_SELECTION","[MIN_RNG_NO]=0 AND [MAX_RNG_NO]>0 AND [MIN_RNG_Dir] = 0 AND [MAX_RNG_Dir]=1")
    arcpy.CalculateField_management(cclUD,"RANGE",'"R."&[MAX_RNG_NO]&" E"',"VB","#")
    arcpy.SelectLayerByAttribute_management(cclUD,"NEW_SELECTION","[MIN_RNG_NO]=0 AND [MAX_RNG_NO]>0 AND [MIN_RNG_Dir] = 0 AND [MAX_RNG_Dir]=2")
    arcpy.CalculateField_management(cclUD,"RANGE",'"R."&[MAX_RNG_NO]&" W"',"VB","#")

    arcpy.SelectLayerByAttribute_management(cclUD,"NEW_SELECTION","[CITYNO]=0")

    arcpy.AddField_management(cclUD,"CountyNum","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    arcpy.AddField_management(cclUD,"County","TEXT","120","#","#","#","NULLABLE","NON_REQUIRED","#")
    arcpy.AddField_management(cclUD,"City","TEXT","120","#","#","#","NULLABLE","NON_REQUIRED","#")
    arcpy.AddField_management(cclUD,"District","TEXT","120","#","#","#","NULLABLE","NON_REQUIRED","#")
    arcpy.AddField_management(cclUD,"Orientation","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    arcpy.AddField_management(cclUD,"Scale","LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    arcpy.AddJoin_management(cclUD,"CITYNO","SDE.DW_CITY_LIMITS_MV","CITYNUMBER","KEEP_ALL")

    arcpy.CalculateField_management(cclUD,"CCL_UD.City","!SDE.DW_CITY_LIMITS_MV.CITY!","PYTHON","#")
    arcpy.CalculateField_management(cclUD,"CCL_UD.County","!SDE.DW_CITY_LIMITS_MV.COUNTY!","PYTHON","#")
    arcpy.CalculateField_management(cclUD,"CCL_UD.District","!SDE.DW_CITY_LIMITS_MV.DIST!","PYTHON","#")

    arcpy.RemoveJoin_management(cclUD,"#")

    arcpy.DeleteField_management(cclUD,"MIN_TWP_NO;MAX_TWP_NO;MIN_RNG_NO;MAX_RNG_NO;MIN_TWP_Dir;MAX_TWP_Dir;MIN_RNG_Dir;MAX_RNG_Dir")



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