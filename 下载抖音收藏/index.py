import urllib.request
import json
import os

import requests, re, time, pymongo, os, queue, threading
from bs4 import BeautifulSoup
from urllib.parse import quote



def save(video_url,filename, aweme_id):
    client = pymongo.MongoClient('127.0.0.1', 27017)
    db = client.douyin

    collection = db.douyin_shoucang

    x = collection.find_one({'aweme_id':aweme_id})
    if x:
        print('have this one')
    else:
        if video_url:
            collection.update({'aweme_id':aweme_id },
                              {'$set': {'filename': filename, 'url': video_url
                                        }}, upsert=True)



path = 'video'
url_key = 'aweme/v1/aweme/favorite/'


def response(flow):
    if url_key in flow.request.url:
        print("hello\n" * 3)
        data = json.loads(flow.response.text)  # 以json方式加载response
        items = data.get('aweme_list')

        print('uiui',flow.response.text)






         # 以用户ID为目录，判断用户ID，不下载重复文件


        l = []
        for data in data['aweme_list']:
            try:
                video_name = data['desc'] or data['aweme_id']  # 视频描述或视频ID，作为文件名
                video_url = data['video']['play_addr']['url_list'][0]  # 视频链接
                aweme_id = data['aweme_id']
                print('video_name',video_name)
            except:
                video_name = None
            if video_name:
                file_dict = {}
                filename =path + '/' +  video_name
                if not os.path.exists(filename):
                    file_dict['name'] = filename
                    file_dict['url'] = video_url
                    l.append(file_dict)
                    # urllib.request.urlretrieve(video_url, filename=filename + '.mp4')
                    print('下载完成：------------------>' + filename)
                    save(video_url,filename, aweme_id)

                else:
                    print('already download')
        print('len l',len(l))
        print(l)

