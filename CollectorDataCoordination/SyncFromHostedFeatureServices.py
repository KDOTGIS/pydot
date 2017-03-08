'''
Created on Jan 20, 2017

So... at this point...
the data model created in Sparx Enterprise Architect
it was exported to file geodatabase
that file geodatabase was copied to SQL server (dev, prod, etc)
the feature classes are staged in SQL Server (data loaded, relationships created, etc)
are INDIVIDUALLY published to hosted feature services 
data is being collected, edited, updated in the hosted feature service on KanPlan, 
and we need to get changes from the hosted environment to our local environment.

This script shall perform that synchronization

these scripts require  ArcGIS Pro and the Conda Python 3.5 libs
which have the ability to edit feature services in the pro environment 



@author: kyleg
'''
import arcpy

if __name__ == '__main__':
    pass

db = 'Klekt17'
dbo = 'SDE'
Railroad = ["MastCrossbuckAssembly", "RailCrossing", "Cantilever"]
Roadside = ["BrushTreeControl", "CulvertsPipes", "Ditch", "EdgeUnderDrains", 
            "ErosionControlDevices", "Fencing", "Guardrail", "Lighting", "LitterDebris", 
            "Obstacle", "PavedShoulder", "Permit", "Sidewalk", "SlopeErosion", "UnpavedShoulder", "VegetationWeedControl"]
Roadway = ["Crosswalk", "Gate", "Median", "MedianCrossover", "ParkingLanes", "PavDeformation", "PavFlexPotholes", "PavFlexRutting", 
           "PavMarking", "PavRigidCracking", "PavRigidFaulting", "PavRigidJointSealant", "PavRigidPotholes", "RumbleStripsLongitudinal",
            "RumbleStripTransverse", "ThroughLanes", "TurnLaneLeft", "TurnLaneRight"]
Signs = ["Signals", "Signs_Information", "Signs_Other", "Signs_Regulatory", "Signs_Warning"]

#first, ensure we are running the correct python.
def pyversion():
    #this script requires arcgis pro librarires of python 3.5x, which run from conda
    import sys
    print (sys.version)
    #this is not a check, this is a print of the sys environment version
    #if not running 3.5.x or Anaconda 4x or the latest for Pro, 
    #the environment needs to change for the python path
    
def syncfields(layer):
    #editor tracking should be enabled on the hosted feature services
    #when we sync to the local env (SQL server) we want to keep that edit tracking info
    #therefore we need to add new edit tracking fields for the local environment
    #we will also retain the edit tracking from the hosted environment
    railroadurlroot = r"\\gisdata\planning\cart\projects\KanPLan\MXD\HostedServices\Collect17\sde@Klekt17.sde\KLEKT17.SDE.Railroad\KLEKT17.SDE."
    arcpy.management.EnableEditorTracking(railroadurlroot+"MastCrossbuckAssembly", "sync_user", "loaded_date", "sync_over_user", "sync_over_date", "ADD_FIELDS", "UTC")
    arcpy.management.EnableEditorTracking(railroadurlroot+"RailCrossing", "sync_user", "loaded_date", "sync_over_user", "sync_over_date", "ADD_FIELDS", "UTC")
    arcpy.management.EnableEditorTracking(railroadurlroot+"Cantilever", "sync_user", "loaded_date", "sync_over_user", "sync_over_date", "ADD_FIELDS", "UTC")
    #in SQL server, add "sync_guid" as text which is the hosted feature service guid as text

def RepublishService():
    ''''when a service needs to be updated:

    communicate update to field community, have them all sync and remain on-hold
    update the data in the local repository, for collector apps the SQL server geodatabase
    once it's updated,  delete the service from KanPlan, it should be set to prevent accidental deletion (by over publishing)
    uncheck "prevent accidental deletion", save, delete, save, delete again, check it's deleted thoroughly 
    disable edit tracking in the local repository
    delete the edit tracking fields from the local repository, we will add them back post-publish
    
    once re-published, users with disconnected edit workflows in collector app need to go to manage, remove the features only, then re-initiate a synchronnization
    this is because the GUIDS for replication/distributed geodatabase will be reset upon the new publish operation 
    perform additions again now to add back the static hosted GUIDs and synch tracking
    '''
    arcpy.management.DisableEditorTracking(r"\\gisdata\planning\cart\projects\KanPLan\MXD\HostedServices\Collect17\sde@Klekt17.sde\KLEKT17.SDE.Railroad\KLEKT17.SDE.MastCrossbuckAssembly", "DISABLE_CREATOR", "DISABLE_CREATION_DATE", "DISABLE_LAST_EDITOR", "DISABLE_LAST_EDIT_DATE")
    arcpy.management.DeleteField("MastCrossbuckAssembly_SQL", "loaded_date;sync_user;sync_over_user;sync_over_date;sync_GUID")
    arcpy.management.DeleteField("MastCrossbuckAssembly_SQL", "last_edited_date;last_edited_user;created_date;created_user")

def additions():
    
    
    arcpy.management.AddJoin(r"MastCrossbuckAssembly_SQL", "sync_guid", r"MastCrossbuckAssembly\MastCrossbuckAssembly", "GlobalID", "KEEP_ALL")
    arcpy.management.Append(r"MastCrossbuckAssembly\MastCrossbuckAssembly", "MastCrossbuckAssembly_SQL", "NO_TEST", r'AssetID "AssetID" true true false 50 Text 0 0,First,#,MastCrossbuckAssembly\MastCrossbuckAssembly,AssetID,0,50;Start_Date "Start_Date" true true false 8 Date 0 0,First,#,MastCrossbuckAssembly\MastCrossbuckAssembly,Start_Date,-1,-1;End_Date "End_Date" true true false 8 Date 0 0,First,#,MastCrossbuckAssembly\MastCrossbuckAssembly,End_Date,-1,-1;Source "Source Citation" true true false 5 Text 0 0,First,#,MastCrossbuckAssembly\MastCrossbuckAssembly,Source,0,5;CrossbuckAssembly "Mast Crossbuck Assembly" true true false 50 Text 0 0,First,#,MastCrossbuckAssembly\MastCrossbuckAssembly,CrossbuckAssembly,0,50;NoRoadGates "Road Gate Count" true true false 4 Long 0 10,First,#,MastCrossbuckAssembly\MastCrossbuckAssembly,NoRoadGates,-1,-1;LightPairsCount "Number of Light Pairs" true true false 4 Long 0 10,First,#,MastCrossbuckAssembly\MastCrossbuckAssembly,LightPairsCount,-1,-1;MastLightType "Mast Light Type" true true false 50 Text 0 0,First,#,MastCrossbuckAssembly\MastCrossbuckAssembly,MastLightType,0,50;MastLightBack "Back Lights Included" true true false 1 Text 0 0,First,#,MastCrossbuckAssembly\MastCrossbuckAssembly,MastLightBack,0,1;NoPedGates "Pedestrian Gate Count" true true false 4 Long 0 10,First,#,MastCrossbuckAssembly\MastCrossbuckAssembly,NoPedGates,-1,-1;LensSize "Lens Size" true true false 2 Text 0 0,First,#,MastCrossbuckAssembly\MastCrossbuckAssembly,LensSize,0,2;MastLightSides "Side Lights Included" true true false 1 Text 0 0,First,#,MastCrossbuckAssembly\MastCrossbuckAssembly,MastLightSides,0,1;created_user "created_user" true true false 255 Text 0 0,First,#;created_date "created_date" true true false 8 Date 0 0,First,#;last_edited_user "last_edited_user" true true false 255 Text 0 0,First,#;last_edited_date "last_edited_date" true true false 8 Date 0 0,First,#;sync_GUID "sync_GUID" true true false 50 Text 0 0,First,#,MastCrossbuckAssembly\MastCrossbuckAssembly,GlobalID,0,50', None)

    
def main():
    pyversion()
    
main()
