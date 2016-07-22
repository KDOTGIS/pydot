'''
Created on Jun 8, 2016

@author: kyleg
'''

if __name__ == '__main__':
    pass

from arcpy import ImportXMLWorkspaceDocument_management, ChangePrivileges_management, env, EnableEditorTracking_management

from config_collector import ODB

env.workspace = ODB

xmlversion = r"\\gisdata\planning\GIS\datamodel\sparx\Design\Collector2016062100.XML"

ImportXMLWorkspaceDocument_management(ODB, xmlversion, import_type="SCHEMA_ONLY", config_keyword="GEOMETRY")


#Datasets = "Collector.SDE.RailroadCrossing;Collector.SDE.RoadSide;Collector.SDE.Roadway;Collector.SDE.Signs"
#DatasetList = ["Collector.SDE.RailroadCrossing", "Collector.SDE.RoadSide", "Collector.SDE.Roadway", "Collector.SDE.Signs"]

## Have to assign Collector user in SQL Management Studio security mapping first.

#ChangePrivileges_management(Datasets, user="Collector", View="GRANT", Edit="GRANT")

## Enabling Editor Tracking by feature dataset doesnt work in python at 10.3.1 - would have to do it by feature class, or apply to FD in catalog
## Add GUIDS