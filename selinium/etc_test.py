from mariadb_test import *

mlist = [
    ('1', '2', '3'),
    ('4', '5', '6'),
    ('7', '8', '9')
]
sql = ""


def make(data):
    global sql
    print(data)
    sql = sql + data[0]
    sql = sql + data[1]
    sql = sql + data[2]
    print(sql)


for i in range(0, mlist.__len__()):
    make(mlist[i])
#     sql = sql + list[i][0]
#     sql = sql + list[i][1]
#     sql = sql + list[i][2]
#     print(sql)

mmlist = [1, 2, 3, 4]
for i in range(mmlist.__len__()):
    print(i)


result = find_all('food')
# tuple to dict
result_dict = dict((y, x) for x, y, z in result)

# print(result_dict)
# print(result_dict['계란볶음밥'])
# dict의 key를 꺼내는 방법
# for key in result_dict:
#     print(key)

# dict의 value를 꺼내는 방법
# for value in result_dict.values():
#     print(value)

# for value in (result_dict.values()):
#     print(value)


str = '계란 볶음밥'
str2 = '맛있는 게살계란볶음밥 드셔보세요'

# 문자열 한문자씩 list에 넣기 => list함수 사용
print(list(str))

str = '계란 볶음밥'

# list 함수를 이용 한 문자씩 리스트에 넣는다.
r1 = list(str)

# split 함수를 이용한다.
# 인자가 없는 경우 공백을 기준으로 나눈다.
r2 = str.split()
r3 = str.split('계')

print('r1 : ', r1)
print('r2 : ', r2)
print('r3 : ', r3)
