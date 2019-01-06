from flask import Flask
import requests, re, hashlib
from bs4 import BeautifulSoup
import library_login

l = ['taea0015565', 'taea0013896', 'taea0013798', 'taea0018776', 'taea0013797']  # 空港图书馆卡号
lit = ''
for i in l:

    card = i.upper()
    password = library_login.md5(str(i[-6:]))

    a,b = library_login.get_info(card=card, password=password)

    lit = lit + a + '\n' + b + '\n'

lit = lit.replace('\n','<br/>').replace('(','').replace(')','').replace("'","").replace(',','&nbsp;')





app = Flask(__name__)

@app.route('/')
def index():

    return lit



if __name__ == '__main__':
    app.run(port = 8000,debug = True)