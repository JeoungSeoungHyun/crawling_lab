from mariadb_test import *


mmlist = [1, 2, 3, 4]
for i in range(mmlist.__len__()):
    print(i)


result = find_all('food')
# tuple to dict
result_dict = dict((y, x) for x, y, z in result)
# print(result_dict)
# print(result_dict['계란볶음밥'])

# dict의 key를 꺼내는 방법
for key in result_dict:
    print(key)

# dict의 value를 꺼내는 방법1
for value in result_dict.values():
    print(value)

# dict의 value를 꺼내는 방법2
for value in (result_dict.values()):
    print(value)


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

# tuple 을 가진 list 하나의 리스트로 바꾸기
mmmlist = [(1, 2, 3), (4, 5, 6)]

mmlist = []

mmlist.append(mmmlist[0][0])
mmlist.append(mmmlist[0][1])
mmlist.append(mmmlist[0][2])
print(mmlist)
mmlist.append(mmmlist[1][0])
mmlist.append(mmmlist[1][1])
mmlist.append(mmmlist[1][2])
print(mmlist)
