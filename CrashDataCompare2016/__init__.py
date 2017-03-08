'''
created by Kyle G
This script will compare the old KCaRS locations which were generally entered by the prisoners at KCI 
with the new accident locations, which were calculated by the KDOT/DASC Geocoding procedures

the crash data located by dasc included crashes with accident keys from 20100000001 to 20160109278

Unlocated by KCARS:
-94  40 Decimal Degrees

Unlocated by Geocoding
-93.5  40.5 Decimal Degrees
'''

from arcpy import MakeTableView_management, 

def ConnectTheDots():
    #Compare KCARS and geocoded accident layers by location
    #
    MakeTableView_management("KCARS_ACCIDENTS", "KCARS_ACCIDENTS_DOT_LAT_NONLOCATED", "DOT_LATITUDE is null ", "", "")



def CursorCopy():
    import pyodbc
    cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE=testdb;UID=me;PWD=pass')
    cursor = cnxn.cursor()
    cursor.execute("select user_id, user_name from users")
    rows = cursor.fetchall()
    for row in rows:
        print row.user_id, row.user_name
