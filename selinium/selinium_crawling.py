# python -m pip install selenium

import multiprocessing
import time
import datetime
from lib2to3.pgen2 import driver
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from mariadb_test import *
# from pymysql_test import *
# import pandas as pd

# 크롬창 열기
options = wd.ChromeOptions()
# options.headless= True
options.add_experimental_option("excludeSwitches",["enable-logging"])
driver = wd.Chrome(executable_path="chromedriver.exe",options=options)
# 로직이 바로 안찾아지는 경우 10초 대기
# driver.implicitly_wait(10)  # seconds

# 특정날짜지정하여 찾아오기
url = "https://search.naver.com/search.naver?where=blog&query=김치찌개레시피&sm=tab_opt&nso=so:r,p:from20220520to20220527"

# 검색어 지정하여 찾아오기
# url = "https://search.naver.com/search.naver?query=김치찌개 레시피&nso=&where=blog&sm=tab_opt"
driver.get(url)

# 최하단까지 스크롤 읽기
SCROLL_PAUSE_SEC = 1
count = 0

# 스크롤 높이 가져옴
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # 끝까지 스크롤 다운
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # n초 대기
    time.sleep(SCROLL_PAUSE_SEC)

    # 스크롤 다운 후 스크롤 높이 다시 가져옴
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        if count == 0:
            count += 1
            time.sleep(SCROLL_PAUSE_SEC)
        else:
            break
    else:
        last_height = new_height
        count = 0
        

def findEle(i):  # 원하는 값을 찾는 함수
    # print(i)
    # t1 = time.time()
    el = driver.find_element(By.ID, f'sp_blog_{i}')
    # t2 = time.time()
    # print('li 찾는시간 :', t2-t1)
    element = el.find_element(By.CLASS_NAME, 'api_txt_lines')
    # t3 = time.time()
    # print('엘레멘트 찾는시간 :', t3-t2)
    title = element.text
    # t4 = time.time()
    # print('타이틀 찾는시간 :', t4-t3)
    try:
        imgTag = el.find_element(By.CLASS_NAME, 'api_get')
        img = imgTag.get_attribute('src')
        # t5 = time.time()
        # print('이미지 찾는시간 :', t5-t4)
    except:
        img = None
    url = element.get_attribute('href')
    # t6 = time.time()
    # print('url 찾는시간 :', t6-t5)
    date = check_date(el.find_element(By.CLASS_NAME, 'sub_time').text)
    # t7 = time.time()
    # print('날짜 찾는시간 :', t7-t6)
    return title, url, img, date


def get_now_timestamp():  # 현재 시간을 timestamp로 구하는 함수
    return datetime.datetime.now().timestamp()


def check_date(date_string):  # 실제 날짜 구하는 함수
    now_timestamp = get_now_timestamp()
    if '어제' in date_string:
        real_timestamp = now_timestamp - 86400
    elif '일' in date_string:
        tokens = date_string.split('일')
        real_timestamp = now_timestamp - int(tokens[0]) * 86400
    elif '시간' in date_string or '분' in date_string or '방금' in date_string:
        real_timestamp = now_timestamp
    else:
        format = '%Y-%m-%d'
        replace_date = date_string.replace('.', '-')
        parse_date = datetime.datetime.strptime(replace_date[:-1], format)
        real_timestamp = time.mktime(parse_date.timetuple())
    return datetime.date.fromtimestamp(real_timestamp)

# i=0
# t1 = time.time()
# while True:
#     try:
#         i +=1
#         el = driver.find_element(By.ID, f'sp_blog_{i}')
#     except:
#         break
# t2 = time.time()
# print('count 시간 : ',t2-t1)
# print('총 개수 : ',i-1)
# driver.close()
# # dict으로 변경하기 위한 키값 튜플
# keys = ('title', 'url', 'img', 'date')
# starttime = time.time()


# 정보 읽어오기
if __name__ == '__main__':
    i=0
    count = 390
    pool = multiprocessing.Pool(processes=2)
    coli = []
    t1 = time.time()
    for i in range(count):
        coli.append(str(i))
    pool.map(findEle(i),coli)
    t2 = time.time()
    print('멀티 시간 :',t2-t1)
    driver.close()

while True:
# for i in range(1, 11):
    try:
        i += 1
        # dict으로 바꿔서 세이브 => bulk insert 처리 필요 / 필터링 필요 / 빅데이터? 처리 필요
        # print(i)
        # save(findEle(i))
        # save(**dict(zip(keys, findEle(i))))
        # list.append(dict(zip(keys, findEle(i))))
        list.append(findEle(i))
    except:
        break
# df = pd.DataFrame(list, columns=['title', 'url', 'img', 'date'])
middletime = time.time()
# save(list)
save_many(list)
endtime = time.time()
conn.commit()
conn.close()
print('전반시간 :', middletime -starttime)
print('후반시간 :', endtime -middletime)
print('총시간 :', endtime-starttime)
