'''
Created on Feb 19, 2014
This script is task scheduled to update data from unregistered SDO to a Geodatabase
The unregistered data sources are layers in an MXD
because they are unregistered, ArcMap has already done the work of referencing a coordinate system, and determining extents
This method of updating will overwrite the table that already exists, then assign permissions
while the script is updating, non-administrative connections to the database are restricted (not allowed)

Modified Oct 21, 2014 by dtalley
Updated Jan 08, 2015 by dtalley to use the new ScriptStatusLogging format for SQL Server.
@author: kyleg
'''
import datetime, sys, traceback
# Placed above the rest of the imports to get a better
# measure of the total time it takes this script to run.
startingTime = datetime.datetime.now()

try:
    from KDOT_Imports.dt_functions import (ScriptStatusLogging, scriptSuccess, scriptFailure)  # @UnresolvedImport
except:
    print 'Import from dt_functions failed.'
    pass

if 'ScriptStatusLogging' in locals():
    print "ScriptStatusLogging exists in locals()"
else:
    print "ScriptStatusLogging does not exist in locals()"

#from arcpy, import the specific geoprocessing tools used by this script
from arcpy import (Delete_management, AddXY_management, Exists, FeatureVerticesToPoints_management,
                   MakeFeatureLayer_management, ChangePrivileges_management, DisconnectUser,
                   AcceptConnections, GetMessages, AddError, Dissolve_management, mapping,
                   FeatureClassToFeatureClass_conversion, env, ExecuteError)

#this is the MXD with  the layers to be exported
mxd = mapping.MapDocument(r"D:\SCHED\inv sdo views.mxd")
nusys_mxd = mapping.MapDocument(r"\\gisdata\arcgis\GISdata\MXD\NUSYS_EXTRACT.mxd")

#this is the administrative connection to the destination database (using the admin user/password)
admin_workspace = r"D:\SCHED\SQL61_GIS_CANSYS.sde"

#set the environment to allow new data to overwrite old data
env.overwriteOutput = True

#only layers explicitly listed will be exported.  CANPlist is the data from CANP, cansys production
#there can be other lists, like gisprod, or list for testing new CANSYS layers or updating specific layers

#notlist = #"NM3.NM_INV_ACCL_SDO_V" "NM3.NM_INV_AADT_SDO_V", "NM3.NM_INV_CAPS_SDO_V","NM3.NM_INV_EPFS_SDO_V",
#dolist = ["NM3.NM_INV_SMAP_SDO_V"]

CANPlist ="""
["NM3.EVENTS_LRSC_SDO_R", "NM3.EVENTS_LRSS_SDO_R", "NM3.NM_NLT_SRND_SDO_R", "NM3.NM_NLT_CRND_SDO_R",
"NM3.NM_INV_CPMS_SDO_V", "NM3.NM_INV_ACCS_SDO_V", "NM3.NM_INV_ADMO_SDO_V",
"NM3.NM_INV_ANAL_SDO_V","NM3.NM_INV_AVSP_SDO_V","NM3.NM_INV_CITY_SDO_V",
"NM3.NM_INV_CPAV_SDO_V","NM3.NM_INV_FLEX_SDO_V","NM3.NM_INV_CONC_SDO_V",
"NM3.NM_INV_FUN_SDO_V","NM3.NM_INV_GPGR_SDO_V","NM3.NM_INV_GRAD_SDO_V",
"NM3.NM_INV_HPPA_SDO_V","NM3.NM_INV_HCUR_SDO_V","NM3.NM_INV_HPMS_SDO_V",
"NM3.NM_INV_INTC_SDO_V","NM3.NM_INV_INTR_SDO_V",
"NM3.NM_INV_LANE_SDO_V",
"NM3.NM_INV_LNCL_SDO_V","NM3.NM_INV_LYRS_SDO_V","NM3.NM_INV_MASA_SDO_V",
"NM3.NM_INV_MED_SDO_V","NM3.NM_INV_MNTR_SDO_V","NM3.NM_INV_MSSS_SDO_V",
"NM3.NM_INV_NHS_SDO_V","NM3.NM_INV_PASS_SDO_V","NM3.NM_INV_PMID_SDO_V",
"NM3.NM_INV_POEQ_SDO_V",
"NM3.NM_INV_PSE_SDO_V","NM3.NM_INV_RMBL_SDO_V","NM3.NM_INV_ROWY_SDO_V",
"NM3.NM_INV_RPAC_SDO_V","NM3.NM_INV_SAFE_SDO_V","NM3.NM_INV_SCID_SDO_V",
"NM3.NM_INV_SHLD_SDO_V","NM3.NM_INV_SKID_SDO_V","NM3.NM_INV_SMAP_SDO_V",
"NM3.NM_INV_SNIC_SDO_V","NM3.NM_INV_SPED_SDO_V","NM3.NM_INV_SSF_SDO_V",
"NM3.NM_INV_STHN_SDO_V","NM3.NM_INV_STP_SDO_V",
"NM3.NM_INV_STRP_SDO_V","NM3.NM_INV_SWID_SDO_V",
"NM3.NM_INV_SWZ_SDO_V", "NM3.NM_INV_TOLL_SDO_V",
"NM3.NM_INV_TRAF_SDO_V", "NM3.NM_INV_TRUS_SDO_V", "NM3.NM_INV_UABR_SDO_V",
"NM3.NM_INV_UAB_SDO_V",
"NM3.NM_INV_UABL_SDO_V", "NM3.NM_INV_VCUR_SDO_V", "NM3.NM_INV_WDOB_SDO_V"]
#"""
#CANPlist = ["NM3.NM_INV_MED_SDO_V"]
CANPlistAADT ="""
 "NM3.NM_INV_A004_SDO_V",
"NM3.NM_INV_A005_SDO_V",
"NM3.NM_INV_A006_SDO_V",
"NM3.NM_INV_A007_SDO_V",
"NM3.NM_INV_A008_SDO_V",
"NM3.NM_INV_A009_SDO_V",
"NM3.NM_INV_A010_SDO_V",
"NM3.NM_INV_A011_SDO_V",
"NM3.NM_INV_A012_SDO_V",
"NM3.NM_INV_A013_SDO_V",
"NM3.NM_INV_AADT_SDO_V",
"""
#CANPlist5 = 'NM3.NM_INV_LANE_SDO_V"'
gisprodlist = ["SHARED.FUTURE_NETWORK", "SHARED.GIS_STATE_SYSTEM"]
#CANPlist = ["NM3.NM_NLT_SRND_SDO_R", "NM3.NM_NLT_CRND_SDO_R","NM3.NM_INV_AADT_SDO_V"]
#CANPlist = ["NM3.NM_INV_LANE_SDO_V", "NM3.NM_INV_MED_SDO_V", "NM3.NM_INV_SHLD_SDO_V"]

#print CANPlist

def ListAllLyrs():
    #function to list all the layers in the MXD/data frame, can be used to compare to printed CANPlist
    print "layer list initialized at "+str(datetime.datetime.now())
    for lyr in mapping.ListLayers(mxd):
        try:
            lyrname = lyr.name
            print lyrname
        except:
            print "There was a problem with this layer: "  + str(lyr.name)
            endingTime = datetime.datetime.now()
            ScriptStatusLogging('CANP_LRS_EXPORT.py', 'ListAllLyrs Function',
                            scriptFailure, startingTime,
                            endingTime, 'There was a problem with this layer: ' + str(lyr.name))


def ExportCANPLyrs(admin_workspace):
    print "exporting initialized at "+str(datetime.datetime.now())
    #set the output database, this could be changed to admin workspace
    destConnection = admin_workspace
    #copy the map extract table to the destination commented 5/8/2014
    #TableToTable_conversion("MAP_EXTRACT",destConnection,"Map_Extract","#","#","#")
    #start the loop for layers in the mxd
    for lyr in mapping.ListLayers(mxd):
        #continue the loop operations for layers in the CANPlist
        if lyr.name in CANPlist:
            try:
                #manipulate the layer name a little bit
                lyrname = lyr.name[11:]
                print lyrname +" exporting..."
                outlyrname = "V_"+lyrname
                outlyrobj = destConnection+"\\GIS_CANSYS.DBO."+outlyrname
                #this should prevent ERROR 000258: Layer already exists, even though OverwriteOutput is true
                if Exists(outlyrobj):
                    Delete_management(outlyrobj)
                #export the layer to SQL server
                FeatureClassToFeatureClass_conversion(lyr, destConnection, outlyrname, "#","#","#")
                #this is a total replacement, so grant the necessary administrative privileges
                ChangePrivileges_management(outlyrobj, "readonly", "GRANT", "AS_IS")
                #tell me what happened
                print lyrname +" exported to " +outlyrname +" "+ str(datetime.datetime.now())
            except ExecuteError:
                msgs = GetMessages(2)
                AddError(msgs)
                #tell me what went wrong if there was an execute error
                print msgs
                AcceptConnections(admin_workspace, True)
                endingTime = datetime.datetime.now()
                ScriptStatusLogging('CANP_LRS_EXPORT.py', 'ExportCANPLyrs Function',
                            scriptFailure, startingTime,
                            endingTime, GetMessages(2))

                pass
            except (RuntimeError, TypeError, NameError):
                #tell me if there is a problem with one of the layers
                print "TypeError on item" + lyr.name
                AcceptConnections(admin_workspace, True)
                endingTime = datetime.datetime.now()
                ScriptStatusLogging('CANP_LRS_EXPORT.py', 'ExportCANPLyrs Function',
                            scriptFailure, startingTime,
                            endingTime, GetMessages(2))

                pass
            except:
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                # Concatenate information together concerning the error into a message string

                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                msgs = "ArcPy ERRORS:\n" + GetMessages(2) + "\n"
                print pymsg + "\n"
                print msgs
                AcceptConnections(admin_workspace, True)
                endingTime = datetime.datetime.now()
                ScriptStatusLogging('CANP_LRS_EXPORT.py', 'ExportCANPLyrs Function',
                            scriptFailure, startingTime,
                            endingTime, GetMessages(2))

        else:
            #tell me if the layer was there bit skipped because it was not added to the CANPlist
            print lyr.name +" was not in the export list and will be skipped"
            pass

def ExportGISProdLyrs(admin_workspace):
    #similar to CANP, only for layers in another geodatabase, like GISPROD.
    print "exporting initialized at "+str(datetime.datetime.now())
    destConnection = admin_workspace #once again, this could be change to the admin workspace
    for lyr in mapping.ListLayers(mxd):
        if lyr.name in gisprodlist:
            try:
                #manipulate the layer name a little bit differently
                lyrname = lyr.name[7:]
                print lyrname +" exporting..."
                outlyrname = lyrname
                outlyrobj = destConnection+"\\GIS_CANSYS.DBO."+outlyrname
                Unlock(admin_workspace)
                FeatureClassToFeatureClass_conversion(lyr, destConnection, outlyrname, "#","#","#")
                ChangePrivileges_management(outlyrobj, "readonly", "GRANT", "AS_IS")
                print lyrname +" exported to " +outlyrname +" "+ str(datetime.datetime.now())
            except ExecuteError:
                msgs = GetMessages(2)
                AddError(msgs)
                print msgs
                endingTime = datetime.datetime.now()
                ScriptStatusLogging('CANP_LRS_EXPORT.py', 'ExportGISProdLyrs Function',
                            scriptFailure, startingTime,
                            endingTime, GetMessages(2))

                pass
            except (RuntimeError, TypeError, NameError):
                print "TypeError on item" + lyr.name
                endingTime = datetime.datetime.now()
                ScriptStatusLogging('CANP_LRS_EXPORT.py', 'ExportGISProdLyrs Function',
                            scriptFailure, startingTime,
                            endingTime, GetMessages(2))

                pass
            except:
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                msgs = "ArcPy ERRORS:\n" + GetMessages(2) + "\n"
                print pymsg + "\n"
                print msgs
                endingTime = datetime.datetime.now()
                ScriptStatusLogging('CANP_LRS_EXPORT.py', 'ExportGISProdLyrs Function',
                            scriptFailure, startingTime,
                            endingTime, GetMessages(2))

        else:
            #print lyr.name +" was not in the export list and will be skipped"
            return

def ExportNUSYS(admin_workspace):
    print "exporting initialized at "+str(datetime.datetime.now())
    #set the output database, this could be changed to admin workspace
    destConnection = admin_workspace
    #copy the map extract table to the destination commented 5/8/2014
    #TableToTable_conversion("MAP_EXTRACT",destConnection,"Map_Extract","#","#","#")
    #start the loop for layers in the mxd
    for lyr in mapping.ListLayers(nusys_mxd):
        #continue the loop operations for layers in the NUSYS MXD (unlisted)
        try:
            #manipulate the layer name a little bit
            lyrname = lyr.name
            print lyrname +" exporting..."
            outlyrname = lyrname
            outlyrobj = destConnection+"\\GIS_CANSYS.DBO."+outlyrname
            #this should prevent ERROR 000258: Layer already exists, even though OverwriteOutput is true
            if Exists(outlyrobj):
                Delete_management(outlyrobj)
            #export the layer to SQL server
            FeatureClassToFeatureClass_conversion(lyr, destConnection, outlyrname, "#","#","#")
            #this is a total replacement, so grant the necessary administrative privileges
            ChangePrivileges_management(outlyrobj, "readonly", "GRANT", "AS_IS")
            #tell me what happened
            print lyrname +" exported to " +outlyrname +" "+ str(datetime.datetime.now())
        except ExecuteError:
            msgs = GetMessages(2)
            AddError(msgs)
            #tell me what went wrong if there was an execute error
            print msgs
            AcceptConnections(admin_workspace, True)
            endingTime = datetime.datetime.now()
            ScriptStatusLogging('CANP_LRS_EXPORT.py', 'ExportNUSYS Function',
                            scriptFailure, startingTime,
                            endingTime, GetMessages(2))

            pass
        except (RuntimeError, TypeError, NameError):
            #tell me if there is a problem with one of the layers
            print "TypeError on item" + lyr.name
            AcceptConnections(admin_workspace, True)
            endingTime = datetime.datetime.now()
            ScriptStatusLogging('CANP_LRS_EXPORT.py', 'ExportNUSYS Function',
                            scriptFailure, startingTime,
                            endingTime, GetMessages(2))

            pass
        except:
            tb = sys.exc_info()[2]
            tbinfo = traceback.format_tb(tb)[0]
            # Concatenate information together concerning the error into a message string

            pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
            msgs = "ArcPy ERRORS:\n" + GetMessages(2) + "\n"
            print pymsg + "\n"
            print msgs
            AcceptConnections(admin_workspace, True)
            endingTime = datetime.datetime.now()
            ScriptStatusLogging('CANP_LRS_EXPORT.py', 'ExportNUSYS Function',
                            scriptFailure, startingTime,
                            endingTime, GetMessages(2))

def Unlock(admin_workspace):
    #unlock the database so we can really overwrite the tables, and prevent non-administrative users from connecting while operating
    env.workspace = admin_workspace
    #users = ListUsers(admin_workspace) #
    #print users
    AcceptConnections(admin_workspace, False)
    DisconnectUser(admin_workspace, "All")

def PostProcDissolveOne():
    owner = "GIS_CANSYS.DBO."
    outpre = admin_workspace+"/"+owner
    DissolveLayer = "MED"
    PostProcDissolveLocation = "MED"  # @UnusedVariable
    #each layer for GIS should be dissolved as multi-part lines so they can more efficiently be mapped online
    #each layer has different fields so each of these dissolves can be tested in ArcMap and copied to this script as needed
    try:
        Outputlyr = outpre+DissolveLayer
        MakeFeatureLayer_management(owner+"V_MED_SDO_V","MED_PRIMARY","CRND_RTE LIKE '%EB' OR CRND_RTE LIKE '%NB'","#","#")
        Dissolve_management("MED_PRIMARY",Outputlyr,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;MED_ID;MED_ID_DESC;MED_WDTH;MED_WDTH_FT","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(Outputlyr, "readonly", "GRANT", "AS_IS")
        #print "MED dissolved for viewing"

    except:
        print "oops"
        pass

def PostProcDissolve():
    owner = "GIS_CANSYS.DBO."
    outpre = admin_workspace+"/"+owner
    PostProcDissolveLocation = ""
    #each layer for GIS should be dissolved as multi-part lines so they can more efficiently be mapped online
    #each layer has different fields so each of these dissolves can be tested in ArcMap and copied to this script as needed
    try:

        PostProcDissolveLocation = "ACCS"
        ACCS = outpre+"ACCS"
        Unlock(admin_workspace)
        Dissolve_management(owner+"V_ACCS_SDO_V",ACCS,"CRND_RTE;LRS_KEY;STATE_LRS;ROUTE_NO;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;ACS_CTRL_ID;ACS_CTRL_ID_DESC","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(ACCS, "readonly", "GRANT", "AS_IS")

        PostProcDissolveLocation = "SMAP"
        SMAP = outpre+"SMAP"
        Unlock(admin_workspace)
        Dissolve_management(owner+"V_SMAP_SDO_V",SMAP,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;STATIONING_TYPE;STATIONING_TYPE_DESC;BEGIN_STATIONING;BEGIN_STATIONING_DECIMAL;END_STATIONING;END_STATIONING_DECIMAL;PROJECT_YEAR;PROJECT_NUMBER;PROJECT_TYPE;PROJECT_TYPE_DESC;HOST_PROJECT_NUMBER;PW_URL","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(SMAP, "readonly", "GRANT", "AS_IS")
        print "SMAP dissolved for viewing"

        PostProcDissolveLocation = "LYRS"
        LYRS = outpre+"LYRS"
        Dissolve_management(owner+"V_LYRS_SDO_V",LYRS,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;LAYER_TYPE;LAYER_TYPE_DESC;MATERIAL_TYPE;MATERIAL_TYPE_DESC;DEPTHS_MILLIMETERS;LAYER_DATE;MATERIAL_WIDTH_METERS;MATERIAL_WIDTH_FEET;SOURCE_TYPE;SOURCE_TYPE_DESC;PROJECT_ID;PW_URL","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(LYRS, "readonly", "GRANT", "AS_IS")
        print "LYRS dissolved for viewing"

        PostProcDissolveLocation = "LNCL"
        LNCL = outpre+"LNCL"
        MakeFeatureLayer_management(outpre+"V_LNCL_SDO_V","LNCL_PRIMARY","CRND_RTE LIKE '%EB' OR CRND_RTE LIKE '%NB'","#","OBJECTID OBJECTID VISIBLE NONE;CRND_RTE CRND_RTE VISIBLE NONE;LRS_KEY LRS_KEY VISIBLE NONE;BCMP BCMP VISIBLE NONE;ECMP ECMP VISIBLE NONE;BSMP BSMP VISIBLE NONE;ESMP ESMP VISIBLE NONE;COUNTY_CD COUNTY_CD VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;LANE_DIRECTION LANE_DIRECTION VISIBLE NONE;DISTRICT DISTRICT VISIBLE NONE;DIV_UNDIV DIV_UNDIV VISIBLE NONE;LNCL_CLS_ID LNCL_CLS_ID VISIBLE NONE;LNCL_CLS_ID_DESC LNCL_CLS_ID_DESC VISIBLE NONE;LNCL_DT LNCL_DT VISIBLE NONE;Shape Shape VISIBLE NONE;Shape.STLength() Shape.STLength() VISIBLE NONE")
        Dissolve_management("LNCL_PRIMARY",LNCL,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;LNCL_CLS_ID;LNCL_CLS_ID_DESC","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(LNCL, "readonly", "GRANT", "AS_IS")
        print "LNCL dissolved for viewing"

        PostProcDissolveLocation = "CPMS"
        CPMS = outpre+"CPMS"
        Dissolve_management(owner+"V_CPMS_SDO_V", CPMS,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;SCHEME_ID;PROJECT_ID;TECH_NAME;WORK_TYPE_DESC;DESIGN_CRITERIA;LEG_MAP_ID;CATEGORY_CODE;SUBCAT_CODE;PROJECT_DESC_FRND;PROJ_DISTRICT;PROJ_AREA;PROJ_SUB_AREA;PROJ_LENGTH;HOST_PROJ_NUM;FISCAL_YEAR_PRGM;LETTING_DATE;PW_URL","BCMP MIN;BSMP MIN;ECMP MAX;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(CPMS, "readonly", "GRANT", "AS_IS")
        print "CPMS dissolved for viewing"

        PostProcDissolveLocation = "POEQ"
        POEQ = outpre+"POEQ"
        Dissolve_management(owner+"V_POEQ_SDO_V",POEQ, "CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;IRIR;RLIFE;RLIFE_DEFAULT;RLIFE_DEFAULT_DESC;EQFAULT;EQJD;EQTCR;RUTVAL;PVMTGRP;PVMTGRP_DESC;DEF_FLAG;DEF_FLAG_DESC;POEQ_DT;MEAN_IRIR;YEAR_LAST_IMP;YEAR_LAST_CONST;LAST_OVERLAY_THIC;IRIR_DATE;IRIR_DATE_DEFAULT;IRIR_DATE_DEFAULT_DESC","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(POEQ, "readonly", "GRANT", "AS_IS")
        print "POEQ dissolved for viewing"

        PostProcDissolveLocation = "HPPA"
        HPPA = outpre+"HPPA"
        Dissolve_management(owner+"V_HPPA_SDO_V", HPPA,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;HPMS_SURFACE_TYPE;HPMS_SURFACE_TYPE_DESC;HPMS_YEAR_LAST_IMPROV;HPMS_YEAR_LAST_CONST;HPMS_LAST_OVERLAY_THICK;HPMS_THICKNESS_RIGID;HPMS_THICKNESS_FLEXIBLE;HPMS_BASE_TYPE;HPMS_BASE_TYPE_DESC;HPMS_BASE_THICKNESS","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(HPPA, "readonly", "GRANT", "AS_IS")
        #print "HPPA dissolved for viewing"

        PostProcDissolveLocation = "SPED"
        SPED = outpre+"SPED"
        Dissolve_management(owner+"V_SPED_SDO_V", SPED,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;SPD_LMT;SPD_LMT_DESC;SPED_RESOL","#","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(SPED, "readonly", "GRANT", "AS_IS")
        #print "SPED dissolved for viewing"

        PostProcDissolveLocation = "FUN"
        FUN =  outpre+"FUN"
        Dissolve_management(owner+"V_FUN_SDO_V",FUN,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;FUN_CLASS;FUN_CLASS_DESC;OLD_FUN_CLASS","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(FUN, "readonly", "GRANT", "AS_IS")
        #print "FUN dissolved for viewing"

        PostProcDissolveLocation = "LANE"
        LANE = outpre+"LANE"
        Dissolve_management(owner+"V_LANE_SDO_V",LANE,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;LN_ID;LN_ID_DESC;LN_WDTH;LN_WDTH_FT;XSP;XSP_DESCR;HOV;HOV_DESC","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(LANE, "readonly", "GRANT", "AS_IS")
        #print "LANE dissolved for viewing"

        PostProcDissolveLocation = "NHS"
        NHS = outpre+"NHS"
        Dissolve_management(owner+"V_NHS_SDO_V",NHS,"LRS_KEY;COUNTY_CD;COUNTY_NAME;DISTRICT;NHS_ID;NHS_ID_DESC","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(NHS, "readonly", "GRANT", "AS_IS")
        #print "NHS dissolved for viewing"

        PostProcDissolveLocation = "SHLD"
        SHLD = outpre+"SHLD"
        Dissolve_management(owner+"V_SHLD_SDO_V",SHLD,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;SHLDR_ID;SHLDR_ID_DESC;FORESLOPE;SHLDR_WDTH;SHLDR_WDTH_FT;XSP;XSP_DESCR","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(SHLD, "readonly", "GRANT", "AS_IS")
        #print "SHLD dissolved for viewing"

        PostProcDissolveLocation = "MED"
        MED = outpre+"MED"
        MakeFeatureLayer_management(owner+"V_MED_SDO_V","MED_PRIMARY","CRND_RTE LIKE '%EB' OR CRND_RTE LIKE '%NB'","#","#")
        Dissolve_management("MED_PRIMARY",MED,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;MED_ID;MED_ID_DESC;MED_WDTH; MED_WDTH_FT","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(MED, "readonly", "GRANT", "AS_IS")
        #print "MED dissolved for viewing"

        PostProcDissolveLocation = "RMBL"
        RMBL = outpre+"RMBL"
        Dissolve_management(owner+"V_RMBL_SDO_V", RMBL,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;RMBL_SHAPE;RMBL_SHAPE_DESC;HOST_PRJCT_ID;PRJCT_ID;RMBL_SOURCE;RMBL_SOURCE_DESC;XSP;XSP_DESCR","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(RMBL, "readonly", "GRANT", "AS_IS")
        #print "RMBL dissolved for viewing"

        PostProcDissolveLocation = "SWID"
        SWID = outpre+"SWID"
        Dissolve_management(owner+"V_SWID_SDO_V",SWID, "CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;SRFC_WDTH; SRFC_WDTH_FT","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
        ChangePrivileges_management(SWID, "readonly", "GRANT", "AS_IS")

        PostProcDissolveLocation = ""

    except:
        endingTime = datetime.datetime.now()
        if PostProcDissolveLocation != "":
            ScriptStatusLogging('CANP_LRS_EXPORT.py', 'PostProcDissolve failed while attempting to dissolve ' + str(PostProcDissolveLocation),
                            scriptFailure, startingTime,
                            endingTime, GetMessages(2))
        #elif:
            #ERROR 000732: path not valid
        else:
            ScriptStatusLogging('CANP_LRS_EXPORT.py', 'PostProcDissolve Function',
                            scriptFailure, startingTime,
                            endingTime, GetMessages(2))
        pass

def PostProcAnnum(admin_workspace):
    Unlock(admin_workspace)
    #AADT is historical and left open so it takes a really long time to run all the junk that exists in this layer
    #It might help to put a def query in the MXD that ilmits AADT to 5 years
    #sine AADT is only updated once a year, this can be run manually annually or as needed
    AADT = admin_workspace+"/GIS_CANSYS.DBO.ACCS"
    Unlock(admin_workspace)
    Dissolve_management(admin_workspace+"/GIS_CANSYS.DBO.V_ACCS_SDO_V",AADT,"CRND_RTE;LRS_KEY;STATE_LRS;ROUTE_NO;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;ACS_CTRL_ID;ACS_CTRL_ID_DESC","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
    ChangePrivileges_management(AADT, "readonly", "GRANT", "AS_IS")

def PostProcLRS():
    #this will create the calibrated network LRMs and the calibration points which are useful for other referential methods
    MResolution = 0.0005
    MTolerance = 0.001
    env.MTolerance = MTolerance
    env.MResolution = MResolution

    try:
        #copying these layers, the routes measures are already calibrated, measures as they should be
        #the FC2Fc was changed in the document to show only the primary route, mitigating hte need for the V_LRSNETS view
        FeatureClassToFeatureClass_conversion(admin_workspace+"/GIS_CANSYS.DBO.V_LRSS_SDO_R",admin_workspace,"SMLRS","DIRECTION in (1, 2)","#","#")
        ChangePrivileges_management(admin_workspace+"/GIS_CANSYS.DBO.SMLRS", "readonly", "GRANT", "AS_IS")
        FeatureClassToFeatureClass_conversion(admin_workspace+"/GIS_CANSYS.DBO.V_LRSC_SDO_R",admin_workspace,"CMLRS","DIRECTION in (1, 2)","#","#")
        ChangePrivileges_management(admin_workspace+"/GIS_CANSYS.DBO.CMLRS", "readonly", "GRANT", "AS_IS")
        #Oracle EXOR require M values at ever vertex
        #over time EXOR measures have become a bit of a mess, because of non-functional route calibration tools prior to 2012-2013
        #measures should be based on stationing and increase linearly along a project except at the location of an equation
        #assets are based on whatever section reference they are given, so if the section measures change, so does the asset location
    except:
        endingTime = datetime.datetime.now()
        ScriptStatusLogging('CANP_LRS_EXPORT.py', 'PostProcLRS Function',
                            scriptFailure, startingTime,
                            endingTime, GetMessages(2))

        pass

def PostProcCalibPts():
    #this will create the calibrated network LRMs and the calibration points which are useful for other referential methods
    MResolution = 0.0005
    MTolerance = 0.001
    env.MTolerance = MTolerance
    env.MResolution = MResolution

    LRM_NAMES = ["SMLRS", "CMLRS"]
    try:
        for LRM in LRM_NAMES:
            print "converting "+LRM+" to point features "+str(datetime.datetime.now())
            #this is rather expensive
            FeatureVerticesToPoints_management(admin_workspace+"/GIS_CANSYS.DBO."+LRM,admin_workspace+"/GIS_CANSYS.DBO."+LRM+"_Point","ALL")
            print "adding calibration values to "+LRM+" point features "+str(datetime.datetime.now())
            #this is VERY expensive and should be replaced by a da cursor that calculates SHAPE@M
            #for now this is easy and convenient to attribute the M value at every point
            AddXY_management(admin_workspace+"/GIS_CANSYS.DBO."+LRM+"_Point")
            #AddXY might take an hour total for both LRMS
            print "finished " +LRM +" LRM processing " +str(datetime.datetime.now())
            ChangePrivileges_management(admin_workspace+"/GIS_CANSYS.DBO."+LRM+"_Point", "readonly", "GRANT", "AS_IS")
    except:
        endingTime = datetime.datetime.now()
        ScriptStatusLogging('CANP_LRS_EXPORT.py', 'PostProcCalibPts Function failed while attempting to calibrate ' + str(LRM),
                            scriptFailure, startingTime,
                            endingTime, GetMessages(2))

        pass

if __name__ == '__main__':
    #Listing all the layers helps to troubleshoot the script sometimes, no need to run this as automation
    #ListAllLyrs()
    #unlock and block connections to the working database
    Unlock(admin_workspace)

    #Export the listed CANP layers
    ExportCANPLyrs(admin_workspace)

    #Export the NUSYS Rootes and layers
    #ExportNUSYS(admin_workspace)

    #update and process data that changes annually or less, or is time consuming to run
    #!PostProcAnnum(admin_workspace)

    #Export the listed GISPROD layers
    ExportGISProdLyrs(admin_workspace)

    #Update the Routes and Calibration Points
    #PostProcLRS()

    #Post process and dissolve the CANP layers for basic, efficient GIS use
    PostProcDissolve()

    #Don't run PostProcCalibPts every day, as needed
    #PostProcCalibPts()

    AcceptConnections(admin_workspace, True)
    print "done"

    endingTime = datetime.datetime.now()
    try:
        ScriptStatusLogging('CANP_LRS_EXPORT.py', 'CANSYS.DBO.V_*',
                            scriptSuccess, startingTime,
                            endingTime, 'Completed Successfully')
    except:
        print "script completed, but no logging was written"