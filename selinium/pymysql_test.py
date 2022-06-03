import pymysql

db = pymysql.connect(
    user='green',
    passwd='green1234',
    host='localhost',
    db='greendb',
    charset='utf8'
)

# 커서 획득
cursor = db.cursor(pymysql.cursors.DictCursor)

# 데이터 입력. dict형 데이터


def save(list):
    insert_sql = 'INSERT INTO post VALUES (%(title)s,%(url)s,%(img)s,%(date)s);'
    cursor.executemany(insert_sql, list)
    db.commit()
