import urllib.request
import json
import os

import requests, re, time, pymongo, os, queue, threading
from bs4 import BeautifulSoup
from urllib.parse import quote



client = pymongo.MongoClient('127.0.0.1', 27017)
db = client.douyin

collection = db.douyin_shoucang

def save_image(name,image_url):
    file_path = u'{0}.{1}'.format(name,'mp4')

    if os.path.exists(file_path):
        print('have this one')
    else:

        if not os.path.exists('{0}'.format('video')):
            try:
                os.makedirs('{0}'.format('video'))
            except:
                pass

        try:

            new_image_url = image_url
            try:
                response = requests.get(new_image_url, timeout=(3,10))
            except:
                print('等待 5 秒钟')
                print(name)
                print(image_url)
                response = requests.get(new_image_url, timeout=(3, 15))
            if response.status_code == 200:
                file_path = u'{0}.{1}'.format(name, 'mp4')
                if not os.path.exists(file_path):
                    # os.makedirs(file_path)
                    with open(file_path, 'wb')as f:
                        print('now download', file_path)
                        f.write(response.content)

                else:
                    print('Already Downloaded', file_path)
        except requests.ConnectionError:
            print('Failed to save image')

items = collection.find()

l = []
for item in items:
    file_dict = {}
    url = item.get('url')
    filename = item.get('filename')
    print('filename',filename)
    print('addr',url)
    if filename:
        if '' in filename:
            filename2 = re.sub('/','\//',filename)
        print(item)
        print(filename)
        print(url)
        file_dict['filename'] = filename
        file_dict['url'] = url
        l.append(file_dict)



    # break

class MyThread(threading.Thread):
    def __init__(self, func):
        threading.Thread.__init__(self)
        self.func = func
    def run(self):
        self.func()


def worker():
    while not q.empty():
        item = q.get()  # 或得任务
        save_image(item['filename'],item['url'])
        # print('Processing : ',item)
        # time.sleep(1)
def main():
    threads = []
    for task in l:
        q.put(task)
    for i in range(threadNum):   #开启三个线程
        thread = MyThread(worker)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

q = queue.Queue()
threadNum = 100
main()

