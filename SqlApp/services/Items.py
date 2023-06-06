
from pydantic import BaseModel 

class GoudsGroupItem(BaseModel):
    title : str

class Goods(BaseModel):
    
    title : str
    GoodsGroupId : int

class UnitTyp(BaseModel):
    title : str
    
class GoodsUnitType(BaseModel):
    goodsId : int
    unitTypeId : int
    Coefficient :float
    isPrimaty : bool

    isDefault:bool

class Factory(BaseModel):
    name:str
    address : str
    phoneNUmber : str

class Stock(BaseModel):
    title:str
    factoryId:int
    address: str
    phoneNumber :str
    description :str
    goodsGroup : list
    
class stockPeriodItem(BaseModel):
    title : str
    stockId: int
    fromDate: str
    toDate :str

class StockClerck(BaseModel):
    stockId:int
    fullName : str
    nationalCode : str
    address : str
    phoneNumber : str

class docType(BaseModel):
    title:str

class Docheadertype(BaseModel):
    doctypeId:int
    title : str

class GoodsGroupStock(BaseModel):
    stockId : int
    goosGroupId : int
    discription : str
    


class CreateDoc(BaseModel):

    StockFrom : int | None=None
    StockTo : int  | None=None
    TransfereeUser : int | None=None
    SenderUser : int | None=None
    GoodsInfo : list



