'''
Created on Oct 12, 2015

@author: kyleg
'''


if __name__ == '__main__':
    pass

def main():
    pass
    #LoadARegion()
    LoadAliasTables()

def LoadARegion():
    from arcpy import Append_management, ListFeatureClasses, ListDatasets, env, ListTables
    #importGDB = r"//gisdata/planning/Cart/projects/Conflation/GIS_DATA/GEO_COMM/REGION3_20151002/REGION3_20151002.gdb"
    #importGDB = r"\\gisdata\planning\Cart\projects\Conflation\GIS_DATA\GEO_COMM\REGION4_20151021\REGION4_20151021\REGION4_20151021.gdb"
    importGDB = r"\\gisdata\planning\Cart\projects\Conflation\GIS_DATA\GEO_COMM\REGION5_20151211\REGION5_20151211.gdb"
    LoadTarget = r"\\gisdata\planning\Cart\projects\Conflation\Workflow\conflation_sqlgis_geo.sde\Conflation.GEO."
    env.workspace = importGDB
    ### There are no tables in the conflated dataset products
    skiplist = ['Stitch_Lines', 'RoadCenterlines', 'Overlaps_Gaps_MunicipalBoundary', 'Overlaps_Gaps_FIRE', 'Overlaps_Gaps_LAW', 'Overlaps_Gaps_PSAP', 'Overlaps_Gaps_ESZ', 'Overlaps_Gaps_EMS', 'Overlaps_Gaps_CountyBoundary', 'Overlaps_Gaps_AuthoritativeBoundary']
    tables = ListTables()
    for table in tables:
        print table
        target = LoadTarget+table
        print target
        
    datasets = ListDatasets("*")
    for fd in datasets:
        print fd
        featureClasses = ListFeatureClasses("*", "All", fd)
        for fc in featureClasses:
            print fc
            if fc in skiplist:
                print 'skipping'
            else:
                target = LoadTarget+fd+"/"+fc
                print "loading to "+target
                Append_management(fc, target, schema_type="NO_TEST")
                
def LoadAliasTables():
    from arcpy import Append_management, env, ListTables, ListWorkspaces, CalculateField_management
    importFolder = r"\\gisdata\planning\Cart\projects\Conflation\GIS_DATA\R1\Alias3"
    LoadTarget = r"Database Connections\Conflation2012_sde.sde\Conflation.SDE.RoadAlias"
    env.workspace = importFolder
    GDBList = []
    for gdb in ListWorkspaces("*", "FileGDB"):
        GDBList.append(gdb)
    
    for geodatabase in GDBList:
        env.workspace = geodatabase
        tables = ListTables("RoadAlias")
        for table in tables:
            print table
            CalculateField_management(table, "SEGID", expression="""[STEWARD]&" "& [SEGID]""", expression_type="VB", code_block="")
            Append_management(table, LoadTarget, schema_type="NO_TEST")
        print geodatabase
        
        
        
'''        
        
    ### There are no tables in the conflated dataset products
    tables = ListTables()
    for table in tables:
        print table
        target = LoadTarget+table
        print target
        
    datasets = ListDatasets("*")
    for fd in datasets:
        print fd
        featureClasses = ListFeatureClasses("*", "All", fd)
        for fc in featureClasses:
            print fc
            if fc in skiplist:
                print 'skipping'
            else:
                target = LoadTarget+fd+"/"+fc
                print "loading to "+target
                Append_management(fc, target, schema_type="NO_TEST")
'''
main()