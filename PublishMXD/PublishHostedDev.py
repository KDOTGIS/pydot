'''
Created on Oct 27, 2016
referencing 
https://blogs.esri.com/esri/arcgis/2013/04/23/updating-arcgis-com-hosted-feature-services-with-python/

SCRUB THIS for SECURITY

@author: kyleg
'''

if __name__ == '__main__':
    pass

import arcpy, os, sys
import xml.dom.minidom as DOM

arcpy.env.overwriteOutput = True

# Update these variables
# The tempPath variable is a relative path which is the same directory
# this script is saved to. You can modify this value to a path on your
# system to hold the temporary files.
serviceName = "RailCrossing"
tempPath = sys.path[0]
MXDPath = r"F:\Cart\projects\KanPlan\MXD\HostedServices\Collect17\MXD/"
MXDocument = "Collect17_65_Master_Dev"
MXDseed = MXDPath+MXDocument+".mxd"
path2MXD = mxd.saveACopy(MXDPath+MXDocument+serviceName+".mxd", version)
userName = "KanDOT"
passWord = "KanDOTGIS"

# All paths are built by joining names to the tempPath
SDdraft = os.path.join(tempPath, "tempdraft.sddraft")
newSDdraft = os.path.join(tempPath, "updatedDraft.sddraft")
SD = os.path.join(tempPath, serviceName + ".sd")

arcpy.SignInToPortal_server(userName, passWord, "http://www.arcgis.com/")
mxd = arcpy.mapping.MapDocument(path2MXD)

arcpy.mapping.CreateMapSDDraft(mxd, SDdraft, serviceName, "MY_HOSTED_SERVICES")

# Read the contents of the original SDDraft into an xml parser
doc = DOM.parse(SDdraft)

# The follow 5 code pieces modify the SDDraft from a new MapService
# with caching capabilities to a FeatureService with Query,Create,
# Update,Delete,Uploads,Editing capabilities. The first two code
# pieces handle overwriting an existing service. The last three pieces
# change Map to Feature Service, disable caching and set appropriate
# capabilities. You can customize the capabilities by removing items.
# Note you cannot disable Query from a Feature Service.
tagsType = doc.getElementsByTagName('Type')
for tagType in tagsType:
    if tagType.parentNode.tagName == 'SVCManifest':
        if tagType.hasChildNodes():
            tagType.firstChild.data = "esriServiceDefinitionType_Replacement"

tagsState = doc.getElementsByTagName('State')
for tagState in tagsState:
    if tagState.parentNode.tagName == 'SVCManifest':
        if tagState.hasChildNodes():
            tagState.firstChild.data = "esriSDState_Published"

# Change service type from map service to feature service
typeNames = doc.getElementsByTagName('TypeName')
for typeName in typeNames:
    if typeName.firstChild.data == "MapServer":
        typeName.firstChild.data = "FeatureServer"

#Turn off caching
configProps = doc.getElementsByTagName('ConfigurationProperties')[0]
propArray = configProps.firstChild
propSets = propArray.childNodes
for propSet in propSets:
    keyValues = propSet.childNodes
    for keyValue in keyValues:
        if keyValue.tagName == 'Key':
            if keyValue.firstChild.data == "isCached":
                keyValue.nextSibling.firstChild.data = "false"

#Turn on feature access capabilities
configProps = doc.getElementsByTagName('Info')[0]
propArray = configProps.firstChild
propSets = propArray.childNodes
for propSet in propSets:
    keyValues = propSet.childNodes
    for keyValue in keyValues:
        if keyValue.tagName == 'Key':
            if keyValue.firstChild.data == "WebCapabilities":
                keyValue.nextSibling.firstChild.data = "Query,Create,Update,Delete,Uploads,Editing"

# Write the new draft to disk
f = open(newSDdraft, 'w')
doc.writexml( f )
f.close()

# Analyze the service
analysis = arcpy.mapping.AnalyzeForSD(newSDdraft)

if analysis['errors'] == {}:
    # Stage the service
    arcpy.StageService_server(newSDdraft, SD)

    # Upload the service. The OVERRIDE_DEFINITION parameter allows you to override the
    # sharing properties set in the service definition with new values. In this case,
    # the feature service will be shared to everyone on ArcGIS.com by specifying the
    # SHARE_ONLINE and PUBLIC parameters. Optionally you can share to specific groups
    # using the last parameter, in_groups.
    arcpy.UploadServiceDefinition_server(SD, "My Hosted Services", serviceName,
                                         "", "", "", "", "OVERRIDE_DEFINITION","SHARE_ONLINE",
                                         "PUBLIC","SHARE_ORGANIZATION", "")

    print "Uploaded and overwrote service"

else:
    # If the sddraft analysis contained errors, display them and quit.
    print analysis['errors']
