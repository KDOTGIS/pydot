'''
Created on Apr 18, 2013

@author: kyleg
'''
import arcpy
arcpy.env.overwriteOutput = True 
ws = r"\\gisdata\arcgis\GISdata\KDOT\BTST\DeerAccs3.gdb"
arcpy.env.workspace = ws
#start with Accident Data points
crashlyr = "DeerCrashes"
sumlyr = "Deer_Crash_Summary"
#locate the points along the County Route LRS
arcpy.LocateFeaturesAlongRoutes_lr(crashlyr,"LRS_Route_CRM","LRS_KEY","0 Feet","LFAR_CRASHES","LRS_KEY POINT CRMP","FIRST","DISTANCE","ZERO","FIELDS","M_DIRECTON")
#Calculate the begin and end miles post integer around the CR_MP
arcpy.AddField_management("LFAR_CRASHES", "BeginCMP", "LONG")
arcpy.AddField_management("LFAR_CRASHES", "EndCMP", "LONG")
#take the crash location and calculate the integer part of the Logmile
arcpy.CalculateField_management("LFAR_CRASHES","BeginCMP","long( !CRMP! )","PYTHON_9.3","#")
#and add one to it - now we have the crashes overlapping every mile covering the extent of the LRS Geometry
arcpy.CalculateField_management("LFAR_CRASHES","EndCMP","long( !CRMP! )+1","PYTHON_9.3","#")
#locate the events now as lines 
#dissolve the lines as follows
arcpy.MakeRouteEventLayer_lr("LRS_Route_CRM","LRS_KEY","LFAR_CRASHES","LRS_KEY LINE BeginCMP EndCMP","LFAR_CRASHES lines","#","ERROR_FIELD","NO_ANGLE_FIELD","NORMAL","ANGLE","LEFT","POINT")
arcpy.Dissolve_management("LFAR_CRASHES lines","LFAR_Dissolve","LRS_KEY;BeginCMP;EndCMP","ACCIDENT_KEY COUNT","SINGLE_PART","DISSOLVE_LINES")
arcpy.FeatureClassToFeatureClass_conversion("LFAR_Dissolve", ws, sumlyr)
arcpy.AddField_management(sumlyr, "ID1", "LONG")
#arcpy.CalculateField_management(sumlyr,"ID1","[OBJECTID]","VB","#")
#I used a cursor for fun!
cursor = arcpy.UpdateCursor(sumlyr)
for row in cursor:
    row.ID1 = row.OBJECTID
    cursor.updateRow(row)
# Delete cursor and row objects to remove locks on the data
del row
del cursor
#now we have the a single line every mile and can join the crashes and count.  
#make a list of years
yearlist = ['2009','2010','2011','2012']
# loop through the list doing the operations to def query, join, and count the annual crashes
for year in yearlist:
    #year = '2009' #FOR NON-LOOP TESTING
    #definition query expression
    selxpression = '"Year_" = '+"'"+year+"'"
    #output layer 
    outlyr = "DeerCrashes_"+year
    #just checking
    print "selecting "+ selxpression
    print "saving layer view as "+outlyr
    #execute the definition query - make feature layer
    arcpy.MakeFeatureLayer_management(crashlyr,outlyr, selxpression,"#", "#")
    #set up for next operation
    inlyr = "DeerCrashes_"+year    
    outlyr = "DeerCrashCount"+year
    Countfield = "DeerCrash"+year
    #count crashes for the year
    arcpy.SpatialJoin_analysis(sumlyr,inlyr,outlyr,"JOIN_ONE_TO_ONE","KEEP_ALL",'#',"INTERSECT","#","#")
    #Put the crashes for that year into that count field
    arcpy.AddField_management(sumlyr,Countfield,"LONG","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    arcpy.AddJoin_management(sumlyr, "ID1", outlyr, "ID1")
    #calc LFAR dissolve field with Join Count field, because looping doesnt keep adding fields
    calxp = "["+outlyr+".Join_Count]"
    calfield = sumlyr+"."+Countfield
    arcpy.CalculateField_management(sumlyr, calfield, calxp,"VB","#")
    arcpy.RemoveJoin_management(sumlyr,outlyr)
    #due ot the field mapping in the spatial join
    arcpy.DeleteField_management(outlyr,"TARGET_FID;Join_Count")
    #restart loop
    print "operations completed for year "+year
print "It worked!"