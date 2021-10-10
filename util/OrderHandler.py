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
        num = int(split_text[2][0] + split_text[2][1:])
        new_qt = dbpm.QUY_Shopping_Cart_item_Quantity(split_text[1], scid) + num
    elif(split_text[2].isnumeric()):
        new_qt = split_text[2]
    if(new_qt < 0):
        new_qt = 0
    dbpm.INS_UPD_Prod_to_Cart(scid, split_text[1], new_qt)
    p_name, p_price = dbpm.QUY_Prod_Name_and_Price_by_pid(split_text[1])
    dbpm.DEL_Shopping_Cart_items(scid)
    if(new_qt == 0):
        return f"已將{p_name}自購物車中刪除"
    else:
        return f"已將{p_name}(單價:{p_price})的購買數量設定為{new_qt}"
    