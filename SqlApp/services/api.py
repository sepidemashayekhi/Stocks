from fastapi import FastAPI
import pandas as pd

from  services.Items import GoudsGroupItem
from  database import Conection


conection=Conection()

# class Item
app = FastAPI()

@app.post('/goodsGroup/')
def goodsGroup(item:GoudsGroupItem):
    
    queryStr=f"""
    INSERT INTO GoodsGroup(Title)
    VALUES('{item.title}');    
    """
    
    conection.cursor.execute(queryStr)
    data=pd.read_sql(F"SELECT top 1 * FROM GoodsGroup ORDER BY -GoodsGroupId ",conection.cnxn)
    

    returnData={
        "GoodsGroupId":str(data.iloc[0,0]),
        "title":item.title
    }
    
    return returnData
    

