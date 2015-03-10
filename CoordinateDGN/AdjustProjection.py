'''
Created on Aug 7, 2013

@author: kyleg
'''
import arcpy
arcpy.env.overwriteOutput = True
DGN_IN = arcpy.GetParameterAsText(0)
#r"C:/pwworking/kyleg/dms90199/slt_ROW_exist.dgn"
Projection = arcpy.GetParameterAsText(1)
Projection = 'North'
CAF = arcpy.GetParameterAsText(2)
# = 0.99992146
wsuser = "%APPDATA%\ESRI\ESRI\Desktop10.1\ArcMap\Coordinate Systems"
PAF = 1/float(CAF)
GCS_NAD83= r"GEOGCS['GCS_North_American_1983',"
DATUM = r"DATUM['D_North_American_1983',"
KSS = r"PROJCS['NAD_1983_StatePlane_Kansas_South_custom',"
KSN = r"PROJCS['NAD_1983_StatePlane_Kansas_North_custom',"
SPH = r"SPHEROID['GRS_1980',6378137.0,298.257222101]],"
PRIMEM = r"PRIMEM['Greenwich',0.0],"
UNIT = r"UNIT['Degree',0.0174532925199433]],"
PROJ = r"PROJECTION['Lambert_Conformal_Conic'],"
EAST = "PARAMETER['False_Easting',"+str(1312333.333333333*PAF)+"],"
NorthN = "PARAMETER['False_Northing',"+str(0.0*PAF)+"],"
NorthS = "PARAMETER['False_Northing',"+str(1312333.333333333*PAF)+"]"
MeridN = "PARAMETER['Central_Meridian',-98.0],"
MeridS = "PARAMETER['Central_Meridian',-98.5], "
Paral1N = "PARAMETER['Standard_Parallel_1',38.71666666666667],"
Paral2N = "PARAMETER['Standard_Parallel_2',39.78333333333333],"
Paral1S = "PARAMETER['Standard_Parallel_1',37.26666666666667],"
Paral2S = "PARAMETER['Standard_Parallel_2',38.56666666666667],"
SF = "PARAMETER'[Scale_Factor',"+str(PAF)+"]"
OrgLatN = "PARAMETER['Latitude_Of_Origin',38.33333333333334],"
OrgLatS = "PARAMETER['Latitude_Of_Origin',36.66666666666666],"
Unit = "UNIT['Foot_US',0.3048006096012192]]"

KSN1 = KSN+GCS_NAD83+DATUM+SPH+PRIMEM+UNIT+PROJ+EAST+NorthN+MeridN+Paral1N+Paral2N+SF+OrgLatN+Unit
KSS1 = KSS+GCS_NAD83+DATUM+SPH+PRIMEM+UNIT+PROJ+EAST+NorthS+MeridS+Paral1S+Paral2S+SF+OrgLatS+Unit

print KSN1
def project(DGN_IN, Projection):
    if Projection == 'North':
        arcpy.DefineProjection_management(DGN_IN,KSN1)
        print "projected in Modified State Plane north"
        arcpy.SpatialReference.createFromFile(self)
    elif Projection == 'South':
        arcpy.DefineProjection_management(DGN_IN,KSS1)
        print "projected in Modified State Plane South"
    else:        
        print "could not project - enter north or south"
    return project