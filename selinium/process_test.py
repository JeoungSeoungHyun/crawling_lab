from multiprocessing import Pool
import time


def save_food(list):
    print('리스트', list)
    print('리스트사이즈', list.__len__())
    for i in range(list.__len__()):
        my_list.append(list[i])
        print("="*30)
        print(my_list.__len__())


if __name__ == "__main__":
    global my_list
    my_list = []
    food1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    food2 = [11, 12, 13, 14, 15, 16, 17, 18, 19]
    food3 = [21, 22, 23, 24, 25, 26, 27, 28, 29]
    food4 = [31, 32, 33, 34, 35, 36, 37, 38, 39]
    list_food = [food1, food2, food3, food4]

    starttime = time.time()
    pool = Pool(processes=1)
    pool.map(save_food, list_food)
    middletime3 = time.time()

    print(my_list.__len__())
