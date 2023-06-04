import pandas as pd
from database import Conection
import time
conect=Conection()

def getId(tableName,title,condition):
    queryStr=f"SELECT {tableName}Id FROM {tableName} WHERE {condition}=N'{title}';"
    try:
        Id=pd.read_sql(queryStr,conect.cnxn).iloc[0,0]
    except:
        Id=None
    return Id


def insertTableValue(tablename:str, columnsName, values):


    queryStr=f"""
    INSERT INTO {tablename} {columnsName} OUTPUT INSERTED.{tablename}Id VALUES {values} ;
    """
    # print(queryStr,"===========")
    # try:
    if True:
        conect.cursor.execute(queryStr)
        id = conect.cursor.fetchone()[0]
        conect.cursor.commit()

    # except:
    #     return False

    
    return id


def getMax(tableName:str,columnsName:str):
    quryStr=f"""
    SELECT MAX({columnsName})
    FROM {tableName};
    """
    try:
        max_=pd.read_sql(quryStr,conect.cnxn).iloc[0,0]
    except:
        max_= 0
    if not max_:
        max_=0

    return max_


def returenAll(tableName):

    queyStr=f"""
    SELECT * FROM {tableName};
    """
    try:
        data = pd.read_sql_query(queyStr,conect.cnxn)
    except: 
        return False
    return data


def returnWithCondition(tableName :str ,title , condition :str):

    queryStr=f"""
    SELECT * FROM {tableName} WHERE {condition}={title}
    """
    data = pd.read_sql_query(queryStr , conect.cnxn)
    return data

   
def returnGoodsStock(stockId,goodsId=None):
    result={"goodsInventory":[]}
    querStr=f"""
    SELECT TOP 1
    DocHeaderId,
    CASE 
        WHEN StockTO = {stockId} THEN 'InventoryTo' 
        WHEN StockFrom = {stockId} THEN 'InventoryFrom'
        ELSE 'not found'
    END AS result
    FROM DocHeader
    WHERE 
    (StockTO = {stockId} OR StockFrom = {stockId})
    ORDER BY DocHeaderId DESC;
    """

    
    try:
        finalDocHeaderId=pd.read_sql_query(querStr,conect.cnxn)
        HeaderId=finalDocHeaderId.iloc[0,0]
        typeStock=finalDocHeaderId.iloc[0,1]
        print(typeStock,"==========================ID OF HEADER==================",HeaderId)
    except:
        return False
    
    print(finalDocHeaderId,"final header +===================================")
    
    print(goodsId==None,"====================goooooooooooooooooooods+==========")
    if goodsId:
        querStr=f"""
        SELECT GoodsId,{typeStock} FROM DocItem 
        WHERE DocHeaderId={HeaderId} and GoodsId={goodsId};
        """
    
    elif  goodsId==None:
        querStr=f"""
        SELECT GoodsId,{typeStock} FROM DocItem 
        WHERE DocHeaderId={HeaderId} ;
        """
    
    try:
    # if True:
        data=pd.read_sql_query(querStr,conect.cnxn)
    except:
        return False
    
    
    for i in range(len(data.index)):
        re={}
        goodID=data.iloc[i,0]
        goodInv=data.iloc[i,1]
        re['GoodsId']=int(goodID)
        re['goodInv']=int(goodInv)
        result["goodsInventory"].append(re)
        
    
    return result



def _checkInv(DocTypeId,DocHeaderId,goodsInfo,inventory,inventory2):

    if isinstance(inventory,dict):
        inventoryDict={}
        for item in inventory.get("goodsInventory"):
            inventoryDict[item['GoodsId']]=item['goodInv']
    
    if isinstance(inventory2,dict):
        inventoryDict2={}
        for item in inventory2.get("goodsInventory"):
            inventoryDict2[item['GoodsId']]=item['goodInv'] 
        
    for goods in goodsInfo:
       
        GoodsId=goods.get("GoodsId")
        Quantity=goods.get('Quantity')
        GoodsUnit=goods.get('GoodsUnitId')
       
        if not inventory  and DocTypeId !=3:
                
                insertTableValue(tablename='DocItem' , columnsName="(DocHeaderId,GoodsId,GoodsUnitId,Quantity,InventoryTO)",
                                    values=f"( {int(DocHeaderId)}  , {GoodsId} , {GoodsUnit} , {Quantity} , {Quantity} )")
                continue
        
        
        
        if GoodsId in inventoryDict and DocTypeId==2:
            goodsInv=inventoryDict[GoodsId]

            inv=int(Quantity)+int(goodsInv)
            insertTableValue(tablename='DocItem' , columnsName="(DocHeaderId,GoodsId,GoodsUnitId,Quantity,InventoryTO)",
                            values=f"( {int(DocHeaderId)}  , {GoodsId} , {GoodsUnit} , {Quantity} , {inv} )")
        
        if GoodsId in inventoryDict and DocTypeId==1:
            goodsInv=inventoryDict[GoodsId]
            inv=int(goodsInv)-int(Quantity)
            insertTableValue(tablename='DocItem' , columnsName="(DocHeaderId,GoodsId,GoodsUnitId,Quantity,InventoryFrom)",
                            values=f"( {int(DocHeaderId)}  , {GoodsId} , {GoodsUnit} , {Quantity} , {inv} )")
        
        if inventory2 != None :
            goodsInv=inventoryDict[GoodsId]
            invfrom = int(goodsInv)-int(Quantity)
            
            if inventory2 ==False:
                print("ooooooooooooooooooin oooooooooooooooo in ooooooooooooooooin oooooooooooooin ")
                insertTableValue(tablename='DocItem' , columnsName="(DocHeaderId,GoodsId,GoodsUnitId,Quantity,InventoryFrom,InventoryTO)",
                            values=f"( {int(DocHeaderId)}  , {GoodsId} , {GoodsUnit} , {Quantity} , {invfrom} ,{Quantity} )")
                continue


            if GoodsId in inventoryDict2:
                goodsInv2=inventoryDict[GoodsId]

            invTo = int(goodsInv2)+int(Quantity)
            
            insertTableValue(tablename='DocItem' , columnsName="(DocHeaderId,GoodsId,GoodsUnitId,Quantity,InventoryFrom,InventoryTO)",
                        values=f"( {int(DocHeaderId)}  , {GoodsId} , {GoodsUnit} , {Quantity} , {invfrom} ,{invTo} )")
    


            



                



           

    

def createDocquery(stockFrom,Stockto,transfereeUSER,senderUSER,goodsInfo):

    if not stockFrom:
        inventory=returnGoodsStock(Stockto)
        print("inventory,=======================================================",inventory)
        DocHeadertypeId=int(2)
        id=insertTableValue(tablename='DocHeader',
                        columnsName="(DocTypeId,DocCode,StockTo,TransfereeUSER)",
                        values=f"({DocHeadertypeId},65,{Stockto},{transfereeUSER})")
        
        _checkInv(DocHeadertypeId,id,goodsInfo,inventory,None)


    elif not Stockto:
        inventory=returnGoodsStock(stockFrom)
        DocHeadertypeId=int(1)
        
        id=insertTableValue(tablename='DocHeader',
                        columnsName="(DocTypeId,DocCode,stockFrom,senderUSER)",
                        values=f"({DocHeadertypeId},65,{stockFrom},{senderUSER})")
        
        _checkInv(DocHeadertypeId,id,goodsInfo,inventory,None)

    else:
        inventoryFrom=returnGoodsStock(stockFrom)
        inventoryTo=returnGoodsStock(Stockto)
        DocHeadertypeId=int(3)
        id=insertTableValue(tablename='DocHeader',
                        columnsName="(DocTypeId,DocCode,stockFrom,StockTo,senderUSER)",
                        values=f"({DocHeadertypeId},65,{stockFrom},{Stockto},{senderUSER})")
        print(inventoryTo,"===============inventory too==================")
        
      
        
        _checkInv(DocHeadertypeId,id,goodsInfo,inventoryFrom,inventoryTo)
    
    
