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

    def INS_UPD_cus(self, prof):
        # display_name (str) – Display name
        # user_id (str) – User ID
        # picture_url (str) – Image URL
        # status_message (str) – Status message
        # language (str) – Get user’s language

        cur = self.conn.cursor()
        query = sql.SQL("SELECT 1 AS isExists FROM {} WHERE uid = %s").format(sql.Identifier('customers'))
        app.logger.debug(f"query={query}")
        app.logger.debug(f"prof.user_id={prof.user_id}")
        cur.execute(query, ([prof.user_id]))
        r = cur.fetchone()
        app.logger(f"INS_UPD_cus:{r}")
        cur.close()

        if(r['isExists'] != 1):
            cur = self.conn.cursor()
            query = sql.SQL("INSERT INFO {}(uid, displayName, language) VALUES(%s, %s, %s)").format(sql.Identifier('customers'))
            cur.execute(query, (prof.user_id, prof.display_name, prof.language))
            self.conn.commit()
            app.logger.debug(f"New User:{prof.display_name} - {prof.user_id}, Created")
            cur.close()
        return True