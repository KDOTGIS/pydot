'''
Created on Dec 18, 2014

@author: kyleg
'''
from arcpy import AddField_management, SelectLayerByAttribute_management, CalculateField_management
def MSAG_CHECK_LRS1():
    #Add fields to model the MSAG Street keys and ranges
    AddField_management("RoadCenterline","MSAG_KEY","TEXT","#","#","#","#","NULLABLE","NON_REQUIRED","#")
    AddField_management("RoadCenterline","MSAG_HIGH","TEXT","#","#","6","#","NULLABLE","NON_REQUIRED","#")
    AddField_management("RoadCenterline","MSAG_LOW","TEXT","#","#","6","#","NULLABLE","NON_REQUIRED","#")
        
    #these are the rows where the left from address is the lowest valid address range number
    SelectLayerByAttribute_management("RoadCenterline","NEW_SELECTION","(PARITY_L  in ( 'E' , 'O' ) AND L_F_ADD < R_T_ADD AND L_F_ADD < R_F_ADD AND L_F_ADD <= L_T_ADD ) OR (PARITY_R= 'Z' AND PARITY_L  in ( 'E' , 'O' ))")
    CalculateField_management("RoadCenterline","MSAG_LOW","!L_F_ADD!","PYTHON_9.3","#")
    
    #these are the rows where the right from address is the lowest valid address range number
    SelectLayerByAttribute_management("RoadCenterline","NEW_SELECTION","(PARITY_R  in ( 'E' , 'O' ) AND R_F_ADD < R_T_ADD AND R_F_ADD < L_F_ADD AND R_F_ADD <= L_T_ADD ) OR (PARITY_L= 'Z' AND PARITY_R  in ( 'E' , 'O' ))")
    CalculateField_management("RoadCenterline","MSAG_LOW","!R_F_ADD!","PYTHON_9.3","#")
    
    #these are the rows where the left TO address is the lowest valid address range number
    SelectLayerByAttribute_management("RoadCenterline","NEW_SELECTION","(PARITY_L  in ( 'E' , 'O' ) AND L_T_ADD < L_F_ADD AND L_T_ADD < R_T_ADD AND L_T_ADD <= R_T_ADD ) OR (PARITY_R= 'Z' AND PARITY_L  in ( 'E' , 'O' ))")
    CalculateField_management("RoadCenterline","MSAG_LOW","!L_F_ADD!","PYTHON_9.3","#")
    
    #these are the rows where the right TO address is the lowest valid address range number
    SelectLayerByAttribute_management("RoadCenterline","NEW_SELECTION","(PARITY_R  in ( 'E' , 'O' ) AND R_F_ADD < R_T_ADD AND R_F_ADD < L_F_ADD AND R_F_ADD <= L_T_ADD ) OR (PARITY_L= 'Z' AND PARITY_R  in ( 'E' , 'O' ))")
    CalculateField_management("RoadCenterline","MSAG_LOW","!R_F_ADD!","PYTHON_9.3","#")
    
    
    #create routes based on MSAG keys and MSAG ranges