from selenium import webdriver
from selenium.webdriver.common.by import By
import time

if __name__ == '__main__':
    # 创建Chrome参数对象
    options = webdriver.ChromeOptions()
    # 添加试验性参数,隐藏“Chrome正受到自动测试软件的控制”
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    # 设置无头浏览器
    options.add_argument('--headless')
    # 创建Chrome浏览器对象
    browser = webdriver.Chrome(executable_path='/Users/yinchao/Work/webdriver/chromedriver', options=options)
    browser.execute_cdp_cmd(
        'Page.addScriptToEvaluateOnNewDocument',
        {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
    )
    browser.set_window_size(1200, 800)
    # 加载指定的页面
    browser.get('https://www.baidu.com/')

    # 通过元素ID获取元素
    kw_input = browser.find_element(By.ID, 'kw')
    # 模拟用户输入行为
    kw_input.send_keys('Python')
    # 通过CSS选择器获取元素
    su_button = browser.find_element(By.CSS_SELECTOR, '#su')
    # 模拟用户点击行为
    su_button.click()
    time.sleep(10)
