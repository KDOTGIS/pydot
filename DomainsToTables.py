'''
Created on May 11, 2015

mostly copied from http://resources.arcgis.com/en/help/main/10.1/index.html#//018w0000001z000000
which prints the domain name and values, 
also added the line to export the domain to table, for data diagramming

@author: kyleg
'''
import arcpy
indb = r"\\gisdata\planning\Cart\projects\ARNOLD POOLED FUND\geodata\MIRE_GDB_Template_DecodeToTable.gdb"
domains = arcpy.da.ListDomains(indb)  # @UndefinedVariable

for domain in domains:
    print('Domain name: {0}'.format(domain.name))
    if domain.domainType == 'CodedValue':
        coded_values = domain.codedValues     
        for val, desc in coded_values.iteritems():
            print('{0} : {1}'.format(val, desc))
        
    elif domain.domainType == 'Range':
        print('Min: {0}'.format(domain.range[0]))
        print('Max: {0}'.format(domain.range[1]))
    print domain.name
    outtbl = indb+"/"+domain.name
    
    arcpy.DomainToTable_management(in_workspace=indb, domain_name=domain.name, out_table=outtbl, code_field="CODE", description_field="DESC", configuration_keyword="")

    #arcpy.DomainToTable_management(in_workspace=indb, domain_name=domain.name, out_table=outtbl, code_field="CODE", description_field="DESC", configuration_keyword="")
