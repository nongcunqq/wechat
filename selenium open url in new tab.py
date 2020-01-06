from selenium import webdriver

from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Chrome()

shop_dict = wanju_dict = {'智恩堡': '830022', '迪士尼': '1000079261', '奥迪双钻': '1000002019', '培乐多': '1000001507', '酷骑': '786200', '小猪佩奇': '193850', '美乐': '1000004701', '贝芬乐': '1000001602', '好孩子': '782097', '智伴': '1000102506', '哆啦A梦': '1000017330', '托马斯&朋友': '1000014691',  'toyroyal': '1000281561', '纽奇': '1000091202'}



url = 'https://mall.jd.com/index-{}.html'

m = 0
for k, v in shop_dict.items():
    m = m + 1
    print(k)
    print(v)
    print(url.format(v))
    browser.execute_script("window.open('{}','_blank');".format(url.format(v)))

    if m > 3:
        break
