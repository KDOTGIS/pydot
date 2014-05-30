'''
Created on Mar 3, 2014

@author: kyleg
'''
def CityLimitsMod():
    from arcpy import MakeFeatureLayer_management, Erase_analysis, Append_management, env, CalculateField_management, Dissolve_management, FeatureToLine_management
    env.overwriteOutput= 1
    modfile = r'Database Connections\SDEPROD_GIS.sde\GIS.Administrative_Boundary\GIS.CITY_LIMITS_MODS_KDOT'
    taxfile = r'Database Connections\SDEPROD_GIS.sde\GIS.Administrative_Boundary\GIS.CITY_LIMITS_KDOR'
    CalculateField_management(modfile,"LOAD_DATE","str(datetime.datetime.now( ))[0:4]+str(datetime.datetime.now( ))[5:7]+str(datetime.datetime.now( ))[8:10]","PYTHON_9.3","#")
    MakeFeatureLayer_management(modfile,"CITY_LIMITS_MODS_ADD","MODTYPE = 'ADD'","#","#")
    MakeFeatureLayer_management(modfile,"CITY_LIMITS_MODS_SUBTRACT","MODTYPE = 'SUBTRACT'","#","#")
    KDOTcity = r'Database Connections\SDEPROD_GIS.sde\GIS.Administrative_Boundary\GIS.CITY_LIMITS'
    CityTemp = r'Database Connections\SDEPROD_GIS.sde\GIS.Administrative_Boundary\GIS.TempCity'
    Erase_analysis(taxfile,"CITY_LIMITS_MODS_SUBTRACT",CityTemp,"#")
    Append_management("CITY_LIMITS_MODS_ADD", CityTemp,"NO_TEST","#","#")
    Dissolve_management(CityTemp, KDOTcity,"CITYNUMBER;CITY;COUNTY;DIST;TYPE;POPCENSUS;POPCURRENT;ID1","LOAD_DATE MAX","MULTI_PART","DISSOLVE_LINES")
    CityOutlines = r"Database Connections/SDEPROD_GIS.sde/GIS.Administrative_Boundary/GIS.CITY_LIMITS_LN"
    FeatureToLine_management("GIS.CITY_LIMITS", CityOutlines,"0.01 Feet","ATTRIBUTES")
    
    
if __name__ == '__main__':
    CityLimitsMod()
    print "updated city limits in SDEPROD"
    pass