'''
Created on Jun 24, 2015

@author: kyleg
'''
from arcpy import (CreateFileGDB_management, CreateFeatureclass_management, AddField_management, CreateDomain_management, 
                   DomainToTable_management, CreateDomain_management, AddCodedValueToDomain_management, MakeTableView_management, 
                   TableToDomain_management, SetValueForRangeDomain_management)
                  
from arcpy.management import AddField

workspace ='C:/temp'
version = '01'
spatialCRS = ''
gdbname = 'RailCrossing'+str(version)
gdb = workspace + '/'+gdbname+'.gdb'
print gdb


def main():
    #GdbCreate(workspace, gdbname)
    #dDirection(gdb)
    #dCity(gdb)
    #dCounty(gdb)
    #dCoordinateX(gdb)
    #dCoordinateY(gdb)
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
    cDomainName = 'dGeneric'
    cdDomainValueDict = {"0T":"No Turn", "0L":"No Left Turn", "0R":"No Right Turn", "00":"None", 
                         "R":"Red", "SZ":"School Zone", "TY":"Truck Yard", "Y":"Yellow"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dENSPhone(igdb):  
    cDomainName = 'dGeneric'
    cdDomainValueDict = {"800-832-5452":"800-832-5452 BNSF",
                         "620-649-3280":"620-649-3280 Cimarron Valley", 
                         "800-914-7850":"800-914-7850 Garden City Western",\
                         "866-386-9321":"866-386-9321 Kansas & Oklahoma",\
                         "877-527-9464":"877-527-9464 Kansas City Southern",\
                         "913-551-2179":"913-551-2179 Kansas City Terminal ",\
                         "800-800-3490":"800-800-3490 Kyle",\
                         "800-533-9416":"800-533-9416 Nebraska, Kansas, Colorado",\
                         "913-785-0720":"913-785-0720 New Century AirCenter",\
                         "866-386-9321":"866-386-9321 South Kansas & Oklahoma",\
                         "800-848-8715":"800-848-8715 Union Pacific",\
                         "800-639-5054":"800-639-5054 V & S",\
                         "800-832-5452":"800-832-5452 Wichita Terminal"}
    CreateDomain_management  (gdb, cDomainName, 'Emergency Phone Number', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dMUTCDno(igdb):  
    cDomainName = 'dGeneric'
    cdDomainValueDict = {"MUTCD signage number list"}
    CreateDomain_management  (gdb, cDomainName, 'MUTCD Sign Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName

def dStrPrefix(igdb):  
    cDomainName = 'dGeneric'
    cdDomainValueDict = {"AVE":"Avenue", "BLVD":"Boulevard", "CIR":"Circle", "DR":"Drive", "HWY":"Highway", 
                         "LN":"Lane", "PKWY":"Parkway", "PL":"Place", "RD":"Road", "ST":"Street", "TER":"Terrace", "WAY":"Way"}
    CreateDomain_management  (gdb, cDomainName, 'Road Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dRdSuffix(igdb):  
    cDomainName = 'dGeneric'
    cdDomainValueDict = {"I":"Interstate","US":"US Route", "SH": "State Highway", "CR":"County Road", 
                         "TL":"Toll Road", "LS":"Local Street", "FM":"Farm to Market"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dSpeedLim(igdb):  
    cDomainName = 'dGeneric'
    cdDomainValueDict = {"10":"10 mph","15":"15 mph","20":"20 mph","25":"25 mph","30":"30 mph",
                         "35":"35 mph","40":"40 mph","45":"45 mph","50":"50 mph","55":"55 mph",
                         "60":"60 mph","65":"65 mph","70":"70 mph","75":"75 mph","80":"80 mph"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dSpeedReg(igdb):  
    cDomainName = 'dGeneric'
    cdDomainValueDict = {"P":"Posted", "S":"Statutory"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dNHS(igdb):  
    cDomainName = 'dGeneric'
    cdDomainValueDict = {"I":"Interstate National Highway System", "N":"Non-Federal-Aid", "O":"Other Federal-Aid Highway-Not NHS", 
                         "H":"Other National Highway System"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  
    
def UrbanRural(igdb):  
    cDomainName = 'dGeneric'
    cdDomainValueDict = {"U":"Urban", "R":"Rural"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  
    
def dFunClass(igdb):  
    cDomainName = 'dGeneric'
    cdDomainValueDict = {"1":"Interstate", "2":"Other Freeway and Exressway", "3":"Other Principal Arterial", 
                         "4":"Minor Arterial", "5":"Major Collector", "6":"Minor Collector", "7":"Local"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  

def dApproach(igdb):  
    cDomainName = 'dGeneric'
    cdDomainValueDict = {"1a":"Approach Side Only", "2":"Both Approach and Depart Sides", 
                         "1d":"Depart Side only", "0":"Neither Approach nor Depart Sides"}
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  
    
def dRailRoadAdmo(igdb):  
    cDomainName = 'dGeneric'
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
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName  
    
def dTrackType(igdb):  
    cDomainName = 'dGeneric'
    cdDomainValueDict = {"I":"Industry", "S":"Siding", "T":"Transit", "Y":"Yard" }
    CreateDomain_management  (gdb, cDomainName, 'Railroad Crossing Type', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
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
    TableToDomain_management('Database Connections\SDEPROD_SHARED.sde\SHARED.CITY_LIMITS', "CITYNUMBER", "CITY", gdb, "dCityNum", "List of Cities in Kansas")
    print "added dCityNum domain"
    
def dCounty(igdb):
    #tblCityList = MakeTableView_management('Database Connections\SDEPROD_SHARED.sde\SHARED.CITY_LIMITS', 'CityList', gdb)
    TableToDomain_management('Database Connections\SDEPROD_SHARED.sde\SHARED.counties', "COUNTY_NO", "COUNTY_NAME", gdb, "dCountyNum", "List of Counties in Kansas")
    print "added dCountyNum domain"
    
    
def dCodedValueDomain(igdb):    
    cdDomainValueDict = {"E":"East", "N":"North", "NE":"Northeast", "NW":"Northwest", "S":"South", "SE":"Southeast", "SW":"Southwest", "W":"West"}
    cDomainName = 'dDirection'
    CreateDomain_management  (gdb, cDomainName, 'Valid Reference Directions', 'TEXT', 'CODED', 'DEFAULT', 'DEFAULT')
    for code in cdDomainValueDict:        
        AddCodedValueToDomain_management(gdb, cDomainName, code, cdDomainValueDict[code])
    print cDomainName
    
def CrossingFields(workspace):
    #The letter contains a parity check or some type of logic that is required based on the number.  Leading zeros are required.
    AddField_management('ENS_ID_N', 'TEXT', precision ='#', scale='#', length='7', 
                        alias ='ENS Crossing Number', Nullable = 'NULLABLE', Required = 'NON_REQUIRED' , Domain = '#')
    
def GdbCreate(iworkspace, igdb):
    gdb = igdb
    workspace = iworkspace
    CreateFileGDB_management(iworkspace, gdb)
    outpathfc = workspace + '/'+gdbname+'.gdb'
    CreateFeatureclass_management(outpathfc, 'Crossings', 'POINT', '#', 'DISABLED', 'ENABLED', spatialCRS)
    
'''
    AddField_management(ENS_ID_N    ENS Crossing Number    Text(7)                            
    InspDir    Direction of Inspection (or Approach)    Text(2)    coded value    dDirection        East, North, Northeast, Northwest, South, Southeast, Southwest, West        East, North, Northeast, Northwest, South, Southeast, Southwest, West    
    InvDate    Inventory Date    Date            current date            Calendar  DD-MMM-YYYY    inspection date
    InvBy    Inventoried by (name(s))    Text(55)    (track changes - edited by)        user name    active directory user name            need acutal name
    XInstallDate    Crossing Installation Date    Date                            
    XInstallProj    Crossing Project ID    text(9)                            Project numbner
                                        
def Location                                        
    City    City    Text(3)    coded value    dCity        List of cities            
    County    County    Text(3)    coded value    dCounty        List of 100 counties            
    Latitude    Latitude    Number(24,7)    range    dKSLat        34-39        Must be seven digit to the right of the decimal point.  (Middle of railroad tracks and roadway)  example 37.8687700    
    Longitude    Longitude    Number(24,7)    range    dKSLong        -94--101        Must be seven digit to the right of the decimal point.  (Middle of railroad tracks and roadway) example -97.6722970    
    LocSource    Lat/Long Source    Text(3)    coded value    dSource    Actual    Actual, Estimated        Actual, Estimated    
    Power    Power    boolean    coded value    dYesNo        Yes, No        Yes, No    estimates usually come from Railroad companies, KDOT does actual location.  Actual location means we located the site.  
    District    District    Text(3)    coded value    dDistrict        1, 2, 3, 4, 5, 6        1, 2, 3, 4, 5, 6    is there electricity there?  Can you see a powerline that is within about 50 feet of the intersection?
    CityVicin    City In Near Indicator    Text(3)    coded value    dCityNear        Within City Limits, Near/Outside City Limits        Within City Limits, Near/Outside City Limits    what is the closest city?  
    OnSHS    On State Highway System    boolean    coded value    dYesNo                Non-State System (Rural), Non-State System (City Classified), State System    
    Position    FRA Crossing Position    Text(3)    coded value    dPosition        At Grade, Railroad Over, Railroad Under        At Grade, Railroad Over, Railroad Under    
    Zoning    Development:    Text(12)    coded value    dZoned        Commercial, Industrial, Institutional, Open Space, Residential        Commercial, Industrial, Institutional, Open Space, Residential    
    Quiet    Quiet Zone    boolean    coded value    dYesNo        Yes, No        Yes, No    
    Public    Open to Public    boolean    coded value    dYesNo        Yes, No        Yes, No    
                                        
def Geometry                                        
    Angle    Crossing Angle    Number    range    dRange0_90        0-90        0 to 14 degrees, 15 to 29 degrees, 30 to 44 degrees, 45 to 59 degrees, 60 to 74 degrees, 75 to 90 degrees    what is the smallest angle between the railroad and the roadway?
    Length    Surface Length Feet    Number(6,1)    range    dLength10_220        10-220        By full or half foot measurement    what is the length of the trackage crossing surface at the roadway? The surface length of the crossing is measured in the general direction of the roadway width, perpendicular to the roadway. The measurement should be done with a wheel, rounded to one half of a foot.
    Separation    Distance to Separation Feet    Number(6,1)    range    dLength0_100                If less than 100 feet on the same roadway    what is the distance between multiple rails at a crossing
    Gouge    Gouge Marks    boolean    coded value    dYesNo        Yes, No        Yes, No    
    LeftAlign    Left Rail Alignment    Text(3)    coded value    dAlignment        Tangent, Curve        Tangent, Curve    within about 600 feet of the crossing, is the railroad straight (tangent) or is there a horizontal curve (Curve)?
    RightAlign    Right Rail Alignment    Text(3)    coded value    dAlignment                Tangent, Curve    within about 600 feet of the crossing, is the railroad straight (tangent) or is there a horizontal curve (Curve)?
    DownRoad    Track Down Road    boolean    coded value    dYesNo        Yes, No        Yes, No    
    RdWidth    Roadway Width (Feet)    Number(6,1)    range    dLength10_220                By full or half foot measurement    width of the driving surface (curb to curb, no shoulders) of the road at the crossing location, to one-half foot.
    AppAlign    Approach Alignment    Text(3)    coded value    dAlignment                Tangent, Curve    within about 500 feet of the crossing, is the roadway straight (tangent) or is there a horizontal curve (Curve)?
    DeptAlign    Depart Alignment    Text(3)    coded value    dAlignment                Tangent, Curve    within about 500 feet of the crossing, is the roadway straight (tangent) or is there a horizontal curve (Curve)?
                                        
                                        
def General                                        
    Status    Crossing Status    Text(12)    coded value    dStatus        Crossing Actively Used, Railroad Abandonment, Road closed, Tracks present but Unusable, Tracks Removed, Crossing Closed        Crossing Actively Used, Railroad Abandonment, Road closed, Tracks present but Unusable, Tracks Removed, Crossing Closed    
    Material    Mainline Surface Material     Text(12)    coded value    dMaterialKDOT        Asphalt, Asphalt and Flange, Concrete, Concrete and Rubber, Metal, Other, Rubber, Timber, Unconsolidated        Asphalt, Asphalt and Flange, Concrete, Concrete and Rubber, Metal, Other, Rubber, Timber, Unconsolidated, Composite    KDOT and FRA have different materials lists, merge the lists by adding composite. Composite means there are two distinct materials from the list used at the crossing.  
    Type    FRA Crossing Type    Drop down list    coded value    dCrossingType        Pedestrian Crossing, Private Vehicle Crossing, Public Vehicle Crossing        Pedestrian Crossing, Private Vehicle Crossing, Public Vehicle Crossing    
    Quadrants    Quadrants Blocks    Number(2)    range    dRange0_5                    At 23 feet from the track (8 feet back from the stop) is there anything blocking the view from the road the track?  If there is, anything blocking, how many quadrants are blocked?
    Illumination    Crossing Illumination    Drop down list    coded value    dYesNo        Yes, No        Yes, No    
    Narrative    Narrative    Text(99)                        Limited to 99 spaces    
                                        
def Warning Device                                        
    Crossbuck    Crossbucks    Number(2)    range    dRange0_8        0-6        Enter a count of the number of mast or posts with mounted crossbucks, not a count of the number of crossbucks.    
    XBReflect    Crossbuck Reflectorization    Drop down list    coded value    dReflective        Nonreflectorized, Prismatic, Reflectorized        Nonreflectorized, Prismatic, Reflectorized    
    FlashLight    Flashing Light Pairs    Number(2)    range    dRange0_18                    
    Lens    Lens Size    Drop down list    coded value    dFlashLight        Regular pair, 6 inch diameter, 8 inch diameter, 10 inch diameter, 12 inch diameter        Regular pair: 6 inch diameter, 8 inch diameter, 10 inch diameter, 12 inch diameter    
    Masts    Mast Count    Number(2)    range    dRange0_6    III3D                
    MastLightType    Mast Light Type    Drop down list    coded value    dtLightType    III3D    Incandescent, LED, Both            
    MastLightConfig    Mast Light Configuration    Drop down list    coded value    dMastLightConfig    III3D    Back, Side            
    CantOver    Cantilever Over Thru Lanes    Number(2)    range    dRange0_4    III3C                
    CantNotOver    Cantilever Not Over Thru Lanes    Number(2)    range    dRange0_4    III3C                this the number of cantilvever structures over a turn lane, parking lane, auxillary lane, shoulder, or other than the thru lanes.  
    CantOverType    Cantilever Flashing Light    Drop down list    coded value    dLightType    III3C    Incandescent, LED, Both            
    NoGatesRd    Number of Gates Roadway    Number(2)    range    dRange0_8    III 3 A                
    NoGatesPed    Number of Gates Sidewalk    Number(2)    range    dRange0_8    III 3 A                
    GateLight    Gate Mounted Flashing Lights    boolean    coded value    dYesNo                Yes, No    
    Horn    Wayside Horn    boolean    coded value    dYesNo    III3G                
    Bells    Bells    Number    range    dRange0_4    III3I                
    QuadGates    Four Quad Gates Present    boolean    coded value    dYesNo        Yes, No        Yes, No    
    GateChan    Channelization with Gates    Text(4)    coded value    dSideDesc    r    Both Sides, One Side, Neither Side        Both Sides, One Side, Neither Side    
    TrafSig    Traffic Signals    Number(2)    range    dRange0_4                    how many traffic signals are acitvated by the train at the crossing?  Assume that any traffic signal is train activated. 
    HwyTrafSig    Highway Traffic Signals controling crossing    boolean    coded value    dYesNo    III3H                
    FlshOthr    Other Flashing Lights    Number(2)    range    dRange0_12    III3K                 
    FlshOthrTyp    Other Flashing Lights Type    Text(12)        dFlashType        No Turn, No Left Turn, No Right Turn, None, Red, School Zone, Truck Yard, Yellow        No Turn, No Left Turn, No Right Turn, None, Red, School Zone, Truck Yard, Yellow    
    WInstallDate    Warning Device Installation Date    Date            III 3 F                
    WInstallProj    Warning Device Installation Project ID    text(9)                            
                                        
                                        
def Signage                                        
    W10_1    Advanced Warning Sign W10-1 Count    Number    range    dRange0_6                    
    W10_1a    yellow exempt warning sign    Number    range    dRange0_6                    
    W10_2    Advanced Warning Sign W10-2 Count    Number    range    dRange0_6                    
    W10_3    Advanced Warning Sign W10-3 Count    Number    range    dRange0_6                    
    W10_4    Advanced Warning Sign W10-4 Count    Number    range    dRange0_6                    
    W10_11    Advanced Warning Sign W10-11 Count    Number    range    dRange0_6                    
    W10_12    Advanced Warning Sign W10-12 Count    Number    range    dRange0_6                    
    W10_5    Hump Crossing Sign    Number    range    dRange0_6                    
    R15_3    white exempt sign on crossbuck    boolean    coded value    dYesNo                    
    AdvWrnSgnRef    Advanced Warning Signs Reflectivity    boolean    coded value    dYesNo                Yes, No    
    PostedNo    Crossing number Posted    boolean    coded value    dYesNo                Yes, No    
    HumpSign    Hump Signs Indicator    boolean    coded value    dYesNo                Yes, No    
    StopSign    Stop Signs    Number(2)    range    dRange0_5                    
    YieldSign    Yield Signs    Number(2)    range    dRange0_5                    
    NoESNSign    How many ENS signs posted    Number    range    dRange0_5                    
    EmgcySgn    Emergency Signs (ENS/DOT) 1-13    text    coded value    dRailPhone        Telephone Number list        Telephone Number list    
    MUTCD1    Other Sign MUTCD 1    Number(2)    range    dRange0_2                    
    MUTCDTyp1    Other Sign MUTCD Type 1    Drop down list    coded value    dMUTCDCode        MUTCD signage number list        MUTCD signage number list    
    MUTCD2    Other Sign MUTCD 2    Number(2)    range    dRange0_2                    
    MUTCDTyp2    Other Sign MUTCD Type 2    Drop down list    coded value    dMUTCDCode        MUTCD signage number list        MUTCD signage number list    
    MUTCD3    Other Sign MUTCD 3    Number(2)    range    dRange0_2                    
    MUTCDTyp3    Other Sign MUTCD Type 3    Drop down list    coded value    dMUTCDCode        MUTCD signage number list        MUTCD signage number list    
                                        
                                        
def Road Node                                        
    PreDir    Prefix Direction of Street    Text(2)    coded value    dDirection        East, North, Northeast, Northwest, South, Southeast, Southwest, West            
    StrName    Street Name    Text(64)                            
    StrType    Street Type    Text(10)    coded value    dStrType        Avenue, Boulevard, Circle, Drive, Highway, Lane, Parkway, Place, Road, Street, Terrace, Way        Avenue, Boulevard, Circle, Drive, Highway, Lane, Parkway, Place, Road, Street, Terrace, Way    
    RoadType    Roadway Type    Text(2)    coded value    dRdType        CR, I, LS, SR, TR, US        County Road, Interstate, Local City Street, State Route, Toll Road, U. S. Highway System    
    NoLanes    Traffic Lanes    Number(2,0)    range    dRange0_12                    
    ShldWidth    Shoulder Width (Feet)    Number(2,0)    range    dRange0_12                    
    ShldSurf    Shoulder Surface Indicator    boolean    coded value    dYesNo                Yes, No    
    SpeedLim    Speed Limit    Number(2,0)    coded value    dSpeedLim        10,15,20,25,30,35,40,45,50,55,60,65,70,75,80            
    SpeedReg    Speed Regulation    Text(2)    coded value    dSpeedReg        Posted, Statutory            
    Turnout    Truck Turnout    boolean    coded value    dYesNo                Yes, No    
    Curb    Curb Gutter    boolean    coded value    dYesNo                Yes, No    
    NHS    Highway System    text(2)    coded value    dNHS        Interstate National Highway System, Non-Federal-Aid, Other Federal-Aid Highway-Not NHS, Other National Highway System        Interstate National Highway System, Non-Federal-Aid, Other Federal-Aid Highway-Not NHS, Other National Highway System    
    EmergencyRoute    Emergency Services Route    boolean    coded value    dYesNo                    Route leads to an emergency service such as Hospital, Police, or Fire Station
    UrbanCode    Urban Rural    text(1)    coded value    dUrbanRural        Urban, Rural            
    Funclass    Functional Classification    text(1)    coded value    dFUN        1 Interstate, 2 Other Freeway and Exressway, 3 Other Principal Arterial, 4 Minor Arterial, 5 Major Collector, 6 Minor Collector, 7 Local        Rural Interstate 11, Rural Local Roads 31, Rural Major Collectors 21, Rural Minor Arterials 13, Rural Minor Collectors 22, Rural Other Pricipal Arterial 12, Urban Collectors 61, Urban Freeways and Expressways 52, Urban Interstate 51, Urban Local Streets 71, Urban Minor Arterials 54, Urban Other Principal Arterials 53    
    Sidewalk    Sidewalk    Text(4)    coded value    dSideDesc                Both Sides, One Side, Neither Side    
    PavMark    Pavement Markings    text(12)    coded value    dApproach    III.2F    Approach Side Only, Both Approach and Depart Sides, Depart Side only, Neither Approach nor Depart Sides        Approach Side Only, Both Approach and Depart Sides, Depart Side only, Neither Approach not Depart Sides    
    PavMarkStop    Stopline Pavement Markings    text(12)    coded value    dApproach    III.2F, III5            Approach Side Only, Both Approach and Depart Sides, Depart Side only, Neither Approach not Depart Sides    
    Channels    ChannelizationDevices    text(12)    coded value    dApproach    III.2G                
    Medians    ChannelizationMedians    boolean    coded value    dYesNo    III.2G                
    Passing    No Passing Lines    text(12)    coded value    dApproach                Approach Side Only, Both Approach and Depart Sides, Depart Side only, Neither Approach not Depart Sides    
    HwySigs    Nearby Highway Intersection Signals    boolean    coded value    dYesNo    III4a                
    AppHwyInt    Approach Nearby Intersecting Highway    Number(3,1)    range    dLength500                The measurement or No intersection within 500 feet of crossing (-1 = no)    
    AppSurfType    Approach Roadway Surface Type    Text(12)    coded value    dMaterial                Asphalt, Brick, Concrete, Earth, Gravel    
    AppHwySigs    Approach Intersecting Highway Signals    boolean    coded value    dYesNo                Yes, No    
    DepHwyInt    Depart Nearby Intersecting Highway    Number(3,1)    range    dLength500                The measurement or No intersection within 500 feet of crossing (-1 = no)    
    DepSurfType    Depart Roadway Surface Type    Text(12)    coded value    dMaterial                Asphalt, Brick, Concrete, Earth, Gravel    
    DepHwySigs    Depart Intersecting Highway Signals    boolean    coded value    dYesNo                Yes, No    
                                        
def Rail Node                                        
    OpCo    Operating Railroad Company    Text(12)    coded value            Railroad list for Kansas        Railroad list for Kansas    
    MainTrk    Main Tracks    Number(2,0)    range    dRange0_5                    
    OtherTrk    Other Tracks    Number(2,0)    range    dRange0_12                    
    OtherTrkDesc    Other Tracks Description    text(12)    coded value    dTrackType        Industry, Siding, Transit, Yard         Industry, Siding, Transit, Yard     
    Milepost    Railroad Milepost    Number(3,3)    range    dRange0_800                    
    Notes    Notes    Text(750)                        Limited to 750 spaces    
'''

if __name__ == '__main__':
    main()
    pass