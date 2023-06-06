import pandas as pd
from database import Conection
import time
import jdatetime 
from persiantools.jdatetime import JalaliDate
import datetime
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


def returenAll(tableName,pk):
    if pk:
        queyStr=f"""
        SELECT * FROM {tableName} WHERE {tableName}Id={pk}
        """
    else:
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
    result=[]
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
        re=[]
        goodID=data.iloc[i,0]
        goodsditale=returnWithCondition(tableName='Goods',title=goodID , condition='GoodsId')
        goodsditale=goodsditale.iloc[0].to_dict()
        goodInv=data.iloc[i,1]

        goodsditale['goodInv']=int(goodInv)
        re.append(goodsditale)
        result.append(re[0])
        
    
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
        

def docHeaders(stockId):

    queryStr=f"""
    SELECT DocHeaderId,Docdate,DocType.DocTypeId,DocType.Title FROM DocHeader JOIN  DocType ON DocHeader.DocTypeId=DocType.DocTypeId
    WHERE DocHeader.StockFrom={stockId} OR DocHeader.StockTO={stockId} ;
    """
    returnData=[]
    try:
    # if True:
        data=pd.read_sql_query(queryStr,conect.cnxn)
    except:
        return []
    
    for i in range(len(data.index)):
        re=data.iloc[i].to_dict()
        date=re['Docdate']
        j_date=jdatetime.datetime.fromgregorian( year=date.year , month=date.month , day=date.day , hour=date.hour , minute=date.minute)
        j_date=str(j_date).replace('-','/')
        re['Docdate']=j_date
        returnData.append(re)
    
    return returnData


def docHeadersDetali(docHeaderId):

    queryStr=f"""
    SELECT Doctype.Title,Stock.Title AS StockName,DocDate ,StockFrom,StockTo,SenderUSER,TransfereeUSER FROM DocHeader
    INNER JOIN Stock ON DocHeader.StockFrom=Stock.StockId OR DocHeader.StockTo=Stock.StockId
    INNER JOIN Doctype ON DocHeader.DocTypeId=DocType.DocTypeId
    WHERE DocHeaderId={docHeaderId} ; 
    """
    try:
        data=pd.read_sql_query(queryStr,conect.cnxn)
    except:
        return []
    

    returnDate={}

    for i in range(len(data)):
        result=data.iloc[i].to_dict()
        if i==1:
            if result['SenderUSER']:
                returnDate['SenderUSER']=returenAll(tableName='StockClerck',pk=result['SenderUSER']).iloc[0].to_dict()
            else:
                returnDate['SenderUSER']=None
            
            returnDate[f'stockFrom']=result['StockName']
            returnDate[f'stockFromId']=result['StockFrom']
        if result['TransfereeUSER']:
            returnDate['TransfereeUSER']=returenAll(tableName='StockClerck',pk=result['TransfereeUSER']).iloc[0].to_dict()
        else:
            returnDate['TransfereeUSER']=None
        returnDate[f'StockTo']=result['StockName']
        returnDate[f'StockToId']=result['StockTo']
    returnDate['headerTtype']=result['Title']


    queryStr=f"""
    SELECT 
    Goods.Title AS GoodsName,
    Goods.GoodsId AS GoodsID,
    InventoryFrom,InventoryTO,UnitType.Title,Quantity
    FROM DocItem
    INNER JOIN Goods ON Goods.GoodsId=DocItem.GoodsId
    INNER JOIN DocHeader ON DocHeader.DocHeaderId=DocItem.DocHeaderId
    INNER JOIN GoodsUnit ON GoodsUnit.GoodsUnitId=DocItem.GoodsUnitId
    INNER JOIN UnitType ON GoodsUnit.UnitTypeId=UnitType.UnitTypeId
    WHERE DocItem.DocHeaderId={docHeaderId};
    """
    try:
        data=pd.read_sql_query(queryStr,conect.cnxn)
    except:
        return []
    returnDate['Goods']=[]
    
    for i in range(len(data.index)):
        re={}
        result=data.iloc[i].to_dict()
        for item in result:
            re[item]=result.get(item)            
        returnDate['Goods'].append(re)
    

    return  returnDate


def docHeaderFilter(DateFrom:str,DateTo:str):

    DateFrom = jdatetime.datetime.strptime(DateFrom,'%Y/%m/%d')
    DateFrom=jdatetime.datetime.togregorian(DateFrom)

    DateTo = jdatetime.datetime.strptime(DateTo,'%Y/%m/%d')
    DateTo=jdatetime.datetime.togregorian(DateTo)
    

    queryStr=f"""
    SELECT * FROM DocHeader
    WHERE DocDate BETWEEN '{DateFrom}' AND '{DateTo}';
    """
    
    try:
        conect.cursor.execute(queryStr)
    except:
        return []
    
    columns=[column[0] for column in conect.cursor.description]
    rows=[dict(zip(columns,row)) for row in conect.cursor.fetchall()]
    
    for i  in range(len(rows)):
        date=rows[i].get('DocDate')
        j_date=jdatetime.datetime.fromgregorian( year=date.year , month=date.month , day=date.day , hour=date.hour , minute=date.minute)
        j_date=str(j_date).replace('-','/')
        rows[i]['DocDate']=j_date

    return rows

