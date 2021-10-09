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
    app.logger.debug(f"prod_list:{prod_list}")
    if(not prod_list):return None

    info_list = []
    for prod in prod_list:
        info_list.append(f"{prod[0]}\n{prod[1]}\n庫存:{prod[2]}\t售價:{prod[3]}\t訂購代號:{prod[4]}")
    app.logger.debug(f"info_list:{info_list}")

    return '\n'.join(str(v) for v in info_list)