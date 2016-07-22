'''
Created on May 4, 2016

@author: kyleg
'''

from config_collector import ADB, ODB, SDE
import os
from arcpy import ReconcileVersions_management, ListVersions, AnalyzeDatasets_management, Compress_management, ListDatasets, env, ListTables, ListFeatureClasses
env.workspace = ODB

def main(ODB):
    Analyzer(ODB)
    Reconciler(ODB)
    Compress_management(ODB)
    Analyzer(ODB)
    print "completed database maintenance activities"
    
def Reconciler(startworkspace):
    env.workspace = startworkspace
    skip_versions = ['GEO.Master', 'sde.DEFAULT']
    postversionlist = []
    for version in ListVersions(SDE):
        if version not in skip_versions:
            print " "+version
            postversionlist.append(str(version))
    ReconcileVersions_management(SDE, "ALL_VERSIONS", "GEO.Master", postversionlist, "LOCK_ACQUIRED", abort_if_conflicts="NO_ABORT", conflict_definition="BY_OBJECT", conflict_resolution="FAVOR_TARGET_VERSION", with_post="POST", with_delete="KEEP_VERSION")
    print "Versions reconciled and posted to SDE.Master"

def Analyzer(startworkspace):
    env.workspace = startworkspace
    dataList = ListTables() + ListFeatureClasses() 
    
    for dataset in ListDatasets("*", "Feature"):
        env.workspace = os.path.join(startworkspace, dataset)
        dataList += ListFeatureClasses() + ListDatasets()
        AnalyzeDatasets_management(startworkspace, include_system="NO_SYSTEM", in_datasets=dataList, analyze_base="ANALYZE_BASE", analyze_delta="ANALYZE_DELTA", analyze_archive="ANALYZE_ARCHIVE")
        print "analyzed " + str(dataList)
    env.workspace = SDE
    AnalyzeDatasets_management(SDE, include_system="SYSTEM", in_datasets="", analyze_base="ANALYZE_BASE", analyze_delta="ANALYZE_DELTA", analyze_archive="ANALYZE_ARCHIVE")
    print "analyzed system tables"

    env.workspace = startworkspace
    
if __name__ == '__main__':
    print 'This program - Reconcile and Post -  is being run by itself'
    main(ODB)
else:
    print 'Reconcile and Post  imported from another module'
                
