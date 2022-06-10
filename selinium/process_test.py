from multiprocessing import Pool
import time

food = [1, 2, 3, 4, 5, 6, 7, 8, 9]


def get_count(num, p=4):
    list = []
    allocate = int(num/p)  # 한 프로세스가 맡을 개수
    for i in range(p):
        list.append(allocate)
    list[p-1] += num % p  # 남는 작업은 마지막 프로세스에 추가
    print('프로세스 할당량 : ', list)


def output(data):
    count = 0
    for i in range(10000):
        count += 1


print(get_count(food.__len__()))

if __name__ == '__main__':
    starttime = time.time()
    pool = Pool(processes=4)
    pool.map(output, food)
    pool.close()
    pool.join()
    endtime = time.time()
    print(endtime - starttime)
