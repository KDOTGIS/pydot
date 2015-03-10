'''
Created on Jan 28, 2015

@author: kyleg
'''

if __name__ == '__main__':
    pass

from arcpy import env, Compress_management, RebuildIndexes_management, CreateVersion_management, DisconnectUser, AcceptConnections, ListVersions, ReconcileVersions_management, AnalyzeDatasets_management
#import datetime

connection = r'D:\SCHED\SDEPROD_SDE.sde'
shared_schema = r'D:/SCHED/SDEPROD_SHARED.sde'

env.workspace = connection
env.overwriteOutput = True

AcceptConnections(connection, False)
print "connections blocked"
DisconnectUser(connection, "ALL")
print "users disconnected"
versionList = ListVersions(connection)
print "versions identified:"
for version in versionList:
    print version
ReconcileVersions_management(connection, "ALL_VERSIONS", "sde.DEFAULT", versionList, "LOCK_ACQUIRED", "NO_ABORT", "BY_OBJECT", "FAVOR_TARGET_VERSION", "POST", "DELETE_VERSION", "D:/SCHED/LOGS/reconcilelog.txt")
print "version reconciled"
AnalyzeDatasets_management(connection, "SYSTEM", "SDE.COMPRESS_LOG", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
print "database analyzed"
Compress_management(connection)
print "database compressed"
RebuildIndexes_management(connection,"SYSTEM","SDE.COMPRESS_LOG","ALL")
AcceptConnections(connection, True)
RebuildIndexes_management(shared_schema,"NO_SYSTEM","NON_STATE_SYSTEM","ALL")
print "indexes rebuilt"
print "Accepting connections"
AnalyzeDatasets_management(connection, "SYSTEM", "SDE.COMPRESS_LOG", "ANALYZE_BASE", "ANALYZE_DELTA", "ANALYZE_ARCHIVE")
print "database analyzed"
CreateVersion_management(shared_schema, "SDE.DEFAULT", "ESRI_EDIT", "PRIVATE")
print "edit version re-created"
