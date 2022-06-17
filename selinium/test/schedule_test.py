# python -m pip install schedule

import schedule
import time
import datetime

# 동작할 테스트 함수


def test_function():
    now = datetime.datetime.now()
    print(now)


# 3초 마다 동작
# schedule.every(3).seconds.do(test_function)

# 특정시간 동작
schedule.every().day.at("14:56").do(test_function)

while True:
    schedule.run_pending()
    time.sleep(1)
