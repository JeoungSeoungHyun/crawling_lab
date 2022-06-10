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
        database="greendb"
    )
    engine = create_engine(
        "mysql://{user}:{pw}@localhost/{db}".format(user='green', pw='green1234', db='greendb'))
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
    # print(type(list))
    # print(type(list[0]))
    # print(list[0])
    print(list.__len__(), "개")
    sql = "INSERT INTO post (title,img,url,date) VALUES (%s,%s,%s,%s)"
    try:
        cursor.executemany(sql, list)
    except Exception as e:
        print(e)
        conn.rollback()
        return -1
    return 1


def save_bulk(df):
    print(df)
    df.to_sql('post', engine, if_exists='replace',
              chunksize=1000, method='multi')
