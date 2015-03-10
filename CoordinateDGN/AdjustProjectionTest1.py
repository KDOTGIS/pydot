'''
Created on Aug 7, 2013

@author: kyleg
'''
import arcpy

DGN_IN = r"C:/pwworking/kyleg/dms90199/slt_ROW_exist.dgn"

CAF = '0.9997'
PAF = 1/CAF
GCS_NAD83= r"GEOGCS['GCS_North_American_1983',"
DATUM = r"DATUM['D_North_American_1983',"
KSS = r"PROJCS['NAD_1983_StatePlane_Kansas_South_FIPS_1501_Feet',"
KSN = r"PROJCS['NAD_1983_StatePlane_Kansas_North_FIPS_1501_Feet',"
SPH = r"SPHEROID['GRS_1980',6378137.0,298.257222101]],"
PRIMEM = r"PRIMEM['Greenwich',0.0],"
UNIT = r"UNIT['Degree',0.0174532925199433]],"
PROJ = r"PROJECTION['Lambert_Conformal_Conic'],"
EAST = "PARAMETER['False_Easting',"+1312333.333333333*PAF+"],"
NorthN = "PARAMETER['False_Northing',"+0.0*PAF+"],"
NorthS = "PARAMETER['False_Northing',"+1312333.333333333*PAF+"]"
MeridN = "PARAMETER['Central_Meridian',-98.0],"
MeridS = "PARAMETER['Central_Meridian',-98.5], "
Paral1N = "PARAMETER['Standard_Parallel_1',38.71666666666667],"
Paral2N = "PARAMETER['Standard_Parallel_2',39.78333333333333],"
Paral1S = "PARAMETER['Standard_Parallel_1',37.26666666666667],"
Paral2S = "PARAMETER['Standard_Parallel_2',38.56666666666667],"
SF = "PARAMETER'Scale_Factor',"+PAF+"]"
OrgLatN = "PARAMETER['Latitude_Of_Origin',38.33333333333334],"
OrgLatS = "PARAMETER['Latitude_Of_Origin',36.66666666666666],"
Unit = "UNIT['Foot_US',0.3048006096012192]]"

#multiply  false easting * PAF
#multiply false northing * PAF
#set PAF as Scale Factor
#reset Meridians, standard parallels, and lat or orgin if needed

KSN = GCS_NAD83+DATUM+KSN+SPH+PRIMEM+UNIT+PROJ+EAST+NorthN+MeridN+Paral1N+Paral2N+SF+OrgLatN+Unit
KSS = GCS_NAD83+DATUM+KSS+SPH+PRIMEM+UNIT+PROJ+EAST+NorthS+MeridS+Paral1S+Paral2S+SF+OrgLatS+Unit

arcpy.DefineProjection_management(DGN_IN,KSN)