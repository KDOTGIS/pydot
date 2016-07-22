'''
Created on Mar 7, 2016

@author: kyleg
'''


from config_collector import ADB, ODB, SDE
print ODB

from arcpy import CreateVersion_management

def main():
    CollectorVersionCreate()


def CollectorVersionCreate():
    CreateVersion_management(ODB, 'sde.DEFAULT', 'Master', 'Private')
    print "created master version"
    CreateVersion_management(ODB, 'Master', 'KanPlan', 'Public')
    
    CreateVersion_management(ODB, 'Master', 'KanPlan_QA', 'Public')
    
    CreateVersion_management(ODB, 'KanPlan_QA', 'Collector', 'Public')
    
if __name__ == '__main__':
    print 'This program will Create the root Versions for the Collector Geodatabase -  is being run by itself'
    main()
else:
    print 'Reconcile and Post  imported from another module'
## Version Tree:
##
##                DEFAULT
##                MASTER
##    KANPLAN                KANPLAN QA
##                            COLLECTOR    
##                                enumerate - FieldCollector User Sync Checkout - disconnected Edits_XXXXXXXXXXXXX
##
##