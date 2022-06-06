list = [
    ('1','2','3'),
    ('4','5','6'),
    ('7','8','9')
    ]
sql =''
def make(data):
    global sql
    print(data)
    sql = sql + data[0]
    sql = sql + data[1]
    sql = sql + data[2]
    print(sql)
    

for i in range(0,list.__len__()):
    make(list[i])
#     sql = sql + list[i][0]
#     sql = sql + list[i][1]
#     sql = sql + list[i][2]
#     print(sql)
