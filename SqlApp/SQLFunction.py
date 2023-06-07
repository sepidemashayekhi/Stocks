
from database import Conection
conect=Conection()


queryStrGetInventory="""
--CREATE FUNCTION [dbo].[GetInventory]

CREATE FUNCTION [dbo].[GetInventory]
(
    @GoodsID BIGINT,
    @StockID BIGINT

)


RETURNS @Mytable TABLE 
(
    ResidI DECIMAL, 
    HavalehI DECIMAL,
	Inventory DECIMAL
)
AS 
BEGIN
   

	Insert into @Mytable
 SELECT ResidI,--مجموع قبوض
        HavaleI,--مجموع حواله ها
        (ResidI.ResidI - HavaleI.HavaleI) Inventory  -- موجودی قطعی
			    FROM
	    (
           SELECT  ISNULL(SUM(ISNULL(CAST(Quantity AS DECIMAL),0)),0)  ResidI  
           FROM  dbo.DocHeader WITH (NOLOCK)
               INNER JOIN dbo.DocItem  WITH (NOLOCK)
                   ON DocItem.DocHeaderId=DocHeader.DocHeaderId
				   INNER JOIN dbo.Stock WITH (NOLOCK) ON Stock.StockId=DocHeader.StockTo 
			
           WHERE 
				 Stock.StockId=@StockID
                 AND (DocTypeId = 1) -- رسید
                 AND (DocItem.GoodsId = @GoodsID)
			
       ) ResidI 
	       OUTER APPLY
       (
          SELECT ISNULL(SUM(ISNULL(CAST(Quantity AS decimal),0)),0)  HavaleI  
           FROM  dbo.DocHeader WITH (NOLOCK)
               INNER JOIN dbo.DocItem  WITH (NOLOCK)
                   ON DocItem.DocHeaderId=DocHeader.DocHeaderId
				   INNER JOIN dbo.Stock WITH (NOLOCK) ON Stock.StockId=DocHeader.StockFrom
				  
           WHERE 
				 Stock.StockId=@StockID
                 AND (DocTypeId = 2) -- حواله
                 AND (DocItem.GoodsId = @GoodsID)
         ) HavaleI;


  RETURN;
END
  
"""

quryStrStockGoodsInventory="""

CREATE PROCEDURE StockGoodsInventory
(
    @stockId bigint 
)
AS
BEGIN

	SELECT DISTINCT Goods.Title,
	Goods.GoodsId ,
	GoodsGroup.Title AS GroupName,
	Stock.StockId,
	GetInventory.Inventory
	FROM Goods
	LEFT JOIN  GoodsUnit ON Goods.GoodsId=GoodsUnit.GoodsId AND IsDefault=1
	LEFT JOIN  UnitType ON UnitType.UnitTypeId=GoodsUnit.UnitTypeId
	INNER JOIN  GoodsGroup ON GoodsGroup.GoodsGroupId=Goods.GoodsGroupId
	INNER JOIN  GoodsGroupStock ON GoodsGroupStock.GoodSGroupId=GoodsGroup.GoodsGroupId
	INNER JOIN  Stock ON Stock.StockId=GoodsGroupStock.StockId
	OUTER APPLY GetInventory(Goods.GoodsId,Stock.StockId)
	WHERE Stock.StockId=@stockId

END

"""

conect.cursor.execute(queryStrGetInventory)
conect.cursor.commit()


conect.cursor.execute(quryStrStockGoodsInventory)
conect.cursor.commit()


conect.closedConection
