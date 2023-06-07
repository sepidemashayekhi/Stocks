from database import Conection


conect=Conection()

dataQuery="""
INSERT INTO GoodsGroup (Title) OUTPUT INSERTED.GoodsGroupId VALUES (N'تاسیسات') ;
INSERT INTO GoodsGroup (Title) OUTPUT INSERTED.GoodsGroupId VALUES (N'تجهیزات') ;
INSERT INTO GoodsGroup (Title) OUTPUT INSERTED.GoodsGroupId VALUES (N'خوراکی') ;
INSERT INTO GoodsGroup (Title) OUTPUT INSERTED.GoodsGroupId VALUES (N'خشک بار') ;
INSERT INTO GoodsGroup (Title) OUTPUT INSERTED.GoodsGroupId VALUES (N'الکترونیکی') ;

INSERT INTO Goods (Title,GoodsGroupId) OUTPUT INSERTED.GoodsId VALUES (N'میز', 2) ;
INSERT INTO Goods (Title,GoodsGroupId) OUTPUT INSERTED.GoodsId VALUES (N'صندلی', 2) ;
INSERT INTO Goods (Title,GoodsGroupId) OUTPUT INSERTED.GoodsId VALUES (N'کمد', 2) ;

INSERT INTO Goods (Title,GoodsGroupId) OUTPUT INSERTED.GoodsId VALUES (N'آچار', 1) ;
INSERT INTO Goods (Title,GoodsGroupId) OUTPUT INSERTED.GoodsId VALUES (N'سنگ بر', 1) ;

INSERT INTO Goods (Title,GoodsGroupId) OUTPUT INSERTED.GoodsId VALUES (N'مرغ', 3) ;
INSERT INTO Goods (Title,GoodsGroupId) OUTPUT INSERTED.GoodsId VALUES (N'گوشت', 3) ;

INSERT INTO Goods (Title,GoodsGroupId) OUTPUT INSERTED.GoodsId VALUES (N'برنج', 4) ;
INSERT INTO Goods (Title,GoodsGroupId) OUTPUT INSERTED.GoodsId VALUES (N'گردو', 4) ;
INSERT INTO Goods (Title,GoodsGroupId) OUTPUT INSERTED.GoodsId VALUES (N'عدس', 4) ;

INSERT INTO Goods (Title,GoodsGroupId) OUTPUT INSERTED.GoodsId VALUES (N'مانیتور', 5) ;
INSERT INTO Goods (Title,GoodsGroupId) OUTPUT INSERTED.GoodsId VALUES (N'تلوزیون', 5) ;

INSERT INTO UnitType (Title) OUTPUT INSERTED.UnitTypeId VALUES ( N'عدد')
INSERT INTO UnitType (Title) OUTPUT INSERTED.UnitTypeId VALUES ( N'کیلوگرم') ;

INSERT INTO GoodsUnit (GoodsId,UnitTypeId,Coefficient,IsPrimary,IsDefault) OUTPUT INSERTED.GoodsUnitId VALUES (1, 1, 1.0, 1, 1) ;
INSERT INTO GoodsUnit (GoodsId,UnitTypeId,Coefficient,IsPrimary,IsDefault) OUTPUT INSERTED.GoodsUnitId VALUES (2, 1, 1.0, 1, 1) ;
INSERT INTO GoodsUnit (GoodsId,UnitTypeId,Coefficient,IsPrimary,IsDefault) OUTPUT INSERTED.GoodsUnitId VALUES (3, 1, 1.0, 1, 1) ;
INSERT INTO GoodsUnit (GoodsId,UnitTypeId,Coefficient,IsPrimary,IsDefault) OUTPUT INSERTED.GoodsUnitId VALUES (4, 1, 1.0, 1, 1) ;
INSERT INTO GoodsUnit (GoodsId,UnitTypeId,Coefficient,IsPrimary,IsDefault) OUTPUT INSERTED.GoodsUnitId VALUES (5, 1, 1.0, 1, 1) ;
INSERT INTO GoodsUnit (GoodsId,UnitTypeId,Coefficient,IsPrimary,IsDefault) OUTPUT INSERTED.GoodsUnitId VALUES (6, 2, 1.0, 1, 1) ;
INSERT INTO GoodsUnit (GoodsId,UnitTypeId,Coefficient,IsPrimary,IsDefault) OUTPUT INSERTED.GoodsUnitId VALUES (7, 2, 1.0, 1, 1) ;
INSERT INTO GoodsUnit (GoodsId,UnitTypeId,Coefficient,IsPrimary,IsDefault) OUTPUT INSERTED.GoodsUnitId VALUES (8, 2, 1.0, 1, 1) ;
INSERT INTO GoodsUnit (GoodsId,UnitTypeId,Coefficient,IsPrimary,IsDefault) OUTPUT INSERTED.GoodsUnitId VALUES (9, 2, 1.0, 1, 1) ;
INSERT INTO GoodsUnit (GoodsId,UnitTypeId,Coefficient,IsPrimary,IsDefault) OUTPUT INSERTED.GoodsUnitId VALUES (10, 2, 1.0, 1, 1) ;
INSERT INTO GoodsUnit (GoodsId,UnitTypeId,Coefficient,IsPrimary,IsDefault) OUTPUT INSERTED.GoodsUnitId VALUES (11, 1, 1.0, 1, 1) ;
INSERT INTO GoodsUnit (GoodsId,UnitTypeId,Coefficient,IsPrimary,IsDefault) OUTPUT INSERTED.GoodsUnitId VALUES (12, 1, 1.0, 1, 1) ;

INSERT INTO Factory (FactoryName , FactoryAddress , PhoneNumber) OUTPUT INSERTED.FactoryId VALUES (N'میهن' ,N'تهران',0912458679) ;


INSERT INTO stock (Title,FactoryId,StockAddress,StockDescription,PhoneNumber,StockCode, CreatUser) OUTPUT INSERTED.stockId VALUES (N'انبارشماره1' , 1 ,N'تهران',N'',0215869,101, 'Admin' ) ;
INSERT INTO GoodsGroupStock (StockId,GoodSGroupId) OUTPUT INSERTED.GoodsGroupStockId VALUES (1 , 1) ;
INSERT INTO GoodsGroupStock (StockId,GoodSGroupId) OUTPUT INSERTED.GoodsGroupStockId VALUES (1 , 2) ;


INSERT INTO stock (Title,FactoryId,StockAddress,StockDescription,PhoneNumber,StockCode, CreatUser) OUTPUT INSERTED.stockId VALUES (N'انبار شماره2' , 1 ,N'تهران',N'',265487455,102, 'Admin' ) ;
INSERT INTO GoodsGroupStock (StockId,GoodSGroupId) OUTPUT INSERTED.GoodsGroupStockId VALUES (2 , 1) ;
INSERT INTO GoodsGroupStock (StockId,GoodSGroupId) OUTPUT INSERTED.GoodsGroupStockId VALUES (2 , 2) ;
INSERT INTO GoodsGroupStock (StockId,GoodSGroupId) OUTPUT INSERTED.GoodsGroupStockId VALUES (2 , 5) ;

INSERT INTO stock (Title,FactoryId,StockAddress,StockDescription,PhoneNumber,StockCode, CreatUser) OUTPUT INSERTED.stockId VALUES (N'انبار شماره3' , 1 ,N'تهران',N'',65487949,103, 'Admin' ) ;
INSERT INTO GoodsGroupStock (StockId,GoodSGroupId) OUTPUT INSERTED.GoodsGroupStockId VALUES (3 , 3) ;
INSERT INTO GoodsGroupStock (StockId,GoodSGroupId) OUTPUT INSERTED.GoodsGroupStockId VALUES (3 , 4) ;

INSERT INTO stock (Title,FactoryId,StockAddress,StockDescription,PhoneNumber,StockCode, CreatUser) OUTPUT INSERTED.stockId VALUES (N'انبار شماره4' , 1 ,N'تهران',N'',021589674,104, 'Admin' ) ;
INSERT INTO GoodsGroupStock (StockId,GoodSGroupId) OUTPUT INSERTED.GoodsGroupStockId VALUES (4 , 3) ;
INSERT INTO GoodsGroupStock (StockId,GoodSGroupId) OUTPUT INSERTED.GoodsGroupStockId VALUES (4 , 4) ;

INSERT INTO StockPeriod (Title , StockId ,FromDate,ToDate,CreatorUser) OUTPUT INSERTED.StockPeriodId VALUES (N'یک ساله' , 1 , 1402/01/07 , 1403/01/07 ,'Admin') ;
INSERT INTO StockPeriod (Title , StockId ,FromDate,ToDate,CreatorUser) OUTPUT INSERTED.StockPeriodId VALUES (N'یک ساله' , 2 , 1402/01/07 , 1403/01/07 ,'Admin') ;
INSERT INTO StockPeriod (Title , StockId ,FromDate,ToDate,CreatorUser) OUTPUT INSERTED.StockPeriodId VALUES (N'یک ساله' , 3 , 1402/01/07 , 1403/01/07 ,'Admin') ;
INSERT INTO StockPeriod (Title , StockId ,FromDate,ToDate,CreatorUser) OUTPUT INSERTED.StockPeriodId VALUES (N'یک ساله' , 4 , 1402/01/07 , 1403/01/07 ,'Admin') ;

INSERT INTO StockClerck (StockId , FullName , PersonalCode , NationalCode , HomeAddress , PhoneNumber ) OUTPUT INSERTED.StockClerckId VALUES (1,N'رضا حسنی ' ,'011' , '05524198674', N'تهران' , '0914758632') ;
INSERT INTO StockClerck (StockId , FullName , PersonalCode , NationalCode , HomeAddress , PhoneNumber ) OUTPUT INSERTED.StockClerckId VALUES (1,N'محمد حسینی' ,'111' , '012345678', N'تهران' , '09125687496') ;
INSERT INTO StockClerck (StockId , FullName , PersonalCode , NationalCode , HomeAddress , PhoneNumber ) OUTPUT INSERTED.StockClerckId VALUES (2,N'احمد رنجبیر' ,'211' , '0235698741', N'تهران' , '09125687496') ;
INSERT INTO StockClerck (StockId , FullName , PersonalCode , NationalCode , HomeAddress , PhoneNumber ) OUTPUT INSERTED.StockClerckId VALUES (2,N'اامیر یاسری' ,'311' , '0147852356', N'تهران' , '09125687496') ;
INSERT INTO StockClerck (StockId , FullName , PersonalCode , NationalCode , HomeAddress , PhoneNumber ) OUTPUT INSERTED.StockClerckId VALUES (2,N'اامیر یاسری' ,'311' , '0147852356', N'تهران' , '09125687496') ;
INSERT INTO StockClerck (StockId , FullName , PersonalCode , NationalCode , HomeAddress , PhoneNumber ) OUTPUT INSERTED.StockClerckId VALUES (3,N'امید میرزایی' ,'511' , '7539516284', N'تهران' , '09125687496') ;
INSERT INTO StockClerck (StockId , FullName , PersonalCode , NationalCode , HomeAddress , PhoneNumber ) OUTPUT INSERTED.StockClerckId VALUES (4,N'یاسر حجازی' ,'611' , '4628931798', N'تهران' , '09125687496') ;
INSERT INTO StockClerck (StockId , FullName , PersonalCode , NationalCode , HomeAddress , PhoneNumber ) OUTPUT INSERTED.StockClerckId VALUES (4,N'مرتضی نجفی' ,'711' , '5362987412', N'تهران' , '09125687496') ;

INSERT INTO Doctype (title) OUTPUT INSERTED.DoctypeId VALUES (N'ورود') ;
INSERT INTO Doctype (title) OUTPUT INSERTED.DoctypeId VALUES (N'خروج');
     
"""

conect.cursor.execute(dataQuery)
conect.cursor.commit()
conect.closedConection