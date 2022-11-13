import traceback

from selenium import webdriver
import datetime
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
driver = webdriver.Chrome(executable_path="chromedriver", options=options)


def login(url):
    # driver.get(url)
    # 打开淘宝登录页，并进行登录
    driver.get("https://www.taobao.com")
    time.sleep(3)
    # F12 点击事件name定位（注意空格）
    if driver.find_element("link text", "亲，请登录"):
        driver.find_element("link text", "亲，请登录").click()
        time.sleep(2)
        #driver.find_element("name", "fm-login-id").send_keys("tb899725058919")
        driver.find_element("name", "fm-login-id").send_keys("图涂ch")
        time.sleep(2)
        #driver.find_element("name", "fm-login-password").send_keys("Yc123456")
        driver.find_element("name", "fm-login-password").send_keys("Yin19920626")
        time.sleep(2)
        try:
            # 找到滑块
            #slider = driver.find_element("xpath", "//span[contains(@class, 'btn_slide')]")
            slider = driver.find_element("xpath", "//div[contains(@id, 'nocaptcha')]")
            slider1 = driver.find_element("name", "fm-login-id")
            # 判断滑块是否可见
            print("开始点击滑块")
            if slider:
                time.sleep(2)
                print("正在点击滑块")
                # 对定位到的元素执行悬停操作
                # ActionChains(driver).move_to_element(slider).perform()
                # 点击并且不松开鼠标
                action = ActionChains(driver)
                action.click_and_hold(on_element=slider)
                action.perform()
                # 往右边移动258个位置
                ActionChains(driver).move_by_offset(xoffset=258, yoffset=0).perform()
                # 松开鼠标
                ActionChains(driver).pause(0.5).release().perform()
        except Exception as e:
            # traceback.print_exc()
            print("登录失败")
            pass
        time.sleep(2)
        driver.find_element("xpath", '//*[@id="login-form"]/div[4]/button').click()
        now = datetime.datetime.now()
        print('login success:', now.strftime('%Y-%m-%d %H:%M:%S'))
        time.sleep(5)
        driver.get(url)
    # time.sleep(3)


def buy(buytime):
    while True:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        # 对比时间，时间到的话就点击结算
        driver.get(url)
        try:
            # 找到滑块
            #slider = driver.find_element("xpath", "//span[contains(@class, 'btn_slide')]")
            slider = driver.find_element("xpath", "//div[contains(@id, 'nocaptcha')]")
            # 判断滑块是否可见
            print("开始点击滑块")
            if slider:
                time.sleep(2)
                print("正在点击滑块")
                # 点击并且不松开鼠标
                action = ActionChains(driver)
                action.click_and_hold(on_element=slider)
                action.perform()
                # 往右边移动258个位置
                ActionChains(driver).move_by_offset(xoffset=258, yoffset=0).perform()
                # 松开鼠标
                ActionChains(driver).pause(0.5).release().perform()
        except Exception as e:
            # traceback.print_exc()
            print("登录失败")
            pass
        if now >= buytime:
            try:
                # 立即抢购
                print("开始抢购")
                if driver.find_element("id", "J_LinkBuy"):  # F12 点击事件id定位
                    print("速度点击！！！")
                    driver.find_element("id", "J_LinkBuy").click()
                    time.sleep(0.09)
                    while now >= buytime:
                        try:
                            print("赶紧买！！！")
                            # 提交订单
                            if driver.find_element("class name", "go-btn"):  # F12 点击事件class定位
                                driver.find_element("class name", "go-btn").click()
                        except:
                            time.sleep(0.02)
            except Exception as e:
                # traceback.print_exc()
                time.sleep(1.00)
        print(now)
        time.sleep(0.05)

#  定位元素方式三种任何一个都可以使用过，实际使用自由组合。
# （1）id定位 driver.find_element_by_id("id")
# （2）name定位 driver.find_element_by_name("name")
# （3）class定位 driver.find_element_by_class_name("class_name")


# 抢购主函数
if __name__ == "__main__":
    # times = input("请输入抢购时间：时间格式：2021-12-29 19:45:00.000000")
    times = "2022-09-05 09:59:59.200000"
    url = "https://detail.tmall.com/item.htm?id=681221873091&spm=a1z0d.6639537/tb.1997196601.12.52957484xQODOM"
    # url = input("请输入抢购地址")
    login(url)
    buy(times)