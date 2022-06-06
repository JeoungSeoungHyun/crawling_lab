import encodings
import pymysql

db = pymysql.connect(
    user='green',
    passwd='green1234',
    host='192.168.89.62',
    db='greendb3',
    charset='utf8'
)

# 커서 획득
cursor = db.cursor()

# 데이터 입력. dict형 데이터


def save(list):
    insert_sql = 'INSERT INTO post (title,url,img,date) VALUES (%s,%s,%s,%s);'
    # insert_sql = 'INSERT INTO post (title,url,img,date) VALUES (%(title)s,%(url)s,%(img)s,%(date)s);'
    cursor.executemany(insert_sql, list)
    db.commit()
    db.close()