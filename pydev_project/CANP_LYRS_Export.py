'''
Created on Feb 19, 2014

@author: kyleg
'''
import datetime, sys, traceback
from arcpy import ListUsers, AddXY_management, FeatureVerticesToPoints_management, MakeFeatureLayer_management, TableToTable_conversion, ChangePrivileges_management, DisconnectUser, AcceptConnections, GetMessages, AddError, Dissolve_management, mapping, FeatureClassToFeatureClass_conversion, env, ExecuteError
mxd = mapping.MapDocument(r"\\dt00mh71\Planning\Gad\Maps\inv sdo views1.mxd")
admin_workspace = r"Database Connections\SQL61_GIS_CANSYS.sde"
env.overwriteOutput = True
#notlist = #"NM3.NM_INV_ACCL_SDO_V" "NM3.NM_INV_AADT_SDO_V", "NM3.NM_INV_CAPS_SDO_V","NM3.NM_INV_EPFS_SDO_V",
#dolist = ["NM3.NM_INV_SMAP_SDO_V"]
CANPlist = ["KDOT.MVMAP_STATE_SYSTEM","KDOT.MVMAP_CMLRS", "KDOT.MVMAP_SMLRS", "NM3.NM_NET_SECT_SDO_R", "NM3.NM_NLT_SRND_SDO_R", "NM3.NM_NLT_CRND_SDO_R", "NM3.NM_INV_CPMS_SDO_V", "NM3.NM_INV_ACCS_SDO_V","NM3.NM_INV_ADMO_SDO_V","NM3.NM_INV_ANAL_SDO_V","NM3.NM_INV_AVSP_SDO_V","NM3.NM_INV_CITY_SDO_V","NM3.NM_INV_CPAV_SDO_V","NM3.NM_INV_DLDS_SDO_V","NM3.NM_INV_FHWA_SDO_V","NM3.NM_INV_FLDN_SDO_V","NM3.NM_INV_FLEX_SDO_V","NM3.NM_INV_FRNT_SDO_V","NM3.NM_INV_FUN_SDO_V","NM3.NM_INV_GPGR_SDO_V","NM3.NM_INV_GRAD_SDO_V","NM3.NM_INV_HPPA_SDO_V","NM3.NM_INV_HCUR_SDO_V","NM3.NM_INV_HPMS_SDO_V","NM3.NM_INV_HPSR_SDO_V","NM3.NM_INV_INTC_SDO_V","NM3.NM_INV_INTR_SDO_V","NM3.NM_INV_LAND_SDO_V","NM3.NM_INV_LANE_SDO_V","NM3.NM_INV_LINT_SDO_V","NM3.NM_INV_LNCL_SDO_V","NM3.NM_INV_LYRS_SDO_V","NM3.NM_INV_MASA_SDO_V","NM3.NM_INV_MED_SDO_V","NM3.NM_INV_MNTR_SDO_V","NM3.NM_INV_MSSS_SDO_V","NM3.NM_INV_NHS_SDO_V","NM3.NM_INV_PASS_SDO_V","NM3.NM_INV_PMID_SDO_V","NM3.NM_INV_POEQ_SDO_V","NM3.NM_INV_PONO_SDO_V","NM3.NM_INV_POPD_SDO_V","NM3.NM_INV_PSE_SDO_V","NM3.NM_INV_RMBL_SDO_V","NM3.NM_INV_ROWY_SDO_V","NM3.NM_INV_RPAC_SDO_V","NM3.NM_INV_SAFE_SDO_V","NM3.NM_INV_SCID_SDO_V","NM3.NM_INV_SHLD_SDO_V","NM3.NM_INV_SKID_SDO_V","NM3.NM_INV_SMAP_SDO_V","NM3.NM_INV_SNIC_SDO_V","NM3.NM_INV_SPED_SDO_V","NM3.NM_INV_SSF_SDO_V","NM3.NM_INV_STHN_SDO_V","NM3.NM_INV_STND_SDO_V","NM3.NM_INV_STP_SDO_V","NM3.NM_INV_STRP_SDO_V","NM3.NM_INV_SWID_SDO_V","NM3.NM_INV_SWMN_SDO_V", "NM3.NM_INV_SWZ_SDO_V", "NM3.NM_INV_TERR_SDO_V", "NM3.NM_INV_TOLL_SDO_V", "NM3.NM_INV_TRAF_SDO_V", "NM3.NM_INV_TRUS_SDO_V", "NM3.NM_INV_UAB_SDO_V", "NM3.NM_INV_UABL_SDO_V", "NM3.NM_INV_VCUR_SDO_V", "NM3.NM_INV_WDOB_SDO_V"]
#CANPlist = ["KDOT.MVMAP_LRSNETC", "KDOT.MVMAP_LRSNETS"]
gisprodlist = ["SHARED.FUTURE_NETWORK"]
#CANPlist = ["NM3.NM_NLT_SRND_SDO_R", "NM3.NM_NLT_CRND_SDO_R","NM3.NM_INV_AADT_SDO_V"]
#CANPlist = ["NM3.NM_INV_LANE_SDO_V", "NM3.NM_INV_MED_SDO_V", "NM3.NM_INV_SHLD_SDO_V"]
#print CANPlist
def ListAllLyrs():
    print "layer list initialized at "+str(datetime.datetime.now())
    for lyr in mapping.ListLayers(mxd):
        try:
            lyrname = lyr.name 
            print lyrname
        except:
            print "there was a problem with this layer"  +str(datetime.datetime.now())
            pass
        
        
def ExportCANPLyrs():
    print "exporting initialized at "+str(datetime.datetime.now())
    destConnection = r"D:\SQL61_GIS_CANSYS.sde" 
    TableToTable_conversion("MAP_EXTRACT",r"Database Connections/SQL61_GIS_CANSYS.sde","Map_Extract","#","#","#")
    for lyr in mapping.ListLayers(mxd):
        if lyr.name in CANPlist:
            try:
                lyrname = lyr.name[11:] 
                print lyrname +" exporting..."
                outlyrname = "V_"+lyrname
                outlyrobj = destConnection+"\\GIS_CANSYS.DBO."+outlyrname
                FeatureClassToFeatureClass_conversion(lyr, destConnection, outlyrname, "#","#","#")
                ChangePrivileges_management(outlyrobj, "readonly", "GRANT", "AS_IS")
                print lyrname +" exported to " +outlyrname +" "+ str(datetime.datetime.now())
            except ExecuteError: 
                msgs = GetMessages(2) 
                AddError(msgs) 
                print msgs
                pass 
            except (RuntimeError, TypeError, NameError):
                print "TypeError on item" + lyr.name
                pass
            except:
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                # Concatenate information together concerning the error into a message string
                #
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                msgs = "ArcPy ERRORS:\n" + GetMessages(2) + "\n"
                print pymsg + "\n"
                print msgs
                            
        else:
            #print lyr.name +" was not in the export list and will be skipped"
            pass

def ExportGISProdLyrs():
    print "exporting initialized at "+str(datetime.datetime.now())
    destConnection = r"D:\SQL61_GIS_CANSYS.sde" 
    for lyr in mapping.ListLayers(mxd):
        if lyr.name in gisprodlist:
            try:
                lyrname = lyr.name[7:]
                print lyrname +" exporting..."
                outlyrname = lyrname
                outlyrobj = destConnection+"\\GIS_CANSYS.DBO."+outlyrname
                FeatureClassToFeatureClass_conversion(lyr, destConnection, outlyrname, "#","#","#")
                ChangePrivileges_management(outlyrobj, "readonly", "GRANT", "AS_IS")
                print lyrname +" exported to " +outlyrname +" "+ str(datetime.datetime.now())
            except ExecuteError: 
                msgs = GetMessages(2) 
                AddError(msgs) 
                print msgs
                pass 
            except (RuntimeError, TypeError, NameError):
                print "TypeError on item" + lyr.name
                pass
            except:
                tb = sys.exc_info()[2]
                tbinfo = traceback.format_tb(tb)[0]
                #
                pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
                msgs = "ArcPy ERRORS:\n" + GetMessages(2) + "\n"
                print pymsg + "\n"
                print msgs   
        else:
            #print lyr.name +" was not in the export list and will be skipped"
            return

def Unlock(admin_workspace):
    env.workspace = admin_workspace
    users = ListUsers(admin_workspace) #
    print users
    AcceptConnections(admin_workspace, False)
    DisconnectUser(admin_workspace, "All")

def PostProcDissolve():
    Unlock(admin_workspace)
    
    ACCS = "Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.ACCS"
    Unlock(admin_workspace)
    Dissolve_management("Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.V_ACCS_SDO_V",ACCS,"CRND_RTE;LRS_KEY;STATE_LRS;ROUTE_NO;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;ACS_CTRL_ID;ACS_CTRL_ID_DESC","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
    ChangePrivileges_management(ACCS, "readonly", "GRANT", "AS_IS")
    
    SMAP = "Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.SMAP"
    Unlock(admin_workspace)
    Dissolve_management("Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.V_SMAP_SDO_V",SMAP,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;STATIONING_TYPE;STATIONING_TYPE_DESC;BEGIN_STATIONING;BEGIN_STATIONING_DECIMAL;END_STATIONING;END_STATIONING_DECIMAL;PROJECT_YEAR;PROJECT_NUMBER;PROJECT_TYPE;PROJECT_TYPE_DESC;HOST_PROJECT_NUMBER;PW_URL","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
    ChangePrivileges_management(SMAP, "readonly", "GRANT", "AS_IS")
    print "SMAP dissolved for viewing"
    
    LYRS = "Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.LYRS"
    Dissolve_management("Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.V_LYRS_SDO_V",LYRS,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;LAYER_TYPE;LAYER_TYPE_DESC;MATERIAL_TYPE;MATERIAL_TYPE_DESC;DEPTHS_MILLIMETERS;LAYER_DATE;MATERIAL_WIDTH_METERS;MATERIAL_WIDTH_FEET;SOURCE_TYPE;SOURCE_TYPE_DESC;PROJECT_ID;PW_URL","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
    ChangePrivileges_management(LYRS, "readonly", "GRANT", "AS_IS")
    print "LYRS dissolved for viewing"
    
    LNCL = "Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.LNCL"
    MakeFeatureLayer_management("Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.V_LNCL_SDO_V","LNCL_PRIMARY","CRND_RTE LIKE '%EB' OR CRND_RTE LIKE '%NB'","#","OBJECTID OBJECTID VISIBLE NONE;CRND_RTE CRND_RTE VISIBLE NONE;LRS_KEY LRS_KEY VISIBLE NONE;BCMP BCMP VISIBLE NONE;ECMP ECMP VISIBLE NONE;BSMP BSMP VISIBLE NONE;ESMP ESMP VISIBLE NONE;COUNTY_CD COUNTY_CD VISIBLE NONE;COUNTY_NAME COUNTY_NAME VISIBLE NONE;LANE_DIRECTION LANE_DIRECTION VISIBLE NONE;DISTRICT DISTRICT VISIBLE NONE;DIV_UNDIV DIV_UNDIV VISIBLE NONE;LNCL_CLS_ID LNCL_CLS_ID VISIBLE NONE;LNCL_CLS_ID_DESC LNCL_CLS_ID_DESC VISIBLE NONE;LNCL_DT LNCL_DT VISIBLE NONE;Shape Shape VISIBLE NONE;Shape.STLength() Shape.STLength() VISIBLE NONE")
    Dissolve_management("LNCL_PRIMARY",LNCL,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;LNCL_CLS_ID;LNCL_CLS_ID_DESC","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
    ChangePrivileges_management(LNCL, "readonly", "GRANT", "AS_IS")
    print "LYRS dissolved for viewing"
    
    CPMS = "Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.CPMS"
    Dissolve_management("Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.V_CPMS_SDO_V", CPMS,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;SCHEME_ID;PROJECT_ID;TECH_NAME;WORK_TYPE_DESC;DESIGN_CRITERIA;LEG_MAP_ID;CATEGORY_CODE;SUBCAT_CODE;PROJECT_DESC_FRND;PROJ_DISTRICT;PROJ_AREA;PROJ_SUB_AREA;PROJ_LENGTH;HOST_PROJ_NUM;FISCAL_YEAR_PRGM;LETTING_DATE;PW_URL","BCMP MIN;BSMP MIN;ECMP MAX;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
    ChangePrivileges_management(CPMS, "readonly", "GRANT", "AS_IS")    
    print "CPMS dissolved for viewing"
    
    POEQ = "Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.POEQ"
    Dissolve_management("Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.V_POEQ_SDO_V",POEQ, "CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;IRIR;RLIFE;RLIFE_DEFAULT;RLIFE_DEFAULT_DESC;EQFAULT;EQJD;EQTCR;RUTVAL;PVMTGRP;PVMTGRP_DESC;DEF_FLAG;DEF_FLAG_DESC;POEQ_DT;MEAN_IRIR;YEAR_LAST_IMP;YEAR_LAST_CONST;LAST_OVERLAY_THIC;IRIR_DATE;IRIR_DATE_DEFAULT;IRIR_DATE_DEFAULT_DESC","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
    ChangePrivileges_management(POEQ, "readonly", "GRANT", "AS_IS")   
    print "POEQ dissolved for viewing"
    
    HPPA = "Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.HPPA"
    Dissolve_management("GIS_CANSYS.DBO.V_HPPA_SDO_V", HPPA,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;HPMS_SURFACE_TYPE;HPMS_SURFACE_TYPE_DESC;HPMS_YEAR_LAST_IMPROV;HPMS_YEAR_LAST_CONST;HPMS_LAST_OVERLAY_THICK;HPMS_THICKNESS_RIGID;HPMS_THICKNESS_FLEXIBLE;HPMS_BASE_TYPE;HPMS_BASE_TYPE_DESC;HPMS_BASE_THICKNESS","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
    ChangePrivileges_management(HPPA, "readonly", "GRANT", "AS_IS")   
    print "HPPA dissolved for viewing"
    
    SPED = "Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.SPED"
    Dissolve_management("GIS_CANSYS.DBO.V_SPED_SDO_V", SPED,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;SPD_LMT;SPD_LMT_DESC;SPED_RESOL","#","MULTI_PART","DISSOLVE_LINES")
    ChangePrivileges_management(SPED, "readonly", "GRANT", "AS_IS")   
    print "SPED dissolved for viewing"
    
    FUN =  "Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.FUN"
    Dissolve_management("GIS_CANSYS.DBO.V_FUN_SDO_V", FUN,"CRND_RTE;LRS_KEY;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;FUN_CLASS;FUN_CLASS_DESC;DONUT_SMPL;DONUT_SMPL_DESC;FUN_DT;OLD_FUN_CLASS","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
    ChangePrivileges_management(FUN, "readonly", "GRANT", "AS_IS")  
    print "FUN dissolved for viewing"
    
    AcceptConnections(admin_workspace, True) 

def PostProcAnnum():
    Unlock(admin_workspace)
    
    AADT = "Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.ACCS"
    Unlock(admin_workspace)
    Dissolve_management("Database Connections/SQL61_GIS_CANSYS.sde/GIS_CANSYS.DBO.V_ACCS_SDO_V",AADT,"CRND_RTE;LRS_KEY;STATE_LRS;ROUTE_NO;COUNTY_CD;COUNTY_NAME;LANE_DIRECTION;DISTRICT;DIV_UNDIV;ACS_CTRL_ID;ACS_CTRL_ID_DESC","BCMP MIN;ECMP MAX;BSMP MIN;ESMP MAX","MULTI_PART","DISSOLVE_LINES")
    ChangePrivileges_management(AADT, "readonly", "GRANT", "AS_IS")
    
    AcceptConnections(admin_workspace, True)

def PostProcLRS():
    MResolution = 0.0005 
    MTolerance = 0.001 
    env.MTolerance = MTolerance
    env.MResolution = MResolution
    LRM_NAMES = ["CMLRS", "SMLRS"]
    FeatureClassToFeatureClass_conversion(admin_workspace+"/GIS_CANSYS.DBO.V_LRSNETS",admin_workspace,"SMLRS","DIRECTION in (1, 2)","#","#")
    ChangePrivileges_management(admin_workspace+"/GIS_CANSYS.DBO.SMLRS", "readonly", "GRANT", "AS_IS")
    FeatureClassToFeatureClass_conversion(admin_workspace+"/GIS_CANSYS.DBO.V_LRSNETC",admin_workspace,"CMLRS","DIRECTION in (1, 2)","#","#")
    ChangePrivileges_management(admin_workspace+"/GIS_CANSYS.DBO.CMLRS", "readonly", "GRANT", "AS_IS")
    for LRM in LRM_NAMES:
        print "converting "+LRM+" to point features "+str(datetime.datetime.now())
        FeatureVerticesToPoints_management(admin_workspace+"/GIS_CANSYS.DBO."+LRM,admin_workspace+"/GIS_CANSYS.DBO."+LRM+"_Point","ALL")
        print "adding calibration values to "+LRM+" point features "+str(datetime.datetime.now())
        AddXY_management(admin_workspace+"/GIS_CANSYS.DBO."+LRM+"_Point")
        print "finished " +LRM +" LRM processing " +str(datetime.datetime.now())
        ChangePrivileges_management(admin_workspace+"/GIS_CANSYS.DBO."+LRM+"_Point", "readonly", "GRANT", "AS_IS")

if __name__ == '__main__':
    #ListAllLyrs()
    Unlock(admin_workspace)
    ExportCANPLyrs()
    PostProcDissolve()
    #PostProcAnnum()
    ExportGISProdLyrs()
    PostProcLRS()
    AcceptConnections(admin_workspace, True)
    print "completed view export processes"