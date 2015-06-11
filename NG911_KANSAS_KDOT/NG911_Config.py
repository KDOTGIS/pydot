#-------------------------------------------------------------------------------
# Name:        NG911_Config
# Purpose:      Configuration variables for the NG911 Data Check
#
# Author:      kristen
#
# Created:     24/09/2014
# Modified:    11/05/2014 by dirktall04
#-------------------------------------------------------------------------------

esb = ["ESB_EMS", "ESB_FIRE", "ESB_Law"] #list of layers that are emergency services boundaries
gdb = r'\\gisdata\arcgis\GISdata\DASC\NG911\DataRemediation_NG911\ATCi\Marshall County\Marshall County_1st_QA\KSNG911N_MS.gdb' #r"R:\BigDrives\internal\internal1\NG911_Pilot_Agg\Final_GIS_Data\Region1_PR_Final_KJ.gdb" #full path of the NG911 geodatabase
folder = r"E:\Kristen\Data\NG911\NG911_Metadata_Fix\Domains" #folder containing the magical text files
DOTRoads = r"\\gisdata\arcgis\GISdata\DASC\NG911\KDOTReview\KDOT_Roads.gdb"
ReviewPath = r"\\gisdata\arcgis\GISdata\DASC\NG911\DataRemediation_NG911\ATCi\Marshall County\Marshall County_1st_QA"


# These soundexNameExclusions entries are already checked for a space immediately following them.
# There is no need to add a trailing space as in "RD ". Use "RD" instead.
# Also, this means that "CR" will only be matched to road names like "CR 2500",
# it will not be matched to road names like "CRAFT".

#soundexNameExclusions = ["ROAD", "US HIGHWAY", "RD", "CO RD", "CR", "RS", "R", "STATE HIGHWAY", "STATE ROAD", "BUSINESS US HIGHWAY"]
#ordinalNumberEndings = ["ST", "ND", "RD", "TH"]

currentLayerList = ["RoadAlias", "AddressPoints", "RoadCenterline", "AuthoritativeBoundary", "CountyBoundary", "ESZ", "PSAP", "MunicipalBoundary"]
nonDisplayFields = ["ObjectID", "Shape", "Shape_Area", "Shape_Length"]

# This is a class used to pass information to the Data Check functions.
class pathInformationClass:
    def __init__(self):
        self.gdbPath = gdb
        self.domainsFolderPath = folder
        self.FinalPath = r"\\gisdata\arcgis\GISdata\DASC\NG911\Final"
        self.EntDB = r"\\gisdata\arcgis\GISdata\DASC\NG911\Final\geo@ng911.sde"
        self.EDBO = "geo"
        self.EFD = "NG911"
        self.EDBName = "NG911"
        self.addressPointsPath = ""
        self.fieldNames = ""
        self.otherPath = ""
        self.esbList = esb
        self.DOTRoads = DOTRoads
        self.PSAP = "Admin"
        

currentPathSettings = pathInformationClass()