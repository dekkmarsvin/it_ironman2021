from ast import Try
import os
from shutil import ExecError
from linebot import LineBotApi
from linebot.models import (
    TextSendMessage
)
import psycopg2
from psycopg2 import sql
from flask import current_app as app
from datetime import datetime, timedelta

from util import GenApi
from util.dbPm import DBPm
from util import APIModel

dbpm = DBPm()

def OrderPayQueryHandler(resp:APIModel.ResOrderPayQuery, line_bot_api:LineBotApi):
    app.logger.debug(f"ResOrderPayQuery:{resp}")
    payinfo = resp.TSResultContent
    if(payinfo.Status != 'S'):
        dbpm.UPD_payment_bytsno(ispaid=False, paytoken=resp.PayToken, tsno=payinfo.TSNo, aptype=payinfo.APType)
        app.logger.info(f"訂單{payinfo.Param1}付款失敗, 付款編號:{payinfo.OrderNo} - {payinfo.Description}")
        uid = dbpm.UPD_Order_status_by_paid(ostatus=f"付款失敗-{payinfo.Description}", paid = payinfo.OrderNo)
        line_bot_api.push_message(uid, TextSendMessage(text=f"您的訂單: {payinfo.Param1} 付款失敗，原因可能為:\n{payinfo.Description}"))
    else:
        dbpm.UPD_payment_bytsno(ispaid=True, paytoken=resp.PayToken, tsno=payinfo.TSNo, aptype=payinfo.APType)
        app.logger.info(f"訂單{payinfo.Param1}付款成功, 付款編號:{payinfo.OrderNo} - {payinfo.Description}")
        uid = dbpm.UPD_Order_status_by_paid(ostatus=f"付款成功-{payinfo.Description}", paid = payinfo.OrderNo)
        line_bot_api.push_message(uid, TextSendMessage(text=f"您的訂單: {payinfo.Param1} 付款成功囉"))

def ShowProductListHandler(pcid):
    prod_list = dbpm.QUY_Products_info_by_pcid(pcid=pcid)
    # app.logger.debug(f"prod_list:{prod_list}")
    if(not prod_list):return None

    info_list = []
    for prod in prod_list:
        info_list.append(f"【{prod[0]}】 餐點說明↓\n\n{prod[1]}\n\n庫存:{prod[2]}\t售價:{prod[3]}\t訂購代號:{prod[4]}\n")
    # app.logger.debug(f"info_list:{info_list}")

    return '\n'.join(str(v) for v in info_list)

def Control_Shopping_Cart_ViaMessageText(uid, user_type_text):
    split_text = user_type_text.split(' ')
    if(len(split_text) > 3):return "錯誤的購物車指令\ncart \{要加入或變更的產品ID\} \{該產品的數量\}\n輸入數字不需要大括弧\{\}"
    if(not split_text[1].isnumeric()):return "請輸入羅馬數字的產品ID"

    scid = dbpm.INS_QUY_SC(uid)

    if((split_text[2][0] == '+' or split_text[2][0] == '-') and split_text[2][1:].isnumeric()):
        num = int(split_text[2])
        new_qt = dbpm.QUY_Shopping_Cart_item_Quantity(split_text[1], scid) + num
    elif(split_text[2].isnumeric()):
        new_qt = int(split_text[2])
    else:
        return "請直接輸入訂購數量的羅馬數字，或是+/-符號加數字"

    if(new_qt < 0):
        new_qt = 0
    # app.logger.debug(f"{split_text[1]}, {new_qt}")
    p_name, p_price = dbpm.QUY_Prod_Name_and_Price_by_pid(split_text[1])
    current_quantity = dbpm.QUY_Prod_Quantity_by_pid(split_text[1])
    if(current_quantity >= new_qt):
        dbpm.INS_UPD_Prod_to_Cart(scid, split_text[1], new_qt)
        if(new_qt == 0):
            dbpm.DEL_Shopping_Cart_items(scid)
            return f"已將{p_name}自購物車中刪除"
        else:
            return f"已將{p_name}(單價:{p_price})的購買數量設定為{new_qt}"
    else:
        return f"{p_name}目前的庫存不足，無法加入購物車"

def MakeOrder_1_Check_Cart(uid):
    scid = dbpm.INS_QUY_SC(uid)
    isSucc, msg = CheckQuantity(scid)
    if(isSucc):
        dbpm.UPD_Shopping_Cart_lock_bY_scid(True, scid)
        return True, scid
    else:
        return False, msg
    # shopping_list = dbpm.QUY_Shopping_Cart_by_scid(scid)
    # if(not shopping_list):
    #     return False, "購物車內沒有商品喔"
    # for prod in shopping_list:
    #     current_quantity = dbpm.QUY_Prod_Quantity_by_pid(prod[0])
    #     if(current_quantity - prod[1] < 0):
    #         dbpm.INS_UPD_Prod_to_Cart(scid, prod[0], current_quantity)
    #         app.logger.error(f"商品{prod[0]}，庫存不足無法滿足訂單需求數量({prod[1]})")
    #         return False, "部分商品庫存不足，請稍後重試"

def MakeOrder_2_Create_Order(scid, uid):
    try:
        oid = dbpm.INS_Order(uid, scid, ostatus="初始化訂單")
        return True, oid
    except ExecError as Err:
        app.logger.error(scid, uid, Err)
        return False, f"建立訂單時發生錯誤\n{Err}"

def MakeOrder_3_Request_Pay(oid, scid, paytype):
    if(Check_order_ispaid(oid)):return False, "該筆訂單已完成付款"

    # shopping_list = dbpm.QUY_Shoppint_Cart_items_by_oid(oid)
    shopping_list = dbpm.QUY_Shopping_Cart_by_scid(scid)
    amount = 0
    msg = None
    # app.logger.debug(f"MakeOrder_3_Request_Pay({oid}, {paytype}, {type(oid)}, {type(paytype)})")
    for cart_item in shopping_list:
        product_name, product_price = dbpm.QUY_Prod_Name_and_Price_by_pid(cart_item[0])
        amount = amount + product_price * cart_item[1]
    if(paytype == "1"):
        # ATM
        expiredate = (datetime.now() + timedelta(days = 1)).strftime("%Y%m%d")
        paid = dbpm.INS_payment_req('ATM', amount)
        neworder = APIModel.ReqOrderCreate(ShopNo=os.environ['ShopNo'], OrderNo=paid, Amount=amount*100, \
        PrdtName='IT鐵人賽虛擬商店', Param1=oid, ReturnURL=os.environ['ReturnURL'], BackendURL=os.environ['BackendURL'], PayType="A", ExpireDate=expiredate)
        msg = GenApi.OrderCreate(neworder)
        app.logger.debug(f"MakeOrder:{msg}")
    elif(paytype == "2"):
        # 信用卡一次付清
        paid = dbpm.INS_payment_req('C-1', amount)
        neworder = APIModel.ReqOrderCreate(ShopNo=os.environ['ShopNo'], OrderNo=paid, Amount=amount*100, \
        PrdtName='IT鐵人賽虛擬商店', Param1=oid, ReturnURL=os.environ['ReturnURL'], BackendURL=os.environ['BackendURL'], PayType="C")
        msg = GenApi.OrderCreate(neworder)
        app.logger.debug(f"MakeOrder:{msg}")

    if(msg):
        if(msg.Status == 'S'):
            dbpm.UPD_payment_bypaid(paid=paid, tsno=msg.TSNo, ts_decp=msg.Description, ts_status=True, cardpayurl=msg.CardParam.CardPayURL)
            dbpm.UPD_Order_by_oid(paid=paid, ostatus="已產生付款請求", oid=oid)
            isSucc, errmsg = UpdateQuantity(shopping_list)
            if(isSucc):
                return True, msg
            else:
                return False, errmsg
        else:
            dbpm.UPD_payment_bypaid(paid=paid, tsno=msg.TSNo, ts_decp=msg.Description, ts_status=False)
            dbpm.UPD_Order_by_oid(paid=paid, ostatus="產生付款請求失敗", oid=oid)
            errmsg = f"與金流系統通訊時發生錯誤，{msg.Description}"
    dbpm.UPD_Shopping_Cart_lock_bY_scid(False, scid)
    return False, errmsg or "建立付款請求時發生錯誤"

def CheckQuantity(scid):
    shopping_list = dbpm.QUY_Shopping_Cart_by_scid(scid)
    if(not shopping_list):
        return False, "購物車內沒有商品喔"
    for prod in shopping_list:
        current_quantity = dbpm.QUY_Prod_Quantity_by_pid(prod[0])
        if(current_quantity - prod[1] < 0):
            dbpm.INS_UPD_Prod_to_Cart(scid, prod[0], current_quantity)
            dbpm.DEL_Shopping_Cart_items(scid)
            app.logger.warn(f"商品{prod[0]}，庫存不足無法滿足訂單需求數量({prod[1]})")
            return False, "部分商品庫存不足，請稍後重試"
    return True, None

def UpdateQuantity(shopping_list, mode = 1):
    if(shopping_list):
        try:
            if(mode):
                for prod in shopping_list:
                    current_quantity = dbpm.QUY_Prod_Quantity_by_pid(prod[0])
                    new_quantity = current_quantity - prod[1]
                    dbpm.UPD_Prod_Quantity(prod[0], new_quantity)
                    # app.logger.debug(f"pid:{prod[0]}, oldqt:{current_quantity}, newqt:{new_quantity}")
            else:
                for prod in shopping_list:
                    current_quantity = dbpm.QUY_Prod_Quantity_by_pid(prod[0])
                    new_quantity = current_quantity + prod[1]
                    dbpm.UPD_Prod_Quantity(prod[0], new_quantity)
            return True, None
        except Exception as err:
            return False, err
    return False, f"shopping_list:{shopping_list}"

def MakeOrder(uid):
    scid = dbpm.INS_QUY_SC(uid)
    prodlist = []
    tot_price = 0
    shopping_list = dbpm.QUY_Shopping_Cart_by_scid(scid)
    if(not shopping_list):
        return False, "購物車內沒有商品喔"
    for prod in shopping_list:
        # print(f"商品:{prod[0]}, 數量:{prod[1]}")
        current_quantity = dbpm.QUY_Prod_Quantity_by_pid(prod[0])
        if(current_quantity - prod[1] < 0):
            dbpm.INS_UPD_Prod_to_Cart(scid, prod[0], current_quantity)
            app.logger.error(f"商品{prod[0]}，庫存不足無法滿足訂單需求數量({prod[1]})")
            return False, "部分商品庫存不足，請稍後重試"
        else:
            new_quantity = current_quantity - prod[1]
            dbpm.UPD_Prod_Quantity(prod[0], new_quantity)
            product_name, product_price = dbpm.QUY_Prod_Name_and_Price_by_pid(prod[0])
            prodlist.append(f"{product_name} * {prod[1]}")
            tot_price = tot_price + product_price * prod[1]

    # 鎖定購物車 
    dbpm.UPD_Shopping_Cart_lock_bY_scid(True, scid)

    # 建立訂單
    oid = dbpm.INS_Order(uid, scid, ostatus="初始化訂單")

    # 建立信用卡付款交易編號
    paid = dbpm.INS_payment_req('C-1', tot_price)
    neworder = APIModel.ReqOrderCreate(ShopNo=os.environ['ShopNo'], OrderNo=oid, Amount=tot_price*100, \
        PrdtName='IT鐵人賽虛擬商店', ReturnURL=os.environ['ReturnURL'], BackendURL=os.environ['BackendURL'], PayType="C")
    msg = GenApi.OrderCreate(neworder)
    app.logger.debug(f"MakeOrder:{msg}")

    if(msg):
        if(msg.Status == 'S'):
            print(f"建立訂單: 編號:{msg.OrderNo}:{prodlist}, 請款金額 = {tot_price}, 付款ID:{paid}, {msg.Description}", {msg.CardParam.CardPayURL})
            dbpm.UPD_payment_bypaid(paid=paid, tsno=msg.TSNo, ts_decp=msg.Description, ts_status=True, cardpayurl=msg.CardParam.CardPayURL)
            dbpm.UPD_Order_by_oid(paid=paid, ostatus="已產生付款請求", oid=oid)
            return True, msg
        else:
            dbpm.UPD_payment_bypaid(paid=paid, tsno=msg.TSNo, ts_decp=msg.Description, ts_status=False)
            dbpm.UPD_Order_by_oid(paid=paid, ostatus="產生付款請求失敗", oid=oid)
            dbpm.UPD_Shopping_Cart_lock_bY_scid(False, scid)
    return False, "與金流系統通訊，建立訂單時發生錯誤"

def Check_order_ispaid(oid):
    paid = dbpm.QUY_paid_by_oid(oid)
    if(paid):
        ispaid = dbpm.QUY_IsPaid_by_paid(paid)
        if(ispaid):
            return True
    return False