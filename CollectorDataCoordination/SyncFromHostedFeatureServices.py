'''
Created on Jan 20, 2017

This script uses ARcGIS Pro, and refers to a map in a Pro Project.

pyversion():    
    #this script requires arcgis pro librarires of python 3.5x, which run from conda

LearnTheDictionaryLoops():
    #how to loop through SQL Server (or other) feature datasets and feature classes using the dict and the feature class lists 
    #print (dict["Railroad"])  
    #print (dict.items())
    
 TruncateAndAppend():
    #UPDATE THE LOCAL DATA SOURCE FROM THE HOSTED DATA SOURCE
    
CopyAndOverwrite():
    #Create new feature classes locally from the hosted source (needs work)
    
Addsyncfields():
    #editor tracking should be enabled on the hosted feature services
    #when we sync to the local env (SQL server) we want to keep that edit tracking info
    #therefore we need to add new edit tracking fields for the local environment
    #we will also retain the edit tracking from the hosted environment
    #there are a variety of options here, needs more careful model standardization across dev, test, and prod

DropSyncFields():
    #needed for working around the problem referenced on line 25

RepublishService():
    when a service needs to be updated:

    communicate update to field community, have them all sync and remain on-hold
    update the data in the local repository, for collector apps the SQL server geodatabase
    once it's updated,  delete the service from ArcGIS Online, it should be set to prevent accidental deletion (by over publishing)
    uncheck "prevent accidental deletion", save, delete, save, delete again, check it's deleted thoroughly 
    disable edit tracking in the local repository
    delete the edit tracking fields from the local repository, we will add them back post-publish
    
    once re-published, users with disconnected edit workflows in collector app need to go to manage, remove the features only, then re-initiate a synchronnization
    this is because the GUIDS for replication/distributed geodatabase will be reset upon the new publish operation 
    perform additions again now to add back the static hosted GUIDs and synch tracking



***REQUIRED!!!!!!!!!!

The map referenced in ArcGIS pro must contain a hosted feature service, and a local geodatabase feature class of the same name.
The layer name must be the same between the hosted source and the local target
The local target must be named like 'Database.Owner.FeatureClass'
The hosted source may appear to be in a group, aka the service containing the layer, and only the layer name matters.  
This Services may be named TEST DEV or PROD for example, but the layers should be named consistently 

To publish/add/test new services and data alterations:
This Collector app data model is developed using Sparx Enterprise Architect
that file geodatabase was copied to SQL server (dev, prod, etc)...
the feature classes are staged in SQL Server (data loaded, relationships created, etc)
are INDIVIDUALLY published to hosted feature services 
data is being collected, edited, updated in the hosted feature service on KanPlan, 
and we need to get changes from the hosted environment to our local environment.

This script shall perform that synchronization

these scripts require  ArcGIS Pro and the Conda Python 3.5 libs
which have the ability to edit feature services in the pro environment 

May 15, 2015 tested Truncate and Append, Add SyncFields, moved to production: mission accomplished

@author: kyleg
'''
#import arcpy
import sys
from arcpy import mp

#Sys will tell us if we have the right python environment

#to use the ArcGIS.com hosted feature services secured by groups in ArcGIS online, we are leveraging an ArcGIS Pro project
#the person logged into ArcGIS pro must be in the correct collector group

if __name__ == '__main__':
    pass

#Production Environment

railroadurlroot = r"\\gisdata\planning\cart\projects\KanPLan\MXD\HostedServices\Collect17\sde@Klekt17.sde\KLEKT17.SDE."
remainder = "\KLEKT17.SDE."
db = 'Klekt17'
dbo = 'SDE'

p = mp.ArcGISProject(r'\\gisdata\planning\Cart\projects\KanPlan\MXD\HostedServices\Collect16\Collector_Prod\Collector_Prod.aprx')
m = p.listMaps("ProdUpdate")[0]


#Test Environment - remove comments to run script in Test environment
'''
railroadurlroot = r"\\gisdata\planning\cart\projects\KanPLan\MXD\HostedServices\Collect17\sde@Collect17_dev.sde\Collect17.SDE."
remainder  = "\Collect17.SDE."
db = 'Collect17'
dbo = 'SDE'

p = arcpy.mp.ArcGISProject(r'\\gisdata\planning\Cart\projects\KanPlan\MXD\HostedServices\Collect16\Collector_Prod\Collector_Prod.aprx')
m = p.listMaps("Test and Development")[0]

'''

Railroad = ["MastCrossbuckAssembly", "RailCrossing", "Cantilever"]
Roadside = ["BrushTreeControl", "CulvertsPipes", "Ditch", "EdgeUnderDrains", 
            "ErosionControlDevices", "Fencing", "Guardrail", "Lighting", "LitterDebris", 
            "Obstacle", "PavedShoulder", "Permit", "Sidewalk", "SlopeErosion", "UnpavedShoulder", "VegetationWeedControl"]
Roadway = ["Crosswalk", "Gate", "Median", "MedianCrossover", "ParkingLanes", "PavDeformation", "PavFlexPotholes", "PavFlexRutting", 
           "PavMarking", "PavRigidCracking", "PavRigidFaulting", "PavRigidJointSealant", "PavRigidPotholes", "RumbleStripsLongitudinal",
            "RumbleStripTransverse", "ThroughLanes", "TurnLaneLeft", "TurnLaneRight"]
Signs = ["Signals", "Signs_Information", "Signs_Other", "Signs_Regulatory", "Signs_Warning"]


dict = {"Railroad":Railroad, "Roadside":Roadside, "Roadway":Roadway, "Signs":Signs}
#dict = {"Railroad":Railroad}

def pyversion():
    #this script requires arcgis pro librarires of python 3.5x, which run from conda
    import sys
    print (sys.version)
    #this is a print of the sys environment version
    #if not running 3.5.x or Anaconda 4x or the latest for Pro, 
    #the environment needs to change for the python path
    #in eclipse, the python path for ArcGIS Pro 1.4.1 installed is ...ArcGIS\Pro\bin\python\envs\arcgispro-py3
    
    
def LearnTheDictionaryLoops():
    #how to loop through my feature datasets and feature classes using the dict and the feature class lists 
    #print (dict["Railroad"])  
    #print (dict.items())
    for key, value in dict.items():
        print(key)
        for featureclass in value:
            print ("   "+featureclass)    

def TruncateAndAppend():
    #UPDATE THE LOCAL DATA SOURCE FROM THE HOSTED DATA SOURCE
    '''for key, value in dict.items():
        print(key)
        for featureclass in value:
            print ("   "+featureclass)
            '''
    from arcpy import management, TruncateTable_management
    for source in m.listLayers():
        if source.isWebLayer is True and source.isFeatureLayer is True:
            print("hosted  ", source.name)
            for target in m.listLayers():
                if target.isWebLayer is False and target.isFeatureLayer is True:
                    print(target)
                    db, owner, targetname = target.name.split(".")
                    print(targetname)
                    if targetname == source.name:
                        print("local  ", targetname)
                        TruncateTable_management(target)
                        management.Append(source, target, "NO_TEST")
                        
    # need a little bit of code here for layers not conforming, error handling a ValueError:

def CopyAndOverwrite():
    #Create new feature classes locally from the hosted source (needs work)
    '''for key, value in dict.items():
        print(key)
        for featureclass in value:
            print ("   "+featureclass)
            '''
    from arcpy import management, env, Exists
    env.overwriteOutput = 1
    for source in m.listLayers():
        if source.isWebLayer is True and source.isFeatureLayer is True:
            print("hosted  ", source.name)
            
            
        for target in m.listLayers():
            if target.isWebLayer is False and target.isFeatureLayer is True:
                db, owner, targetname = target.name.split(".")
                if targetname == source.name:
                    output = r"F:/Cart/projects/KanPlan/MXD/HostedServices/Collect16/Collector_Prod/Collector_Prod.gdb/"+targetname
                    print("local  ", target)
                    management.CopyFeatures(source, output)
                    """
                    if Exists(output):
                        print("output exists, deleting output")
                        management.Delete(output)
                        management.CopyFeatures(source, output)
                        pass
                    else:
                        print("output does not exist, continue")
                        management.CopyFeatures(source, output)
                        pass
                    
                    print("copy features" + output)
                    """
                    #management.CopyFeatures(r"MastCrossbuckAssembly\MastCrossbuckAssembly", r"F:\Cart\projects\KanPlan\MXD\HostedServices\Collect16\Collector_Prod\dt00ar56.sde\KLEKT17.SDE.Railroad\KLEKT17.SDE.MastCrossbuckAssembly", None, None, None, None)
                    #management.CopyFeatures(source, target)
    
def Addsyncfields():
    #editor tracking should be enabled on the hosted feature services
    #when we sync to the local env (SQL server) we want to keep that edit tracking info
    #therefore we need to add new edit tracking fields for the local environment
    #we will also retain the edit tracking from the hosted environment
        
    #print (dict["Railroad"])  
    #print (dict.items())
    from arcpy import management
    for key, value in dict.items():
        #print(key)
        for featureclass in value:
            """
            #print ("   "+featureclass)
            try:
                #print(railroadurlroot+str(key)+remainder+str(featureclass), " hosted edit tracking added")
                management.AddField(railroadurlroot+str(key)+remainder+str(featureclass), "CreationDate", "Date", None, None, None, "CreationDate", "NULLABLE", "NON_REQUIRED", None)
                management.AddField(railroadurlroot+str(key)+remainder+str(featureclass), "Creator", "Text", None, None, 50, "Creator", "NULLABLE", "NON_REQUIRED", None)
                management.AddField(railroadurlroot+str(key)+remainder+str(featureclass), "EditDate", "Date", None, None, None, "EditDate", "NULLABLE", "NON_REQUIRED", None)
                management.AddField(railroadurlroot+str(key)+remainder+str(featureclass), "Editor", "Text", None, None, 50, "Editor", "NULLABLE", "NON_REQUIRED", None)
                print(railroadurlroot+str(key)+remainder+str(featureclass), " hosted edit tracking added")
            except Exception:
                print("Error...")
                e = sys.exc_info()[1]
                print(e.args[0])
                continue

            """
            try:
                print(railroadurlroot+str(key)+remainder+str(featureclass), " edit tracking added")
                management.EnableEditorTracking(railroadurlroot+str(key)+remainder+str(featureclass), "sync_user", "loaded_date", "sync_over_user", "sync_over_date", "ADD_FIELDS", "UTC")  
            except Exception:
                e = sys.exc_info()[1]
                print(e.args[0])
                continue
           


'''
            try:
                #note - esri GUIDs are much longer than 50 characters
                #arcpy.management.AddField(railroadurlroot+str(key)+remainder+str(featureclass), "sync_guid", "TEXT", None, None, 50, "GUID from Hosted Service as text", "NULLABLE", "NON_REQUIRED", None)
            except Exception:
                e = sys.exc_info()[1]
                print(e.args[0])
                continue
'''
           
def DropSyncFields():
    from arcpy import management
    #when we truncate and append, I don't care about these fields for now
    #eventually the change detection capture scripts will evolve, for now, I just want to get this data into SQL server for validation
        
    #print (dict["Railroad"])  
    #print (dict.items())
    for key, value in dict.items():
        #print(key)
        for featureclass in value:
            
            try:
                print(railroadurlroot+str(key)+remainder+str(featureclass))
                #management.DeleteField(railroadurlroot+str(key)+remainder+str(featureclass), "sync_guid;CreationDate;Creator;EditDate;Editor")
                management.DeleteField(railroadurlroot+str(key)+remainder+str(featureclass), "editor;editdate;creator;creationdate")
                management.DisableEditorTracking(railroadurlroot+str(key)+remainder+str(featureclass), "DISABLE_CREATOR", "DISABLE_CREATION_DATE", "DISABLE_LAST_EDITOR", "DISABLE_LAST_EDIT_DATE")
                management.DeleteField(railroadurlroot+str(key)+remainder+str(featureclass), "loaded_date;sync_user;sync_over_user;sync_over_date;sync_GUID")
                #management.DeleteField("MastCrossbuckAssembly_SQL", "last_edited_date;last_edited_user;created_date;created_user")
                management.DeleteField(railroadurlroot+str(key)+remainder+str(featureclass), "sync_guid;created_user;created_date;last_edited_user;last_edited_date")
                
                print("deleted fields sync_guid;CreationDate;Creator;EditDate;Editor in ", railroadurlroot+str(key)+remainder+str(featureclass))
            except Exception:
                print("Error...")
                e = sys.exc_info()[1]
                print(e.args[0])
                continue



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
    from arcpy import management
    management.DisableEditorTracking(r"\\gisdata\planning\cart\projects\KanPLan\MXD\HostedServices\Collect17\sde@Klekt17.sde\KLEKT17.SDE.Railroad\KLEKT17.SDE.MastCrossbuckAssembly", "DISABLE_CREATOR", "DISABLE_CREATION_DATE", "DISABLE_LAST_EDITOR", "DISABLE_LAST_EDIT_DATE")
    management.DeleteField("MastCrossbuckAssembly_SQL", "loaded_date;sync_user;sync_over_user;sync_over_date;sync_GUID")
    management.DeleteField("MastCrossbuckAssembly_SQL", "last_edited_date;last_edited_user;created_date;created_user")
    
def main():
    #pyversion tests to ensure you are using the ArcGIS Pro Py environment, you should see 3.5.3 or higher from the Conda install (continuum analytics, INC)
    #pyversion()
    print ('You should review the script, and test it carefully')
    #Syncfields adds columns to the local SQL server geodatabase
    
    #DropSyncFields()
    #Addsyncfields()
    #CompareAndAdd()
    #TruncateAndAppend()
    #CopyAndOverwrite()
    
    
main()
