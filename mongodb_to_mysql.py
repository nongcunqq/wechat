import pymysql, json
import requests, re, time, pymongo, os
from bs4 import BeautifulSoup
from urllib.parse import quote

client = pymongo.MongoClient('127.0.0.1', 27017)
db = client.jd
collection = db.jd_jiadian

items = collection.find()

db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='jd', charset='utf8')

# db = pymysql.connect(host='db4free.net', user='shenlongds', password='12345678', port=3306, db='shenlongds')

cursor = db.cursor()
# sql = 'create table if not exists students (id varchar(255) not null, name varchar(255) not null, age INT NOT NULL,' \
#       'PRIMARY KEY(id))'
#
# cursor.execute(sql)
# db.close()
m = 0
for i in collection.find():
    m = m + 1
    print(i)
    print('m', m)
    sku = i.get('sku')
    big_pics = i.get('big_pics')
    big_pics = json.dumps(big_pics)

    detail_pics = i.get('detail_pics')
    detail_pics = json.dumps(detail_pics)

    parameters = i.get('parameters')
    parameters = json.dumps(parameters)

    shop_id = i.get('shop_id')
    shopname = i.get('shopname')

    small_pics = i.get('small_pics')
    small_pics = json.dumps(small_pics)

    subtitle = i.get('subtitle')
    title = i.get('title')

    if m >= 20:
        break

    print('sku', sku)
    print('big_pics', big_pics)
    print('detail_pics', detail_pics)
    print('parameters', parameters)
    print('shop_id', shop_id)
    print('shopname', shopname)
    print('small_pics', small_pics)
    print('subtitle', subtitle)
    print('title', title)


    data = {
        'sku':sku,
        'big_pics':big_pics,
        'detail_pics':detail_pics,
        'parameters':parameters,
        'shop_id':shop_id,
        'shopname':shopname,
        'small_pics':small_pics,
        'subtitle':subtitle,
        'title':title



    }

    table = 'jiadian'
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
    update = ', '.join([" {key} = %s".format(key=key) for key in data])
    sql += update



    try:
        if cursor.execute(sql, tuple(data.values())*2):
            print('successful')
            db.commit()
    except:
        print('Failed')
        db.rollback()

db.close()
