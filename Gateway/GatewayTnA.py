'''
Created on Aug 13, 2014
Truncate and Append LRS elements from the Gateway MXD to static features classes in the Gateway SQL server GEodatabase
Moved to Production on Aug 20 2014
@author: kyleg
'''
from arcpy import mapping, Append_management,TruncateTable_management
GDB = r'D:\HNTB_GATEWAY\ProductionMOT\SQL54_GATEWAY15.sde'
mxd = mapping.MapDocument(r'D:\HNTB_GATEWAY\ProductionMOT\2014111401_GatewayExec.mxd')

lyrs = mapping.ListLayers(mxd)
#D:\HNTB_GATEWAY\ProductionMOT\SQL54_GATEWAY15.sde\Gateway2015.GATEWAY_SPATIAL.LongTermApproved
TargetLT= r"D:\HNTB_GATEWAY\ProductionMOT\SQL54_GATEWAY15.sde\Gateway2015.GATEWAY_SPATIAL.LongTermApproved"
TargetST = r'D:\HNTB_GATEWAY\ProductionMOT\SQL54_GATEWAY15.sde\Gateway2015.Gateway_Spatial.ShortTermApproved'

print lyrs[0]
TruncateTable_management(TargetST)
Append_management(lyrs[0], TargetST, "NO_TEST", "#")

print lyrs[1]
TruncateTable_management(TargetLT)
Append_management(lyrs[1], TargetLT, "NO_TEST", "#")

#if __name__ == '__main__':
#    pass