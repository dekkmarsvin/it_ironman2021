from flask import Flask, request, abort, jsonify
from flask_restful import Api, utils
import sqlite3 as db
from types import SimpleNamespace
import logging
from datetime import date
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import psycopg2

import util.dbcc as dbcc

app = Flask(__name__)
api = Api(app)

line_bot_api = LineBotApi(os.environ['LCAT'])
handler = WebhookHandler(os.environ['Cst'])

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
    app.logger.debug(f"event:{event}")
    format_time = date.fromtimestamp(event.timestamp / 1000).strftime("%Y/%m/%d %H:%M:%S")
    app.logger.debug(f"message:{event.message.type}-{event.message.id} = {event.message.text}, from {event.source.type}:{event.source.userId} at {format_time}")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

@app.route('/')
def default_route():
    """Default route"""
    app.logger.debug('this is a DEBUG message')
    app.logger.info('this is an INFO message')
    app.logger.warning('this is a WARNING message')
    app.logger.error('this is an ERROR message')
    app.logger.critical('this is a CRITICAL message')
    return jsonify('hello world')

@app.route("/dbstatus", methods=['GET'])
def HelloWorld():
    # conn = db.connect(os.environ['sqlite_URL'], check_same_thread=False)
    # if(dbcc.quy_dbonline(conn)):
    #     return "Database ONLINE"
    # else:
    #     return "Database OFFLINE"
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute('SELECT VERSION()')
    rr = cur.fetchall()
    conn.commit()
    cur.close()
    return jsonify(f"Database version : {rr}")

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