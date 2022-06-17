# python -m pip install selenium

from multiprocessing import Pool
import time
import datetime
from lib2to3.pgen2 import driver
from matplotlib.pyplot import title
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from db import *
# from pymysql_test import *
# import pandas as pd
from concurrent.futures import ThreadPoolExecutor  # 멀티쓰레드 import
import concurrent.futures  # 멀티쓰레드 import

# 크롬창 열기
options = wd.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = wd.Chrome(executable_path="chromedriver.exe", options=options)
# 로직이 바로 안찾아지는 경우 10초 대기
# driver.implicitly_wait(10)  # seconds


def scroll():
    # 최하단까지 스크롤 읽기
    SCROLL_PAUSE_SEC = 1
    count = 0

    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 끝까지 스크롤 다운
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

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


list_food = ['김치볶음밥', '김치찌개', '된장찌개']

for food in list_food:
    # 특정날짜지정하여 찾아오기
    # url = "https://search.naver.com/search.naver?where=blog&query=김치찌개레시피&sm=tab_opt&nso=so:r,p:from20220520to20220527"

    # 검색어 지정하여 찾아오기
    url = f"https://search.naver.com/search.naver?query={food} 레시피&nso=&where=blog&sm=tab_opt"
    print(url)
    driver.get(url)
    scroll()


def find_li(i):  # 하나의 게시글을 찾는 함수
    return driver.find_element(By.ID, f'sp_blog_{i}')


def find_m_el(li):  # 게시글의 정보가 담긴 상위 element 찾는 함수
    return li.find_element(By.CLASS_NAME, 'api_txt_lines')


def find_title(li):  # 게시글의 제목을 찾는 함수
    return find_m_el(li).text


def find_img(li):  # 게시글의 이미지 url을 찾는 함수
    try:  # 이미지가 없는 경우가 있기 때문에 try_except 사용
        return li.find_element(By.CLASS_NAME, 'api_get').get_attribute('src')
    except:
        return None


def find_url(li):  # 게시글의 url을 찾는 함수
    return find_m_el(li).get_attribute('href')


def format_date(date_string):  # 날짜 포맷 함수
    format = '%Y-%m-%d'
    replace_date = date_string.replace('.', '-')
    return datetime.datetime.strptime(replace_date[:-1], format)


def check_date(date_string):  # 실제 날짜 구하는 함수
    now_timestamp = datetime.datetime.now().timestamp()
    if '어제' in date_string:
        real_timestamp = now_timestamp - 86400
    elif '일' in date_string:
        tokens = date_string.split('일')
        real_timestamp = now_timestamp - int(tokens[0]) * 86400
    elif '시간' in date_string or '분' in date_string or '방금' in date_string:
        real_timestamp = now_timestamp
    else:
        real_timestamp = time.mktime(format_date(date_string).timetuple())
    return datetime.date.fromtimestamp(real_timestamp)


def find_date(li):  # 게시글의 게시일을 찾는 함수
    return check_date(li.find_element(By.CLASS_NAME, 'sub_time').text)


def find_info(i):
    li = find_li(i)
    title = find_title(li)
    img = find_img(li)
    url = find_url(li)
    date = find_date(li)
    return title, img, url, date


i = 0
keys = {'title', 'url', 'img', 'date'}
list_num = []
starttime = time.time()


def find_list(url):
    while True:
        # for i in range(1, 11):
        try:
            i += 1
            # dict으로 바꿔서 세이브 => bulk insert 처리 필요 / 필터링 필요 / 빅데이터? 처리 필요
            # print(i)
            # save(findEle(i))
            # save(**dict(zip(keys, findEle(i))))
            # list.append(dict(zip(keys, findEle(i))))
            find_li(i)
            list_num.append(i)
        except:
            break
    middletime1 = time.time()


if __name__ == '__main__':
    pool = Pool(processes=4)  # 4개의 프로세스를 사용합니다.
    list_info = pool.map(find_list, list_food)  # pool에 일을 던져줍니다.
    middletime2 = time.time()
    save_many(list_info)
    conn.commit()
    conn.close()
    endtime = time.time()
    print('list[i] 생성 소요 시간 ; ', middletime1 - starttime)
    print('list_info 생성 소요 시간 : ', middletime2 - middletime1)
    print('save 소요 시간 : ', endtime - middletime2)
    print('총 소요 시간 : ', endtime-starttime)
