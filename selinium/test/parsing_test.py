# from selinium_crawling import *
# 파싱 테스트
import datetime
import time
string = "3시간 전"
tokens = string.split('시간')
# print(tokens[0] * 3)
# print(int(tokens[0]) * 3)

# print(type(get_now_timestamp()))
# print(get_now_timestamp()-3600)

date = '2022.04.25.'
format = '%Y-%m-%d'
replace_date = date.replace('.', '-')
print(replace_date)
parse_date = datetime.datetime.strptime(replace_date[:-1], format)
print(type(parse_date))
real_timestamp = time.mktime(parse_date.timetuple())
print(real_timestamp)
result = datetime.date.fromtimestamp(real_timestamp)

print(result)
# print(datetime.datetime.strptime(result[:-1]))

# if '시간' in date or '분' in date or '방금' in date:
#     print('걸림')
# else:
#     print('안걸림')
