'''
Created on Jan 28, 2015

@author: kyleg
'''

if __name__ == '__main__':
    pass

from arcpy import env, AcceptConnections, CreateVersion_management, Compress_management, RebuildIndexes_management, ListVersions, ReconcileVersions_management, AnalyzeDatasets_management
#import datetime

connection = r'D:\SCHED\SDEPROD_SDE.sde'
shared_schema = r'D:/SCHED/SDEPROD_SHARED.sde'

env.workspace = connection
env.overwriteOutput = True
try:
    AcceptConnections(connection, True)
    versionList = ListVersions(connection)
    print "versions identified:"
    for version in versionList:
        for version in versionList:
            if version == "SDE.DEFAULT":
                print "no child versions from Default version"
            else:
                print version
                ReconcileVersions_management(connection, "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "DELETE_VERSION", "D:/SCHED/LOGS/reconcilelog.txt")
                CreateVersion_management(shared_schema, "SDE.DEFAULT", version, "PUBLIC")
                print version + "version reconciled"
    AnalyzeDatasets_management(connection, "SYSTEM", "SDE.COMPRESS_LOG", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
    print "database analyzed"
    Compress_management(connection)
    print "database compressed"
    RebuildIndexes_management(connection,"SYSTEM","SDE.COMPRESS_LOG","ALL")
    print "indexes rebuilt"
    AnalyzeDatasets_management(connection, "SYSTEM", "SDE.COMPRESS_LOG", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
    print "database analyzed"
    AcceptConnections(connection, True)
except:
    AcceptConnections(connection, True)
    
    