
from database import Conection


conection=Conection()
cursor=conection.cursor

##  Create Table in Data Base
FactoryTable="""
CREATE TABLE Factory(
    FactoryId BIGINT NOT NULL IDENTITY PRIMARY KEY ,
    FactoryName NVARCHAR(200) NULL ,
    FactoryAddress NVARCHAR(250) NULL ,
    PhoneNumber VARCHAR(11) NULL,
    );
"""



StockTable="""
CREATE TABLE Stock(
    StockId BIGINT NOT NULL IDENTITY PRIMARY KEY,
    FactoryId BIGINT FOREIGN KEY REFERENCES Factory(FactoryId),
    Title NVARCHAR(100) NULL,
    IsActive BIT DEFAULT 0,
    StockAddress NVARCHAR(250) NULL ,
    PhoneNumber VARCHAR(11) NULL ,
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
	StockId BIGINT FOREIGN KEY REFERENCES Stock(StockId),
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
    PersonalCode VARCHAR(10) UNIQUE NOT NULL,
    NationalCode VARCHAR(10) UNIQUE NOT NULL,
    HomeAddress NVARCHAR(250) NULL,
    PhoneNumber VARCHAR(11) NULL
    );
"""



unitType="""
CREATE TABLE UnitType(
    UnitTypeId BIGINT PRIMARY KEY IDENTITY NOT NULL,
    Tiltle NVARCHAR(50) NOT NULL,
    IsActive BIT DEFAULT 1,
    Coefficient INT NOT NULL,
    IsPrimary BIT DEFAULT 0,
    IsDefault BIT DEFAULT 0
    );
"""



goodsGroupTable="""
CREATE TABLE GoodsGroup(
    GoodsGroupId BIGINT NOT NULL PRIMARY KEY IDENTITY ,
    Title NVARCHAR(50) NOT NULL,
    IsActive BIT DEFAULT 1,
    ParentId BIGINT FOREIGN KEY REFERENCES GoodsGroup(GoodsGroupId)
    );
"""


goodsTable="""
CREATE TABLE Goods(
    GoodsId BIGINT PRIMARY KEY NOT NULL IDENTITY,
    Title NVARCHAR(150) NOT NULL ,
    GoodsGroupId BIGINT FOREIGN KEY REFERENCES GoodsGroup(GoodsGroupId),
    IsActive BIT DEFAULT 1
    );
"""


goodsUnitTable="""
CREATE TABLE GoodsUnit(
    GoodsId BIGINT FOREIGN KEY REFERENCES Goods(GoodsId),
    UnitTypeId BIGINT FOREIGN KEY REFERENCES UnitType(UnitTypeId),
    IsActive BIT DEFAULT 1
    );
"""



docTypeTable="""
CREATE TABLE Doctype(
    DocTypeId BIGINT NOT NULL PRIMARY KEY IDENTITY,
    Title NVARCHAR(50) NOT NULL,
    IsActive BIT DEFAULT 1
    );
"""



docHeaderTypeTable="""
CREATE TABLE DocHeaderType(
    DocHeaderTypeId BIGINT NOT NULL IDENTITY PRIMARY KEY,
    DocTypeId BIGINT FOREIGN KEY REFERENCES DocType(DocTypeId),
    Title NVARCHAR(50) NOT NULL,
    IsActive BIT DEFAULT 1,
    );
"""



docHeaderTable="""
CREATE TABLE DocHeader(
    DocHeaderId BIGINT NOT NULL IDENTITY PRIMARY KEY,
    DocHeadertypeId BIGINT FOREIGN KEY REFERENCES DocHeaderType(DocHeaderTypeId),
    DocCode NVARCHAR(10) UNIQUE NOT NULL,
    DocDate DATETIME DEFAULT GETDATE(),
    StockPeriodId BIGINT FOREIGN KEY REFERENCES StockPeriod(StockPeriodId),
    StockFrom BIGINT FOREIGN KEY REFERENCES Stock(StockId),
    StockTo BIGINT FOREIGN KEY REFERENCES Stock(StockId),
    TransfereeUSER BIGINT FOREIGN KEY REFERENCES StockClerck(StockClerckId),
    SenderUSER BIGINT FOREIGN KEY REFERENCES StockClerck(StockClerckId),
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
    Quantity VARCHAR(50) NOT NULL,
    Inventory VARCHAR(50) NOT NULL,
    CreatorUser NVARCHAR(150) NULL,
    CreateDate DATETIME DEFAULT GETDATE(),
    ModifierUser NVARCHAR(150) NULL,
    Modifierdate DATETIME NULL,
    );
"""



querySintacs =FactoryTable+StockTable+StockPeriodtable+cherckTable+unitType\
    +goodsGroupTable+goodsTable+goodsUnitTable+docTypeTable+docHeaderTypeTable\
    +docHeaderTable+docItemTable

cursor.execute(querySintacs)
cursor.commit()
conection.closedConection
