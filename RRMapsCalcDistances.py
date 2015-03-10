'''
Created on Mar 12, 2013

@author: kyleg
'''
import arcpy
#export working railroad files to shapefiles 

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "ActiveLines2013"
arcpy.CalculateField_management("ActiveLines2013","LRSKEY","""[RAILROAD] &"_" & [SUBDIVISIO]""","VB","#")

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "ActiveLines2013"
arcpy.CreateRoutes_lr("ActiveLines2013","LRSKEY","//gisdata/arcgis/GISdata/KDOT/BTP/Projects/RAIL/R1.shp","ONE_FIELD","LENGTHMILE","#","UPPER_RIGHT","1","0","IGNORE","INDEX")

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "ActiveStations", "R1"
arcpy.LocateFeaturesAlongRoutes_lr("ActiveStations","R1","LRSKEY","1 Miles","//gisdata/arcgis/gisdata/kdot/btp/projects/rail/stationlraf","LRSKEY POINT MEAS","FIRST","DISTANCE","ZERO","FIELDS","M_DIRECTON")

#Make Route event layer

# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "ActiveLines2013", "ActiveStationsSnap"
arcpy.SplitLineAtPoint_management("ActiveLines2013","ActiveStationsSnap","//gisdata/arcgis/GISdata/KDOT/BTP/Projects/RAIL/SplitLines.shp","50 Feet")