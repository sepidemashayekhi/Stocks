
from fastapi import FastAPI ,Response , status
from fastapi.responses import JSONResponse


import json
import pandas as pd
import persian
from persiantools import characters
import jdatetime

from  services.Items import GoudsGroupItem , Goods , UnitTyp , GoodsUnitType , Factory , Stock , \
    stockPeriodItem , StockClerck , docType , Docheadertype , GoodsGroupStock  ,CreateDoc

from services.functions import getId , insertTableValue , getMax , returenAll , returnWithCondition ,returnGoodsStock , \
                                createDocquery ,docHeaders ,docHeadersDetali ,docHeaderFilter , clerckDetail

from services.errorConfig import errorList




app = FastAPI()

returnData={
    "message":None,
    'data':None,
    "code":None,
    "success":None
}



@app.post('/goodsGroup')
def goodsGroup(item:GoudsGroupItem,response:Response):

    title=persian.convert_en_characters(item.title)

    result=insertTableValue(tablename='GoodsGroup',columnsName='(Title)',values=f"(N'{title}')")

    if result:
        # print(errorList[110])
        returnData['message']=errorList[100]
        returnData['data']=None
        returnData['code']=201
        returnData['success']=True
        response.status_code=status.HTTP_201_CREATED

        return returnData
    
    returnData['message']=errorList[101]
    returnData['data']=None
    returnData['code']=400
    returnData['success']=False
    response.status_code=status.HTTP_400_BAD_REQUEST

    return returnData



@app.post('/goods')
def goods(item:Goods,response:Response):

    result=insertTableValue(tablename='Goods',columnsName='(Title,GoodsGroupId)',values=f"(N'{item.title}', {item.GoodsGroupId})")

    if not result:
        
        returnData['message']=errorList[101]
        returnData['data']=None
        returnData['code']=400
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
            
        return returnData

    returnData['message']=errorList[100]
    returnData['data']=None
    returnData['code']=201
    returnData['success']=True    
    response.status_code=status.HTTP_201_CREATED
    return returnData



@app.post('/UnitType')
def unitType(item:UnitTyp,response:Response):
    
    result=insertTableValue(tablename='UnitType',columnsName='(Title)',
                            values=f"( N'{item.title}')" )
    if not result:
        returnData['message']=errorList[101]
        returnData['data']=None
        returnData['code']=400
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
        
    returnData['message']=errorList[100]
    returnData['data']=None
    returnData['code']=201
    returnData['success']=True    
    response.status_code=status.HTTP_201_CREATED
       
    return returnData



@app.post('/goodsUnitType')
def goodsUnitType(item:GoodsUnitType,response:Response):

    result=insertTableValue(tablename='GoodsUnit',columnsName='(GoodsId,UnitTypeId,Coefficient,IsPrimary,IsDefault)',
                            values=(item.goodsId,item.unitTypeId,item.Coefficient,int(item.isPrimaty),int(item.isDefault),))
    if not result:
        returnData['message']=errorList[101]
        returnData['data']=None
        returnData['code']=400
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return  returnData
    
    returnData['message']=errorList[100]
    returnData['data']=None
    returnData['code']=201
    returnData['success']=True    
    response.status_code=status.HTTP_201_CREATED

    return returnData



@app.post('/factory')
def factory(item:Factory,response:Response):

    result=insertTableValue(tablename='Factory',columnsName="(FactoryName , FactoryAddress , PhoneNumber)" ,
                             values=f"(N'{item.name}' ,N'{item.address}',{item.phoneNUmber})")
    
    if not result:
        returnData['message']=errorList[101]
        returnData['data']=None
        returnData['code']=400
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
    
    returnData['message']=errorList[100]
    returnData['data']=None
    returnData['code']=201
    returnData['success']=True    
    response.status_code=status.HTTP_201_CREATED
    
    return returnData


@app.post('/Stock')
def stock(item:Stock,response:Response):

    StockCode=getMax(tableName='Stock',columnsName='StockId')
    StockCode=100 + int(StockCode)

    id=insertTableValue(tablename="stock",columnsName="(Title,FactoryId,StockAddress,StockDescription,PhoneNumber,StockCode, CreatUser)",
                            values=f"(N'{item.title}' , {item.factoryId} ,N'{item.address}',N'{item.description}',{item.phoneNumber},{StockCode}, 'Admin' )")
    
    for GoodSGroupId in item.goodsGroup:
        
        re=insertTableValue(tablename='GoodsGroupStock',columnsName="(StockId,GoodSGroupId)",
                            values=f"({id} , {GoodSGroupId})")
    
    
    if not id:
        returnData['message']=errorList[101]
        returnData['data']=None
        returnData['code']=400
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
    
    returnData['message']=errorList[100]
    returnData['data']=None
    returnData['code']=201
    returnData['success']=True    
    response.status_code=status.HTTP_201_CREATED
    return returnData



@app.post('/stockPeriod')
def stockPeriod(item:stockPeriodItem , response:Response):

    result=insertTableValue(tablename='StockPeriod', 
                            columnsName='(Title , StockId ,FromDate,ToDate,CreatorUser)',
                            values=f"(N'{item.title}' , {item.stockId} , {item.fromDate} , {item.toDate} ,'Admin')" )
    
    if not result:
        returnData['message']=errorList[101]
        returnData['data']=None
        returnData['code']=400
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
    
    returnData['message']=errorList[100]
    returnData['data']=None
    returnData['code']=201
    returnData['success']=True    
    response.status_code=status.HTTP_201_CREATED
    return returnData


@app.post('/stockClerck')
def clerck(item:StockClerck, response:Response):
    
    personalCode=getMax(tableName='StockClerck',columnsName='StockClerckId')
    personalCode = str(personalCode)+'11'

    result =insertTableValue(tablename='StockClerck',
                             columnsName=f"(StockId , FullName , PersonalCode , NationalCode , HomeAddress , PhoneNumber )" , 
                             values=f"({item.stockId},N'{item.fullName}' ,'{personalCode}' , '{item.nationalCode}', N'{item.address}' , '{item.phoneNumber}')"
                             )

    if not result:
        returnData['message']=errorList[101]
        returnData['data']=None
        returnData['code']=400
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
    
    returnData['message']=errorList[100]
    returnData['data']=None
    returnData['code']=201
    returnData['success']=True    
    response.status_code=status.HTTP_201_CREATED
    return returnData


@app.post('/docType')
def docTypes(item:docType , response:Response):
    result= insertTableValue(tablename='Doctype', 
                             columnsName="(title)" , values=f"(N'{item.title}')")
    
    if not result:
        returnData['message']=errorList[101]
        returnData['data']=None
        returnData['code']=400
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
    
    returnData['message']=errorList[100]
    returnData['data']=None
    returnData['code']=201
    returnData['success']=True    
    response.status_code=status.HTTP_201_CREATED
    return returnData


@app.post('/docHeaderType')
def docHeaderType(item:Docheadertype, response:Response):
    
    result=insertTableValue(tablename='DocHeaderType' ,
                     columnsName="(DocTypeId ,Title)" , 
                     values=f"({item.doctypeId} , N'{item.title}')")
    
    if not result:
        returnData['message']=errorList[101]
        returnData['data']=None
        returnData['code']=400
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
    
    returnData['message']=errorList[100]
    returnData['data']=None
    returnData['code']=201
    returnData['success']=True    
    response.status_code=status.HTTP_201_CREATED
    return returnData


@app.post('/goodsGroupStock')
def goodsGroupStock(item:GoodsGroupStock , response:Response):
    
    result=insertTableValue(tablename='GoodsGroupStock' , 
                            columnsName="(StockId,GoodSGroupId,Discription,CreateUser)",
                            values=f"( {item.stockId} , {item.goosGroupId} , N'{item.discription}' , 'Admin' )"
                            )
    
    if not result:
        returnData['message']=errorList[101]
        returnData['data']=None
        returnData['code']=400
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
    
    returnData['message']=errorList[100]
    returnData['data']=None
    returnData['code']=201
    returnData['success']=True    
    response.status_code=status.HTTP_201_CREATED
    return returnData
    

@app.get('/valuesList')
def valuesList(dataRequest ,response:Response,id:int| None=None ):

    results=[]
    data=returenAll(tableName=dataRequest,pk=id)
    

    if not data:
        returnData['message']=errorList[102]
        returnData['code']=400
        returnData['data']=None
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
    
    returnData['message']=errorList[100]
    returnData['data']=data
    returnData['code']=200
    returnData['success']=True    
    response.status_code=status.HTTP_200_OK
    return returnData


# @app.post('/docHeader')
# def docHeader(item:DocHeader , response:Response):

    dockCode=getMax(tableName="DocHeader",columnsName='DocHeaderId')
    dockCode=str(dockCode)

    StockPeriodId =getId(tableName='StockPeriod' , title=f'{item.stockTo}' , condition='StockId')
    

    result = insertTableValue(tablename='DocHeader' ,
                              columnsName="( DocCode , StockPeriodId , StockFrom ,StockTo , TransfereeUSER , SenderUSER)" ,
                              values=f"( {dockCode} , {StockPeriodId}  , {item.stockFrom} , {item.stockTo} , {item.transfereeUser} , {item.senderUser} )")
    if not result:
        returnData['message']=errorList[102]
        returnData['code']=400
        returnData['data']=None
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
    
    DocHeaderId=getId(tableName='DocHeader' , title=dockCode , condition='DocCode')

    results={
        "DocHeaderId":int(DocHeaderId),
        "DocHeaderTypeId":item.docHeaderTypeId
    }
    
    returnData['message']=errorList[100]
    returnData['data']=results
    returnData['code']=200
    returnData['success']=True    
    response.status_code=status.HTTP_200_OK

    return returnData


@app.get('/clerckStockList')
def clerckStockList(stockId,response:Response):
    
    results={"clercks":[]}
    
    clercks= returnWithCondition(tableName='StockClerck' , title=stockId , condition="stockId")
    
    for i in range(len(clercks.index)):
        result=clercks.iloc[i]
        results['clercks'].append(result.to_dict())

    if not results["clercks"]:
        returnData['message']=errorList[102]
        returnData['code']=400
        returnData['data']=None
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
    
    returnData['message']=errorList[100]
    returnData['data']=results
    returnData['code']=200
    returnData['success']=True    
    response.status_code=status.HTTP_200_OK
    return returnData


@app.get('/stockDetails')
def stockDetails(stockId:int,response:Response):

    stockDetail=returnWithCondition(tableName='Stock',title=stockId,condition="StockId")
    try:
        stockDetail=[stockDetail.iloc[i].to_dict() for i in range(len(stockDetail.index))][0]
    except:
        returnData['message']=errorList[102]
        returnData['code']=400
        returnData['data']=None
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
    
    GoodSGroup=[]
    stockGoodsGroup=returnWithCondition(tableName='GoodsGroupStock', title=stockId, condition='StockId')
    stockGoodsGroupDetails=[stockGoodsGroup.iloc[i].to_dict() for i in range(len(stockGoodsGroup.index))]
    for stockGoodsGroupDetail in stockGoodsGroupDetails:
        GoodSGroupDetail=returnWithCondition(tableName='GoodsGroup',title=stockGoodsGroupDetail['GoodSGroupId'] , condition='GoodSGroupId')
        GoodSGroupDetail=[GoodSGroupDetail.iloc[i].to_dict() for i in range(len(GoodSGroupDetail.index))][0]
        GoodSGroup.append(GoodSGroupDetail)


    DocHeaders=docHeaders(stockId)


    clerckList=returnWithCondition(tableName='StockClerck', title=stockId , condition="StockId" )
    clerckListDict=[]
    for i in range(len(clerckList.index)):
        re=clerckList.iloc[i]
        clerckListDict.append(re.to_dict())

    
    inventoryGoods=returnGoodsStock(stockId)

    stocksPriod=returnWithCondition(tableName='StockPeriod',title=stockId,condition='StockId')
    try:
        stocksPriodName=stocksPriod.iloc[0].values[2]
        stocksPriodId=stocksPriod.iloc[0].values[0]
        stocksPriodJson={
            "stocksPriodId":int(stocksPriodId),
            "stocksPriodName":stocksPriodName
        }
    except:
        stocksPriodJson=None
    
    
    data={
        "stockDetail":stockDetail,
        'clercks':clerckListDict,
        "inventoryGoods":inventoryGoods,
        "stocksPriod":stocksPriodJson,
        "stockGoodsGroupDetails":GoodSGroup,
        "DocHeaders":DocHeaders
    
    }

    return data


@app.post('/createDocTransfer')
def createDocTransfer(item:CreateDoc,response:Response):
    
    docheaderId=createDocquery(item.StockFrom,item.StockTo,item.TransfereeUser,item.SenderUser,item.GoodsInfo)
    data=[]
    for id in docheaderId:
        if id:
            result=docHeadersDetali(id)
            data.append(result)
    
    returnData['message']=errorList[100]
    returnData['data']=data
    returnData['code']=200
    returnData['success']=True    
    response.status_code=status.HTTP_200_OK
    return returnData



@app.get('/docheaderDitail')
def docheaderDitail(docheaderId,response:Response):
    
    data=docHeadersDetali(docheaderId)
    if not len(data):
        returnData['message']=errorList[102]
        returnData['code']=400
        returnData['data']=None
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData

   

    returnData['message']=errorList[100]
    returnData['data']=data
    returnData['code']=200
    returnData['success']=True    
    response.status_code=status.HTTP_200_OK
    return returnData


@app.get('/headerDateFilter')
def headerDateFilter(datefrom,dateTo,response:Response):
    result=docHeaderFilter(datefrom,dateTo)

    if not result:
        returnData['message']=errorList[102]
        returnData['code']=400
        returnData['data']=None
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
    

    returnData['message']=errorList[100]
    returnData['data']=result
    returnData['code']=200
    returnData['success']=True    
    response.status_code=status.HTTP_200_OK
    return returnData


@app.get('/stockClerckDitali')
def stockClerckDitali(stockClerckId,response:Response):
    result=clerckDetail(stockClerckId)
    if not result:
        returnData['message']=errorList[104]
        returnData['code']=400
        returnData['data']=None
        returnData['success']=False
        response.status_code=status.HTTP_400_BAD_REQUEST
        return returnData
    
    returnData['message']=errorList[100]
    returnData['data']=result
    returnData['code']=200
    returnData['success']=True    
    response.status_code=status.HTTP_200_OK
    return returnData
    