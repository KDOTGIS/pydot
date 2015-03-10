#written by Kyle 10/11/12
# Description
# Select overridden endpoint coordinates, calculate the DMS from the position coordinates, and populate the fields for KAAT

import arcpy
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "SDE.RunwayEndpoint"
arcpy.CalculateField_management("SDE.RunwayEndpoint","FAACONVLATDD","float(!FAA_LAT_RNWY1![0:2])+float(!FAA_LAT_RNWY1![3:5])/60+float(!FAA_LAT_RNWY1![6:12])/3600","PYTHON_9.3","#")

arcpy.CalculateField_management("SDE.RunwayEndpoint","FAACONVLNGDD","float(!FAA_LNG_RNWY1! [0:3])+float(!FAA_LNG_RNWY1![4:6])/60+float(!FAA_LNG_RNWY1![7:14])/3600","PYTHON_9.3","#")

