import pandas as pd
from database import Conection


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
    INSERT INTO {tablename} {columnsName} VALUES {values};
    """
    print(queryStr)
    # try:
    if True:
        conect.cursor.execute(queryStr)
        conect.cursor.commit()
    # except:
    #     return False

    
    return True


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

   
def returnGoodsStock(stockId):
    result={"goodsInventory":[]}
    querStr=f"""
    SELECT TOP 1 * FROM  DocHeader 
    WHERE StockFrom={stockId}
    ORDER BY CreateDate DESC ;
    """ 
    try:
        finalDocHeaderId=pd.read_sql_query(querStr,conect.cnxn).iloc[0,0]
    except:
        return False
    
    querStr=f"""
    SELECT GoodsId,Inventory FROM DocItem 
    WHERE DocHeaderId={finalDocHeaderId};
    """
    try:
        data=pd.read_sql_query(querStr,conect.cnxn)
    except:
        return False
    for i in range(len(data.index)):
        nameGoods=returnWithCondition(tableName='Goods' , title=int(data.iloc[i,0]) , condition='GoodsId')
        nameGoods=nameGoods.Title.values[0]
        re=data.iloc[i].to_dict()
        re['nameGoods']=nameGoods
        result['goodsInventory'].append(re)
    
    return result





def createDocquery(stockFrom,Stockto,transfereeUSER,senderUSER,goodsInfo):

    if not stockFrom:
        inventoryGoods=returnGoodsStock(Stockto)
    else:
        inventoryGoods=returnGoodsStock(stockFrom)
        

    docCode=getMax(tableName='DocHeader',columnsName='DocHeaderId')
    docCode=str(docCode)
    queryStr=f"""
    INSERT INTO DocHeader(DocHeadertypeId,DocCode,StockPeriodId,StockFrom,StockTo,TransfereeUSER,SenderUSER) OUTPUT INSERTED.DocHeaderId
    VALUES (4,{docCode},3,{stockFrom},{Stockto},{transfereeUSER},{senderUSER});
    """

    data=conect.cursor.execute(queryStr)
    id = conect.cursor.fetchone()[0]

    for goods in goodsInfo:
        print(goods,"====================================================" ,inventoryGoods)
        GoodsId=goods.get("GoodsId")
        Quantity=goods.get('Quantity')
        unitType=goods.get('unitTypeId')


    

