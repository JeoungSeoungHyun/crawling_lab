from multiprocessing import Pool
import time


def A(mlist):
    list = []
    print(mlist.__len__())
    for i in range(mlist.__len__()):
        list.append(mlist[i])
    print(list)
    print("*"*60)
    return list


if __name__ == "__main__":
    man_list = []
    pool = Pool(processes=2)
    num = [1, 1, 1, 1, 1, 1]
    num2 = [2, 2, 2, 2, 2]
    num3 = [3, 3, 3, 3, 3]
    num4 = [4, 4, 4, 4, 4]
    num_l = [num, num2, num3, num4]
    print(man_list)
    print("="*60)
    man_list = pool.map(A, num_l)
    print("="*60)
    print(man_list)
