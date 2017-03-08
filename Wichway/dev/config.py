#config to store url and directories


sdeConnectionString = r"D:\wichway\harvesters\python\wichway_spatial.sde\wichway_spatial.WICHWAY_SPATIAL.ConstructionSegments"

harvestEventUrl = 'http://wichway.org/wichway/api/harvestevents' + '?apikey=0ec8f464-7b54-46a7-8d41-ae4571902ece'

logUrl = 'http://wichway.org/wichway/api/harvesteventmessages' + '?apikey=0ec8f464-7b54-46a7-8d41-ae4571902ece'

jsonQueryLayer = 'http://wichway.org/arcgis/rest/services/wichway/harvest/MapServer/3/query?where=1%3D1&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&f=json'

sdeCDRS = r"D:\wichway\harvesters\python\KRPublic.sde\KANROAD.CDRS_ALERT_ROUTE"
sdeCDRSWZ = r"D:\wichway\harvesters\python\KRPublic.sde\KANROAD.CDRS_WZ_DETAIL"

stageDB = r"D:\wichway\harvesters\python"

sdeWichwayCDRS = r"D:\wichway\harvesters\python\wichway_spatial.sde\wichway_spatial.WICHWAY_SPATIAL.CDRS_Segments"

WWDB = r"D:/wichway/harvesters/python/Wichway_Spatial_Dev.sde"
WWHDB = r"D:/wichway/harvesters/python/Wichway_Harvest_Dev.sde"
WWLRS = WWHDB+"/INTERSEC_BASEMAP_WEBMERC"
WWConstHar = WWHDB+"/wichway_spatial.WICHWAY_SPATIAL.CDRS_segments"
WWConstruction = WWDB+"/wichway_spatial.WICHWAY_SPATIAL.CDRS_segments"
mapdoc = "D:/wichway/agsmaps/CDRS_HARVESTER.mxd"
