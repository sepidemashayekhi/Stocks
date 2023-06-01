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
    return max_


