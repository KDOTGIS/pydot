'''
Created on Jun 24, 2015

@author: kyleg
'''
from arcpy import (CreateFileGDB_management, CreateFeatureclass_management, AddField_management, CreateDomain_management, 
                   DomainToTable_management, CreateDomain_management, AddCodedValueToDomain_management, MakeTableView_management, 
                   TableToDomain_management, SetValueForRangeDomain_management, Exists, Delete_management)
                  
workspace ='C:/temp'
version = '02'
spatialCRS = ''
gdbname = 'RailCrossing'+str(version)
gdb = workspace + '/'+gdbname+'.gdb'
CountyList = r'Database Connections\SDEPROD_SHARED.sde\SHARED.counties'
CityList = r'Database Connections\SDEPROD_SHARED.sde\SHARED.CITY_LIMITS'
MUTCDList = r'Database Connections\geo@sign_sqlgis.sde'
in_table = gdb+"/Crossings"

print gdb

def main():
    #RestartGDB()
    #GdbCreate()
    #CreateDomains()
    CrossingFields()
    pass

def CrossingFields():
    print in_table
    #This wohle section was copied from the RailCrossingDBDef20150728.xls in the CART/PROJECTS/RAilCrossing directory
        #This spreadsheet was populated by Logan referencing the forms, reviewed by DArlene and Kyle a few times'
    AddField_management(in_table, 'CrossingID', 'TExt', '#', '#', '7', 'Crossing ID', 'NULLABLE', 'NON_REQUIRED', '')
    AddField_management(in_table, 'ENS_ID_N', 'Text', '#', '#', '3', 'ENS Crossing Number', 'NULLABLE', 'NON_REQUIRED', 'dENSPhone')
    AddField_management(in_table, 'InspDir', 'Text', '#', '#', '2', 'Direction of Inspection (or Approach)', 'NULLABLE', 'NON_REQUIRED', 'dDirection')
    AddField_management(in_table, 'InvDate', 'Date', '#', '#', '#', 'Inventory Date', 'NULLABLE', 'NON_REQUIRED', '#')
    AddField_management(in_table, 'InvBy', 'Text', '#', '#', '55', 'Inventoried by (name(s))', 'NULLABLE', 'NON_REQUIRED', '#')
    AddField_management(in_table, 'XInstallDate', 'Date', '#', '#', '#', 'Crossing Installation Date', 'NULLABLE', 'NON_REQUIRED', '#')
    AddField_management(in_table, 'XInstallProj', 'Text', '#', '#', '9', 'Crossing Project ID', 'NULLABLE', 'NON_REQUIRED', '#')
    AddField_management(in_table, 'City', 'Text', '#', '#', '3', 'City', 'NULLABLE', 'NON_REQUIRED', 'dCity')
    AddField_management(in_table, 'County', 'Text', '#', '#', '3', 'County', 'NULLABLE', 'NON_REQUIRED', 'dCounty')
    AddField_management(in_table, 'Latitude', 'Double', '24', '7', '#', 'Latitude', 'NULLABLE', 'NON_REQUIRED', 'dKSLat')
    AddField_management(in_table, 'Longitude', 'Double', '24', '7', '#', 'Longitude', 'NULLABLE', 'NON_REQUIRED', 'dKSLong')
    AddField_management(in_table, 'LocSource', 'Text', '#', '#', '3', 'Lat/Long Source', 'NULLABLE', 'NON_REQUIRED', 'dSource')
    AddField_management(in_table, 'Power', 'Text', '#', '#', '1', 'Power', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'District', 'Text', '#', '#', '3', 'District', 'NULLABLE', 'NON_REQUIRED', 'dDistrict')
    AddField_management(in_table, 'CityVicin', 'Text', '#', '#', '3', 'City In Near Indicator', 'NULLABLE', 'NON_REQUIRED', 'dCityNear')
    AddField_management(in_table, 'OnSHS', 'Text', '#', '#', '1', 'On State Highway System', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'Position', 'Text', '#', '#', '3', 'FRA Crossing Position', 'NULLABLE', 'NON_REQUIRED', 'dPosition')
    AddField_management(in_table, 'Zoning', 'Text', '#', '#', '2', 'Development:', 'NULLABLE', 'NON_REQUIRED', 'dDevelopmentZoned')
    AddField_management(in_table, 'Quiet', 'Text', '#', '#', '1', 'Quiet Zone', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'Public', 'Text', '#', '#', '1', 'Open to Public', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'Angle', 'LONG', '3', '0', '#', 'Crossing Angle', 'NULLABLE', 'NON_REQUIRED', 'dRange0_90')
    AddField_management(in_table, 'Length', 'Double', '6', '1', '#', 'Surface Length Feet', 'NULLABLE', 'NON_REQUIRED', 'dLength10_220')
    AddField_management(in_table, 'Separation', 'Double', '6', '1', '#', 'Distance to Separation Feet', 'NULLABLE', 'NON_REQUIRED', 'dLength0_100')
    AddField_management(in_table, 'Gouge', 'Text', '#', '#', '1', 'Gouge Marks', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'LeftAlign', 'Text', '#', '#', '3', 'Left Rail Alignment', 'NULLABLE', 'NON_REQUIRED', 'dAlignment')
    AddField_management(in_table, 'RightAlign', 'Text', '#', '#', '3', 'Right Rail Alignment', 'NULLABLE', 'NON_REQUIRED', 'dAlignment')
    AddField_management(in_table, 'DownRoad', 'Text', '#', '#', '1', 'Track Down Road', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'RdWidth', 'Double', '6', '1', '#', 'Roadway Width (Feet)', 'NULLABLE', 'NON_REQUIRED', 'dLength10_220')
    AddField_management(in_table, 'AppAlign', 'Text', '#', '#', '3', 'Approach Alignment', 'NULLABLE', 'NON_REQUIRED', 'dAlignment')
    AddField_management(in_table, 'DeptAlign', 'Text', '#', '#', '3', 'Depart Alignment', 'NULLABLE', 'NON_REQUIRED', 'dAlignment')
    AddField_management(in_table, 'Status', 'Text', '#', '#', '2', 'Crossing Status', 'NULLABLE', 'NON_REQUIRED', 'dStatus')
    AddField_management(in_table, 'Material', 'Text', '#', '#', '3', 'Mainline Surface Material ', 'NULLABLE', 'NON_REQUIRED', 'dMaterialKDOT')
    AddField_management(in_table, 'Type', 'Text', '#', '#', '3', 'FRA Crossing Type', 'NULLABLE', 'NON_REQUIRED', 'dCrossingType')
    AddField_management(in_table, 'Quadrants', 'LONG', '1', '0', '#', 'Quadrants Blocks', 'NULLABLE', 'NON_REQUIRED', 'dRange0_5')
    AddField_management(in_table, 'Illumination', 'Text', '#', '#', '1', 'Crossing Illumination', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'Narrative', 'Text', '#', '#', '99', 'Narrative', 'NULLABLE', 'NON_REQUIRED', '#')
    AddField_management(in_table, 'Crossbuck', 'LONG', '1', '0', '#', 'Crossbucks', 'NULLABLE', 'NON_REQUIRED', 'dRange0_8')
    AddField_management(in_table, 'XBReflect', 'Text', '#', '#', '2', 'Crossbuck Reflectorization', 'NULLABLE', 'NON_REQUIRED', 'dReflective')
    AddField_management(in_table, 'FlashLight', 'LONG', '2', '0', '#', 'Flashing Light Pairs', 'NULLABLE', 'NON_REQUIRED', 'dRange0_18')
    AddField_management(in_table, 'Lens', 'Text', '#', '#', '2', 'Lens Size', 'NULLABLE', 'NON_REQUIRED', 'dFlashLight')
    AddField_management(in_table, 'Masts', 'LONG', '1', '0', '#', 'Mast Count', 'NULLABLE', 'NON_REQUIRED', 'dRange0_6')
    AddField_management(in_table, 'MastLightType', 'Text', '#', '#', '3', 'Mast Light Type', 'NULLABLE', 'NON_REQUIRED', 'dtLightType')
    AddField_management(in_table, 'MastLightConfig', 'Text', '#', '#', '3', 'Mast Light Configuration', 'NULLABLE', 'NON_REQUIRED', 'dMastLightConfig')
    AddField_management(in_table, 'CantOver', 'LONG', '1', '0', '#', 'Cantilever Over Thru Lanes', 'NULLABLE', 'NON_REQUIRED', 'dRange0_4')
    AddField_management(in_table, 'CantNotOver', 'LONG', '1', '0', '#', 'Cantilever Not Over Thru Lanes', 'NULLABLE', 'NON_REQUIRED', 'dRange0_4')
    AddField_management(in_table, 'CantOverType', 'Text', '#', '#', '3', 'Cantilever Flashing Light', 'NULLABLE', 'NON_REQUIRED', 'dLightType')
    AddField_management(in_table, 'NoGatesRd', 'LONG', '1', '0', '#', 'Number of Gates Roadway', 'NULLABLE', 'NON_REQUIRED', 'dRange0_8')
    AddField_management(in_table, 'NoGatesPed', 'LONG', '1', '0', '#', 'Number of Gates Sidewalk', 'NULLABLE', 'NON_REQUIRED', 'dRange0_8')
    AddField_management(in_table, 'GateLight', 'Text', '#', '#', '1', 'Gate Mounted Flashing Lights', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'Horn', 'Text', '#', '#', '1', 'Wayside Horn', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'Bells', 'LONG', '1', '0', '#', 'Bells', 'NULLABLE', 'NON_REQUIRED', 'dRange0_4')
    AddField_management(in_table, 'QuadGates', 'Text', '#', '#', '1', 'Four Quad Gates Present', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'GateChan', 'Text', '#', '#', '2', 'Channelization with Gates', 'NULLABLE', 'NON_REQUIRED', 'dSideDesc')
    AddField_management(in_table, 'TrafSig', 'LONG', '1', '0', '#', 'Traffic Signals', 'NULLABLE', 'NON_REQUIRED', 'dRange0_4')
    AddField_management(in_table, 'HwyTrafSig', 'Text', '#', '#', '1', 'Highway Traffic Signals controling crossing', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'FlshOthr', 'LONG', '2', '0', '#', 'Other Flashing Lights', 'NULLABLE', 'NON_REQUIRED', 'dRange0_12')
    AddField_management(in_table, 'FlshOthrTyp', 'Text', '#', '#', '2', 'Other Flashing Lights Type', 'NULLABLE', 'NON_REQUIRED', 'dFlashType')
    AddField_management(in_table, 'WInstallDate', 'Date', '#', '#', '#', 'Warning Device Installation Date', 'NULLABLE', 'NON_REQUIRED', '#')
    AddField_management(in_table, 'WInstallProj', 'Text', '#', '#', '9', 'Warning Device Installation Project ID', 'NULLABLE', 'NON_REQUIRED', '#')
    AddField_management(in_table, 'W10_1', 'LONG', '1', '0', '#', 'Advanced Warning Sign W10-1 Count', 'NULLABLE', 'NON_REQUIRED', 'dRange0_6')
    AddField_management(in_table, 'W10_1a', 'LONG', '1', '0', '#', 'yellow exempt warning sign', 'NULLABLE', 'NON_REQUIRED', 'dRange0_6')
    AddField_management(in_table, 'W10_2', 'LONG', '1', '0', '#', 'Advanced Warning Sign W10-2 Count', 'NULLABLE', 'NON_REQUIRED', 'dRange0_6')
    AddField_management(in_table, 'W10_3', 'LONG', '1', '0', '#', 'Advanced Warning Sign W10-3 Count', 'NULLABLE', 'NON_REQUIRED', 'dRange0_6')
    AddField_management(in_table, 'W10_4', 'LONG', '1', '0', '#', 'Advanced Warning Sign W10-4 Count', 'NULLABLE', 'NON_REQUIRED', 'dRange0_6')
    AddField_management(in_table, 'W10_11', 'LONG', '1', '0', '#', 'Advanced Warning Sign W10-11 Count', 'NULLABLE', 'NON_REQUIRED', 'dRange0_6')
    AddField_management(in_table, 'W10_12', 'LONG', '1', '0', '#', 'Advanced Warning Sign W10-12 Count', 'NULLABLE', 'NON_REQUIRED', 'dRange0_6')
    AddField_management(in_table, 'W10_5', 'LONG', '1', '0', '#', 'Hump Crossing Sign', 'NULLABLE', 'NON_REQUIRED', 'dRange0_6')
    AddField_management(in_table, 'R15_3', 'Text', '#', '#', '1', 'white exempt sign on crossbuck', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'AdvWrnSgnRef', 'Text', '#', '#', '1', 'Advanced Warning Signs Reflectivity', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'PostedNo', 'Text', '#', '#', '1', 'Crossing number Posted', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'HumpSign', 'Text', '#', '#', '1', 'Hump Signs Indicator', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'StopSign', 'LONG', '1', '0', '#', 'Stop Signs', 'NULLABLE', 'NON_REQUIRED', 'dRange0_5')
    AddField_management(in_table, 'YieldSign', 'LONG', '1', '0', '#', 'Yield Signs', 'NULLABLE', 'NON_REQUIRED', 'dRange0_5')
    AddField_management(in_table, 'NoESNSign', 'LONG', '1', '0', '#', 'How many ENS signs posted', 'NULLABLE', 'NON_REQUIRED', 'dRange0_5')
    AddField_management(in_table, 'EmgcySgn', 'Text', '#', '#', '3', 'Emergency Signs (ENS/DOT) 1-13', 'NULLABLE', 'NON_REQUIRED', 'dRailPhone')
    AddField_management(in_table, 'MUTCD1', 'LONG', '1', '0', '#', 'Other Sign MUTCD 1', 'NULLABLE', 'NON_REQUIRED', 'dRange0_2')
    AddField_management(in_table, 'MUTCDTyp1', 'Text', '#', '#', '8', 'Other Sign MUTCD Type 1', 'NULLABLE', 'NON_REQUIRED', 'dMUTCDCode')
    AddField_management(in_table, 'MUTCD2', 'LONG', '1', '0', '#', 'Other Sign MUTCD 2', 'NULLABLE', 'NON_REQUIRED', 'dRange0_2')
    AddField_management(in_table, 'MUTCDTyp2', 'Text', '#', '#', '8', 'Other Sign MUTCD Type 2', 'NULLABLE', 'NON_REQUIRED', 'dMUTCDCode')
    AddField_management(in_table, 'MUTCD3', 'LONG', '1', '0', '#', 'Other Sign MUTCD 3', 'NULLABLE', 'NON_REQUIRED', 'dRange0_2')
    AddField_management(in_table, 'MUTCDTyp3', 'Text', '#', '#', '8', 'Other Sign MUTCD Type 3', 'NULLABLE', 'NON_REQUIRED', 'dMUTCDCode')
    AddField_management(in_table, 'PreDir', 'Text', '#', '#', '2', 'Prefix Direction of Street', 'NULLABLE', 'NON_REQUIRED', 'dDirection')
    AddField_management(in_table, 'StrName', 'Text', '#', '#', '64', 'Street Name', 'NULLABLE', 'NON_REQUIRED', '#')
    AddField_management(in_table, 'StrType', 'Text', '#', '#', '10', 'Street Type', 'NULLABLE', 'NON_REQUIRED', 'dStrType')
    AddField_management(in_table, 'RoadType', 'Text', '#', '#', '2', 'Roadway Type', 'NULLABLE', 'NON_REQUIRED', 'dRdType')
    AddField_management(in_table, 'NoLanes', 'LONG', '2', '0', '#', 'Traffic Lanes', 'NULLABLE', 'NON_REQUIRED', 'dRange0_12')
    AddField_management(in_table, 'ShldWidth', 'LONG', '2', '0', '#', 'Shoulder Width (Feet)', 'NULLABLE', 'NON_REQUIRED', 'dRange0_12')
    AddField_management(in_table, 'ShldSurf', 'Text', '#', '#', '1', 'Shoulder Surface Indicator', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'SpeedLim', 'Text', '#', '#', '2', 'Speed Limit', 'NULLABLE', 'NON_REQUIRED', 'dSpeedLim')
    AddField_management(in_table, 'SpeedReg', 'Text', '#', '#', '2', 'Speed Regulation', 'NULLABLE', 'NON_REQUIRED', 'dSpeedReg')
    AddField_management(in_table, 'Turnout', 'Text', '#', '#', '1', 'Truck Turnout', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'Curb', 'Text', '#', '#', '1', 'Curb Gutter', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'NHS', 'Text', '#', '#', '2', 'Highway System', 'NULLABLE', 'NON_REQUIRED', 'dNHS')
    AddField_management(in_table, 'EmergencyRoute', 'Text', '#', '#', '1', 'Emergency Services Route', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'UrbanCode', 'Text', '#', '#', '1', 'Urban Rural', 'NULLABLE', 'NON_REQUIRED', 'dUrbanRural')
    AddField_management(in_table, 'Funclass', 'Text', '#', '#', '1', 'Functional Classification', 'NULLABLE', 'NON_REQUIRED', 'dFUN')
    AddField_management(in_table, 'Sidewalk', 'Text', '#', '#', '4', 'Sidewalk', 'NULLABLE', 'NON_REQUIRED', 'dSideDesc')
    AddField_management(in_table, 'PavMark', 'Text', '#', '#', '2', 'Pavement Markings', 'NULLABLE', 'NON_REQUIRED', 'dApproach')
    AddField_management(in_table, 'PavMarkStop', 'Text', '#', '#', '2', 'Stopline Pavement Markings', 'NULLABLE', 'NON_REQUIRED', 'dApproach')
    AddField_management(in_table, 'Channels', 'Text', '#', '#', '2', 'ChannelizationDevices', 'NULLABLE', 'NON_REQUIRED', 'dApproach')
    AddField_management(in_table, 'Medians', 'Text', '#', '#', '1', 'ChannelizationMedians', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'Passing', 'Text', '#', '#', '2', 'No Passing Lines', 'NULLABLE', 'NON_REQUIRED', 'dApproach')
    AddField_management(in_table, 'HwySigs', 'Text', '#', '#', '1', 'Nearby Highway Intersection Signals', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'AppHwyInt', 'Double', '3', '1', '#', 'Approach Nearby Intersecting Highway', 'NULLABLE', 'NON_REQUIRED', 'dLength500')
    AddField_management(in_table, 'AppSurfType', 'Text', '#', '#', '2', 'Approach Roadway Surface Type', 'NULLABLE', 'NON_REQUIRED', 'dMaterial')
    AddField_management(in_table, 'AppHwySigs', 'Text', '#', '#', '1', 'Approach Intersecting Highway Signals', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'DepHwyInt', 'Double', '3', '1', '#', 'Depart Nearby Intersecting Highway', 'NULLABLE', 'NON_REQUIRED', 'dLength500')
    AddField_management(in_table, 'DepSurfType', 'Text', '#', '#', '2', 'Depart Roadway Surface Type', 'NULLABLE', 'NON_REQUIRED', 'dMaterial')
    AddField_management(in_table, 'DepHwySigs', 'Text', '#', '#', '1', 'Depart Intersecting Highway Signals', 'NULLABLE', 'NON_REQUIRED', 'dYesNo')
    AddField_management(in_table, 'OpCo', 'Text', '#', '#', '4', 'Operating Railroad Company', 'NULLABLE', 'NON_REQUIRED', '#')
    AddField_management(in_table, 'MainTrk', 'LONG', '1', '0', '#', 'Main Tracks', 'NULLABLE', 'NON_REQUIRED', 'dRange0_5')
    AddField_management(in_table, 'OtherTrk', 'LONG', '2', '0', '#', 'Other Tracks', 'NULLABLE', 'NON_REQUIRED', 'dRange0_12')
    AddField_management(in_table, 'OtherTrkDesc', 'Text', '#', '#', '2', 'Other Tracks Description', 'NULLABLE', 'NON_REQUIRED', 'dTrackType')
    AddField_management(in_table, 'Milepost', 'Double', '5', '3', '#', 'Railroad Milepost', 'NULLABLE', 'NON_REQUIRED', 'dRange0_800')
    AddField_management(in_table, 'Notes', 'Text', '#', '#', '750', 'Notes', 'NULLABLE', 'NON_REQUIRED', '#')



def CreateDomains():
    dDirection(gdb)
    dCity(gdb)
    #dCounty(gdb)
    dCoordinateX(gdb)
    dCoordinateY(gdb)
    dCodedValueDomainYN(gdb)
    dCodedValueDomainDistrict(gdb)
    dCodedValueDomainLocSource(gdb)
    dCodedValueDomainNearCity(gdb)
    dCodedValueDomainDevelopmentZoned(gdb)
    dCodedCrossingStatus(gdb)
    dMaterialList(gdb)
    dCodedValueAlignment(gdb)
    dRange0_100(gdb)
    dRange0_90(gdb)
    dRange10_220(gdb)
    dCodedValueCrossingType(gdb)
    dRange0_4(gdb)
    dRange0_6(gdb)
    dRange0_8(gdb)
    dReflector(gdb)
    dDiameter(gdb)
    dLighting(gdb)
    dPosition(gdb)
    dSide(gdb)
    dFlashType(gdb)
    dENSPhone(gdb)
    dMUTCDCode(gdb) #copy this domain from the ESRI Sign database
    dStrPrefix(gdb)
    dRdSuffix(gdb)
    dSpeedLim(gdb)
    dSpeedReg(gdb)
    dNHS(gdb)
    dUrbanRural(gdb)
    dFunClass(gdb)
    dApproach(gdb)
    dRailRoadAdmo(gdb)
    dTrackType(gdb)
    

def dReflector(igdb):  
    cDomainName = 'dcReflector'
    cdDomainValueDict = {"N":"Nonreflectorized", "P":"Prismatic", "R":"Reflectorized"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dDiameter(igdb):  
    cDomainName = 'dDiameters'
    cdDomainValueDict = {"RP":"Regular pair", "6":"6 inch diameter", "8":"8 inch diameter", "10":"10 inch diameter", "12":"12 inch diameter"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dLighting(igdb):  
    cDomainName = 'dLighting'
    cdDomainValueDict = {"I":"Incandescent", "L":"LED", "B":"Both"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dPosition(igdb):  
    cDomainName = 'dPositions'
    cdDomainValueDict = {"B":"Back", "S":"Side"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName

def dSide(igdb):  
    cDomainName = 'dSides'
    cdDomainValueDict = {"2":"Both Sides","1":"One Side", "0":"Neither Side"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName

def dFlashType(igdb):  
    cDomainName = 'dFlashType'
    cdDomainValueDict = {"0T":"No Turn", "0L":"No Left Turn", "0R":"No Right Turn", "00":"None", 
                         "R":"Red", "SZ":"School Zone", "TY":"Truck Yard", "Y":"Yellow"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dENSPhone(igdb):  
    cDomainName = 'dENSPhone'
    cdDomainValueDict = {"BN":"800-832-5452 BNSF",
                         "CV":"620-649-3280 Cimarron Valley", 
                         "GCW":"800-914-7850 Garden City Western",\
                         "KO":"866-386-9321 Kansas & Oklahoma",\
                         "KCS":"877-527-9464 Kansas City Southern",\
                         "KCT":"913-551-2179 Kansas City Terminal ",\
                         "K":"800-800-3490 Kyle",\
                         "NKC":"800-533-9416 Nebraska, Kansas, Colorado",\
                         "NCA":"913-785-0720 New Century AirCenter",\
                         "SKO":"866-386-9321 South Kansas & Oklahoma",\
                         "UP":"800-848-8715 Union Pacific",\
                         "VS":"800-639-5054 V & S",\
                         "WT":"800-832-5452 Wichita Terminal"}
    CreateDomain_management  (gdb, cDomainName, 'Emergency Phone Number', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dStrPrefix(igdb):  
    cDomainName = 'dStrPrefix'
    cdDomainValueDict = {"AVE":"Avenue", "BLVD":"Boulevard", "CIR":"Circle", "DR":"Drive", "HWY":"Highway", 
                         "LN":"Lane", "PKWY":"Parkway", "PL":"Place", "RD":"Road", "ST":"Street", "TER":"Terrace", "WAY":"Way"}
    CreateDomain_management  (gdb, cDomainName, 'Road Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dRdSuffix(igdb):  
    cDomainName = 'dRdSuffix'
    cdDomainValueDict = {"I":"Interstate","US":"US Route", "SH": "State Highway", "CR":"County Road", 
                         "TL":"Toll Road", "LS":"Local Street", "FM":"Farm to Market"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dSpeedLim(igdb):  
    cDomainName = 'dSpeedLim'
    cdDomainValueDict = {"10":"10 mph","15":"15 mph","20":"20 mph","25":"25 mph","30":"30 mph",
                         "35":"35 mph","40":"40 mph","45":"45 mph","50":"50 mph","55":"55 mph",
                         "60":"60 mph","65":"65 mph","70":"70 mph","75":"75 mph","80":"80 mph"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dSpeedReg(igdb):  
    cDomainName = 'dSpeedReg'
    cdDomainValueDict = {"P":"Posted", "S":"Statutory"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dNHS(igdb):  
    cDomainName = 'dNHS'
    cdDomainValueDict = {"I":"Interstate National Highway System", "N":"Non-Federal-Aid", "O":"Other Federal-Aid Highway-Not NHS", 
                         "H":"Other National Highway System"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  
    
def dUrbanRural(igdb):  
    cDomainName = 'dUrbanRural'
    cdDomainValueDict = {"U":"Urban", "R":"Rural"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  
    
def dFunClass(igdb):  
    cDomainName = 'dFunClass'
    cdDomainValueDict = {"1":"Interstate", "2":"Other Freeway and Exressway", "3":"Other Principal Arterial", 
                         "4":"Minor Arterial", "5":"Major Collector", "6":"Minor Collector", "7":"Local"}
    CreateDomain_management  (gdb, cDomainName, 'dFunClass', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dApproach(igdb):  
    cDomainName = 'dGeneric'
    cdDomainValueDict = {"1a":"Approach Side Only", "2":"Both Approach and Depart Sides", 
                         "1d":"Depart Side only", "0":"Neither Approach nor Depart Sides"}
    CreateDomain_management  (gdb, cDomainName, 'Approach', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  
    
def dRailRoadAdmo(igdb):  
    cDomainName = 'dRailRoadAdmo'
    cdDomainValueDict =  {"BN":"BNSF",
                         "CV":"Cimarron Valley", 
                         "GCW":"Garden City Western",
                         "KO":"Kansas & Oklahoma",
                         "KCS":"Kansas City Southern",
                         "KCT":"Kansas City Terminal",
                         "K":"Kyle",
                         "NKC":"Nebraska, Kansas, Colorado",
                         "NCA":"New Century AirCenter",
                         "SKO":"South Kansas & Oklahoma",
                         "UP":"Union Pacific",
                         "VS":"V & S",
                         "WT":"Wichita Terminal"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Administrative Owner', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  
    
def dTrackType(igdb):  
    cDomainName = 'dTrackType'
    cdDomainValueDict = {"I":"Industry", "S":"Siding", "T":"Transit", "Y":"Yard" }
    CreateDomain_management  (gdb, cDomainName, 'Track Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dRange0_4(igdb):
    gdb = igdb
    rDomainName = 'dRange0_4'
    CreateDomain_management (gdb, rDomainName, 'Values from 0 to 4', 'DOUBLE', 'RANGE', 'DEFAULT', 'DEFAULT')
    SetValueForRangeDomain_management(gdb, rDomainName, 0, 4)      

def dRange0_6(igdb):
    gdb = igdb
    rDomainName = 'dRange0_6'
    CreateDomain_management (gdb, rDomainName, 'Values from 0 to 6', 'DOUBLE', 'RANGE', 'DEFAULT', 'DEFAULT')
    SetValueForRangeDomain_management(gdb, rDomainName, 0, 6)     
    
def dRange0_8(igdb):
    gdb = igdb
    rDomainName = 'dRange0_8'
    CreateDomain_management (gdb, rDomainName, 'Values from 0 to 8', 'DOUBLE', 'RANGE', 'DEFAULT', 'DEFAULT')
    SetValueForRangeDomain_management(gdb, rDomainName, 0, 8)    

def dCodedValueCrossingType(igdb):    
    cDomainName = 'dRCType'
    cdDomainValueDict = {"Ped":"Pedestrian Crossing", "Pri":"Private Vehicle Crossing", "Pub":"Public Vehicle Crossing"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  


def dMaterialList(igdb):    
    cDomainName = 'dRCcMaterials'
    cdDomainValueDict = {"T":"Timber", "A":"Asphalt", "AT":"Asphalt and Timber", "C":"Concrete", "CR":"Concrete and Rubber", 
                         "M":"Metal", "U":"Unconsolidated", "P":"Composite", "O":"Other"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Material', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName          
    
def dCodedCrossingStatus(igdb):    
    cDomainName = 'dRCStatus'
    cdDomainValueDict = {"A":"Crossing Actively Used", "RA":"Railroad Abandonment", "RC":"Road closed", "TU":"Tracks present but Unusable", 
                         "TR":"Tracks Removed", "XC":"Crossing Closed"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Status', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName      
       
    
def dCodedValueAlignment(igdb):    
    cDomainName = 'dRCAlignment'
    cdDomainValueDict = {"T":"Tangent", "C":"Curve"}
    CreateDomain_management  (gdb, cDomainName, 'Alignment between railroad and roadway', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName      
    

def dRange0_100(igdb):
    gdb = igdb
    rDomainName = 'dRange0_100'
    CreateDomain_management (gdb, rDomainName, 'Value between 0 and 100', 'DOUBLE', 'RANGE', 'DEFAULT', 'DEFAULT')
    SetValueForRangeDomain_management(gdb, rDomainName, 0, 100)       

def dRange10_220(igdb):
    gdb = igdb
    rDomainName = 'dRange10_220'
    CreateDomain_management (gdb, rDomainName, 'Values between 10 and 220', 'DOUBLE', 'RANGE', 'DEFAULT', 'DEFAULT')
    SetValueForRangeDomain_management(gdb, rDomainName, 10, 220)       
    
def dRange0_90(igdb):
    gdb = igdb
    rDomainName = 'dRange0_90'
    CreateDomain_management (gdb, rDomainName, 'Value between 0 and 90', 'DOUBLE', 'RANGE', 'DEFAULT', 'DEFAULT')
    SetValueForRangeDomain_management(gdb, rDomainName, 0, 90)    
        
def dCodedValueDomainDevelopmentZoned(igdb):    
    cDomainName = 'dRCcDevelopmentZoned'
    cdDomainValueDict = {"C":"Commercial", "I":"Industrial", "G":"Institutional", "O":"Open Space", "R":"Residential"}
    CreateDomain_management  (gdb, cDomainName, 'Zoning or Development in Area of Crossing', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName      
    
def dCodedValueDomainLocSource(igdb):    
    cDomainName = 'dRCcLocSource'
    cdDomainValueDict = {"A":"Actual", "E":"Estimated"}
    CreateDomain_management  (gdb, cDomainName, 'Valid Reference Directions', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dCodedValueDomainNearCity(igdb):    
    cDomainName = 'dRCcNearCity'
    cdDomainValueDict = {"C":"Within City Limits", "NO":"Near or Outside City Limits"}
    CreateDomain_management  (gdb, cDomainName, 'Valid Reference Directions', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName         
    
def dCodedValueDomainDistrict(igdb):    
    cdDomainValueDict = {"1":"1", "2":"2", "3":"3","4":"4","5":"5","6":"6"}
    cDomainName = 'dcDistrict'
    CreateDomain_management  (gdb, cDomainName, 'Valid Reference Directions', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName     
    
def dCodedValueDomainYN(igdb):    
    cdDomainValueDict = {"Y":"Yes", "N":"No"}
    cDomainName = 'dYesNo'
    CreateDomain_management  (gdb, cDomainName, 'Valid Reference Directions', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName 
    
def dCoordinateX(igdb):
    gdb = igdb
    rDomainName = 'dRangeLongitude'
    CreateDomain_management (gdb, rDomainName, 'Valid Longitude Range for Kansas', 'DOUBLE', 'RANGE', 'DEFAULT', 'DEFAULT')
    SetValueForRangeDomain_management(gdb, rDomainName, -102.0511217, -94.607190)
    
def dCoordinateY(igdb):
    gdb = igdb
    rDomainName = 'dRangeLatitude'
    CreateDomain_management (gdb, rDomainName, 'Valid Latitude Range for Kansas', 'DOUBLE', 'RANGE', 'DEFAULT', 'DEFAULT')
    SetValueForRangeDomain_management(gdb, rDomainName, 36.9936542, 40.0030821)

    
def dDirection(igdb):
    gdb = igdb 
    
    cdDomainValueDict = {"E":"East", "N":"North", "NE":"Northeast", "NW":"Northwest", "S":"South", "SE":"Southeast", "SW":"Southwest", "W":"West"}
    cDomainName = 'dDirection'
    CreateDomain_management  (gdb, cDomainName, 'Valid Reference Directions', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName
    
def dCity(igdb):
    #tblCityList = MakeTableView_management('Database Connections\SDEPROD_SHARED.sde\SHARED.CITY_LIMITS', 'CityList', gdb)
    TableToDomain_management(CityList, "CITYNUMBER", "CITY", gdb, "dCityNum", "List of Cities in Kansas")
    print "added dCityNum domain"
    
def dCounty(igdb):
    #tblCityList = MakeTableView_management('Database Connections\SDEPROD_SHARED.sde\SHARED.CITY_LIMITS', 'CityList', gdb)
    TableToDomain_management(CountyList, "COUNTY_NO", "COUNTY_NAME", gdb, "dCountyNum", "List of Counties in Kansas", 'REPLACE')
    print "added dCountyNum domain"
    #some geomedia using moron copied and pasted woodson county into the county boundary layer again
    
def dMUTCDCode(igdb):
    #MUTCD codes exist in an ESRI Sign Inventory Data Model for State Government, source geodatabase is defined at the top.
    cDomainName = 'dSignCode'
    print gdb+'/MUTCD'
    DomainToTable_management(MUTCDList, 'SignCode',gdb+'/MUTCD', 'Code', 'Description')
    TableToDomain_management(gdb+'/MUTCD', 'Code', 'Description', gdb, cDomainName, 'MUTCD Sign Code', 'REPLACE')
    
def dCodedValueDomain(igdb):    
    cdDomainValueDict = {"E":"East", "N":"North", "NE":"Northeast", "NW":"Northwest", "S":"South", "SE":"Southeast", "SW":"Southwest", "W":"West"}
    cDomainName = 'dDirection'
    CreateDomain_management  (gdb, cDomainName, 'Valid Reference Directions', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName

def GdbCreate():
    CreateFileGDB_management(workspace, gdbname)
    CreateFeatureclass_management(gdb, 'Crossings', 'POINT', '#', 'DISABLED', 'ENABLED', spatialCRS)

def RestartGDB():
    if Exists(gdb): 
        Delete_management(workspace + '/'+gdbname+'.gdb')
        print "Gdb deleted"

if __name__ == '__main__':
    main()
    pass