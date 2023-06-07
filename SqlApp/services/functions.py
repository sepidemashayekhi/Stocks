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
    results=[]
    # data_=[data.iloc[i].to_dict for i in range(len(data.index))]
    for i in range(len(data.index)):
        result=data.iloc[i].to_dict()
        results.append(result)
    
    return results


def returnWithCondition(tableName :str ,title , condition :str):

    queryStr=f"""
    SELECT * FROM {tableName} WHERE {condition}={title}
    """
    data = pd.read_sql_query(queryStr , conect.cnxn)
    return data


def returnGoodsStock(stockId,goodsId=None):

    queryStr=f"""
    EXEC StockGoodsInventory
    @StockId={stockId}
    """
    data=pd.read_sql(queryStr,conect.cnxn)
    data=[data.iloc[i].to_dict() for i in range(len(data.index))]
    return data


def _checkGroup(stockId):
    queryStr="""
    SElECT DISTINCT GoodsId FROM Goods
    INNER JOIN GoodsGroupStock ON GoodsGroupStock.GoodSGroupId=Goods.GoodsGroupId 
    AND GoodsGroupStock.StockId=1
    ;
    """
    data=pd.read_sql(queryStr,conect.cnxn)
    if not len(data.index):
        return []
    result=[list(data.iloc[i].to_dict().values())[0] for i in range(len(data.index))]
    return result


def _checkInv(DocTypeId,DocHeaderId,goodsInfo,inventory,inventory2):

    
    if inventory:
        inventoryDict={}
        for item in inventory:
            inventoryDict[item['GoodsId']]=item['Inventory']
    # print(inventory2,"==================tttttttttttttttttttttttt=================t")
    if inventory2:
        inventoryDict2={}
        for item in inventory2:
            inventoryDict2[item['GoodsId']]=item['Inventory']


    for goods in goodsInfo:
        
        GoodsId=goods.get("GoodsId")
        Quantity=goods.get('Quantity')
        GoodsUnit=goods.get('GoodsUnitId')
       
        

        if DocTypeId==1 and (GoodsId in inventoryDict2)  :
            
            goodsInv=inventoryDict2[GoodsId]
            print(goodsInv)
            inv=int(Quantity)+int(goodsInv)
            insertTableValue(tablename='DocItem' , columnsName="(DocHeaderId,GoodsId,GoodsUnitId,Quantity,Inventory)",
                            values=f"( {int(DocHeaderId)}  , {GoodsId} , {GoodsUnit} , {Quantity} , {inv} )")
        
        
        if DocTypeId==2 and  GoodsId in inventoryDict :
            goodsInv=inventoryDict[GoodsId]
            inv=int(goodsInv)-int(Quantity)
            if inv<0:
                continue
            insertTableValue(tablename='DocItem' , columnsName="(DocHeaderId,GoodsId,GoodsUnitId,Quantity,Inventory)",
                            values=f"( {int(DocHeaderId)}  , {GoodsId} , {GoodsUnit} , {Quantity} , {inv} )")
        

        
        

def createDocquery(stockFrom,Stockto,transfereeUSER,senderUSER,goodsInfo):

    if not stockFrom:
        inventory=returnGoodsStock(Stockto)
        print("inventory,=======================================================",inventory)
        DocHeadertypeId=int(1)
        id=insertTableValue(tablename='DocHeader',
                        columnsName="(DocTypeId,DocCode,StockTo,TransfereeUSER)",
                        values=f"({DocHeadertypeId},65,{Stockto},{transfereeUSER})")
        
        _checkInv(DocHeadertypeId,id,goodsInfo,None,inventory)

        return [id,None]


    elif not Stockto:
        inventory=returnGoodsStock(stockFrom)
        DocHeadertypeId=int(2)
        
        id=insertTableValue(tablename='DocHeader',
                        columnsName="(DocTypeId,DocCode,stockFrom,senderUSER)",
                        values=f"({DocHeadertypeId},65,{stockFrom},{senderUSER})")
        
        _checkInv(DocHeadertypeId,id,goodsInfo,inventory,None)

        return [None,id]

    else:
        inventoryFrom=returnGoodsStock(stockFrom)
        inventoryTo=returnGoodsStock(Stockto)

        
        id1=insertTableValue(tablename='DocHeader',
                        columnsName="(DocTypeId,DocCode,StockTo,TransfereeUSER)",
                        values=f"({1},65,{Stockto},{transfereeUSER})")
        
        _checkInv(1,id1,goodsInfo,None,inventoryTo)
        
        id2=insertTableValue(tablename='DocHeader',
                        columnsName="(DocTypeId,DocCode,stockFrom,senderUSER)",
                        values=f"({2},65,{stockFrom},{senderUSER})")
        
        _checkInv(2,id2,goodsInfo,inventoryFrom,None)
        return  [id1,id2]
    
        

def docHeaders(stockId):

    queryStr=f"""
    SELECT DocHeaderId,Docdate,DocType.DocTypeId,DocType.Title FROM DocHeader JOIN  DocType ON DocHeader.DocTypeId=DocType.DocTypeId
    WHERE DocHeader.StockFrom={stockId} OR DocHeader.StockTO={stockId} ;
    """
    returnData=[]
    # try:
    if True:
        data=pd.read_sql_query(queryStr,conect.cnxn)
    # except:
    #     return []
    
    
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
    select DISTINCT 
    Goods.Title as  GoodsName,
    Goods.GoodsId,DocHeader.DocTypeId,Doctype.Title,Quantity,UnitType.UnitTypeId,DocHeader.SenderUSER,
    TransfereeUSER,StockFrom,StockTo,UnitType.Title as GoodsUnitTitle
    from DocHeader
    inner join DocItem on DocItem.DocHeaderId=DocHeader.DocHeaderId
    inner join Doctype on Doctype.DocTypeId=DocHeader.DocTypeId
    inner join GoodsUnit on GoodsUnit.GoodsId=DocItem.GoodsId
    inner join UnitType on UnitType.UnitTypeId=GoodsUnit.UnitTypeId
    inner join Goods on Goods.GoodsId=DocItem.GoodsId
    where DocHeader.DocHeaderId={docHeaderId}; 
    """
    returnDate={'goods':[]}
    
    data=pd.read_sql_query(queryStr,conect.cnxn)
    
    # if len(data.index):
    print(data,"00000000000000000000000000000000")
    for i in range((len(data.index))):
        result=data.iloc[i].to_dict()
        re={}
        re["goodName"]=result['GoodsName']
        re['goodsId']=result['GoodsId']
        re['Quantity']=result['Quantity']
        re['GoodUnitName']=result['GoodsUnitTitle']
        re['GoodUnitId']=result['UnitTypeId']
        returnDate['goods'].append(re)
        
    
    
    
    returnDate['doctype']=result['Title']
    returnDate['doctypeId']=result['DocTypeId']
    a={'TransfereeUSER':'StockClerck','SenderUSER':'StockClerck','StockFrom':'Stock','StockTo':'Stock'}
    for item in a:
        print(result[item],item,"=================")
        if  result[item]:
            returnDate[item]=returenAll(tableName=a[item],pk=result[item])[0]
        else:
            returnDate[item]=None
    
    returnDate['docHeaderId']=docHeaderId

    
    
    return returnDate


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



def clerckDetail(clerckId:int):

    querySrt=f"""
    SELECT StockClerckId,StockClerck.StockId,FullName,PersonalCode,
    Stock.Title AS StockName,Stock.StockId
    FROM StockClerck
    INNER JOIN Stock ON Stock.StockId=StockClerck.StockId
    WHERE StockClerckId={clerckId};
    """

    data=pd.read_sql(querySrt,conect.cnxn)
    if not len(data.index):
        return False
    
    result=[data.iloc[i].to_dict() for i in range(len(data.index))][0]

    return result


# EXEC StockGoodsInventoty
# @StockId=1