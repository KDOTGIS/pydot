'''
Created on May 12, 2016

This is what we are going to do:
Drop the versioning down to the default schema
    make sure to check the versions
    control the field collection units -
        schedule "last chance" to check in with field crews
        sync and manage the version checkouts on devices first - delete disconnected/downloaded/synced maps
        account for devices, users, and versions as rigorously as possible
Export the default XML schema with data/recordset
Drop the feature classes needing updates
inport the new XML schema
object load the data/recordset
    check that the changed schema items loaded as intended
reapply security settings/roles
reapply versioning structure
republish/overwrite map services
resynchronize collector devices/downloads


@author: kyleg
'''
from config_collector import ADB, ODB 
from arcpy import ExportXMLWorkspaceDocument_management, ReconcileVersions_management, ListVersions, env, DeleteVersion_management
import ReconcileAndPostVersions
import CreateVersions


def main():
    ReconcileAndPostVersions.Analyzer(ODB)
    ReconcileAndPostVersions.Reconciler(ODB)
    ReconcileAndPostVersions.Compress_management(ODB)
    ReconcileAndPostVersions.Analyzer(ODB)
    RandPWithDelete(ADB)
    ExportXMLWorkspaceDocument_management()
    print "main function of modify schema completed"
    pass

def RandPWithDelete(startworkspace):
    env.workspace = startworkspace
    skip_versions = ['dbo.DEFAULT']
    postversionlist = []
    for version in ListVersions(ADB):
        if version not in skip_versions:
            print " "+version
            postversionlist.append(str(version))
    ReconcileVersions_management(ADB, "ALL_VERSIONS", "dbo.DEFAULT", postversionlist, "LOCK_ACQUIRED", abort_if_conflicts="NO_ABORT", conflict_definition="BY_OBJECT", conflict_resolution="FAVOR_TARGET_VERSION", with_post="POST", with_delete="DELETE_VERSION")
    for version in ListVersions(ADB):
        if version not in skip_versions:
            print " "+version
            postversionlist.append(str(version))
            DeleteVersion_management(str(version))
    print "Versions reconciled and posted to Geo.Master - might be better to do this in catalog - hopefully it doesnt happen often"


if __name__ == '__main__':
    print 'This program - Modify Schema - is being run by itself'
    main()
else:
    print 'I am being imported from another module'
    
    
