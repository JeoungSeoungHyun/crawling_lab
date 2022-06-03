# python -m pip install mariadb
# python -m pip install PyMySQL


from operator import index
from sqlalchemy import create_engine
import pandas as pd
import mariadb
import sys


try:
    conn = mariadb.connect(
        user="green",
        password="green1234",
        host="192.168.0.87",
        port=3306,
        database="greendb"
    )
    engine = create_engine(
        "mysql://{user}:{pw}@192.168.0.87/{db}".format(user='green', pw='green1234', db='greendb'))
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
    sql = "INSERT INTO post (title,url,img,date) VALUES (%(title)s,%(url)s,%(img)s,%(date)s)"
    try:
        cursor.executemany(sql, list)
    except Exception as e:
        print(e)
        conn.rollback()
        return -1
    return 1


def save_bulk(df):
    df.to_sql('post', engine, if_exists='append',
              chunksize=1000, index=False, method='multi')
