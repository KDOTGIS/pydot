#written by Kyle 10/11/12
# Description
# Create Domain, select distinct values in field, append to domain, and assign domain to field

#
from arcpy import SearchCursor, TableToTable_conversion, TableToDomain_management, env, AssignDomainToField_management, RegisterWithGeodatabase_management
env.overwriteOutput = 1

fcName = r'Database Connections\Collect16_SDE.sde\Collect16.sde.CIIMS_CROSSINGDATA_DOMAINVAL'
DomainGDB = r'C:\temp\CrossingDomainTables.gdb'
DataTable = r'Database Connections\Collect16_SDE.sde\Collect16.SDE.CIIMS_CROSSINGDATA'
EnterpriseGDB = r'Database Connections\Collect16_SDE.sde'
fldName = 'CrossingData'

#RegisterWithGeodatabase_management(EnterpriseGDB+r"/Collect16.sde.CIIMS_CROSSINGDATA_DOMAINVAL")

myList = set([row.getValue(fldName) for row in SearchCursor(fcName, fields=fldName)]) 
print myList

for attrib in myList:
    sels = str(fldName.strip())+" = '"+ attrib+"'"
    print sels
    outname = 'd'+str(attrib)
    print outname
    TableToTable_conversion(fcName,DomainGDB,outname,sels)
    TableToDomain_management(DomainGDB+"/"+outname,"DESCRIPTIONS","DESCRIPTIONS",EnterpriseGDB, outname, attrib, "REPLACE")
    AssignDomainToField_management(DataTable, attrib, outname, subtype_code="")
print "All Cansys Domains copied to temp mdb as coded text values"        
