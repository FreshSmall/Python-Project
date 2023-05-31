import random
import time
from threading import Thread
from concurrent.futures import ThreadPoolExecutor
from threading import RLock


class DownloadThread(Thread):

    def __init__(self, filename):
        self.filename = filename
        super().__init__()

    def run(self):
        start = time.time()
        print(f'开始下载 {self.filename}.')
        time.sleep(random.randint(3, 6))
        print(f'{self.filename} 下载完成.')
        end = time.time()
        print(f'下载耗时: {end - start:.3f}秒.')

class Account(object):
    """银行账户"""

    def __init__(self):
        self.balance = 0.0
        self.lock = RLock()

    def deposit(self, money):
        """存钱"""
        self.lock.acquire()
        try:
            new_balance = self.balance + money
            time.sleep(0.01)
            self.balance = new_balance
        finally:
            self.lock.release()

def download(*, filename):
    start = time.time()
    print(f'开始下载 {filename}.')
    time.sleep(random.randint(3, 6))
    print(f'{filename} 下载完成.')
    end = time.time()
    print(f'下载耗时: {end - start:.3f}秒.')


def main():
    start = time.time()
    download(filename='Python从入门到住院.pdf')
    download(filename='MySQL从删库到跑路.avi')
    download(filename='Linux从精通到放弃.mp4')
    end = time.time()
    print(f'总耗时: {end - start:.3f}秒.')

def thread_main():
    threads = [
        Thread(target=download, kwargs={'filename': 'Python从入门到住院.pdf'}),
        Thread(target=download, kwargs={'filename': 'MySQL从删库到跑路.avi'}),
        Thread(target=download, kwargs={'filename': 'Linux从精通到放弃.mp4'})
    ]
    start = time.time()
    # 启动三个线程
    for thread in threads:
        thread.start()
    # 等待线程结束
    for thread in threads:
        thread.join()
    end = time.time()
    print(f'总耗时: {end - start:.3f}秒.')

def clazz_main():
    threads = [
        DownloadThread('Python从入门到住院.pdf'),
        DownloadThread('MySQL从删库到跑路.avi'),
        DownloadThread('Linux从精通到放弃.mp4')
    ]
    start = time.time()
    # 启动三个线程
    for thread in threads:
        thread.start()
    # 等待线程结束
    for thread in threads:
        thread.join()
    end = time.time()
    print(f'总耗时: {end - start:.3f}秒.')

def theadpool_main():
    with ThreadPoolExecutor(max_workers=4) as pool:
        filenames = ['Python从入门到住院.pdf', 'MySQL从删库到跑路.avi', 'Linux从精通到放弃.mp4']
        start = time.time()
        for filename in filenames:
            pool.submit(download, filename=filename)
    end = time.time()
    print(f'总耗时: {end - start:.3f}秒.')

def sync_main():
    """主函数"""
    account = Account()
    with ThreadPoolExecutor(max_workers=16) as pool:
        for _ in range(100):
            pool.submit(account.deposit, 1)
    print(account.balance)

if __name__ == '__main__':
    sync_main()