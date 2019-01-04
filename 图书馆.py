import requests,re,hashlib
from bs4 import BeautifulSoup


def md5(s):
    '''
    md5 加密函数
    :param s:
    :return:
    '''
    s = str(s)
    return hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()

def get_info(card,password):
    headers = {
        'Referer': 'http://221.238.90.11/opac/reader/space',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Host': '221.238.90.11'
    }
    url = 'http://221.238.90.11/opac/reader/login'
    post_url = 'http://221.238.90.11/opac/reader/doLogin'
    space_url = 'http://221.238.90.11/opac/reader/space'
    response = requests.get(url=url, headers=headers)

    v2ex_session = requests.Session()
    f = v2ex_session.get(url, headers=headers)

    postData = {
        'rdid': card,
        'rdPasswd': password,
        'returnUrl': '',
        'password': ''
    }

    f = v2ex_session.post(post_url,
                          data=postData,
                          headers=headers)

    f = v2ex_session.get(url=space_url, headers=headers)

    response = f

    if '读者空间提示' in response.text:
        print('success')
    else:
        print('fail')
    wbdata = response.text
    soup = BeautifulSoup(wbdata, 'lxml')
    tiaoma = soup.find_all('td', {'width': '80'})  # 条码
    book_name = soup.find_all('a', {'target': '_blank'})  # 书名
    author = soup.find_all('td', {'width': '140'})  # 作者
    book_num = soup.find_all('td', {'width': '60'})  # 索书号
    address = soup.find_all('td', {'width': '120'})  # 馆藏地点
    type = soup.find_all('td', {'width': '100'})  # 文献类型
    lent_time = soup.find_all('td', {'width': '90'})  # 借出时间,归还时间
    name = soup.find_all('font', {'class': 'space_font'})
    reader_num = name[0].text  # 卡号
    reader_name = name[1].text  # 读者姓名
    reader_location = name[3].text  # 所属图书馆
    reder_lent = name[9].text  # 已借可借
    print(reader_num, reader_name, reader_location, reder_lent)

    total = len(tiaoma)
    for i in range(total):
        print(tiaoma[i].text, book_name[i].text, author[i].text, book_num[i].text, address[i].text, type[i].text,
              lent_time[i * 2].text, lent_time[i * 2 + 1].text,end='')
l = ['0015565','t0013896','t0013798','t0018776','t0013797'] #图书馆卡号
for i in l:
    card = i.upper()
    password = md5(str(i[-6:]))
    get_info(card=card,password=password)









