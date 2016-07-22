'''
Created on Jun 21, 2016

@author: kyleg
'''
from arcpy import ImportXMLWorkspaceDocument_management, ChangePrivileges_management, env, EnableEditorTracking_management

from config_collector import ODB

env.workspace = ODB

database = "Collector20160621.Geo"

Datasets = "Collector20160621.Geo.Railroad;Collector20160621.Geo.RoadSide;Collector20160621.Geo.Roadway;Collector20160621.Geo.Signs"
#DatasetList = ["Collector.SDE.RailroadCrossing", "Collector.SDE.RoadSide", "Collector.SDE.Roadway", "Collector.SDE.Signs"]

## Have to assign Collector user in SQL Management Studio security mapping first.

ChangePrivileges_management(Datasets, user="Collector", View="GRANT", Edit="GRANT")

## Enabling Editor Tracking by feature dataset doesnt work in python at 10.3.1 - would have to do it by feature class, or apply to FD in catalog
## Add GUIDS

EnableEditorTracking_management()