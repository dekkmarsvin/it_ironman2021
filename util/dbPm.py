import os
from re import match
import psycopg2
from psycopg2 import sql
from requests.api import get
from flask import current_app as app
from flask import jsonify
import logging
from datetime import datetime, timedelta

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
        cur.execute(query, ([prof.user_id]))
        r = cur.fetchone()
        cur.close()

        if(not r):
            cur = self.conn.cursor()
            query = sql.SQL("INSERT INTO {}(uid, \"displayName\", language, \"pictureUrl\") VALUES(%s, %s, %s, %s)").format(sql.Identifier('customers'))
            cur.execute(query, (prof.user_id, prof.display_name, prof.language, prof.picture_url))
            self.conn.commit()
            app.logger.debug(f"New User:{prof.display_name} - {prof.user_id}, Created")
            cur.close()
            return 1
        else:
            cur = self.conn.cursor()
            query = sql.SQL("UPDATE {} SET \"displayName\"=%s, language=%s, \"pictureUrl\"=%s, \"Activate\"=%s WHERE uid = %s").format(sql.Identifier('customers'))
            cur.execute(query, (prof.display_name, prof.language, prof.picture_url, "TRUE", prof.user_id))
            self.conn.commit()
            app.logger.debug(f"User:{prof.display_name} - {prof.user_id}, UPDATED")
            cur.close()
            return 2

    def INS_CPN(self, id, cptype):
        if(cptype == "new" or cptype == "back"):
            code = self.gencode()
            s_time, e_time = self.timedelta_bydays(days=7)
            cur = self.conn.cursor()
            id = '{' + id + '}'
            query = sql.SQL("INSERT INTO {}(type, code, s_time, e_time, times, userids) VALUES (%s, %s, %s, %s, %s, %s);").format(sql.Identifier('coupon'))
            cur.execute(query, (cptype, code, s_time, e_time, str(1), id))
            self.conn.commit()
            cur.close()
            return 1, code
        else:
            print()
            return 0, "placeholder Due no coupon"

    def QUY_CPN(self, id, cptype):
        cur = self.conn.cursor()
        query = sql.SQL("SELECT * from coupon WHERE %s = ANY (userids) and type = %s").format(sql.Identifier('coupon'))
        cur.execute(query, (id, cptype))
        r = cur.fetchall()
        cur.close()
        return r

    def timedelta_bydays(self, days=7):
        s_time = datetime.now().isoformat()
        e_time = (datetime.now() + timedelta(days=days)).isoformat()
        return s_time, e_time

    def gencode(self, mode=0):
        import string, random
        if(mode == 0):
            return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))

    def INS_Prod_Cat(self, category_name, category_decp):
        cur = self.conn.cursor()
        query = sql.SQL("INSERT INTO {}(category, category_decp) VALUES (%s, %s)").format(sql.Identifier('product_category'))
        cur.execute(query, (category_name, category_decp))
        (rows,) = cur.fetchone()
        print(f"{rows} been INSERT")
        self.conn.commit()
        cur.close()