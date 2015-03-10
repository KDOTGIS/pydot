'''
Created on Feb 10, 2015

@author: kyleg
'''
crashdata = r"Database Connections\KCARSPRD.sde\KCARS.ACCIDENTS_TO_GEO"
Roads = "RoadCenterline"
Alias = "RoadAlias"

def PathReSet():
    #use the path from the NG911 config file to create address locators and perform operations that output to the NG911 geodatabase environment
    try:
        from NG911_Config import gdb
    except:
        gdb = r'\\gisdata\arcgis\GISdata\DASC\NG911\Final\Region1_BA_Final.gdb'
    from arcpy import env, Describe
    env.overwriteOutput = 1
    print gdb
    OriginalGDB = gdb
    gdbdesc = Describe(OriginalGDB)
    gdbpath = gdbdesc.Path
    gdbbasename = gdbdesc.Basename
    gdbexts = gdbdesc.Extension
    del gdb
    gdb = gdbpath+"/"+gdbbasename+"_RoadChecks."+gdbexts
    return gdb

def CreateCrashLocator(gdb):
    #create the geocoding address locator service that works the best for locating crashes from KCARS data
    from arcpy import CreateAddressLocator_geocoding
    in_reference_roads=gdb+r"/NG911/RoadCenterline 'Primary Table';"
    in_reference_alias = gdb+r"/RoadAlias 'Alternate Name Table'"
    in_reference_data = in_reference_roads+in_reference_alias
    #in_field_map="'Primary Table:Feature ID' RoadCenterline:SEGID VISIBLE NONE;'*Primary Table:From Left' RoadCenterline:L_F_ADD VISIBLE NONE;'*Primary Table:To Left' RoadCenterline:L_T_ADD VISIBLE NONE;'*Primary Table:From Right' RoadCenterline:R_F_ADD VISIBLE NONE;'*Primary Table:To Right' RoadCenterline:R_T_ADD VISIBLE NONE;'Primary Table:Prefix Direction' RoadCenterline:PRD VISIBLE NONE;'Primary Table:Prefix Type' RoadCenterline:STP VISIBLE NONE;'*Primary Table:Street Name' RoadCenterline:RD VISIBLE NONE;'Primary Table:Suffix Type' RoadCenterline:STS VISIBLE NONE;'Primary Table:Suffix Direction' RoadCenterline:POD VISIBLE NONE;'Primary Table:Left City or Place' RoadCenterline:KDOT_CITY_L VISIBLE NONE;'Primary Table:Right City or Place' RoadCenterline:KDOT_CITY_R VISIBLE NONE;'Primary Table:Left ZIP Code' RoadCenterline:KDOT_COUNTY_L VISIBLE NONE;'Primary Table:Right ZIP Code' RoadCenterline:KDOT_COUNTY_R VISIBLE NONE;'Primary Table:Left State' <None> VISIBLE NONE;'Primary Table:Right State' <None> VISIBLE NONE;'Primary Table:Left Street ID' <None> VISIBLE NONE;'Primary Table:Right Street ID' <None> VISIBLE NONE;'Primary Table:Display X' <None> VISIBLE NONE;'Primary Table:Display Y' <None> VISIBLE NONE;'Primary Table:Min X value for extent' <None> VISIBLE NONE;'Primary Table:Max X value for extent' <None> VISIBLE NONE;'Primary Table:Min Y value for extent' <None> VISIBLE NONE;'Primary Table:Max Y value for extent' <None> VISIBLE NONE;'Primary Table:Left Additional Field' <None> VISIBLE NONE;'Primary Table:Right Additional Field' <None> VISIBLE NONE;'Primary Table:Altname JoinID' <None> VISIBLE NONE;'*Alias Table:Alias' RoadAlias:SEGID VISIBLE NONE;'*Alias Table:Street' RoadAlias:KDOT_ROUTENAME VISIBLE NONE;'Alias Table:City' '' VISIBLE NONE;'Alias Table:State' <None> VISIBLE NONE;'Alias Table:ZIP' <None> VISIBLE NONE"
    in_field_map="'Primary Table:Feature ID' RoadCenterline:SEGID VISIBLE NONE;'*Primary Table:From Left' RoadCenterline:L_F_ADD VISIBLE NONE;'*Primary Table:To Left' RoadCenterline:L_T_ADD VISIBLE NONE;'*Primary Table:From Right' RoadCenterline:R_F_ADD VISIBLE NONE;'*Primary Table:To Right' RoadCenterline:R_T_ADD VISIBLE NONE;'Primary Table:Prefix Direction' RoadCenterline:PRD VISIBLE NONE;'Primary Table:Prefix Type' RoadCenterline:STP VISIBLE NONE;'*Primary Table:Street Name' RoadCenterline:RD VISIBLE NONE;'Primary Table:Suffix Type' RoadCenterline:STS VISIBLE NONE;'Primary Table:Suffix Direction' RoadCenterline:POD VISIBLE NONE;'Primary Table:Left City or Place' RoadCenterline:KDOT_CITY_L VISIBLE NONE;'Primary Table:Right City or Place' RoadCenterline:KDOT_CITY_R VISIBLE NONE;'Primary Table:Left ZIP Code' RoadCenterline:KDOT_COUNTY_L VISIBLE NONE;'Primary Table:Right ZIP Code' RoadCenterline:KDOT_COUNTY_R VISIBLE NONE;'Primary Table:Left State' <None> VISIBLE NONE;'Primary Table:Right State' <None> VISIBLE NONE;'Primary Table:Left Street ID' <None> VISIBLE NONE;'Primary Table:Right Street ID' <None> VISIBLE NONE;'Primary Table:Display X' <None> VISIBLE NONE;'Primary Table:Display Y' <None> VISIBLE NONE;'Primary Table:Min X value for extent' <None> VISIBLE NONE;'Primary Table:Max X value for extent' <None> VISIBLE NONE;'Primary Table:Min Y value for extent' <None> VISIBLE NONE;'Primary Table:Max Y value for extent' <None> VISIBLE NONE;'Primary Table:Left Additional Field' <None> VISIBLE NONE;'Primary Table:Right Additional Field' <None> VISIBLE NONE;'Primary Table:Altname JoinID' RoadCenterline:SEGID VISIBLE NONE;'*Alternate Name Table:JoinID' RoadAlias:SEGID VISIBLE NONE;'Alternate Name Table:Prefix Direction' RoadAlias:A_PRD VISIBLE NONE;'Alternate Name Table:Prefix Type' RoadAlias:A_STP VISIBLE NONE;'Alternate Name Table:Street Name' RoadAlias:KDOT_ROUTENAME VISIBLE NONE;'Alternate Name Table:Suffix Type' RoadAlias:A_STS VISIBLE NONE;'Alternate Name Table:Suffix Direction' RoadAlias:A_POD VISIBLE NONE"
    out_address_locator=gdb+r"/KCARS_Crash_Loc"
    #CreateAddressLocator_geocoding("US Address - Dual Ranges", in_reference_data, in_field_map, out_address_locator, config_keyword="", enable_suggestions="DISABLED")
    CreateAddressLocator_geocoding("US Address - Dual Ranges", in_reference_data, in_field_map, out_address_locator, config_keyword="", enable_suggestions="DISABLED")

def GeocodeAddresses(gdb):
    #Perform the initial Geocode.
    from arcpy import GeocodeAddresses_geocoding
    GeocodeAddresses_geocoding(in_table="BARBER_004", address_locator=gdb+r"/KCARS_Crash_Loc3", in_address_fields="Street ON_AT_ROAD_INTERSECT VISIBLE NONE;City CITY_NBR VISIBLE NONE;ZIP COUNTY_NBR VISIBLE NONE", out_feature_class="/Geocoding_Result1", out_relationship_type="STATIC")
    
def CrashOffsetPoints(gdb):
    #buffer and intersect the crash location to an offset distance, and select the points that hit the "on Road"
    from arcpy import SelectLayerByAttribute_management, AddJoin_management, Intersect_analysis, Buffer_analysis
    Buffer_analysis(in_features="Geocoding Result: Geocoding_Result_9", out_feature_class="//gisdata/arcgis/GISdata/Accident Geocode/GC_OFFSET_20150210.gdb/Geocoding_Result_9_Buffer", buffer_distance_or_field="AT_ROAD_KDOT_DIST_FEET", line_side="FULL", line_end_type="ROUND", dissolve_option="NONE", dissolve_field="", method="PLANAR")
    AddJoin_management(in_layer_or_view="RoadCenterline", in_field="SEGID", join_table="RoadAlias", join_field="RoadAlias.SEGID", join_type="KEEP_ALL")
    Intersect_analysis(in_features="Geocoding_Result_9_Buffer #;RoadCenterline #", out_feature_class="//gisdata/arcgis/GISdata/Accident Geocode/GC_OFFSET_20150210.gdb/Geocoding_Result_9_Buffer_In", join_attributes="ALL", cluster_tolerance="-1 Unknown", output_type="POINT")
    SelectLayerByAttribute_management(in_layer_or_view="Geocoding_Result_9_Buffer_In", selection_type="NEW_SELECTION", where_clause="ON_ROAD_KDOT_NAME like RoadAlias_KDOT_ROUTENAME OR ON_ROAD_KDOT_NAME like RoadCenterline_RD")
    
def OffsetDirectionNearTable():
    from arcpy import GenerateNearTable_analysis, da, AddFieldDelimiters
    GeocodedLayer = 'Geocoding Result: Geocoding_Result_9'
    IntersectLayer = 'Geocoding_Result_9_Buffer_In'
    
    CursorFieldList = ['OBJECTID', 'ACCIDENT_KEY', 'X', 'Y', 'AT_ROAD_KDOT_DIRECTION', 'POINT_X', 'POINT_Y']
    #  cursor to add to list the Accident IDs and Object IDs
    
    CoordFinder =  da.SearchCursor(IntersectLayer, CursorFieldList)  # @UndefinedVariable
    coordlist = []
    rowDictionary = dict()

    for row in CoordFinder:
        print 
        #print('{0}, {1}, {2}, {3}, {4}'.format(row[0], row[1], row[2], row[3], row[4]))
        if str(row[2]) == "E":
            print row[0]
            EastCoord = max(row[0], row[3])
            coordlist.append(EastCoord)
            rowDictionary
    for i in rowDictionary:
        print str(i)
    #GenerateNearTable_analysis(in_features="Geocoding Result: Geocoding_Result_9", near_features="Geocoding_Result_9_Buffer_In", out_table="C:/Users/kyleg/Documents/ArcGIS/Default.gdb/Geocoding_Result_9_GenerateN", search_radius="200 Feet", location="LOCATION", angle="ANGLE", closest="ALL", closest_count="4", method="PLANAR")



def OffsetDirectionMatrix(gdb):
    #select the intersected coordinate that best describes the reported location of the on road from the intersection based on the CrashOffsetPoints function      
    from arcpy import AddXY_management, AddJoin_management, ListFields, da, SelectLayerByAttribute_management, AddFieldDelimiters
    GeocodedLayer = 'Geocoding Result: Geocoding_Result_9'
    IntersectLayer = 'Geocoding_Result_9_Buffer_In'
    AddXY_management(IntersectLayer)
    AddJoin_management(IntersectLayer, "ACCIDENT_KEY", GeocodedLayer, "ACCIDENT_KEY")
    FieldsList = ListFields(IntersectLayer)
    CursorFieldList = ['X', 'Y', 'AT_ROAD_KDOT_DIRECTION', 'POINT_X', 'POINT_Y', 'OBJECTID', 'ACCIDENT_KEY']
    #  cursor to add to list the Accident IDs and Object IDs
    
    CoordFinder =  da.SearchCursor(IntersectLayer, CursorFieldList)  # @UndefinedVariable
    coordlist = []
    rowDictionary = dict()

    for row in CoordFinder:
        print 
        #print('{0}, {1}, {2}, {3}, {4}'.format(row[0], row[1], row[2], row[3], row[4]))
        if str(row[2]) == "E":
            print row[0]
            EastCoord = max(row[0], row[3])
            coordlist.append(EastCoord)
            rowDictionary
    print coordlist
    FinalEastCoordinate = max(coordlist)
    FinalEastCoordInt = int(FinalEastCoordinate)
    print FinalEastCoordinate
    CoordSelExpression = 'POINT_X -'+str(FinalEastCoordInt)+" < 1"
    SelectLayerByAttribute_management(IntersectLayer, "NEW_SELECTION",  CoordSelExpression)

def OffsetDirectionMatrix1():
    #select the intersected coordinate that best describes the reported location of the on road from the intersection based on the CrashOffsetPoints function      
    from arcpy import AddXY_management, AddJoin_management, ListFields, da, SelectLayerByAttribute_management, AddFieldDelimiters
    GeocodedLayer = 'Geocoding Result: Geocoding_Result_9'
    IntersectLayer = 'Geocoding_Result_9_Buffer_In'
    AddXY_management(IntersectLayer)
    AddJoin_management(IntersectLayer, "ACCIDENT_KEY", GeocodedLayer, "ACCIDENT_KEY")
    CursorFieldList = ['X', 'Y', 'AT_ROAD_KDOT_DIRECTION', 'POINT_X', 'POINT_Y', 'OBJECTID', 'ACCIDENT_KEY']
    #  cursor to add to list the Accident IDs and Object IDs
    
    CoordFinder =  da.SearchCursor(IntersectLayer, CursorFieldList)  # @UndefinedVariable
    rowDictionary = dict()
    for row in CoordFinder:
        rowDictionary[row[5]]=row
    try:
        del CoordFinder
    except:
        print "cursor hung"
    for keyname in rowDictionary.keys():
        rowOfInterest = rowDictionary[keyname]
        if str(rowOfInterest[2]) == "E":
            print str(rowOfInterest[2])
            coordlist = []
            OffsetCoord = rowOfInterest[3]
            coordlist.append(OffsetCoord)
            print coordlist
    FinalCoordinate = max(coordlist)
    FinalCoordInt = int(FinalCoordinate)
    
    print FinalCoordinate
    
                                                  
def SetCrashCoordinateFromIntersection(gdb):
    #Populate the lat and long for the crash location
    from arcpy import FeatureClassToFeatureClass_conversion, AddJoin_management

if __name__ == '__main__':
    gdb = PathReSet()
    CreateCrashLocator(gdb)
    
    pass