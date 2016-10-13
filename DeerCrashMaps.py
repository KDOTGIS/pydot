'''
Created on Oct 11, 2016
The script creates the deer crash sign policy map based on the sign policy criteria
5 crashes in one quarter mile per year
15 crashes in one mile per year
Apply this forlmula to the last three years 
for all deer related crashes
note that the policy only applies to the state highway system
off state highway system crash locations can be reviewed 
delete those from the publication map if appropriate

to do:
drop non-essential in_memory files asap

@author: kyleg
'''
#Process:
#copy deer crashes to in memory workspace, one feature class per year
#buff


def DeerCrashWarningSignProcess():
    from arcpy import FeatureClassToFeatureClass_conversion, SpatialJoin_analysis, Buffer_analysis, FeatureToPoint_management, SelectLayerByAttribute_management, DeleteRows_management
    
    
    #the buffer distances are the radius distance in miles.  
    #The policy refers to a whole distance
    #so we need the radius to make a buffer of that distance.
    #this dictionary contains the value pairs for the buffer radius, and the frequency count for that radius
    BufferDistances = {
                       0.125:5, 
                       0.5:15
                       }
    
    #the policy applies to the last three full years of crash data, this list contains those years
    CrashYears = [
                  2013, 
                  2014, 
                  2015
                  ]
    
    #this is the location of the Crash Data on GIS
    CrashData = r"Database Connections\gate@gateprod.sde\GATE.KGATE_ACCIDENTS"
    
    #loop through each year, then loop through each radius and count for each year
    for Year in CrashYears:
        #create a selection expression for each year
        CrashSelect = "ACC_YEAR = "+str(Year)+" AND DEER_ACCS = 1"
        #create an output variable for each year
        DeerCrashYear = 'DeerCrash'+str(Year)
        #bring each data year to in memory feature class
        FeatureClassToFeatureClass_conversion(CrashData, 'in_memory', DeerCrashYear,  CrashSelect)
    
        #print CrashSelect
        
        #now loop through each radius/count for the crash year
        for distance, crashcount in BufferDistances.items():
            
            #test the dictionary values
            #print str(distance), str(crashcount)
            
            i = "in_memory/"
            
            #create the buffer output name
            DeerCrashYearBuf = DeerCrashYear+"_"+str(int(distance*1000))
            
            #create the buffer
            Buffer_analysis(DeerCrashYear, i+DeerCrashYearBuf, str(distance)+" Miles", "FULL", "ROUND", "NONE", "", "PLANAR")
            
            #join all in_memory deer crashes per year to the buffer, and count the total number of deer crashes (points) intersecting the buffer area
            SpatialJoin_analysis(DeerCrashYearBuf, DeerCrashYear, i+DeerCrashYearBuf+"_SJ", "JOIN_ONE_TO_ONE", "KEEP_COMMON", "#", "INTERSECT", "", "")
            
            #delete the buffer areas that don't have a count meeting the threshold
            selectionexpression = '"Join_Count" <'+str(crashcount)
            SelectLayerByAttribute_management(DeerCrashYearBuf+"_SJ", "NEW_SELECTION", selectionexpression)
            DeleteRows_management(DeerCrashYearBuf+"_SJ")
            
            #represent the deer crash locations meeting the criteria as points for the deer sign policy map
            FeatureToPoint_management(i+DeerCrashYearBuf+"_SJ", i+DeerCrashYearBuf+"_pt", "CENTROID")
        
DeerCrashWarningSignProcess()