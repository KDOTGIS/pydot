'''
Created on Oct 31, 2013

@author: kyleg
'''
from arcpy import MakeFeatureLayer_management, Intersect_analysis, LocateFeaturesAlongRoutes_lr, MakeRouteEventLayer_lr, env, AddField_management, CalculateField_management, AddJoin_management, RemoveJoin_management 

try:
    from config import nonstate, connection1, interchange, NewRouteKey, NewRoute, ws, citylimits, schema
except:
    pass

env.workspace = ws
env.overwriteOutput = True
env.MResolution = 0.0001
env.MTolerance = 0.0002 

def NONSTATE_INT():
    print "add intersection points where state routes intersect non-state routes"
    MakeFeatureLayer_management(nonstate, 'NON_STATE_SYSTEM', "CITYNUMBER IS NOT NULL AND CITYNUMBER<999")
    MakeFeatureLayer_management(connection1+NewRoute, NewRoute)
    Intersect_analysis("CCL_LRS_ROUTE #;'NON_STATE_SYSTEM' #",connection1+"Intersect_NONSTATE","ALL","5 Feet","POINT") #this doesnt reference the newroute variable, its easier that way
    MakeFeatureLayer_management(connection1+"Intersect_NONSTATE", "NSI")
    LocateFeaturesAlongRoutes_lr("NSI","CCL_LRS_ROUTE",NewRouteKey,"5 Feet",connection1+"INTR_CCL_NS","CCL_LRS POINT MEASURE","ALL","DISTANCE","ZERO","FIELDS","M_DIRECTON")
    MakeRouteEventLayer_lr("CCL_LRS_ROUTE",NewRouteKey,connection1+"INTR_CCL_NS","CCL_LRS POINT MEASURE","INTR_CCL_NS Events","#","ERROR_FIELD","ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
    AddField_management("INTR_CCL_NS Events", "CITY", "TEXT", "#", "#", "100")
    AddJoin_management("INTR_CCL_NS Events", "CITYNUMBER", citylimits, "CITYNUMBER")
    CalculateField_management("INTR_CCL_NS Events", schema+"INTR_CCL_NS_Features.CITY", "!GIS_DEV.CITY_LIMITS.CITY!", "PYTHON_9.3")    
    RemoveJoin_management("INTR_CCL_NS Events", "#")
   
def STATE_INT():    
    print "add intersect intersection points that are state - state intersections and interchanges"
    MakeFeatureLayer_management(interchange, 'INTR', "ON_STATE_NONSTATE = 'S'")
    LocateFeaturesAlongRoutes_lr("INTR","CCL_LRS_ROUTE",NewRouteKey,"5 Feet",connection1+"INTR_CCL","CCL_LRS POINT MEASURE","ALL","DISTANCE","ZERO","FIELDS","M_DIRECTON")
    MakeRouteEventLayer_lr("CCL_LRS_ROUTE",NewRouteKey,connection1+"INTR_CCL","CCL_LRS POINT MEASURE","INTR_CCL_Events","#","ERROR_FIELD","ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
    AddField_management("INTR_CCL_Events", "CITY", "TEXT", "#", "#", "100")
    AddField_management("INTR_CCL_Events", "CITYNUMBER", "Long", "#", "#", "#")
    CalculateField_management("INTR_CCL_Events", "CITYNUMBER", "int(!CCL_LRS![0:3])", "PYTHON_9.3")  
    AddJoin_management("INTR_CCL_Events", "CITYNUMBER", citylimits, "CITYNUMBER")
    CalculateField_management("INTR_CCL_Events", schema+"INTR_CCL_Features.CITY", "!GIS_DEV.CITY_LIMITS.CITY!", "PYTHON_9.3")    
    RemoveJoin_management("INTR_CCL_Events", "#")
    
    
if __name__ == '__main__':    
    NONSTATE_INT()
    STATE_INT()

print "completed"