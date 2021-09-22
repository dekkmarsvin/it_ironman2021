from os import truncate
import sqlite3 as db
from configparser import ConfigParser
from sqlite3.dbapi2 import Cursor
from types import SimpleNamespace

def quy_dbonline(conn:db.connect):
    sql = "SELECT 1 FROM Users"
    r = conn.execute(sql)
    return r.fetchone()[0] == 1

def quy_user(conn, uid):
    sql = f"SELECT * FROM Users WHERE UID = {uid}"
    # print(sql)
    rr =  conn.execute(sql)
    # print(rr.fetchall())
    return rr.fetchone()

def INS_user(conn, user):
    try:
        sql = f"INSERT INTO Users (TYPE, NAME, PWDHASH) VALUES (?, ?, ?)"
        cursor = conn.cursor()
        cursor.execute(sql, (user.type, user.name, user.pwdhash),)
        uid = cursor.lastrowid
        conn.commit()
        conn.close()
        print(f"Execte INSERTR user successfully:{uid}")
        return uid
    except Exception as err:
        print(err)
        return -1

def exec_sqlfile(conn, fp):
    try:
        with open(fp, 'r') as sql_file:
            sql_script = sql_file.read()
        cursor = conn.cursor()
        cursor.executescript(sql_script)
        conn.commit()
        conn.close()
        print("Execte Script successfully")
        return True
    except Exception as err:
        print(err)
        return False

if __name__ == '__main__':
    env = ConfigParser()
    env.read('env.ini')
    try:
        conn = db.connect(env['SQL']['sqlite_URL'])
        print(f"load database from {env['SQL']['sqlite_URL']} successfully")
        # exec_sqlfile(conn=conn, fp="./data/sql/init.sql")

        user = SimpleNamespace(type = 1, name = "admin", pwdhash = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918")
        # INS_user(conn=conn, user=user)

        quy_user(conn, 7)
        quy_dbonline(conn)
    except Exception as err:
        print(err)