import os
import psycopg2
from psycopg2 import sql
from flask import current_app as app
from datetime import datetime, timedelta

from util import GenApi
from util.dbPm import DBPm
from util import APIModel

dbpm = DBPm()

def OrderPayQueryHandler(resp:APIModel.ResOrderPayQuery):
    app.logger.debug(f"ResOrderPayQuery:{resp}")

    payinfo = resp.TSResultContent
    
    if(payinfo.Status != 'S'):
        dbpm.UPD_payment_bytsno(ispaid=False, paytoken=resp.PayToken, tsno=payinfo.TSNo, aptype=payinfo.APType)
        app.logger.info(f"訂單付款失敗, 訂單編號:{payinfo.OrderNo} - {resp.Description}")
        dbpm.UPD_Order_status_by_oid(ostatus=f"付款失敗-{resp.Description}", oid = payinfo.OrderNo)
    else:
        dbpm.UPD_payment_bytsno(ispaid=True, paytoken=resp.PayToken, tsno=payinfo.TSNo, aptype=payinfo.APType)
        app.logger.info(f"訂單付款成功, 訂單編號:{payinfo.OrderNo} - {resp.Description}")
        dbpm.UPD_Order_status_by_oid(ostatus=f"付款成功-{resp.Description}", oid = payinfo.OrderNo)

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
    if(new_qt < 0):
        new_qt = 0
    app.logger.debug(f"{split_text[1]}, {new_qt}")
    dbpm.INS_UPD_Prod_to_Cart(scid, split_text[1], new_qt)
    p_name, p_price = dbpm.QUY_Prod_Name_and_Price_by_pid(split_text[1])
    dbpm.DEL_Shopping_Cart_items(scid)
    if(new_qt == 0):
        return f"已將{p_name}自購物車中刪除"
    else:
        return f"已將{p_name}(單價:{p_price})的購買數量設定為{new_qt}"

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
            dbpm.UPD_Cart_items(scid, prod[0], current_quantity)
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
    oid = dbpm.INS_Order(os.environ['Me'], scid, ostatus="初始化訂單")

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
            return True, msg.CardParam.CardPayURL
        else:
            dbpm.UPD_payment_bypaid(paid=paid, tsno=msg.TSNo, ts_decp=msg.Description, ts_status=False)
            dbpm.UPD_Order_by_oid(paid=paid, ostatus="產生付款請求失敗", oid=oid)
            dbpm.UPD_Shopping_Cart_lock_bY_scid(False, scid)
    return False, "與金流系統通訊，建立訂單時發生錯誤"