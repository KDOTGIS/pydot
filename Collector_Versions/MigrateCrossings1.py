'''
Created on Aug 1, 2016

@author: kyleg
'''

GateProd = r""

#The CIIMS view should be exported using FME
CIIMSViewSpace = r"C:\temp\CIIMS_Views_CANP.gdb"
IntersectionLocations = r"\\gisdata\planning\Cart\projects\RailCrossing\IntersectRdRail.gdb\RRINT"
TargetDB = r"C:\temp\CollectorTest20160801.gdb"
KGATE_Crossings = r"Database Connections\gate@gateprod.sde\GATE.KGATE_CROSSINGS"

from arcpy import SelectLayerByAttribute_management, CalculateField_management, FeatureClassToFeatureClass_conversion, AddField_management, Append_management

FeatureClassToFeatureClass_conversion(KGATE_Crossings, "in_memory", "KGATE_CROSSINGS")
FeatureClassToFeatureClass_conversion(IntersectionLocations, "in_memory", "RRINT")

target = KGATE_Crossings


#All I need is the Crossing ID
field_mapping="""AssetID "AssetID" true true false 50 Text 0 0 ,First,#,KGATE_CROSSINGS,DOT_CROSSING_NO,-1,-1;"""

# I dont need these fields mapped - I will get them set from joins later in SQL - the formats are all CHAR254 in the view
'''Start_Date "Start_Date" true true false 8 Date 0 0 ,First,#;
End_Date "End_Date" true true false 8 Date 0 0 ,First,#;
Source "Source Citation" true true false 5 Text 0 0 ,First,#;
GlobalID "GlobalID" false false true 38 GlobalID 0 0 ,First,#;
InvBy "Inventoried By" true true false 55 Text 0 0 ,First,#;
InvDate "Inventory Date" true true false 8 Date 0 0 ,First,#;
CrossingSurfaceMaterial "Crossing Surface" true true false 3 Text 0 0 ,First,#;
XingStatus "Crossing Status" true true false 2 Text 0 0 ,First,#;
Subtype "Subtype" true true false 4 Long 0 0 ,First,#;
FraType "Public vs Private" true true false 3 Text 0 0 ,First,#;
Narrative "Narrative" true true false 99 Text 0 0 ,First,#;
SurfaceWidth "Surface Width Feet" true true false 8 Double 0 0 ,First,#;
SurfaceLength "Surface Length Feet" true true false 8 Double 0 0 ,First,#;
Channels "ChannelizationDevices" true true false 255 Text 0 0 ,First,#;
MainTrk "Main Track Count" true true false 4 Long 0 0 ,First,#;
SidingTrk "Siding Track Count" true true false 4 Long 0 0 ,First,#;
YardTrk "Yard Track Count" true true false 4 Long 0 0 ,First,#;
TransitTrk "Transit Track Count" true true false 4 Long 0 0 ,First,#;
IndustryTrk "Industry Track Count" true true false 4 Long 0 0 ,First,#;
SignsOrSignals "Signs or Signals are present" true true false 50 Text 0 0 ,First,#;
WaysideHorn "Wayside Horn" true true false 255 Text 0 0 ,First,#;
HwyTrafSig "Highway Traffic Signals controling crossing" true true false 1 Text 0 0 ,First,#;
Bells "Bells" true true false 2 Short 0 0 ,First,#;
FlshOthr "Other Flashing Lights" true true false 4 Long 0 0 ,First,#;
FlshOthrTyp "Other Flashing Lights Type" true true false 2 Text 0 0 ,First,#;
Zoning "Development" true true false 2 Text 0 0 ,First,#;
OpCo "Operating Railroad Company" true true false 4 Text 0 0 ,First,#;
UserNotes "Notes" true true false 250 Text 0 0 ,First,#;
Lens "Lens Size" true true false 2 Text 0 0 ,First,#;
Separation "Distance to Separation Feet" true true false 8 Double 0 0 ,First,#;
Milepost "Railroad Milepost" true true false 8 Double 0 0 ,First,#;
Quadrants "Quadrants Blocks" true true false 4 Long 0 0 ,First,#;
Illumination "Crossing Illumination" true true false 1 Text 0 0 ,First,#;
PowerAvail "Commercial Power Available" true true false 1 Text 0 0 ,First,#;
Horn "Wayside Horn" true true false 1 Text 0 0 ,First,#;
Gouge "Gouge Marks" true true false 1 Text 0 0 ,First,#;
PostedNo "Crossing Number Posted" true true false 1 Text 0 0 ,First,#;
PublicCrossing "Open to Public" true true false 1 Text 0 0 ,First,#;
QuadGates "Four Quad Gates Present" true true false 1 Text 0 0 ,First,#;
Quiet "Quiet Zone" true true false 1 Text 0 0 ,First,#;
DownRoad "Track Down Road" true true false 1 Text 0 0 ,First,#"""'''

#
Append_management("KGATE_CROSSINGS", "RailCrossing", "NO_TEST", field_mapping, subtype="")



#AddField_management("KGATE_CROSSINGS", "Subtype_field", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
#SelectLayerByAttribute_management(in_layer_or_view="KGATE_CROSSINGS", selection_type="NEW_SELECTION", where_clause=""""CROSSING_TYPE" = 'Active, Crossbuck only'""")
#CalculateField_management(in_table="KGATE_CROSSINGS", field="Subtype_field", expression="3", expression_type="VB", code_block="")
#SelectLayerByAttribute_management(in_layer_or_view="KGATE_CROSSINGS", selection_type="NEW_SELECTION", where_clause=""""CROSSING_TYPE" = 'Active, Flashing lights with gates'""")

#CalculateField_management(in_table="KGATE_CROSSINGS", field="Subtype_field", expression="1", expression_type="VB", code_block="")
#SelectLayerByAttribute_management(in_layer_or_view="KGATE_CROSSINGS", selection_type="NEW_SELECTION", where_clause=""""CROSSING_TYPE" = 'Active, Flashing lights, no gates'""")

#CalculateField_management(in_table="KGATE_CROSSINGS", field="Subtype_field", expression="2", expression_type="VB", code_block="")
#SelectLayerByAttribute_management(in_layer_or_view="KGATE_CROSSINGS", selection_type="NEW_SELECTION", where_clause=""""CROSSING_TYPE" = 'Active, No Flashing lights, gates, or crossbuck'""")

#CalculateField_management(in_table="KGATE_CROSSINGS", field="Subtype_field", expression="4", expression_type="VB", code_block="")
#SelectLayerByAttribute_management(in_layer_or_view="KGATE_CROSSINGS", selection_type="NEW_SELECTION", where_clause=""""CROSSING_TYPE" = 'Not Actively Used'""")




