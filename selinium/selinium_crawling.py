# python -m pip install selenium

import time
from lib2to3.pgen2 import driver
from selenium import webdriver as wd

# 크롬창 열기
driver = wd.Chrome(executable_path="chromedriver.exe")
# 로직이 바로 안찾아지는 경우 10초 대기
# driver.implicitly_wait(10)  # seconds
url = "https://search.naver.com/search.naver?where=blog&query=김치찌개 레시피&sm=tab_opt&nso=so:r,p:from20220525to20220526"
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

# 정보 읽어오기
i = 0
while True:
    try:
        i += 1
        el = driver.find_element_by_id(f'sp_blog_{i}')
        element = el.find_element_by_class_name('api_txt_lines')
        url = element.get_attribute('href')
        title = element.text
        imgTag = el.find_element_by_class_name('api_get')
        img = imgTag.get_attribute('src')
        print(i)
        print(title)
        print(url)
        print(img)
    except:
        break
