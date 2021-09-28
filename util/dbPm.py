import os
import psycopg2
from psycopg2 import sql
from requests.api import get
from flask import current_app as app
from flask import jsonify
import logging

class DBPm:
    def __init__(self, DATABASE_URL=os.environ['DATABASE_URL']):
        self.DATABASE_URL = DATABASE_URL
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    def DBver(self):
        cur = self.conn.cursor()
        cur.execute('SELECT VERSION()')
        rr = cur.fetchall()
        app.logger.debug(f"DBver:{rr}")
        self.conn.commit()
        cur.close()
        return rr

    def INS_msg_log(self, id, msgtype, text, dt, stype, suid):
        cur = self.conn.cursor()
        query = sql.SQL("INSERT INTO {}(id, type, text, datetime, source_uid, source_type) VALUES(%s, %s, %s, %s, %s, %s)").format(sql.Identifier('messaging_log'))
        cur.execute(query, (id, msgtype, text, dt, suid, stype))
        self.conn.commit()
        cur.close()