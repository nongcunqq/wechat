import requests, re, time, pymongo, os
from bs4 import BeautifulSoup
from urllib.parse import quote

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client.jd
collection = db.jd_baojian


def save_image(name, sku, type, num, image_url):
    if not os.path.exists('{0}/{1}'.format(name, sku)):
        os.makedirs('{0}/{1}'.format(name,sku))
    try:

        new_image_url = image_url
        response = requests.get(new_image_url)
        if response.status_code == 200:
            file_path = u'{0}/{1}/{2}_{3}.{4}'.format(name,sku,type, num, 'jpg')
            if not os.path.exists(file_path):
                # os.makedirs(file_path)
                with open(file_path, 'wb')as f:
                    print('now download', file_path)
                    f.write(response.content)

            else:
                print('Already Downloaded', file_path)
    except requests.ConnectionError:
        print('Failed to save image')

# save_image(name, shop, sku, type, img_url)


# 下载数据图片

def download_images():
    items = collection.find()
    l = []
    for item in items:
        sku = item.get('sku')
        big_pics = item.get('big_pics')
        small_pics = item.get('small_pics')
        parameters = item.get('parameters')
        detail_pics = item.get('detail_pics')
        if len(big_pics) == len(small_pics) and len(big_pics) > 0 and len(parameters) > 0 and len(detail_pics) > 0:
            shop = item.get('shopname')
            sku = item.get('sku')
            print(shop)
            print(sku)

            m = 0
            for b in big_pics:
                m = m + 1

                # print(b)
                save_image(name, sku, 'big', str(m), b)

            n = 0
            for s in small_pics:
                n = n + 1

                # print(s)
                save_image(name,  sku, 'small', str(n), s)

            i = 0
            for d in detail_pics:
                i = i + 1

                # print(d)
                save_image(name,  sku, 'detail', str(i), d)

            l.append(item)
            # break
        else:
            print(item)
    print('len l', len(l))

name = 'baojian'

download_images()
