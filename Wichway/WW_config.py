'''
Created on Oct 10, 2013

@author: kyleg
'''
#config to store url and directories


sdeConnectionString = "D:\\wichway\\harvesters\\python\\wichway_spatial.sde\\wichway_spatial.WICHWAY_SPATIAL.ConstructionSegments"

harvestEventUrl = 'http://prod.wichway.org/wichway/api/harvestevents' + '?apikey=0ec8f464-7b54-46a7-8d41-ae4571902ece'

logUrl = 'http://prod.wichway.org/wichway/api/harvesteventmessages' + '?apikey=0ec8f464-7b54-46a7-8d41-ae4571902ece'

jsonQueryLayer = 'http://prod.wichway.org/arcgis/rest/services/wichway/wichwaymap/MapServer/3/query?where=1%3D1&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&f=json'

sdeCDRS = "D:\\wichway\\harvesters\\python\\KRPublic.sde\\KANROAD.CDRS_ALERT_ROUTE"
sdeCDRSWZ = "D:\\wichway\\harvesters\\python\\KRPublic.sde\\KANROAD.CDRS_WZ_DETAIL"
stageDB = "D:\\wichway\\harvesters\\python"