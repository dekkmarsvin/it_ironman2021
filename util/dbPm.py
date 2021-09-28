import os
import psycopg2
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

    def INS_msg_log(self, id, msgtype, text, timestamp, stype, suid):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO messaging_log (id, type, text, timestamp, source_uid, source_type VALUES(%s, %s, %s, %s, %s, %s)", (id, msgtype, text, timestamp, suid, stype))
        r = cur.fetchall()
        app.logger.debug(f"INS_msg_log_r:{r}")
        self.conn.commit()
        cur.close()
        return f"INS_msg_log:{r}"