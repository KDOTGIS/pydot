'''
Created on Mar 17, 2014

@author: kyleg
'''
from arcpy import da, env, Point, MakeQueryTable_management, GetCount_management, Delete_management, FeatureClassToFeatureClass_conversion, DeleteRows_management, Append_management, MakeXYEventLayer_management, ExecuteError, GetMessages, MakeFeatureLayer_management, CalculateField_management, AddJoin_management, MakeTableView_management,SelectLayerByAttribute_management
import datetime

fc = r'Database Connections\sdeprod_ciims.sde\CIIMS.CIIMS\CIIMS.Static_Crossings'
fields = ('CROSSINGLONGITUDE', 'CROSSINGLATITUDE', 'SHAPE@XY', 'LOADDATE')
tbl = r'Database Connections\sdeprod_CIIMS.sde\CIIMS.CIIMS_VWCROSSINGGIS3'
layer_name = 'Static_Crossings'
table_name = 'vwcrossings3'
workspace = r'Database Connections\sdeprod_ciims.sde'
env.overwriteOutput=1
newtbl = r'Database Connections\sdeprod_ciims.sde\CIIMS.NEWROWS'
deltbl = r'Database Connections\sdeprod_ciims.sde\CIIMS.DELROWS'

def PointDelete(fc, layer_name, deltbl, table_name):#delete rows from SDE CIIMS that are removed from CANSYS CIIMS
    MakeFeatureLayer_management(fc, layer_name)
    MakeTableView_management(deltbl, table_name)
    with da.SearchCursor(deltbl, "CROSSINGID") as delcur:
        for row in delcur:
            DelXID=  ("{0}".format(row[0]))
            print DelXID + " is being deleted from the CIIMS table"
            #AddJoin_management(layer_name,"CROSSINGID", deltbl, "CROSSINGID", "KEEP_ALL")
            delsel = "CROSSINGID LIKE '"+str(row)[3:10]+"'"
            SelectLayerByAttribute_management(layer_name,"ADD_TO_SELECTION",delsel)
    DeleteRows_management(layer_name)
    del fc, layer_name, deltbl, table_name
    print "Delete function completed"
def AddInsert(fc, layer_name, newtbl, workspace):   
    MakeTableView_management(newtbl,"NEWROWS_View","#","#","#")
    addcount = int(GetCount_management("NEWROWS_View").getOutput(0)) 
    if addcount == 0:
        print "no new records"
        pass
    else:
        MakeFeatureLayer_management(fc, layer_name)
        MakeXYEventLayer_management("NEWROWS_View","CROSSINGLONGITUDE","CROSSINGLATITUDE","NEWROWS_Layer","GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],VERTCS['NAVD_1988',VDATUM['North_American_Vertical_Datum_1988'],PARAMETER['Vertical_Shift',0.0],PARAMETER['Direction',1.0],UNIT['Meter',1.0]];-400 -400 1000000000;-100000 10000;-100000 10000;8.98315284119522E-09;0.001;0.001;IsHighPrecision","#")
        FeatureClassToFeatureClass_conversion("NEWROWS_Layer","D:/Temp","LOADTHIS1.shp","#","""CROSSINGID "CROSSINGID" true false false 30 Text 0 0 ,First,#,Database Connections/sdedev_ciims.sde/CIIMS.NEWROWS_Features,CROSSINGID,-1,-1;CROSSINGLA "CROSSINGLA" true true false 8 Double 10 38 ,First,#,Database Connections/sdedev_ciims.sde/CIIMS.NEWROWS_Features,CROSSINGLATITUDE,-1,-1;CROSSINGLO "CROSSINGLO" true true false 8 Double 10 38 ,First,#,Database Connections/sdedev_ciims.sde/CIIMS.NEWROWS_Features,CROSSINGLONGITUDE,-1,-1;CROSSINGTY "CROSSINGTY" true true false 2 Text 0 0 ,First,#,Database Connections/sdedev_ciims.sde/CIIMS.NEWROWS_Features,CROSSINGTYPE,-1,-1""","#")
        Append_management("D:/Temp/LOADTHIS1.shp",layer_name,"NO_TEST","""CROSSINGID "CROSSINGID" true false false 30 Text 0 0 ,First,#,D:/Temp/LOADTHIS1.shp,CROSSINGID,-1,-1;CROSSINGLATITUDE "CROSSINGLATITUDE" true true false 8 Double 10 38 ,First,#,D:/Temp/LOADTHIS1.shp,CROSSINGLA,-1,-1;CROSSINGLONGITUDE "CROSSINGLONGITUDE" true true false 8 Double 10 38 ,First,#,D:/Temp/LOADTHIS1.shp,CROSSINGLO,-1,-1;CROSSINGTYPE "CROSSINGTYPE" true true false 2 Text 0 0 ,First,#,D:/Temp/LOADTHIS1.shp,CROSSINGTY,-1,-1;LOADDATE "LOADDATE" true true false 36 Date 0 0 ,First,#""","#")
        Delete_management("D:/Temp/LOADTHIS1.shp","#")
        updatelyr = layer_name+"new"
        MakeFeatureLayer_management(layer_name, updatelyr,"LOADDATE IS NULL")
        with da.Editor(workspace) as edit:
            CalculateField_management(updatelyr,"LOADDATE","datetime.datetime.now( )","PYTHON_9.3","#")
        del fc, layer_name, newtbl, workspace, updatelyr
        print "new rows inserted into Static_Crossings"
def PointCheck(fc, fields, layer_name):
    # Use this to check any situations where the latitude or longitude attributes do not match the point location
    MakeFeatureLayer_management(fc, layer_name)
    with da.SearchCursor(fc, fields) as cursor:
        for row in cursor:
            rowx, rowy = (row[2])
            intolX = abs(row[0]-rowx)
            intolY = abs(row[1]-rowy)
            Tolerance = 0.00000001
            if intolX < Tolerance and intolY < Tolerance:
                pass
            else:
                print(row), row0x, rowxr, row0y, rowyr
    del fc, layer_name, fields
    print "all other points within tolerance"
def LatLongFields(fc, tbl, layer_name, table_name, workspace):    
    #Updates the XY attributes  values in the GIS database from the CANSYS table
    try:
        MakeFeatureLayer_management(fc, layer_name)
        #MakeTableView_management(tbl, table_name)
        MakeQueryTable_management(tbl, table_name,"USE_KEY_FIELDS","CIIMS.CIIMS_VWCROSSINGGIS3.CROSSINGID","#","#")
        AddJoin_management(layer_name,"CROSSINGID", table_name, "CROSSINGID", "KEEP_ALL")
        SelectLayerByAttribute_management(layer_name,"NEW_SELECTION","CIIMS.Static_Crossings.CROSSINGLATITUDE <> vwcrossings3.CROSSINGLATITUDE OR CIIMS.Static_Crossings.CROSSINGLONGITUDE <> vwcrossings3.CROSSINGLONGITUDE")
        with da.Editor(workspace) as edit:
            CalculateField_management(layer_name, 'CIIMS.Static_Crossings.CROSSINGLATITUDE', '!vwcrossings3.CROSSINGLATITUDE!', 'PYTHON_9.3')
            CalculateField_management(layer_name, 'CIIMS.Static_Crossings.CROSSINGLONGITUDE', '!vwcrossings3.CROSSINGLONGITUDE!', 'PYTHON_9.3')
            CalculateField_management(layer_name,"CIIMS.Static_Crossings.LOADDATE","datetime.datetime.now( )","PYTHON_9.3","#")
        del layer_name, fc, table_name, tbl
    except ExecuteError:
        print(GetMessages(2))   
def AttribFields(fc, tbl, layer_name, table_name, workspace):    
    #Updates the crossing type attribute values in the GIS database from the CANSYS table.  I believe this should work but needs to be tested more.  
    try:
        MakeFeatureLayer_management(fc, layer_name)
        MakeQueryTable_management(tbl, table_name,"USE_KEY_FIELDS","CIIMS.CIIMS_VWCROSSINGGIS3.CROSSINGID","#","#")
        AddJoin_management(layer_name,"CROSSINGID", table_name, "CROSSINGID", "KEEP_ALL")
        SelectLayerByAttribute_management(layer_name,"NEW_SELECTION","CIIMS.Static_Crossings.CROSSINGTYPE <> vwcrossings3.CROSSINGTYPE")
        with da.Editor(workspace) as edit:
            CalculateField_management(layer_name, 'CIIMS.Static_Crossings.CROSSINGTYPE', '!vwcrossings3.CROSSINGTYPE!', 'PYTHON_9.3')
            CalculateField_management(layer_name,"CIIMS.Static_Crossings.LOADDATE","datetime.datetime.now( )","PYTHON_9.3","#")
        del layer_name, fc, table_name, tbl
        print "attrib fields updated for crossing type"
    except ExecuteError:
        print(GetMessages(2))     
def PointGEOM(fc, tbl, workspace, layer_name, fields):
    #Updates the Geometry point location based on the XY attributes in the GIS table, run this after the XY attributes have been updated
    try:
        MakeFeatureLayer_management(fc, layer_name)
        Tolerance = 0.000001
        #start the edit operation
        edit = da.Editor(workspace)
        edit.startEditing()
        edit.startOperation()
        with da.UpdateCursor(fc, fields) as ucursor:
            for row in ucursor:
                point = Point(row[0], row[1])
                rowx, rowy = (row[2])
                rowvalues = (row[0], row[1], point, datetime.datetime.now())
                if (type(rowx) == float):   
                    intolX = abs(row[0]-rowx)
                    intolY = abs(row[1]-rowy)
                    if intolX < Tolerance and intolY < Tolerance:
                        pass 
                    else:
                        point = Point(row[0], row[1])
                        rowvalues = (row[0], row[1], point, datetime.datetime.now())
                        print (rowvalues)
                        ucursor.updateRow(rowvalues)
                    #print (rowvalues)  
                else:
                    point = Point(row[0], row[1])
                    rowvalues = (row[0], row[1], point, datetime.datetime.now())
                    print "these rows are outside the position tolerance:"
                    print (rowvalues) 
                    ucursor.updateRow(rowvalues)
        edit.stopOperation()
        edit.stopEditing(True)
        del layer_name, fc, fields, workspace
        print "point geometry updated"
    except ExecuteError:
        print(GetMessages(2))

if __name__ == '__main__':
    
    MakeTableView_management(deltbl, "delcheck")
    delcount = int(GetCount_management("delcheck").getOutput(0)) 
    if delcount > 0:
        print str(delcount)+" rows to delete"
        PointDelete(fc, layer_name, deltbl, table_name)
        pass
    else:
        pass
        print "no rows deleted"
    
    MakeTableView_management(newtbl,"NEWROWS_View","#","#","#")
    addcount = int(GetCount_management("NEWROWS_View").getOutput(0)) 
    if addcount > 0:
        print str(addcount)+" rows to add"
        AddInsert(fc, layer_name, newtbl, workspace) 
    else:
        print "no new records"
        pass
    LatLongFields(fc, tbl, layer_name, table_name, workspace)    
    AttribFields(fc, tbl, layer_name, table_name, workspace)
    PointGEOM(fc, tbl, workspace, layer_name, fields)
    AttribFields(fc, tbl, layer_name, table_name, workspace)
    #PointCheck(fc, fields, layer_name)
    pass