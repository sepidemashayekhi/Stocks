
from database import Conection


conection=Conection()
cursor=conection.cursor

##  Create Table in Data Base

FactoryTable="""
CREATE TABLE Factory(
    FactoryId BIGINT NOT NULL IDENTITY PRIMARY KEY ,
    FactoryName NVARCHAR(200) NULL UNIQUE,
    FactoryAddress NVARCHAR(250) NULL ,
    PhoneNumber VARCHAR(17) NULL,
    );
"""



StockTable="""
CREATE TABLE Stock(
    StockId BIGINT NOT NULL IDENTITY PRIMARY KEY,
    FactoryId BIGINT FOREIGN KEY REFERENCES Factory(FactoryId),
    Title NVARCHAR(100) NULL,
    StockCode NVARCHAR(100) NOT NULL UNIQUE,
    IsActive BIT DEFAULT 1,
    StockAddress NVARCHAR(250) NULL ,
    PhoneNumber VARCHAR(20) NULL ,
    StockDescription NVARCHAR(350) NULL,
    CreatUser NVARCHAR(150) NULL,
    CreateDate DATETIME DEFAULT GETDATE(),
    ModifierDate DATETIME NULL,
    ModifierUser NVARCHAR(150) NULL
    );
"""


StockPeriodtable="""
CREATE TABLE StockPeriod(
	StockPeriodId BIGINT PRIMARY KEY IDENTITY NOT NULL,
	StockId BIGINT FOREIGN KEY REFERENCES Stock(StockId) UNIQUE ,
	Title NVARCHAR(150) NULL,
	FromDate DATETIME NOT NULL,
	ToDate DATETIME NOT NULL,
	CreatorUser NVARCHAR(150) NOT NULL,
	CreateDate DATETIME DEFAULT GETDATE(),
	ModifierUser NVARCHAR(150) NULL,
	ModifierDate DATETIME DEFAULT NULL,
	IsActive BIT DEFAULT 0
);
"""



cherckTable="""
CREATE TABLE StockClerck(
    StockClerckId BIGINT NOT NULL IDENTITY PRIMARY KEY,
    StockId BIGINT FOREIGN KEY REFERENCES  Stock(StockId),
    FullName NVARCHAR(150) NOT NULL,
    PersonalCode VARCHAR(20) UNIQUE NOT NULL,
    NationalCode VARCHAR(20) UNIQUE NOT NULL,
    HomeAddress NVARCHAR(250) NULL,
    PhoneNumber VARCHAR(20) NULL
    );
"""



unitType="""
CREATE TABLE UnitType(
    UnitTypeId BIGINT PRIMARY KEY IDENTITY NOT NULL,
    Title NVARCHAR(50) NOT NULL UNIQUE,
    IsActive BIT DEFAULT 1
    );
"""



goodsGroupTable="""
CREATE TABLE GoodsGroup(
    GoodsGroupId BIGINT NOT NULL PRIMARY KEY IDENTITY ,
    Title NVARCHAR(150) NOT NULL UNIQUE,
    IsActive BIT DEFAULT 1,
    ParentId BIGINT FOREIGN KEY REFERENCES GoodsGroup(GoodsGroupId) NUll
    );
"""


goodsTable="""
CREATE TABLE Goods(
    GoodsId BIGINT PRIMARY KEY NOT NULL IDENTITY,
    Title NVARCHAR(150) NOT NULL UNIQUE,
    GoodsGroupId BIGINT FOREIGN KEY REFERENCES GoodsGroup(GoodsGroupId),
    IsActive BIT DEFAULT 1
    );
"""


goodsUnitTable="""
CREATE TABLE GoodsUnit(
    GoodsUnitId BIGINT PRIMARY KEY NOT NULL IDENTITY,
    GoodsId BIGINT FOREIGN KEY REFERENCES Goods(GoodsId),
    UnitTypeId BIGINT FOREIGN KEY REFERENCES UnitType(UnitTypeId),
    Coefficient float,
    IsPrimary BIT DEFAULT 0,
    IsDefault BIT DEFAULT 0,
    IsActive BIT DEFAULT 1
    );
"""



docTypeTable="""
CREATE TABLE Doctype(
    DocTypeId BIGINT NOT NULL PRIMARY KEY IDENTITY,
    Title NVARCHAR(50) NOT NULL UNIQUE,
    IsActive BIT DEFAULT 1
    );
"""

docHeaderTable="""
CREATE TABLE DocHeader(
    DocHeaderId BIGINT NOT NULL IDENTITY PRIMARY KEY,
    DocTypeId  BIGINT FOREIGN KEY REFERENCES DocType(DocTypeId),
    DocCode NVARCHAR(150)  NOT NULL,
    DocDate DATETIME DEFAULT GETDATE(),
    StockTO BIGINT FOREIGN KEY REFERENCES Stock(StockId)  NULL,
    StockFrom BIGINT FOREIGN KEY REFERENCES Stock(StockId) NULL,
    TransfereeUSER BIGINT FOREIGN KEY REFERENCES StockClerck(StockClerckId) Null,
    SenderUSER BIGINT FOREIGN KEY REFERENCES StockClerck(StockClerckId) Null,
    CreatorUser NVARCHAR(150) NULL,
    CreateDate DATETIME DEFAULT GETDATE(),
    ModifierUser NVARCHAR(150) NULL,
    Modifierdate DATETIME NULL,
    );
"""


docItemTable="""
CREATE TABLE DocItem(
    DocItemId BIGINT NOT NULL PRIMARY KEY IDENTITY ,
    DocHeaderId BIGINT FOREIGN KEY REFERENCES DocHeader(DocHeaderId),
    GoodsId BIGINT FOREIGN KEY REFERENCES Goods(GoodsId),
    GoodsUnitId BIGINT FOREIGN KEY REFERENCES GoodsUnit(GoodsUnitId),
    Quantity VARCHAR(100) NOT NULL,
    Inventory VARCHAR(50)  ,
    CreatorUser NVARCHAR(150) NULL,
    CreateDate DATETIME DEFAULT GETDATE(),
    ModifierUser NVARCHAR(150) NULL,
    Modifierdate DATETIME NULL,
    );
"""

goodsGroupStock="""
CREATE TABLE GoodsGroupStock(
    GoodsGroupStockId BIGINT NOT NULL IDENTITY PRIMARY KEY,
    StockId BIGINT FOREIGN KEY REFERENCES Stock(StockId),
    GoodSGroupId BIGINT FOREIGN KEY REFERENCES GoodSGroup(GoodSGroupId),
    IsActive BIT DEFAULT 1,
    Discription NVARCHAR(300) NULL,
    CreateDate DATETIME DEFAULT GETDATE(),
    CreateUser NVARCHAR(150) NULL,
    ModifireDate DATETIME NULL,
    ModifierUser NVARCHAR(150) NULL
    );
"""

querySintacs =FactoryTable+StockTable+StockPeriodtable+cherckTable+unitType+goodsGroupTable+\
                goodsTable+goodsUnitTable+docTypeTable+docHeaderTable+docItemTable+goodsGroupStock



cursor.execute(querySintacs)
cursor.commit()
conection.closedConection