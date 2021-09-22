import flask
from flask_restful import Api, utils
from configparser import ConfigParser
import sqlite3 as db
from types import SimpleNamespace

import util.dbcc as dbcc

app = flask.Flask(__name__)
api = Api(app)

@app.route("/dbstatus", methods=['GET'])
def HelloWorld():
    if(dbcc.quy_dbonline(conn)):
        return "Database ONLINE"
    else:
        return "Database OFFLINE"

if __name__ == '__main__':
    env = ConfigParser()
    env.read('env.ini')
    try:
        conn = db.connect(env['SQL']['sqlite_URL'], check_same_thread=False)
        print(f"load database from {env['SQL']['sqlite_URL']} successfully")
        app.run(port = 8080, debug=True)
    except Exception as err:
        print(err)