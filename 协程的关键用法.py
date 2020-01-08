#-*- coding:utf-8 -*-
import requests, re
import time
from bs4 import BeautifulSoup
import gevent
from gevent import monkey
monkey.patch_all(select=False) # 不加 False 会报错

url = 'http://www.qupu123.com/minge'
url = 'http://www.qupu123.com/minge/{}.html'

start = time.time()
l = []
def fetch_content(i):
    url = 'http://www.qupu123.com/minge/{}.html'.format(i)
    wbdata = requests.get(url)
    soup = BeautifulSoup(wbdata.text, 'lxml')

    titles = soup.find('table', {'class':'opern_list'}).findAll('a', {'title':re.compile('.*?'), 'target':'_blank'})

    for i, num in enumerate(titles, 1):
        l.append(i)
        print(i, num.text)


# for i in range(1,5):
#     fetch_content(i)


if __name__ == "__main__":
    jobs = [gevent.spawn(fetch_content, url) for url in range(50)] # 协程的关键用法,速度提升异常明显
    gevent.joinall(jobs)
    [job.value for job in jobs]

    print('len l', len(l))
    end = time.time()
    print('Cost {} seconds'.format((end - start) ))
