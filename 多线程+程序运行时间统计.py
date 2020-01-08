#-*- coding:utf-8 -*-
import requests, re
from lxml import etree
from time import time
from bs4 import BeautifulSoup
from threading import Thread

url = 'http://www.qupu123.com/minge'
url = 'http://www.qupu123.com/minge/{}.html'

start = time()

def parse(i):
    url = 'http://www.qupu123.com/minge/{}.html'.format(i)
    wbdata = requests.get(url)
    soup = BeautifulSoup(wbdata.text, 'lxml')

    titles = soup.find('table', {'class':'opern_list'}).findAll('a', {'title':re.compile('.*?'), 'target':'_blank'})



    fetch_list = []
    result = []



    # for title in titles:
    #     print(title.text)

    for i, num in enumerate(titles, 1):
        print(i, num.text)
        pass



threads = []
for i in range(1,100):
    t = Thread(target=parse, args=[i])
    t.start()
    threads.append(t)

for t in threads:
    t.join()
parse(1)

# for i in range(1,10):
#     parse(i)

end = time()
print('Cost {} seconds'.format((end - start) ))
