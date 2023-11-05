import re
from playwright.sync_api import Playwright, Page, expect, sync_playwright

js = """
   Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
   """

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.add_init_script(js)
    page.goto("https://www.taobao.com/")
    page.get_by_role("link", name="亲，请登录").click()
    page.get_by_placeholder("账号名/邮箱/手机号").click()
    page.get_by_placeholder("账号名/邮箱/手机号").fill("图涂ch")
    page.get_by_placeholder("请输入登录密码").click()
    page.get_by_placeholder("请输入登录密码").fill("Yin19920626")
    page.get_by_role("button", name="登录").click()
    page.add_init_script(js)
    page.goto("https://detail.tmall.com/item.htm?abbucket=4&id=743422174665&ns=1&spm=a21n57.1.0.0.3cf9523cNArOuW",
              timeout=30000)
    page.get_by_role("link", name="加入购物车").click()

    page.wait_for_timeout(1000 * 30)

    # ---------------------
    # context.close()
    # browser.close()

# def run(playwright: Playwright) -> None:
#     browser = playwright.chromium.launch(headless=False)
#     context = browser.new_context()
#     page = context.new_page()
#     page.add_init_script(js)
#     page.goto("https://login.taobao.com/")
#     page.get_by_placeholder("账号名/邮箱/手机号").click()
#     page.get_by_placeholder("账号名/邮箱/手机号").fill("图涂ch")
#     page.get_by_placeholder("请输入登录密码").click()
#     page.get_by_placeholder("请输入登录密码").fill("Yin19920626")
#
#
#
#     slider = page.locator('#baxia-dialog-content').bounding_box()
#     page.mouse.move(x=slider['x'], y=slider['y'] + slider['height'] / 2)
#     page.mouse.down()
#     page.mouse.move(x=slider['x'] + 240, y=slider['y'] + slider['height'] / 2)
#     page.mouse.up()
#     page.pause()
#     page.get_by_role("button", name="登录").click()
#     context.close()
#     browser.close()
#
#
# with sync_playwright() as playwright:
#     run(playwright)

if __name__ == "__main__":
    sync_playwright()
