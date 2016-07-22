'''
Created on Jun 22, 2016

@author: kyleg
'''

if __name__ == '__main__':
    pass

def ValidatetoFileGDB(TestFileGDB):
    from arcpy import ImportXMLWorkspaceDocument_management, ChangePrivileges_management, env, EnableEditorTracking_management

    version = 1
    env.workspace = 

    xmlversion = r"\\gisdata\planning\GIS\datamodel\sparx\Design\Collector2016062100.XML"

    ImportXMLWorkspaceDocument_management(ODB, xmlversion, import_type="SCHEMA_ONLY", config_keyword="GEOMETRY")
