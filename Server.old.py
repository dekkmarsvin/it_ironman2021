from flask import Flask, request, abort
from flask_restful import Api, utils
from configparser import ConfigParser
import sqlite3 as db
from types import SimpleNamespace
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import util.dbcc as dbcc

env = ConfigParser()
env.read('env.ini')

app = Flask(__name__)
api = Api(app)

line_bot_api = LineBotApi(env['Line']['LCAT'])
handler = WebhookHandler(env['Line']['Cst'])

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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


@app.route("/dbstatus", methods=['GET'])
def HelloWorld():
    if(dbcc.quy_dbonline(conn)):
        return "Database ONLINE"
    else:
        return "Database OFFLINE"

if __name__ == '__main__':
    try:
        conn = db.connect(env['SQL']['sqlite_URL'], check_same_thread=False)
        print(f"load database from {env['SQL']['sqlite_URL']} successfully")
        app.run(debug=True)
    except Exception as err:
        print(err)