# python -m pip install selenium (자신의 크롬 브라우저에 맞는 드라이버 설치 필요)

# 멀티 프로세싱 사용 import
from multiprocessing import Pool

# 셀레니움을 위한 import
from lib2to3.pgen2 import driver
from selenium import webdriver as wd
from selenium.webdriver.common.by import By

# db와의 연결 위한 import
from mariadb_test import *

# 시간 측정 위한 import
import time

# 날짜 데이터 변환을 위한 import
import datetime

# 드라이버 옵션 설정
options = wd.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = wd.Chrome(executable_path="chromedriver.exe", options=options)

# 로직이 바로 안찾아지는 경우 10초 대기
# driver.implicitly_wait(10)  # seconds


def open_browser(food):  # 브라우저 여는 함수
    # 드라이버 열기
    # 특정날짜지정하여 찾아오기
    # url = f"https://search.naver.com/search.naver?where=blog&query={food} 레시피&sm=tab_opt&nso=so:r,p:from20220520to20220527"

    # 검색어 지정하여 찾아오기
    url = f"https://search.naver.com/search.naver?query={food} 레시피&nso=&where=blog&sm=tab_opt"
    driver.get(url)
    # 최하단까지 스크롤 읽기

    # 대기시간 변수
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


def find_li(i):  # 하나의 게시글(li)을 찾는 함수
    return driver.find_element(By.ID, f'sp_blog_{i}')


def find_m_el(li):  # 게시글의 정보가 담긴 상위 element 찾는 함수
    return li.find_element(By.CLASS_NAME, 'api_txt_lines')


def find_title(li):  # 게시글의 제목을 찾는 함수
    return find_m_el(li).text


def find_thumnail(li):  # 게시글의 이미지 url을 찾는 함수
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


def find_post_date(li):  # 게시글의 게시일을 찾는 함수
    return check_date(li.find_element(By.CLASS_NAME, 'sub_time').text)


def compare(food, title):  # 타이틀에 검색어가 포함되어 있는지 확인하는 함수
    isRight = True
    str_list = list(food)
    for str in str_list:
        if str in title:
            isRight = True
        else:
            isRight = False
            break
    return isRight


def find_info(i, foodId, food):  # 모든 정보를 담아 리턴하는 함수
    li = find_li(i)
    title = find_title(li)
    # 제목에 음식 이름이 들어가는 경우만 골라낸다
    if(compare(food, title)):
        thumnail = find_thumnail(li)
        url = find_url(li)
        post_date = find_post_date(li)
        return title, thumnail, url, post_date, foodId


# db로부터 food 리스트 가져오기
data_food = find_all('food')
# 테스트용 데이터
# data_food = [(1, '계란볶음밥', 1), (2, '김치볶음밥', 2)]

# tuple type의 리스트를 dict type list로 변환하여 사용
dict_data_food = dict((y, x) for x, y, z in data_food)


def make_insert_data(food):  # bulk insert를 위해 food에 대해 크롤링 한 데이터를 리스트에 담는다.
    list_info = []
    middletime1 = time.time()
    i = 0
    open_browser(food)
    while True:
        try:
            i += 1
            info = find_info(i, dict_data_food[food], food)
            # 타이틀에 음식 이름이 없는 내용은 제외한다. 이 때 None이 return되기 때문에 break를 발생
            if info != None:
                list_info.append(info)
            else:
                break
        except:
            break
    middletime2 = time.time()
    print(food, "list_info 생성시간 : ", middletime2 - middletime1)
    print('리스트 사이즈', list_info.__len__())
    return list_info


if __name__ == "__main__":
    # 음식 리스트 저장
    list_food = []
    # id 누락 방지를 위해 하나의 리스트로 옮겨서 한번에 처리
    list_result = []
    # dict의 key를 꺼내는 방법
    for key in dict_data_food:
        list_food.append(key)
    starttime = time.time()
    pool = Pool(processes=4)
    result = pool.map(make_insert_data, list_food)
    print('result 사이즈', result.__len__())
    middletime3 = time.time()
    for i in range(result.__len__()):
        if(result[i].__len__() != 0):
            for j in range(result[i].__len__()):
                list_result.append(result[i][j])
    print(result[i].__len__())
    save_many(list_result)
    conn.commit()
    conn.close()
    endtime = time.time()
    print("save 시간 : ", endtime-middletime3)
    print("총 소요시간 : ", endtime - starttime)
