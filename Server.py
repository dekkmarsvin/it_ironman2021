from flask import Flask, request, abort, jsonify
from flask_restful import Api, utils
import sqlite3 as db
from types import SimpleNamespace
import logging
from datetime import datetime
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, PostbackEvent, PostbackAction, MessageAction
)
import os
from linebot.models.events import FollowEvent
import psycopg2
import pytz
from util import APIModel

import util.dbPm as dbPm
import util.GenApi as FunBizApi
import util.OrderHandler as Handler

app = Flask(__name__)
api = Api(app)

line_bot_api = LineBotApi(os.environ['LCAT'])
handler = WebhookHandler(os.environ['Cst'])
TWT = pytz.timezone('Asia/Taipei')
dbpm = dbPm.DBPm()

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    prof = line_bot_api.get_profile(event.source.user_id)
    r = dbpm.INS_UPD_cus(prof)
    if r == 1:
        msg = "Hello 歡迎鐵人賽的勇者"
        cpl = dbpm.QUY_CPN(event.source.user_id, "new")
        if(cpl and len(cpl) > 0):
            app.logger.debug(f"已經發過優惠券:{cpl}")
        else:
            cr, code = dbpm.INS_CPN(event.source.user_id, "new")
            if(cr == 1):
                msg = msg + f"\n這是您的好友見面禮:{code}"
    else:
        msg = "Hello 歡迎鐵人賽的勇者回來"
        cpl = dbpm.QUY_CPN(event.source.user_id, "back")
        if(cpl and len(cpl) > 0):
            app.logger.debug(f"已經發過優惠券:{cpl}")
        else:
            cr, code = dbpm.INS_CPN(event.source.user_id, "back")
            if(cr == 1):
                msg = msg + f"\n這是您的回歸小禮物:{code}"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=msg))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event:MessageEvent):
    prof = line_bot_api.get_profile(event.source.user_id)
    dt = datetime.fromtimestamp(event.timestamp / 1000.0).astimezone(TWT)
    format_time = dt.strftime("%Y/%m/%d %H:%M:%S")
    app.logger.debug(f"message:{event.message.type}-{event.message.id} = {event.message.text}, from {event.source.type}:{prof.display_name}({event.source.user_id}) at {format_time}")
    dbpm.INS_msg_log(event.message.id, event.message.type, event.message.text, dt.isoformat(), event.source.type, event.source.user_id)
    user_type_text = str(event.message.text).lower()
    if(user_type_text.startswith('cart ')):
        msg = Handler.Control_Shopping_Cart_ViaMessageText(event.source.user_id, event.message.text)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=msg))
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="找不到對應的指令，請參考主選單-幫助"))

@handler.add(PostbackEvent)
def handler_postback(event):
    prof = line_bot_api.get_profile(event.source.user_id)
    data = event.postback.data
    # app.logger.debug(f"data:{data}")
    if(data == 'action=ShowShoppingCartContents'):
        cart_info, cart_amount = dbpm.QUY_Shopping_Cart_info_by_uid(event.source.user_id)
        app.logger.debug(f"{prof.display_name} 查詢購物車, uid:{event.source.user_id}, {cart_info}")
        replay_text = '\n'.join(str(v) for v in cart_info) + f"\n總共:{cart_amount}元"
        template_msg = APIModel.ShoppingCartTemp(replay_text)
        line_bot_api.reply_message(
            event.reply_token, template_msg
        )
    else:
        from urllib.parse import urlparse, parse_qs
        datapath = urlparse(data).path
        datavalue = parse_qs(urlparse(data).query)
        # app.logger.debug(f"data.path = {datapath}, datavalue = {datavalue}")
        if(datapath == "action=ShowProductList"):
            pcid = datavalue.get('pcid')[0] or None
            if(not pcid):
                app.logger.error(f"錯誤:找不到pcid:{pcid}")
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"發生錯誤，請聯絡客服取得協助, 錯誤訊息:找不到pcid:{pcid}")
                )
            else:
                replay_text = Handler.ShowProductListHandler(pcid) or "錯誤:action=ShowProductList Return None"
                # app.logger.debug(f"replay_text:{replay_text}")
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=replay_text)
                )
        elif(datapath == "action=buy"):
            # isSucc, msg = Handler.MakeOrder(event.source.user_id)
            # if(isSucc):
            #     template_msg = APIModel.OrderPayURLTemp(msg)
            #     line_bot_api.reply_message(
            #         event.reply_token,
            #         template_msg
            #     )
            # else:
            #     line_bot_api.reply_message(
            #         event.reply_token,
            #         TextSendMessage(text=msg)
            #     )
            if(not datavalue):
                isSucc, scidormsg = Handler.MakeOrder_1_Check_Cart(event.source.user_id)
                app.logger.debug(f"建立訂單-檢查購物車, {isSucc}, {scidormsg}")
                if(isSucc):
                    isSucc, oidormsg = Handler.MakeOrder_2_Create_Order(scidormsg, event.source.user_id)
                    if(isSucc):
                        template_msg = APIModel.OrderPaySelTemp(scidormsg, oidormsg)
                        line_bot_api.reply_message(
                            event.reply_token,
                            template_msg
                        )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=oidormsg)
                        ) 
                else:
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=scidormsg)
                    )
            else:
                oid = datavalue.get('oid')[0]
                scid = datavalue.get('scid')[0]
                paytype = datavalue.get('paytype')[0]
                app.logger.debug(f"訂單:{oid}(scid:{scid}), 選擇付款方式:{paytype}")
                if(oid and scid and paytype):
                    isSucc, msg = Handler.MakeOrder_3_Request_Pay(oid, scid, paytype)
                    if(isSucc):
                        if(paytype == "1"):
                            app.logger.debug(f"銀行轉帳(ATM)付款資訊:{msg}")
                            template_msg = APIModel.OrderPayATMTemp(msg)
                            line_bot_api.reply_message(
                                event.reply_token,
                                template_msg
                            )
                        elif(paytype == "2"):
                            app.logger.debug(f"信用卡付款資訊:{msg}")
                            template_msg = APIModel.OrderPayURLTemp(msg)
                            line_bot_api.reply_message(
                                event.reply_token,
                                template_msg
                            )
                    else:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TextSendMessage(text=msg)
                        )
                else:
                    app.logger.debug("建立訂單時參數錯誤", datavalue)
                    
@app.route('/')
def default_route():
    """Default route"""
    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message')
    return jsonify('hello world')

@app.route('/funBIZ_backend', methods=['POST'])
def funBIZ_route():
    # app.logger.debug(f"headers:{dict(request.headers)}")
    content = request.json
    # app.logger.debug(f"content:{content}")
    if(content['ShopNo'] == os.environ['ShopNo']):
        resp = FunBizApi.OrderPayQuery(PayToken=content['PayToken'])
        Handler.OrderPayQueryHandler(resp, line_bot_api)
        return jsonify({'Status':'S'})
    else:
        return jsonify({'Status':'F'})

@app.route('/order-summary', methods=['POST'])
def order_summary_route():
    # app.logger.debug(f"headers:{dict(request.headers)}")
    content = request.form
    # app.logger.debug(f"content:{content}")
    if(content.get('ShopNo') == os.environ['ShopNo']):
        resp = FunBizApi.OrderPayQuery(PayToken=content.get('PayToken'))
        Handler.OrderPayQueryHandler(resp, line_bot_api)
    return jsonify({'order-summary':'S'})

@app.route("/dbstatus", methods=['GET'])
def DBversion():
    r = dbpm.DBver()
    app.logger.debug(f"type:{type(r)}, {r}")
    return jsonify(f"Database Version: {r}")

if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if __name__ == '__main__':
    try:
        conn = db.connect(os.environ['sqlite_URL'], check_same_thread=False)
        print(f"load database from {os.environ['sqlite_URL']} successfully")
        app.run(debug=True)
    except Exception as err:
        print(err)