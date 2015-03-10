'''
Created on Aug 7, 2013

@author: kyleg
'''
import os, shutil, arcpy

appdata = os.getenv('APPDATA')
wsuser = appdata+"\ESRI\Desktop10.1\ArcMap\Coordinate Systems"

ProjName = arcpy.GetParameterAsText(0)
#Projection_Name = 'test'
Projection = arcpy.GetParameterAsText(1)
#Projection = 'North'
CAF = arcpy.GetParameterAsText(2)
#CAF = '0.99992146'

PAF = 1/float(CAF)
GCS_NAD83= r'GEOGCS["GCS_North_American_1983",'
DATUM = r'DATUM["D_North_American_1983",'
KSS = r'PROJCS["KDOT_CUSTOM_'+ProjName+'_'+Projection+'",'
KSN = r'PROJCS["KDOT_CUSTOM_'+ProjName+'_'+Projection+'",'
SPH = r'SPHEROID["GRS_1980",6378137.0,298.257222101]],'
PRIMEM = r'PRIMEM["Greenwich",0.0],'
UNIT = r'UNIT["Degree",0.0174532925199433]],'
PROJ = r'PROJECTION["Lambert_Conformal_Conic"],'
EAST = 'PARAMETER["False_Easting",'+str(1312333.333333333*PAF)[0:16]+"],"
NorthN = 'PARAMETER["False_Northing",'+str(0.0*PAF)[0:16]+"],"
NorthS = 'PARAMETER["False_Northing",'+str(1312333.333333333*PAF)[0:16]+"],"
MeridN = 'PARAMETER["Central_Meridian",-98.0],'
MeridS = 'PARAMETER["Central_Meridian",-98.5],'
Paral1N = 'PARAMETER["Standard_Parallel_1",38.71666666666667]'
Paral2N = 'PARAMETER["Standard_Parallel_2",39.78333333333333],'
Paral1S = 'PARAMETER["Standard_Parallel_1",37.26666666666667],'
Paral2S = 'PARAMETER["Standard_Parallel_2",38.56666666666667],'
SF = 'PARAMETER["Scale_Factor",'+str(PAF)[0:8]+"],"
OrgLatN = 'PARAMETER["Latitude_Of_Origin",38.33333333333334],'
OrgLatS = 'PARAMETER["Latitude_Of_Origin",36.66666666666666],'
Unit = 'UNIT["Foot_US",0.3048006096012192]]'

KSN1 = KSN+GCS_NAD83+DATUM+SPH+PRIMEM+UNIT+PROJ+EAST+NorthN+MeridN+Paral1N+Paral2N+SF+OrgLatN+Unit
KSS1 = KSS+GCS_NAD83+DATUM+SPH+PRIMEM+UNIT+PROJ+EAST+NorthS+MeridS+Paral1S+Paral2S+SF+OrgLatS+Unit


if Projection == 'North':
        srcfile = wsuser + "\\CUSTOM_NAD_1983_StatePlane_Kansas_North_FIPS_1501_Feet.prj"
        dstfile = wsuser+"\\"+"KDOT_CUSTOM_"+ProjName+'_'+Projection+".prj"
        shutil.copy2(srcfile, dstfile)
        output = open(dstfile, 'w')
        output.write(dstfile.replace('1312333.333333333',str((1312333.333333333*PAF)))[0:16])
elif Projection == 'South':
        srcfile = wsuser + "\\CUSTOM_NAD_1983_StatePlane_Kansas_South_FIPS_1501_Feet.prj"
        dstfile = wsuser+"\\KDOT_"+ProjName+".prj"
        shutil.copy2(srcfile, dstfile)
        output = open(dstfile, 'w')
        output.write(KSS1)
else:        
        print "enter North or South"
print "Check output workspace " 