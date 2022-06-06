import multiprocessing
import time
a= 2
test =[]
def count(name):
    for i in range(10000):
        a= 3
        # print('이름',name)
        test.append(i)
        # print(test.__len__())
    return test


list = [1,2,3]
if __name__ == '__main__':
    # print(a)
    t1 = time.time()
    pool = multiprocessing.Pool(processes=1)
    result =pool.map(count,list)
    pool.close()
    pool.join()
    t2 = time.time()
    # print(a)
    print('시간',t2-t1)
    # print(result[1][1])
    # print('사이즈',result[0].__len__())