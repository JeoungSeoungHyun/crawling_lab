from multiprocessing import Pool
import time

start_time = time.time()

my_list = []


def fibo(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        # my_list.append(fibo(n-1) + fibo(n-2))
        return fibo(n-1) + fibo(n-2)


def print_fibo(n):  # 피보나치 결과를 확인합니다.
    print(fibo(n))


num_list = [31, 32, 33, 34]

if __name__ == '__main__':

    pool = Pool(processes=4)  # 4개의 프로세스를 사용합니다.
    pool.map(fibo, num_list)  # pool에 일을 던져줍니다. # 결과 자체가 리스트로 나오게 된다!!!!
    # print(type(pool.map(fibo, num_list)))

    print("--- %s seconds ---" % (time.time() - start_time))
