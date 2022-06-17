# python -m pip install mariadb
# python -m pip install PyMySQL


from operator import index
import time
import datetime
from sqlalchemy import create_engine
# import pandas as pd
import mariadb
import sys


try:
    conn = mariadb.connect(
        user="green",
        password="green1234",
        host="localhost",
        port=3306,
        database="greendb3"
    )
    engine = create_engine(
        "mysql://{user}:{pw}@localhost/{db}".format(user='green', pw='green1234', db='greendb3'))
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.ext(1)

cursor = conn.cursor()


def save(**data):
    # print(data)
    sql = "INSERT INTO post (title,url,img,date) VALUES (%(title)s,%(url)s,%(img)s,%(date)s)"
    try:
        cursor.execute(sql, data)
    except Exception as e:
        print(e)
        conn.rollback()
        return -1
    return 1


def save_many(list):
    print(list.__len__(), "개")
    sql = "INSERT INTO post (title,thumnail,url,postDate,foodId) VALUES (%s,%s,%s,%s,%s)"
    # 아래처럼은 바인딩이 안된다..
    # sql = f"INSERT INTO post (title,thumnail,url,date,foodId) VALUES (%s,%s,%s,%s,%s,{foodId})"
    try:
        cursor.executemany(sql, list)
    except Exception as e:
        print('쿼리 :', sql)
        print(e)
        conn.rollback()
        return -1
    return 1


def save_bulk(df):
    print(df)
    df.to_sql('post', engine, if_exists='replace',
              chunksize=1000, method='multi')


def find_all(table):
    sql = "SELECT * FROM " + table
    cursor.execute(sql)
    rows = cursor.fetchall()
    return rows
