# 现成和进程
from random import randint
from time import time, sleep
from multiprocessing import Process
import tkinter
import tkinter.messagebox
from multiprocessing import Process, Queue
from random import randint


# def download_task(filename):
#     print('开始下载%s...' % filename)
#     time_to_download = randint(5, 10)
#     sleep(time_to_download)
#     print('%s下载完成，耗费了%d秒' % (filename, time_to_download))
#
#
# def single_main():
#     start = time()
#     download_task('Python从入门到住院.pdf')
#     download_task('Peking Hot.avi')
#     end = time()
#     print('总共耗费了%.2f秒.' % (end - start))
#
#
# def main():
#     start = time()
#     p1 = Process(target=download_task, args=('Python从入门到住院.pdf',))
#     p1.start()
#     p2 = Process(target=download_task, args=('Peking Hot.avi',))
#     p2.start()
#     p1.join()
#     p2.join()
#     end = time()
#     print('总共耗费了%.2f秒.' % (end - start))

def one_job():
    total = 0
    number_list = [x for x in range(1, 100000001)]
    start = time()
    for number in number_list:
        total += number
    print(total)
    end = time()
    print('Execution time: %.3fs' % (end - start))

def task_handler(curr_list, result_queue):
    total = 0
    for number in curr_list:
        total += number
    result_queue.put(total)


def parallel_job():
    processes = []
    number_list = [x for x in range(1, 100000001)]
    result_queue = Queue()
    index = 0
    # 启动8个进程将数据切片后进行运算
    for _ in range(8):
        p = Process(target=task_handler,
                    args=(number_list[index:index + 12500000], result_queue))
        index += 12500000
        processes.append(p)
        p.start()
    # 开始记录所有进程执行完成花费的时间
    start = time()
    for p in processes:
        p.join()
    # 合并执行结果
    total = 0
    while not result_queue.empty():
        total += result_queue.get()
    print(total)
    end = time()
    print('Execution time: ', (end - start), 's', sep='')




if __name__ == '__main__':
    one_job()
    parallel_job()
