
from pydantic import BaseModel 

class GoudsGroupItem(BaseModel):
    title : str

class Goods(BaseModel):
    
    title : str
    GoodsGroupId : int

class UnitTyp(BaseModel):
    title : str
    coefficient : int
    isPramary : bool
    isDefault : bool
    
class GoodsUnitType(BaseModel):
    goodsId : int
    unitTypeId : int

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
    
class DocHeader(BaseModel):

    docHeaderTypeId: int
    stockFrom : int
    stockTo : int

    transfereeUser : int
    senderUser : int


class CreateDoc(BaseModel):

    StockFrom : int | None=None
    StockTo : int 
    TransfereeUser : int
    SenderUse : int | None=None
    GoodsInfo : list



