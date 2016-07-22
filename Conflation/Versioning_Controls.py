'''
Created on Oct 12, 2015

@author: kyleg
'''

from arcpy import (AnalyzeDatasets_management, ReconcileVersions_management, Compress_management, DisableArchiving_management, 
    UnregisterAsVersioned_management, RegisterAsVersioned_management, EnableArchiving_management, CreateVersion_management,
    DisconnectUser, CreateReplica_management, CreateFileGDB_management, RebuildIndexes_management)
from arcpy.management import CreateFileGDB
input_database_as_owner="Database Connections/conflation_sqlgis_geo.sde"
input_database_as_admin="Database Connections/conflation_sqlgis_admin.sde"
include_system="NO_SYSTEM"
edit_versions="GEO.Master"
out_log="F:/Cart/projects/ARNOLD POOLED FUND/geodata/sqlgis_conflation/version_compress_log"
NG_FeatureDataset = r"Conflation.GEO.NG911"
in_datasets=   """
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.NoConflation_NG;
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.NoConflation_NonState;
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.NoConflation_RampInterchange;
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.NoConflation_StateSystem;
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_AuthoritativeBoundary;
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_CountyBoundary;
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_EMS;
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_ESZ;
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_FIRE;
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_LAW;
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_MunicipalBoundary;
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_PSAP;
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.Stitch_Lines;
    Conflation.GEO.DISCREPANCIES/Conflation.GEO.Stitch_Points;
    Conflation.GEO.KDOT/Conflation.GEO.INTR;
    Conflation.GEO.NG911/Conflation.GEO.AddressPoints;
    Conflation.GEO.NG911/Conflation.GEO.AuthoritativeBoundary;
    Conflation.GEO.NG911/Conflation.GEO.CountyBoundary;
    Conflation.GEO.NG911/Conflation.GEO.EMS;
    Conflation.GEO.NG911/Conflation.GEO.ESZ;
    Conflation.GEO.NG911/Conflation.GEO.FIRE;
    Conflation.GEO.NG911/Conflation.GEO.LAW;
    Conflation.GEO.NG911/Conflation.GEO.MunicipalBoundary;
    Conflation.GEO.NG911/Conflation.GEO.PSAP;
    Conflation.GEO.NG911/Conflation.GEO.RoadCenterlines
                """

if __name__ == '__main__':
    pass
    
def ReconcileChanges(KeepDelete, connected):
    if KeepDelete =='DELETE':
        with_delete=KeepDelete+"_VERSION"
    else:
        with_delete="KEEP_VERSION"
    AnalyzeandCompress(connected)
    ReconcileVersions_management(input_database_as_owner, "ALL_VERSIONS", "dbo.DEFAULT", edit_versions, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", with_delete)
    AnalyzeandCompress(connected)
    print "Versions reconciled"
    
def RemoveVersions(KeepDelete, connected):
    #choose to Keep or Delete the version being posted
    #will keep version by default
    if KeepDelete =='DELETE':
        with_delete=KeepDelete+"_VERSION"
    else:
        with_delete="KEEP_VERSION"
    ReconcileChanges(KeepDelete, connected)
    FD_in = input_database_as_owner+"/"+NG_FeatureDataset
    try:
        DisableArchiving_management(FD_in, preserve_history="PRESERVE")
    except:
        print "no archiving exists here"
    UnregisterAsVersioned_management(FD_in, keep_edit="KEEP_EDIT", compress_default="COMPRESS_DEFAULT")
    print "edits reconciled and database unregistered as versioned with the version with the "+with_delete +" option for child versions"
    
def ApplyVersioning():

    FD_in = input_database_as_owner+"/"+NG_FeatureDataset
    AnalyzeandCompress("Connected")
    
    #RegisterAsVersioned_management(FD_in, "NO_EDITS_TO_BASE")
    #have to reconnect after doing this it seems and manually do these ones, need to check on that 
    #manually,  these tasks take a while
    
    #EnableArchiving_management(FD_in)
    CreateVersion_management(input_database_as_owner, "dbo.DEFAULT", "Master", "PUBLIC")
    print "database registered as versioned, and a master version created"
    #create master version
    #create "load" version - although this is really edit version.
    #delete orphaned version views

def AnalyzeandCompress(ConnectorDisconnect):
    if ConnectorDisconnect == "Disconnect":
        DisconnectUser(input_database_as_admin, "*")
        print "users disconnected"
    else:
        print "proceeding to analyze and compress without disconnecting users"
    AnalyzeDatasets_management(input_database_as_owner, include_system, in_datasets, analyze_base="ANALYZE_BASE", analyze_delta="ANALYZE_DELTA", analyze_archive="ANALYZE_ARCHIVE")
    AnalyzeDatasets_management(input_database_as_admin, include_system="SYSTEM", in_datasets="", analyze_base="ANALYZE_BASE", analyze_delta="ANALYZE_DELTA", analyze_archive="ANALYZE_ARCHIVE")
    Compress_management(input_database_as_admin)
    print "Analyze and compress completed"
    
def CreateFileGDBReplica():
    outpath = "//gisdata/planning/Cart/projects/Conflation/GIS_DATA/replicas"
    outfile = "R2015102001.gdb"
    CreateFileGDB_management(outpath, outfile)
    CreateReplica_management(input_database_as_owner+"/Conflation.GEO.NG911", "CHECK_OUT", outpath+'/'+outfile, out_name="FGDB_CHECKOUT_"+outfile[:10], access_type="FULL", initial_data_sender="CHILD_DATA_SENDER", expand_feature_classes_and_tables="USE_DEFAULTS", reuse_schema="DO_NOT_REUSE", get_related_data="GET_RELATED", geometry_features="", archiving="ARCHIVING")
    
def RebuildIndexes():
    RebuildIndexes_management(input_database="Database Connections/conflation_sqlgis_admin.sde", include_system="SYSTEM", in_datasets="Conflation.dbo.SDE_compress_log", delta_only="ONLY_DELTAS")
    RebuildIndexes_management(input_database="Database Connections/conflation_sqlgis_geo.sde", include_system="NO_SYSTEM", in_datasets="CONFLATION.GEO.ADDRESSPOINTS_H;CONFLATION.GEO.ADDRESSPOINTS_H2;CONFLATION.GEO.ADDRESSPOINTS_H3;CONFLATION.GEO.ADDRESSPOINTS_H4;CONFLATION.GEO.AUTHORITATIVEBOUNDARY_H;CONFLATION.GEO.AUTHORITATIVEBOUNDARY_H2;CONFLATION.GEO.AUTHORITATIVEBOUNDARY_H3;CONFLATION.GEO.AUTHORITATIVEBOUNDARY_H4;CONFLATION.GEO.COUNTYBOUNDARY_H;CONFLATION.GEO.COUNTYBOUNDARY_H2;CONFLATION.GEO.COUNTYBOUNDARY_H3;CONFLATION.GEO.COUNTYBOUNDARY_H4;CONFLATION.GEO.EMS_H;CONFLATION.GEO.EMS_H2;CONFLATION.GEO.EMS_H3;CONFLATION.GEO.EMS_H4;CONFLATION.GEO.ESZ_H;CONFLATION.GEO.ESZ_H2;CONFLATION.GEO.ESZ_H3;CONFLATION.GEO.ESZ_H4;CONFLATION.GEO.FIRE_H;CONFLATION.GEO.FIRE_H2;CONFLATION.GEO.FIRE_H3;CONFLATION.GEO.FIRE_H4;CONFLATION.GEO.LAW_H;CONFLATION.GEO.LAW_H2;CONFLATION.GEO.LAW_H3;CONFLATION.GEO.LAW_H4;CONFLATION.GEO.MUNICIPALBOUNDARY_H;CONFLATION.GEO.MUNICIPALBOUNDARY_H2;CONFLATION.GEO.MUNICIPALBOUNDARY_H3;CONFLATION.GEO.MUNICIPALBOUNDARY_H4;CONFLATION.GEO.PSAP_H;CONFLATION.GEO.PSAP_H2;CONFLATION.GEO.PSAP_H3;CONFLATION.GEO.PSAP_H4;CONFLATION.GEO.ROADCENTERLINES_H;CONFLATION.GEO.ROADCENTERLINES_H2;CONFLATION.GEO.ROADCENTERLINES_H3;CONFLATION.GEO.ROADCENTERLINES_H4;Conflation.GEO.AddressPoints_H1;Conflation.GEO.AuthoritativeBoundary_H1;Conflation.GEO.CountyBoundary_H1;Conflation.GEO.DISCREPANCIES/Conflation.GEO.NoConflation_NG;Conflation.GEO.DISCREPANCIES/Conflation.GEO.NoConflation_NonState;Conflation.GEO.DISCREPANCIES/Conflation.GEO.NoConflation_RampInterchange;Conflation.GEO.DISCREPANCIES/Conflation.GEO.NoConflation_StateSystem;Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_AuthoritativeBoundary;Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_CountyBoundary;Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_EMS;Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_ESZ;Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_FIRE;Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_LAW;Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_MunicipalBoundary;Conflation.GEO.DISCREPANCIES/Conflation.GEO.Overlaps_Gaps_PSAP;Conflation.GEO.DISCREPANCIES/Conflation.GEO.Stitch_Lines;Conflation.GEO.DISCREPANCIES/Conflation.GEO.Stitch_Points;Conflation.GEO.EMS_H1;Conflation.GEO.ESZ_H1;Conflation.GEO.FIRE_H1;Conflation.GEO.KDOT/Conflation.GEO.COUNTIES;Conflation.GEO.KDOT/Conflation.GEO.INTR;Conflation.GEO.LAW_H1;Conflation.GEO.MunicipalBoundary_H1;Conflation.GEO.NG911/Conflation.GEO.AddressPoints;Conflation.GEO.NG911/Conflation.GEO.AuthoritativeBoundary;Conflation.GEO.NG911/Conflation.GEO.CountyBoundary;Conflation.GEO.NG911/Conflation.GEO.EMS;Conflation.GEO.NG911/Conflation.GEO.ESZ;Conflation.GEO.NG911/Conflation.GEO.FIRE;Conflation.GEO.NG911/Conflation.GEO.LAW;Conflation.GEO.NG911/Conflation.GEO.MunicipalBoundary;Conflation.GEO.NG911/Conflation.GEO.PSAP;Conflation.GEO.NG911/Conflation.GEO.RoadCenterlines;Conflation.GEO.PSAP_H1;Conflation.GEO.RoadCenterlines_H1", delta_only="ONLY_DELTAS")
    
    pass

def SynchronizeReplicas():
    pass

#RemoveVersions('KEEP', "Stay")
#ReconcileChanges('KEEP', "Stay")
#ReconcileChanges('KEEP', "Disconnect")
#ReconcileChanges('DELETE', "Disconnect")
RemoveVersions('DELETE', "Disconnect")

#ApplyVersioning()

#CreateFileGDBReplica()
