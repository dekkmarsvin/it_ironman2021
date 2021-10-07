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
        dbpm.UPD_payment_bytsno(ispaid=False, tsno=payinfo.TSNo, aptype=payinfo.APType)
        app.logger.info(f"訂單付款失敗, 訂單編號:{payinfo.OrderNo} - {resp.Description}")
        dbpm.UPD_Order_status_by_oid(ostatus=f"付款失敗-{resp.Description}", oid = payinfo.OrderNo)
    else:
        dbpm.UPD_payment_bytsno(ispaid=True, tsno=payinfo.TSNo, aptype=payinfo.APType)
        app.logger.info(f"訂單付款成功, 訂單編號:{payinfo.OrderNo} - {resp.Description}")
        dbpm.UPD_Order_status_by_oid(ostatus=f"付款成功-{resp.Description}", oid = payinfo.OrderNo)