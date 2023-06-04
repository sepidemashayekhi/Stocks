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
    print(queryStr,"===========")
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
    (StockTO = 1 OR StockFrom = 1)
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
    
    # try:
    if True:
        data=pd.read_sql_query(querStr,conect.cnxn)
        print(len(data.index),"index of len data")
    
    for i in range(len(data.index)):
        re={}
        goodID=data.iloc[i,0]
        goodInv=data.iloc[i,1]
        re['GoodsiId']=int(goodID)
        re['goodInv']=int(goodInv)
        result["goodsInventory"].append(re)
        
    print(result)
    return result


def inventoryGoods(inventory:list,goods):
    for inv in inventory:
        
        invGoodId=inv.get('GoodsId')
        goodsId=goods.get('GoodsId')

        print(str(invGoodId),str(goodsId),'iorerbvehbv===========ejhcbjhbc=jehvbbbbbbbbbb=jvbjhbhjbjh')

        if str(invGoodId)==str(goodsId):
            return inv.get("Inventory")


    

def createDocquery(stockFrom,Stockto,transfereeUSER,senderUSER,StockPeriodId,goodsInfo):

    if not stockFrom:
        stockFrom=Stockto
    
    inventory=returnGoodsStock(stockFrom)

    code=str(time.time()).split('.')[0]
    
    

    
    for goods in goodsInfo:

        GoodsId=goods.get("GoodsId")
        Quantity=goods.get('Quantity')
        GoodsUnit=goods.get('GoodsUnitId')

        print(inventory,"==============inventory+==================")
    
        if  isinstance(inventory,bool):
            
            insertTableValue(tablename='DocItem' , columnsName="(DocHeaderId,GoodsId,GoodsUnitId,Quantity,InventoryTO)",
                                values=f"( {int(id)}  , {GoodsId} , {GoodsUnit} , {Quantity} , {Quantity} )")
        
        elif isinstance(inventory,dict):

            inventory=inventory.get('goodsInventory')

            goodsinv=int(inventoryGoods(inventory,goods))
            newinv=int(Quantity)-int(goodsinv)
            insertTableValue(tablename='DocItem' , columnsName="(DocHeaderId,GoodsId,GoodsUnitId,Quantity,InventoryFrom,InventoryTO)",
                                values=f"( {int(id)}  , {GoodsId} , {GoodsUnit} , {Quantity} , {newinv} ,{newinv})")

        

        
            
        
    

        

