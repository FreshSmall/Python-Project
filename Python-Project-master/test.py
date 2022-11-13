from selenium import webdriver
import datetime
import time

# 连接Chrome浏览器
driver = webdriver.Chrome()

def login(url):
    # 打开淘宝登录页，并进行登录
    driver.get("https://www.taobao.com")
    time.sleep(3)
    if driver.find_element_by_link_text("亲，请登录"): # F12 点击事件name定位（注意空格）
        driver.find_element_by_link_text("亲，请登录").click()
        print("请在20秒内完成登录")
        time.sleep(20)
        driver.get(url)
    time.sleep(3)
    now = datetime.datetime.now()
    print('login success:', now.strftime('%Y-%m-%d %H:%M:%S'))


def buy(buytime):
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # 对比时间，时间到的话就点击结算
        if now >= buytime:
            try:
                # 立即抢购
                if driver.find_element_by_id("J_LinkBuy"): # F12 点击事件id定位
                    print("速度点击！！！")
                    driver.find_element_by_id("J_LinkBuy").click()
                    time.sleep(0.09)
                    while now >= buytime:
                        try:
                            print("赶紧买！！！")
                            # 提交订单
                            if driver.find_element_by_class_name('go-btn'): # F12 点击事件class定位
                                driver.find_element_by_class_name('go-btn').click()
                        except:
                            time.sleep(0.02)
            except:
                time.sleep(0.08)
        print(now)
        time.sleep(0.05)

#  定位元素方式三种任何一个都可以使用过，实际使用自由组合。
# （1）id定位 driver.find_element_by_id("id")
# （2）name定位 driver.find_element_by_name("name")
# （3）class定位 driver.find_element_by_class_name("class_name")


# 抢购主函数
if __name__ == "__main__":
    times = input("请输入抢购时间：时间格式：2021-12-29 19:45:00.000000")
    url = input("请输入抢购地址")
    login(url)
    buy(times)