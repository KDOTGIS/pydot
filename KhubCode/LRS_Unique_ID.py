'''
Created on Mar 5, 2015
Updated 2/16/2017

this was the process at one time used to calculate unique Route IDs for Non State System local LRS Keys
its now modified to calculate the unique ID part of the route number for local roads from conflation
it need to be modified more, the incrementer part is just calculating everything as '00'


@author: kyleg
'''
from arcpy import da, MakeFeatureLayer_management, RemoveJoin_management, Dissolve_management, Delete_management, AddField_management, CalculateField_management, Sort_management, AddJoin_management
#target = r"Database Connections\SDEPROD_SHARED.sde\SHARED.NON_STATE_SYSTEM"
target = 'Database Connections\Conflation2012_ga.sde\Conflation.SDE.NG911\Conflation.SDE.RoadCenterlines'

#target = r'C:\temp\dissolces.gdb\LocalDissolve2'
#target = r"Database Connections\SDETEST_SHARED.sde\SHARED.Non_STATE_SYSTEM_SAMPLE"
#workspace = r"Database Connections\SDEPROD_SHARED.sde"
#env.workspace = workspace

def main():
    UniqueIDgen()
    pass



def UniqueIDgen():
    for i in range(87, 88):
        c = str(i).zfill(3)
        #print "filling in unique Route IDs for county %s" %c
        expression = "LRS_ROUTE_PREFIX = 'L' AND LRS_COUNTY_PRE = '%s'" %c
        layer = "County"+c
        MakeFeatureLayer_management(target, layer, expression)
        #this part of the script performs a couple types of dissolves  to create a unique set of numbers in 4 characters for every route in a county
        #first, do an unsplit dissolve for each local road in the county based on the RD, STS, and POD fields
        #this creates nice segments from which to build the destination routes
        Dissolve_management(layer, "in_memory/"+layer+"d1", "RD;STS;POD;LRS_COUNTY_PRE", "GCID COUNT", "SINGLE_PART", "UNSPLIT_LINES")
        #add, calculate, and index a field for a join operation
        #cant add index to in memory database so skip that part
        AddField_management(layer+"d1", "ConCatRtName", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
        AddField_management(layer+"d1", "RouteNum1", "TEXT", "", "", "6", "", "NULLABLE", "NON_REQUIRED", "")
        AddField_management(layer+"d1", "UniqueNum1", "TEXT", "", "", "3", "", "NULLABLE", "NON_REQUIRED", "")
        CalculateField_management(layer+"d1", "ConCatRtName", """[LRS_COUNTY_PRE]&[RD] & [STS] & [POD] """, "VB", "")
        #dissolve the unsplit dissolve layer to a multipart, full dissolve to get unique road names
        Dissolve_management(layer+"d1", "in_memory/"+layer+"d2", "ConCatRtName;RouteNum1", "", "MULTI_PART", "DISSOLVE_LINES")
        #A spatial sort here might be nice
        #Calculate a unique 4 digit number for each road name
        #I'm just using the Object ID to calculate the unique number string, with a spatial sort another incrementation method would be needed
        #the road names should mostly be unique, so a spatial sort at this level would only be beneficial of there is POD field is the only road name distinction
        #otherwise an attribute sort would be sufficient, if necessary
        CalculateField_management("in_memory/"+layer+"d2", "RouteNum1", "str(!OBJECTID!).zfill(4)", "PYTHON_9.3", "")
        # add the unique id field and increment each duplicate road name part 
        # calculate that unique number back to the split dissolve
        AddJoin_management(layer+"d1", "ConCatRtName", "County087d2", "ConCatRtName", "KEEP_ALL")
        CalculateField_management(layer+"d1", layer+"d1.RouteNum1", "["+layer+"d2.RouteNum1]", "VB", "")
        #AddField_management("in_memory/"+layer+"d2", "UniqueNum1", "TEXT", "", "", "3", "", "NULLABLE", "NON_REQUIRED", "")
        RemoveJoin_management(layer+"d1")
        #try this spatial sort thing here    
        Sort_management("in_memory/"+layer+"d1", "in_memory/"+layer+"d1_Sort", "Shape ASCENDING;RouteNum1 ASCENDING", "LL")
        #now we run the incrementer to calcualte the unique ID's
        #the incrementer isnt working here, but it is calculating a unique ID on for the segments, and it is going it better and much faster than the join method  
        #it might be better to use the incrementer to do this calculation on the sorted table, then figure out the unique ID
        Incrementer("in_memory/"+layer+"d1")
        Delete_management("in_memory/"+layer+"d1")
        Delete_management("in_memory/"+layer+"d2")
        Delete_management("in_memory/"+layer+"d2_Sort")
        
        
def Incrementer(layer):
    #this function calcualtes the unique number for multiple route ID numbers
    fields = ['UniqueNum1', 'RouteNum1']
    string0 = '0000'
    rows = da.UpdateCursor(layer, fields) 
    counter = 0
    for row in rows:
        if string0 == row[1]:
            countstring = str(counter).zfill(2)
            row[0] = countstring
            rows.updateRow(row)
            counter += 1
        else:
            string0 = str(int(string0)+1).zfill(4)
            countstring = str(counter).zfill(2)
            row[0] = countstring
            rows.updateRow(row)
            counter += 1
    del rows
    
def CounterReset():
    counter = 0


if __name__ == '__main__':
    main()
    
    pass
