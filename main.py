from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re



server = 'http://localhost:4723/wd/hub'

desired_caps = {
    'platformName': 'Android',
    'deviceName': 'Hisense_A2',
    "appPackage": "com.tencent.mm",
    "appActivity": ".ui.LauncherUI",
}

desired_caps['chromeOptions'] = {'androidProcess': 'com.tencent.mm:tools'}
desired_caps['noReset'] = True

driver = webdriver.Remote(server, desired_caps)

time.sleep(5)
el1 = driver.find_element_by_xpath("//android.widget.TextView[@text='通讯录']").click()

time.sleep(3)
driver.find_element_by_xpath("//android.widget.TextView[@text='公众号']").click()
time.sleep(2)
driver.find_element_by_xpath("//android.widget.TextView[@text='BetterRead']").click()
time.sleep(2)
driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="聊天信息"]').click()
time.sleep(2)

n = driver.find_element_by_id('com.tencent.mm:id/apa').get_attribute('text')
n = int(n)
print(n) #原创文章总数

driver.swipe(100,1700,100,100,2000)
time.sleep(1)
driver.find_element_by_xpath("//android.widget.TextView[@text='全部消息']").click()


# 获取当前上下文
c = driver.contexts
print(c)
# 输出结果['NATIVE_APP', 'WEBVIEW_com.tencent.mm:tools']
time.sleep(1)
# 切换为 webview，名称就是从上面的语句得来的
# driver._switch_to.context('WEBVIEW_com.tencent.mm:appbrand0')
time.sleep(1)
driver._switch_to.context('WEBVIEW_com.tencent.mm:tools')

time.sleep(1)

handles = driver.window_handles
driver.switch_to_window(handles[1])
time.sleep(2)


while True:
    wbdata = driver.page_source
    soup = BeautifulSoup(wbdata, 'lxml')
    ms = soup.select('#js_history_list > div.weui_msg_card')
    m = len(ms)
    # print(m)
    print('滑动前：————————' + str(len(wbdata)))
    driver._switch_to.context('NATIVE_APP')


    for i in range(10):
        i = i + 1
        driver.swipe(100, 1700, 100, 10, 1000)
        print(i)

    time.sleep(2)
    driver._switch_to.context('WEBVIEW_com.tencent.mm:tools')
    time.sleep(3)
    wbdata2 = driver.page_source
    print('滑动后————————' + str(len(wbdata2)))
    if wbdata2 == wbdata and m >= n:
        print('reach bottom')
        wbdata = driver.page_source
        soup = BeautifulSoup(wbdata, 'lxml')

        ms = soup.select('h4.weui_media_title')
        m = len(ms)

        print(len(ms))  # 当前页面文章数量

        for i in ms:
            # 提取出标题和链接信息
            title = i.get_text()
            link = i.get("hrefs")
            title = re.sub('\n|\s', '', title)
            data = {
                '标题': title,
                '链接': link
            }
            print(data)
            break



































