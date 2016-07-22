'''
Created on Jun 8, 2016

@author: kyleg
'''
from arcpy import CreateEnterpriseGeodatabase_management
database_platform="SQL_Server"
instance_name=r"dt00ar56\GDB_PROD"
database_name="Collector16A"
account_authentication="DATABASE_AUTH"
database_admin="geo_admin"
database_admin_password=raw_input('Enter the geo_admin password:')
sde_schema="SDE_SCHEMA"
gdb_admin_name="sde"
gdb_admin_password=raw_input('Enter the sde user password:')
tablespace_name=""
auth=r"\\dt00ar60\C$\Program Files\ESRI\License10.3\sysgen\keycodes"

CreateEnterpriseGeodatabase_management(database_platform, instance_name, database_name, account_authentication, database_admin, database_admin_password, sde_schema, gdb_admin_name, gdb_admin_password, tablespace_name, auth)

## Collector201621 - drop_fields