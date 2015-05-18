'''
Created on May 12, 2015

@author: kyleadm
'''
  
   
def ChooseTargetEnv(OpEnvironment, RunInProd):
    if RunInProd == False:
        OpEnvironment.OpRunInSum = OpEnvironment.FME_ITEM_SUM
        OpEnvironment.OpRunInDSum = OpEnvironment.FME_ITEM_DIRSUM
        OpEnvironment.OpRunInXSum = OpEnvironment.FME_ITEM_DIRXSP
        OpEnvironment.OpRunInRoutes = OpEnvironment.FME_NET
        OpEnvironment.OpRunOut = OpEnvironment.GIS_TARGET_CONN_DEV
        OpEnvironment.adm = OpEnvironment.GIS_TARGET_CONN_DEV_ADMIN
        OpEnvironment.Owner = OpEnvironment.GIS_TARGET_DB_OWNER_DEV
        OpEnvironment.DB = OpEnvironment.GIS_TARGET_DB_DEV
        return OpEnvironment
        
    elif RunInProd == True:
        OpEnvironment.OpRunInSum = OpEnvironment.FME_ITEM_SUM
        OpEnvironment.OpRunInDSum = OpEnvironment.FME_ITEM_DIRSUM
        OpEnvironment.OpRunInXSum = OpEnvironment.FME_ITEM_DIRXSP
        OpEnvironment.OpRunInRoutes = OpEnvironment.FME_NET
        OpEnvironment.OpRunOut = OpEnvironment.GIS_TARGET_CONN_PROD
        OpEnvironment.adm = OpEnvironment.GIS_TARGET_CONN_PROD_ADMIN     
        OpEnvironment.Owner = OpEnvironment.GIS_TARGET_DB_OWNER_PROD
        OpEnvironment.DB = OpEnvironment.GIS_TARGET_DB_PROD
        return OpEnvironment
    else:
        print "choose an environment to run in, dev, prod, or define other"
        
        
        
if __name__ == '__main__':
   
    pass