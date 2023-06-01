
from pydantic import BaseModel

class GoudsGroupItem(BaseModel):
    title : str

class Goods(BaseModel):
    title : str
    GoodsGroupName : str

class UnitTyp(BaseModel):
    title : str
    coefficient : int
    isPramary : bool
    isDefault : bool
    
class GoodsUnitType(BaseModel):
    goodsName:str
    unitTypeName:str

class Factory(BaseModel):
    name:str
    address : str
    phoneNUmber : str

class Stock(BaseModel):
    title:str
    factoryName:str
    address: str
    phoneNumber :str
    description :str

class stockPeriodItem(BaseModel):
    title : str
    stockName: str
    fromDate: str
    toDate :str

class StockClerck(BaseModel):
    stockName:str
    fullName : str
    nationalCode : str
    address : str
    phoneNumber : str

class docType(BaseModel):
    title:str

class Docheadertype(BaseModel):
    doctypeName:str
    title : str

class GoodsGroupStock(BaseModel):
    stockName : str
    goosGroupName : str
    discription : str
    


