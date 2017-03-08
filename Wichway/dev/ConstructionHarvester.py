# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Usage: Adds and Deletes Construction Features Logs to Wichway API
# Author: NVOLPE and the amazing help of JFOLDS
# ---------------------------------------------------------------------------


#####################################
##                                  #
## URLS NEED UPDATED once published #
## REST Point URL can be shortened  #
## Depending on query requirments   #
##                                  #
#####################################


import arcpy, time, traceback, json, urllib2, urllib, datetime, time
from arcpy import env
import config
from arcpy import DeleteFeatures_management, InsertCursor, GetCount_management, Exists, Point
import os, sys


#######################
####################### private methods
#######################

def harvestEvent(logParams, bool):
    eventId = ''

    ######################  Make call to controller ###########################
    encodedParams = urllib.urlencode(logParams)
    arcpy.AddMessage(" url : %s" % config.harvestEventUrl)
    results = urllib2.urlopen(config.harvestEventUrl, encodedParams).read()
    arcpy.AddMessage("API results: %s" % results)


    result_object = json.loads(results)

    if bool == True:
        for key, value in result_object.items():
            if str(key) == 'id':
                eventId = str(value)
                arcpy.AddMessage("value : " + str(value))

        return eventId


def logMessage(eventId, date, Level, Message):

    ###################  Make call to controller ########################
    parameters = { 'EventId': eventId, 'Datetime': date, 'Level': Level, 'Message': Message }
    encodedParams = urllib.urlencode(parameters)
    arcpy.AddMessage(" url : %s" % config.logUrl)
    results = urllib2.urlopen(config.logUrl, encodedParams).read()
    arcpy.AddMessage("API results: %s" % results)


def getExceptionInfo():
   (type, value, traceback) = sys.exc_info()
   sys.exc_clear()
   error = "Type: %s\nValue: %s\nTraceback: %s" % (type, value, traceback)
   return error

def truncateTable():
    #######################
    # delete all features
    #######################
    try:
        deleteRows = arcpy.SearchCursor(sdeLayer)
        for delrow in deleteRows:
            RouteName = delrow.getValue("RouteName")
            arcpy.AddMessage("Deleting: RouteName-" + RouteName)
        del deleteRows

        arcpy.TruncateTable_management(sdeLayer)
        #DeleteFeatures was replaced with truncate table -- to eliminate datbase transactions
        #arcpy.DeleteFeatures_management(sdeLayer)
        arcpy.AddMessage("Deleted All Construction features")
        logMessage(eventId, timeStamp, 'DEBUG', 'Deleted all features')

    except:
        ex = getExceptionInfo()
        arcpy.AddMessage("Failed to delete Construction features. " + ex)
        #logMessage(eventId, timeStamp, 'DEBUG', 'Failed to delete features. Reason: ' + ex)
        raise Exception('Failed to delete features. Reason: ' + ex)

    finally:
        if 'deleteRows' in locals():
            del deleteRows

def addFeatures():
    #######################
    # add all features
    #######################

    try:
        results = urllib2.urlopen(config.jsonQueryLayer).read()
        content = json.loads(results)
        insertrows = arcpy.InsertCursor(sdeLayer)

        #desc = arcpy.Describe(sdeLayer)
        #for field in desc.fields:
        #    if field.name == 'Status':
        #        StatusField = field


        if 'features' in content:
            features = content['features']

        points = arcpy.Array()

        totalFeatures = 0

        for feature in features:
            totalFeatures += 1

            if len(feature) > 1:
                newRow = insertrows.newRow()
                attributes = feature['attributes']
                RouteName = attributes['RouteName']
                BeginMP = attributes['BeginMP']
                EndMP = attributes['EndMP']
                County = attributes['County']
                StartDate = attributes['StartDate']
                CompDate = attributes['CompDate']
                AlertType = attributes['AlertType']
                AlertDescription = attributes['AlertDescription']
                HeightLimit = attributes['HeightLimit']
                WidthLimit = attributes['WidthLimit']
                TimeDelay = attributes['TimeDelay']
                Comments = attributes['Comments']
                ContactName = attributes['ContactName']
                ContactPhone = attributes['ContactPhone']
                ContactEmail = attributes['ContactEmail']
                WebLink = attributes['WebLink']
                AlertStatus = attributes['AlertStatus']
                FeaClosed = attributes['FeaClosed']

                # fix US route names
                RouteName = (RouteName[0] + "-" + RouteName[1:]).upper()
                if "U-" in RouteName:
                    RouteName = "US-" + RouteName[2:].upper()
                arcpy.AddMessage('Adding : ' + RouteName)


                if StartDate > 0:
                    S_DATE = str(StartDate)[0:-3] + "." + str(StartDate)[-3:]
                    SD = datetime.datetime.fromtimestamp(float(S_DATE)).strftime('%Y-%m-%d %H:%M:%S')
                    newRow.StartDate = SD

                if CompDate > 0:
                    C_DATE = str(CompDate)[0:-3] + "." + str(CompDate)[-3:]
                    CD = datetime.datetime.fromtimestamp(float(C_DATE)).strftime('%Y-%m-%d %H:%M:%S')
                    newRow.CompDate = CD

                newRow.RouteName = RouteName
                newRow.BeginMP = BeginMP
                newRow.EndMP = EndMP
                newRow.County = County
                newRow.AlertType = AlertType
                newRow.AlertDescription = AlertDescription
                newRow.HeightLimit = HeightLimit
                newRow.WidthLimit = WidthLimit
                #newRow.TrafficRouting = RouteName  ##dont seem to have
                newRow.TimeDelay = TimeDelay
                newRow.Comments = Comments ##too many characters, change field for larger character limit
                #newRow.DetourType = RouteName  ##dont seem to have
                #newRow.DetourDescription = RouteName ##dont seem to have
                newRow.ContactName = ContactName
                newRow.ContactPhone = ContactPhone
                newRow.ContactEmail = ContactEmail
                newRow.WebLink = WebLink
                newRow.AlertStatus = AlertStatus
                newRow.FeaClosed = FeaClosed
                #newRow.Status = STATUS #dont seem to have

                if AlertStatus == 1:
                    newRow.Status = 'Planned'

                elif AlertStatus == 2 and FeaClosed == 0:
                    newRow.Status = 'Active'

                elif AlertStatus == 2 and FeaClosed == 1:
                    newRow.Status = 'Closed'

                else:
                    newRow.Status = None

                geometry = feature['geometry']
                paths = geometry['paths']

                for point in paths:
                    points.add(arcpy.Array([arcpy.Point(*coords) for coords in point]))

                polyline = arcpy.Polyline(points)
                newRow.shape = polyline

                insertrows.insertRow(newRow)
                points = arcpy.Array()

            else:
                attributesError = feature['attributes']
                RouteError = attributesError['RouteName']
                logMessage(eventId, timeStamp, 'WARN', 'No Feature Geometry Returned for route : ' + str(RouteError))


        del insertrows

        if features:
            fieldName1 = "X"
            fieldName2 = "Y"

            arcpy.CalculateField_management(sdeLayer, fieldName1,
                                                "!SHAPE.CENTROID.X!",
                                                "PYTHON_9.3")
            arcpy.CalculateField_management(sdeLayer, fieldName2,
                                                "!SHAPE.CENTROID.Y!",
                                                "PYTHON_9.3")

        featureCount = int(arcpy.GetCount_management(sdeLayer).getOutput(0))
        logMessage(eventId, timeStamp, 'DEBUG', 'Saved ' + str(featureCount) + ' of ' + str(totalFeatures) + ' items parsed')


    except:
        ex = getExceptionInfo()
        arcpy.AddMessage("Failed to add Construction features.  Reason: " + ex)
        logMessage(eventId, timeStamp, 'DEBUG', 'Failed to add features. Reason: ' + ex)
        harvestEvent("ERROR", False)
        raise

    finally:
        if 'insertrows' in locals():
            del insertrows


#######################
####################### main
#######################

timeStamp = None
eventId = None

try:
    ##### on initialize: create a harvestevent via api which returns an event id in response which is required for subsequent logging###
    ts = time.time()
    ts = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    timeStamp = str(ts).strip()
    arcpy.AddMessage('Time Stamp : ' + timeStamp)

    # create the harvest event
    logParams = { 'LastRunAt': timeStamp, 'Name': "Construction", 'SourceId': 6, 'Status': 'IN_PROGRESS' }
    eventId = harvestEvent(logParams, True)

    #then log a initializing event message
    arcpy.AddMessage('Event ID : ' + eventId)
    logMessage(eventId, timeStamp, 'DEBUG', 'Initializing parser')

    # Local variables:
    _scratchworkspace = arcpy.env.scratchWorkspace
    arcpy.AddMessage("Scratch workspace : " + arcpy.env.scratchGDB)
    _scratchworkspace = arcpy.env.scratchGDB
    arcpy.env.overwriteOutput = True


    featureWorkspace_connection = config.sdeConnectionString
    sdeLayer = "ConstructionSegments_Lay"

    try:
        if arcpy.Exists(featureWorkspace_connection):
            arcpy.MakeFeatureLayer_management(featureWorkspace_connection, sdeLayer)
            truncateTable()
            addFeatures()
            resultsJSON = "{success : true}"

            logParams = { 'LastRunAt': timeStamp, 'Name': "Construction", 'SourceId': 6, 'Status': 'DONE', 'id': eventId }
            harvestEvent(logParams, False)
            arcpy.SetParameterAsText(0, resultsJSON)
        else:
            raise Exception('Unable to connect to the database or the ConstructionSegments featureclass does not exist.')
    except Exception as e:
        #ex = getExceptionInfo()
        arcpy.AddError(e.message)
        logMessage(eventId, timeStamp, 'ERROR', e.message)
        raise

except:
    resultsJSON = "{success : false}"
    arcpy.SetParameterAsText(0, resultsJSON)
    arcpy.AddMessage("Failed")
    ex = getExceptionInfo()
    logMessage(eventId, timeStamp, 'DEBUG', 'Failed to Complete. Reason: ' + ex)
    logParams = { 'LastRunAt': timeStamp, 'Name': "Construction", 'SourceId': 6, 'Status': 'ERROR', 'id': eventId }
    harvestEvent(logParams, False)


