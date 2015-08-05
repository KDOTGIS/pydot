'''
Created on Apr 27, 2015

@author: kyleg
'''
import arcpy
ws = r"c:/temp"
arcpy.env.overwriteOutput= True
arcpy.env.workspace = ws
gdbname = "RailCrossing.gdb"

arcpy.CreateFileGDB_management(ws, gdbname)

gdb = ws+"/"+gdbname


domname1 = "Reporting_Agency"
domdict1 = {"Railroad":"Railroad", "Transit":"Transit", "State":"State", "Other":"Other"}
domname2 = "Upgrade_Resason"
domdict2 = {"Change in Data":"Change in Data", "Re-Open":"Re-Open", "New Crossing":"New Crossing", "Date Change Only":"Date Change Only",
            "Closed":"Closed", "Change in Primary Operating RR":"Change in Primary Operating RR", "No Train Traffic":"No Train Traffic",
            "Admin Correction":"Admin Correction",
            "Quiet Zone Update":"Quiet Zone Update" }

arcpy.CreateDomain_management(gdbname, domname1, domname1, "TEXT", "CODED")
for code in domdict1:
    arcpy.AddCodedValueToDomain_management(gdbname, domname1, code, domdict1[code])


'''Domains
Reason for Upgrade    Change in Data, Re-Open, New Crossing, Date Change Only, Closed, Change in Primary Operating RR, No Train Traffic, Admin Correction, Quiet Zone Update
City/Municipality    In, Near
Do Other Railroads Operate a Separate Track at Crossing?    Yes, No
Do Other Railroads Operate Over Your Track at Crossing?    Yes, No
Crossing Type    Public, Private
Crossing Purpose    Highway, Pedestrian Pathway, Pedestrian Station
Crossing Position    At Grade, RR Under, RR Over
Public Access    Yes, No
Type of Train    Freight, Intercity, Commuter, Transit, Shared Use Transit, Tourist/Other
Average Passenger Train Count Per Day    Less Than One Per Day, Number Per Day
Type of Land Use    Open Space, Farm, Residential, Commercial, Industrial, Institutional, Recreational, RR Yard
Is there an Adjacent Crossing with a Separate Number?    Yes, No
Quiet Zone    No, 24 hr, Partial, Chicago Excused
Lat/Long Source    Actual, Estimated
Check if Less Than One Movement Per Day    Yes, No
Track Detection (Main track only)    Constant Warning Time, Motion Detection, AFO, PTC, DC, Other, None
Is Track Signaled?    Yes, No
Event Recorder    Yes, No
Remote Health Monitoring    Yes, No
Are there Signs or Signals?    Yes, No
Advance Warning Signs (check all that apply)    None, W10-1, W10-2, W10-3, W10-4, W10-11, W10-12
Low Ground Clearance Sign    Yes, No
Pavement Markings    Stop Lines, RR Xing Symbols, Dynamic Envelope, None
Channelization Devices/Medians    All Approaches, One Approach, Median, None
EXEMPT Sign (R15-3)    Yes, No
ENS Sign (I-35) Displayed    Yes, No
Other MUTCD Signs    Yes, No
Private Crossing Signs (if private)    Yes, No
Gate Configuration    2 Quad, 3 Quad, 4 Quad, Full (barrier resistance), Median Gates
Cantilevered (or Bridged) Flashing Light Structures    Incandescent, LED
Mast Mounted Flashing Lights    Incandescent, Back Lights Included, LED, Side Lights Included
Wayside Horn    Yes, No
Highway Traffic Signals Controlling Crossing    Yes, No
Non-Train Active Warning    Flagging/Flagman, Manually Operated Signals, Watchman, Floodlighting, None
Does nearby Hwy Intersection have Traffic Signals?    Yes, No
Hwy Traffic Signal Interconnection    Not Interconnected, For Traffic Signals, For Warning Signs
Hwy Traffic Signal Preemption    Simultaneous, Advance
Highway Traffic Pre-Signals    Yes, No
Highway Monitoring Devices    Photo/Video Recording, Vehicle Presence Detection, None
Traffic Lanes Crossing Railroad    One-Way Traffic, Two-Way Traffic, Divided Traffic
Is Roadway/Pathway Paved?    Yes, No
Does Track Run Down a Street?    Yes, No
Is Crossing Illuminated?    Yes, No
Crossing Surface    Timber, Asphalt, Asphalt and Timber, Concrete, Concrete and Rubber, Rubber, Metal, Unconsolidated, Composite, Other
Intersecting Roadway within 500 feet?    Yes, No
Smallest Crossing Angle    0-29, 30-59, 60-90
Is Commercial Power Available?    Yes, No
Highway System    (01) Interstate Highway System, (02) Other Nat Hwy System (NHS), (03) Federal AID, Not NHS, (08) Non-Federal Aid
Functional Classification of Road at Crossing    (0) Rural, (1) Urban, (1) Interstate, (2) Other Freeways and Expressways, (3) Other Principal Arterial, (4) Minor Arterial, (5) Major Collector, (6) Minor Collector, (7) Local
Is Crossing on State Highway System?    Yes, No
Highway Speed Limit    Posted, Statutory
Regularly Used by School Buses?    Yes, No

fields:
ID    NAME    DATA_TYPE
A    Revision Date    Date
B    Reporting Agency    Text
C    Reason for Upgrade    Text
D    DOT Crossing Inventory Number    Number
1    Primary Operating Railroad    Text
2    State    Text
3    County    Text
4    City/Municipality    Text
5    Street/Road Name & Block Number    Text
6    Highway Type & No.    Text
7    Do Other Railroads Operate a Separate Track at Crossing?    Boolean
    If Yes, Specify RR    Text
8    Do Other Railroads Operate Over Your Track at Crossing?    Boolean
    If Yes, Specify RR    Text
9    Railroad Division or Region    Text
10    Railroad Subdivision or District    Text
11    Branch or Line Name    Text
12    RR Mileporst    Number
13    Line Segment    Text
14    Nearest RR Timetable Station    Text
15    Parent RR    Text
16    Crossing Owner    Text
17    Crossing Type    Text
18    Crossing Purpose    Text
19    Crossing Position    Text
20    Public Access    Boolean
21    Type of Train    Text
22    Average Passenger Train Count Per Day    Text
23    Type of Land Use    Text
24    Is there an Adjacent Crossing with a Separate Number?    Boolean
    If Yes, Provide Crossing Number    Text
25    Quiet Zone    Text
    Date Quiet Zone Established    Date
26    HSR Corridor ID    Number
27    Latitude in decimal degrees    Decimal
28    Longitude in decimal degrees    Decimal
29    Lat/Long Source    Text
30.A    Railroad Use    Text
30.B    Railroad Use    Text
30.C    Railroad Use    Text
30.D    Railroad Use    Text
31.A    Railroad Use    Text
31.B    Railroad Use    Text
31.C    Railroad Use    Text
31.D    Railroad Use    Text
32.A    Narrative    Text
32.B    Narrative    Text
33    Emergency Notification Telephone No    Number
34    Railroad Contact    Number
35    State Contact    Number
II 1    Estimated Number of Daily Train Movements    Number
II 1.A    Total Day Thru Trains (6AM to 6PM)    Number
II 1.B    Total Night Thru Trains (6PM to 6AM)    Number
II 1.C    Total Switching Trains    Number
II 1.D    Total Transit Trains    Number
II 1.E    Check if Less Than One Movement Per Day    Boolean
II 1.E.1    How many trains per week?    Number
II 2    Year of Train Count Date (yyyy)    Date
II 3    Speed of Train at Crossing    Number
II 3.A    Maximum Timetable Speed (mph)    Number
II 3.B    Typical Speed Range over Crossing (mph)    Number
II 4.A    Count of Main Tracks    Number
II 4.B    Count of Siding Tracks    Number
II 4.C    Count of Yard Tracks    Number
II 4.D    Count of Transit Tracks    Number
II 4.E    Counts of Industry Tracks    Number
II 5    Track Detection (Main track only)    Text
II 6    Is Track Signaled?    Boolean
II 7.A    Event Recorder    Boolean
II 7.B    Remote Health Monitoring    Boolean
III 1    Are there Signs or Signals?    Boolean
III 2.A    Crossbuck Assemblies Count    Number
III 2.B    Stop Sign (R1-1) Count    Number
III 2.C    Yield Signs (R1-2) Count    Number
III 2.D    Advance Warning Signs (check all that apply)    Text
III 2.D.1    W10-1 Count    Number
III 2.D.2    W10-2 Count    Number
III 2.D.3    W10-3 Count    Number
III 2.D.4    W10-4 Count    Number
III 2.D.5    W10-11 Count    Number
III 2.D.6    W10-12 Count    Number
III 2.E.1    Low Ground Clearance Sign    Boolean
III 2.E.2    If yes count    Number
III 2.F    Pavement Markings    Text
III 2.G    Channelization Devices/Medians    Text
III 2.H    EXEMPT Sign (R15-3)    Boolean
III 2.I    ENS Sign (I-35) Displayed    Boolean
III 2.J    Other MUTCD Signs    Boolean
III 2.J.1    If yes, Type    Text
III 2.J.2    If yes, count    Number
III 2.K    Private Crossing Signs (if private)    Boolean
III 2.L    LED Enhanced Signs (types)    Text
III 3.A.1    Gate Arms Roadway    Number
III 3.A.2    Gate Arms Pedestrian    Number
III 3.B    Gate Configuration    Text
III 3.C    Cantilevered (or Bridged) Flashing Light Structures    Text
III 3.C.1    Over Traffic Lane Count    Number
III 3.C.2    Not Over Traffic Lane Count    Number
III 3.D    Mast Mounted Flashing Lights    Text
III 3.D.1    Count of Masts    Number
III 3.E    Total Count of Flashing Light Pairs    Number
III 3.F    Installation Date of Current Active Warning Devices    Date
III 3.G    Wayside Horn    Boolean
III 3.G.1    If yes, Installation date    Date
III 3.H    Highway Traffic Signals Controlling Crossing    Boolean
III 3.I    Bells Count    Number
III 3.J    Non-Train Active Warning    Text
III 3.K    Other Flashing Lights or Warning Devices    Text
III 3.K.1    Other Flashing Lights or Warning Devices Count    Number
III 4.A    Does nearby Hwy Intersection have Traffic Signals?    Boolean
III 4.B    Hwy Traffic Signal Interconnection    Text
III 4.C    Hwy Traffic Signal Preemption    Text
III 5    Highway Traffic Pre-Signals    Boolean
III 5.1    If yes, Storage Distance    Number
III 5.2    If yes, Stop Line Distance    Number
III 6    Highway Monitoring Devices    Text
IV 1    Traffic Lanes Crossing Railroad    Text
IV 1.A    Number of lanes    Number
IV 2    Is Roadway/Pathway Paved?    Boolean
IV 3    Does Track Run Down a Street?    Boolean
IV 4    Is Crossing Illuminated?    Boolean
IV 5    Crossing Surface    Text
IV 5.1    Crossing Surface Installation Date    Date
IV 5.2    Crossing Surface Width    Number
IV 5.3    Crossing Surface Length    Number
IV 6    Intersecting Roadway within 500 feet?    Boolean
IV 6.1    If yes, Approximate Distance    Number
IV 7    Smallest Crossing Angle    Number
IV 8    Is Commercial Power Available?    Boolean
V 1    Highway System    Text
V 2    Functional Classification of Road at Crossing    Text
V 3    Is Crossing on State Highway System?    Boolean
V 4    Highway Speed Limit _____(mph)    Number
V 4.1    Highway Speed Limit    Text
V 5    Linear Referencing System (LRS Route ID)    Number
V 6    LRS Milepost    Number
V 7    Annual Average Daily Traffic (AADT)    Number
V 7.1    AADT year    Date
V 8    Estimated Percent Trucks    Number
V 9    Regularly Used by School Buses?    Boolean
V 9.1    If yes, average number per day    Number
V 10    Emergency Services Route    Boolean
'''