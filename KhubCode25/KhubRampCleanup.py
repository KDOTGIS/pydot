'''
Created on Mar 8, 2018

@author: kyleg
'''
arcpy.Buffer_analysis(in_features="Videolog_CURRENT_RAMPTRACE", out_feature_class="in_memory/Videolog_CURRENT_RAMPTRACE_B", buffer_distance_or_field="24 Feet", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field="", method="PLANAR")
arcpy.Buffer_analysis(in_features="HPMS_RAMPS", out_feature_class="in_memory/HPMS_RAMP_B", buffer_distance_or_field="24 Feet", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field="", method="PLANAR")
arcpy.Merge_management(inputs="HPMS_RAMP_B;Videolog_CURRENT_RAMPTRACE_B", output="in_memory/HPMS_videolog_rampmerge")
#the result of the merge is all buffered ramp geometyry from the two ramp sources.
#the select by location input source is all road centerliens having source route prefix = x
#the selection settings should provide the result of all ramp segments not intersecting the merge buffer
arcpy.SelectLayerByLocation_management(in_layer="source_X_ramps", overlap_type="INTERSECT", select_features="HPMS_videolog_rampmerge", search_distance="", selection_type="NEW_SELECTION", invert_spatial_relationship="INVERT")
#resulting selection set has 542 segments
#34 of these segments have a source LRS Key.  I reviewed most of them and they look like legit ramps.  
arcpy.SelectLayerByAttribute_management(in_layer_or_view="source_X_ramps", selection_type="REMOVE_FROM_SELECTION", where_clause="KDOT_LRS_KEY is not null")
#508 segments remain
#INT_VAL field populated to "-X"
#note 0 null int val codes should be calculated to "" - no character.
arcpy.CalculateField_management(in_table="source_X_ramps", field="INT_VAL", expression="""[INT_VAL]+"-X"""", expression_type="VB", code_block="")
#only 471 fields were calcualted with -X, the feild calc doesnt work if the field starts out null.  
#all non-ramps were given local source route prefix
