import os
import psycopg2
from psycopg2 import sql
from flask import current_app as app
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
        cur_stat = cur.statusmessage
        # print(f"{cur_stat}")
        self.conn.commit()
        cur.close()

    def INS_Prod(self, product_name, quantity, product_decp, createddate, expireddate, category, price):
        cur = self.conn.cursor()
        query = sql.SQL("INSERT INTO {}(product_name, quantity, product_decp, createddate, expireddate, category, price) VALUES (%s, %s, %s, %s, %s, %s, %s)").format(sql.Identifier('products'))
        cur.execute(query, (product_name, quantity, product_decp, createddate, expireddate, category, price))
        cur_stat = cur.statusmessage
        # print(f"{cur_stat}")
        self.conn.commit()
        cur.close()

    def UPD_Prod_Quantity(self, pid, new_quantity):
        cur = self.conn.cursor()
        query = sql.SQL("UPDATE {} SET quantity=%s WHERE pid = %s").format(sql.Identifier('products'))
        cur.execute(query, (new_quantity, pid))
        self.conn.commit()
        cur.close()

    def INS_Order(self,):
        cur = self.conn.cursor()
        query = sql.SQL("INSERT INTO {}(uid, scid, createddate, paid, ostatus) VALUES (?, ?, ?, ?, ?, ?) RETURNING oid").format(sql.Identifier('orders'))
        cur.execute(query, )

    def INS_payment_req(self, pty_type):
        cur = self.conn.cursor()
        query = sql.SQL("INSERT INTO {}(type) VALUES (%s) RETURNING paid").format(sql.Identifier('payment_log'))
        cur.execute(query, (pty_type,))
        paid = cur.fetchone()
        if(paid):
            return paid[0]
        return None

    def UPD_payment_bypaid(self, paid:int, ispaid:bool, paytoken:str):
        cur = self.conn.cursor()
        query = sql.SQL("UPDATE {} SET ispaid=%s, paytoken=%s WHERE paid = %s").format(sql.Identifier('payment_log'))
        cur.execute(query, (ispaid, paytoken, paid))
        self.conn.commit()
        cur.close()

    def INS_QUY_SC(self, id):
        #先檢查是否有存在的可用購物車

        cur = self.conn.cursor()
        query = sql.SQL("SELECT scid FROM {} WHERE uid = %s and lock = false LIMIT 1").format(sql.Identifier('shopping_cart'))
        cur.execute(query, (id,))
        scid = cur.fetchone()
        cur.close()
        print(f"scid-quy:{scid}")

        if(not scid):
            ct = datetime.now().isoformat()
            cur = self.conn.cursor()
            query = sql.SQL("INSERT INTO {}(uid, createddate) VALUES (%s, %s) RETURNING scid").format(sql.Identifier('shopping_cart'))
            cur.execute(query, (id, ct))
            scid = cur.fetchone()
            print(f"scid-ins:{scid}")
            self.conn.commit()
            cur.close()
        return scid[0]

    def QUY_Prod_Name_and_Price_by_pid(self, pid):
        cur = self.conn.cursor()
        query = sql.SQL("SELECT product_name, price FROM {} Where pid = %s").format(sql.Identifier('products'))
        cur.execute(query, (pid,))
        prod_info = cur.fetchone()
        if(prod_info):
            return [prod_info[0], prod_info[1]]
        return None

    def QUY_Prod_Quantity_by_pid(self, pid):
        cur = self.conn.cursor()
        query = sql.SQL("select quantity from {} where pid = %s").format(sql.Identifier('products'))
        cur.execute(query, (pid,))
        qt = cur.fetchone()
        cur.close()
        if(qt):
            return qt[0]
        return None

    def QUY_Shopping_Cart_by_scid(self, scid):
        cur = self.conn.cursor()
        query = sql.SQL("SELECT productid, quantity FROM {} where scid = %s").format(sql.Identifier('cart_items'))
        cur.execute(query, (scid,))
        shopping_list = cur.fetchall()
        if(shopping_list):
            return list(map(list, shopping_list))
        return None

    def UPD_Shopping_Cart_lock_bY_scid(self, lock, scid):
        cur = self.conn.cursor()
        query = sql.SQL("UPDATE {} SET lock=%s WHERE scid = %s").format(sql.Identifier('shopping_cart'))
        cur.execute(query, (lock, scid))
        self.conn.commit()
        cur.close()

    def UPD_Cart_items(self, scid, pid, quantity):
        cur = self.conn.cursor()
        query = sql.SQL("UPDATE {} SET quantity=%s WHERE scid = %s and productid = %s").format(sql.Identifier('cart_items'))
        cur.execute(query, (quantity, scid, pid))
        self.conn.commit()
        cur.close()

    def INS_Prod_to_Cart(self, scid, pid, quantity):
        cur = self.conn.cursor()
        query = sql.SQL("SELECT quantity from {} where scid = %s and productid = %s").format(sql.Identifier('cart_items'))
        cur.execute(query, (scid, pid))
        qt = cur.fetchone()
        cur.close()
        if(qt):
            qt = qt[0] + quantity
            cur = self.conn.cursor()
            query = sql.SQL("UPDATE {} SET quantity=%s WHERE scid = %s and productid = %s").format(sql.Identifier('cart_items'))
            cur.execute(query, (qt, scid, pid))
            self.conn.commit()
            cur.close()
        else:
            cur = self.conn.cursor()
            query = sql.SQL("INSERT INTO {}(scid, productid, quantity) VALUES (%s, %s, %s)").format(sql.Identifier('cart_items'))
            cur.execute(query, (scid, pid, quantity))
            self.conn.commit()
            cur.close()