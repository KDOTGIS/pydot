#written by Kyle 10/11/12
# Description
# Select overridden endpoint coordinates, calculate the DMS from the position coordinates, and populate the fields for KAAT

import arcpy
[End1LongDD] = "[End1LongDD]"


arcpy.SelectLayerByAttribute_management("SDE.RunwayEndpoint","NEW_SELECTION","FAA_OVERRIDE =1")

arcpy.CalculateField_management("SDE.RunwayEndpoint","TMP_DEG","Abs(Int ( [End1LongDD] ))","VB","#")
arcpy.CalculateField_management("SDE.RunwayEndpoint","TMP_MIN","Int ( ( -[TMP_DEG]+ [End1LongDD])*60)","VB","#")
arcpy.CalculateField_management("SDE.RunwayEndpoint","TMP_SEC","Round((([End1LongDD]- [TMP_DEG])*60- [TMP_MIN])*60,4)","VB","#")
#add leading 0 for Deg (Long)
arcpy.SelectLayerByAttribute_management("SDE.RunwayEndpoint","NEW_SELECTION","FAA_OVERRIDE =1 AND tmp_deg<100")
arcpy.CalculateField_management("SDE.RunwayEndpoint","TMP_DEG",""""0"&[TMP_DEG]""","VB","#")
# add the leading 0 for minutes
arcpy.SelectLayerByAttribute_management("SDE.RunwayEndpoint","NEW_SELECTION","FAA_OVERRIDE =1 AND tmp_min<10")
arcpy.CalculateField_management("SDE.RunwayEndpoint","TMP_MIN",""""0"&[TMP_MIN]""","VB","#")
#Add the leading zero for seconds
arcpy.SelectLayerByAttribute_management("SDE.RunwayEndpoint","NEW_SELECTION","FAA_OVERRIDE =1 AND tmp_sec<10")
arcpy.CalculateField_management("SDE.RunwayEndpoint","TMP_SEC",""""0"&[TMP_SEC]""","VB","#")
#pad zeros on the right: DO while len<7 loop
arcpy.CalculateField_management("SDE.RunwayEndpoint","tmp_len","Len( [TMP_SEC] )","VB","#")
arcpy.SelectLayerByAttribute_management("SDE.RunwayEndpoint","NEW_SELECTION","FAA_OVERRIDE =1 AND tmp_len<7")
arcpy.CalculateField_management("SDE.RunwayEndpoint","TMP_SEC","!TMP_SEC! +'0'","PYTHON_9.3","#")

# Populate the KDOT DMS field
arcpy.SelectLayerByAttribute_management("SDE.RunwayEndpoint","NEW_SELECTION","FAA_OVERRIDE =1")
arcpy.CalculateField_management("SDE.RunwayEndpoint","LAT_KDOT","""[TMP_DEG]&"-" & [TMP_MIN]&"-" & [TMP_SEC]&"N"""","VB","#")

arcpy.CalculateField_management("SDE.RunwayEndpoint","LNG_KDOT","""!TMP_DEG! + "-" + !TMP_MIN! + "-" + !TMP_SEC! + "W"""","PYTHON_9.3","#")