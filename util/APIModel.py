import json
from types import SimpleNamespace

from linebot.models import (
    PostbackAction, MessageAction, TemplateSendMessage, ConfirmTemplate, URIAction, ButtonsTemplate
)

def ReqOrderCreate(ShopNo = "", OrderNo = "", Amount = 0, CurrencyID = "TWD", PrdtName = "", Memo = "", \
        Param1 = "", Param2 = "", Param3 = "", ReturnURL = "", BackendURL = "", PayType = "", ExpireDate = "", \
            AutoBilling = "Y", ExpBillingDays = 7, ExpMinutes = 10, PayTypeSub = "ONE"):
    # 永豐銀行- 數位金流 API 技術規格文件 page 32
    return SimpleNamespace(ShopNo = ShopNo, OrderNo = OrderNo, Amount = Amount, CurrencyID = CurrencyID, PrdtName = PrdtName, Memo = Memo, \
        Param1 = Param1, Param2 = Param2, Param3 = Param3, ReturnURL = ReturnURL, BackendURL = BackendURL, PayType = PayType, ATMParam = SimpleNamespace(ExpireDate = ExpireDate), \
            CardParam = SimpleNamespace(AutoBilling = AutoBilling, ExpBillingDays = ExpBillingDays, ExpMinutes = ExpMinutes, PayTypeSub = PayTypeSub))

def ReqOrderQuery(ShopNo = "", OrderNo = "", PayType = "", OrderDateTimeS = "", OrderDateTimeE = "", PayDateTimeS = "", \
        PayDateTimeE = "", PayFlag = "", ):
    # 永豐銀行- 數位金流 API 技術規格文件 page 38
    return SimpleNamespace(ShopNo = ShopNo, OrderNo = OrderNo, PayType = PayType, OrderDateTimeS = OrderDateTimeS, OrderDateTimeE = OrderDateTimeE, \
        PayDateTimeS = PayDateTimeS, PayDateTimeE = PayDateTimeE, PayFlag = PayFlag)

def ResOrderCreate(resp:str):
    resp = json.loads(resp)
    order = SimpleNamespace(OrderNo = resp['OrderNo'], ShopNo = resp['ShopNo'], TSNo = resp['TSNo'], Amount = resp['Amount'], Status = resp['Status'], \
        Description = resp['Description'], Param1 = resp['Param1'], Param2 = resp['Param2'], Param3 = resp['Param3'], PayType = resp['PayType'])
    if(resp.get('ATMParam')):
        order.ATMParam = SimpleNamespace(AtmPayNo = resp['ATMParam']['AtmPayNo'], WebAtmURL = resp['ATMParam']['WebAtmURL'], OtpURL = resp['ATMParam']['OtpURL'])
    elif(resp.get('CardParam')):
        order.CardParam = SimpleNamespace(CardPayURL = resp['CardParam']['CardPayURL'])
    return order

def ResOrderPayQuery(resp:str):
    resp = json.loads(resp)
    return SimpleNamespace(ShopNo = resp['ShopNo'], PayToken = resp['PayToken'], Date = resp['Date'], Status = resp['Status'], Description = resp['Description'], \
        TSResultContent = SimpleNamespace(APType = resp['TSResultContent']['APType'], TSNo = resp['TSResultContent']['TSNo'], OrderNo = resp['TSResultContent']['OrderNo'], \
        ShopNo = resp['TSResultContent']['ShopNo'], PayType = resp['TSResultContent']['PayType'], Amount = resp['TSResultContent']['Amount'], \
        Status = resp['TSResultContent']['Status'], Description = resp['TSResultContent']['Description'], Param1 = resp['TSResultContent']['Param1'], \
        Param2 = resp['TSResultContent']['Param2'], Param3 = resp['TSResultContent']['Param3'], LeftCCNo = resp['TSResultContent']['LeftCCNo'], \
        RightCCNo = resp['TSResultContent']['RightCCNo'], CCExpDate = resp['TSResultContent']['CCExpDate'], CCToken = resp['TSResultContent']['CCToken'], \
        PayDate = resp['TSResultContent']['PayDate'], MasterOrderNo = resp['TSResultContent'].get('MasterOrderNo')))

def ShoppingCartTemp(cart_info_text):
    confirm_order_message = ButtonsTemplate(
        title='購物車明細', text=cart_info_text, actions=[
            PostbackAction(label='點我下訂單', display_text='確認購物車OK，我要下訂單', data='action=buy')
        ]
    )
    return confirm_order_message

def OrderPayURLTemp(msg:ResOrderCreate):
    OrderPayURL_template = ButtonsTemplate(
        title='付款通知', text=f"訂單{msg.OrderNo}，總金額 {msg.Amount / 100}", actions=[
            URIAction(label='點我付款', uri=msg.CardParam.CardPayURL),
    ])
    return OrderPayURL_template