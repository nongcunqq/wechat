import requests,json
import time

url = 'http://open.yto.net.cn/open-platform/debug/apis/258'
url = 'https://mec.yto.net.cn/api/waybillinfo?traceItemRequest=YT9087503464824'

headers_yto = {'Accept': 'application/json, text/plain, */*', 'Accept-Encoding': 'gzip, deflate', 'Accept-Language': 'zh-CN,zh;q=0.9', 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJub25nY3VucXEiLCJpYXQiOjE1Nzg2NDIxMzgsImV4cCI6MTU3OTI0NjkzOH0.zCPQPQsExt_izBj3I6y-xXHH3GfYPvTsFXLTLjXNHSk', 'Cache-Control': 'no-cache', 'Connection': 'keep-alive', 'Content-Length': '81', 'Content-Type': 'application/x-www-form-urlencoded', 'Cookie': 'UM_distinctid=16f8e5794a94c4-03f8e43910a36a-39627c0f-13c680-16f8e5794aa618; CNZZDATA1277696611=1812010662-1578635823-null%7C1578641276; opp-token=Bearer%20eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJub25nY3VucXEiLCJpYXQiOjE1Nzg2NDIxMzgsImV4cCI6MTU3OTI0NjkzOH0.zCPQPQsExt_izBj3I6y-xXHH3GfYPvTsFXLTLjXNHSk; opp-token-expires=1578642139370', 'Host': 'open.yto.net.cn', 'Origin': 'http://open.yto.net.cn', 'Pragma': 'no-cache', 'Referer': 'http://open.yto.net.cn/linkInterFace/onlineApiTesting', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'}
headers_zto = {'Host': 'hdgateway.zto.com', 'Content-Type': 'application/json;charset=UTF-8', 'Origin': 'https://newm.zto.com', 'Accept-Encoding': 'br, gzip, deflate', 'Connection': 'keep-alive', 'Accept': 'application/json, text/plain, */*', 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79ztoIos', 'Referer': 'https://newm.zto.com/Waybill/Detail?id=78118941001359&loginOut=ztoExpressClient', 'Content-Length': '29', 'Accept-Language': 'zh-cn'}
headers_sf = {'Host': 'ccsp-egmas.sf-express.com', 'Cookie': 'SERVERID=web2', 'User-Agent': 'SFMainland_Store_Pro/9.9.0 (iPhone; iOS 11.4; Scale/3.00)', 'languageCode': 'sc', 'clientVersion': '9.9.0', 'mediaCode': 'iOSML', 'systemVersion': '11.4', 'regionCode': 'CN', 'jsbundle': '2267612ddd416ba6990466b9a4e2dfc1', 'Content-Length': '117', 'deviceId': '3BB525E8-814A-4E0B-B8D5-66C429109F3B', 'Connection': 'keep-alive', 'sytToken': '51dfd37b524e20a6b25f2a0cde5a1985', 'carrier': '', 'Accept-Language': 'zh-Hans-CN;q=1', 'model': 'iPhone 6S Plus', 'Accept': '*/*', 'Content-Type': 'application/json', 'Accept-Encoding': 'br, gzip, deflate', 'timeInterval': '1578648095334', 'screenSize': '1242x2208'}
headers_sto = {'Host': 'appsys.sto.cn', 'mac': '02:00:00:00:00:00', 'Accept': '*/*', 'timestamp': '1578649114543', 'nonce': '14dcb254-9576-4d8b-8ef9-b5f02f691ecd', 'appVersion': 'V4.1.3', 'source': 'kdzs', 'Accept-Language': 'zh-Hans-CN;q=1', 'Accept-Encoding': 'br, gzip, deflate', 'tokenId': '', 'signature': '837dbc5920dffceaa2f86ab51781bd26', 'clientType': 'iOS', 'User-Agent': 'STOExpressDelivery/4.1.3 (iPhone; iOS 11.4; Scale/3.00)', 'Connection': 'keep-alive', 'appId': 'app_ios'}

# data = {
#     'app_key': 'sF1Jzn',
#     'user_id': 'YTOTEST',
#     'Secret_Key': '1QLlIZ',
#     'waybillno': 'YT9087503464824',
#     'format': 'JSON'}
#
# response = requests.post(url=url, data=data, headers=headers)
#
# print(response)
# print(json.loads(response.text))

# 查询圆通快递信息
def get_yto_info(num):
    num = str(num)
    url = 'https://mec.yto.net.cn/api/waybillinfo?traceItemRequest={}'.format(num)
    wbdata = requests.get(url)
    print(wbdata)
    while not wbdata.status_code == 200:
        time.sleep(1)
        url = 'https://mec.yto.net.cn/api/waybillinfo?traceItemRequest={}'.format(num)
        wbdata = requests.get(url)
        print('返回码',wbdata)
    else:
        info = json.loads(wbdata.text)
        num = info[0].get('waybillNo')

        print('订单号', num, '\n')
        for i in info[0].get("waybillProcessInfo"):
            upload_time = i.get('waybillProcessInfo').get('upload_Time')
            process_info = i.get('waybillProcessInfo').get('processInfo')

            # print(upload_time)
            # print(process_info.strip(), '\n')

# 查询 中通快递信息
def get_zto_info(num):
    url = 'https://hdgateway.zto.com/WayBill_GetDetail'
    num = str(num)
    data = {"billCode":num}
    wbdata = requests.post(url=url, data=data)
    print(wbdata)
    info = json.loads(wbdata.text)
    print(info)
    while not wbdata.status_code == 200:
        time.sleep(1)
        data = {"billCode": num}
        wbdata = requests.post(url=url, data=data)
        info = json.loads(wbdata.text)
    else:
        messages = info.get('result').get('logisticsRecord')
        print(messages)
        for message in messages:
            for item in message:
                print(item.get('scanDate'))
                print(item.get('stateDescription'),'\n')

# 查询申通快递信息
def get_sto_info(num):
    num = str(num)
    url = 'https://appsys.sto.cn/face-kdzs/logisticsTrack?billcode={}'.format(num)
    wbdata = requests.get(url, headers=headers_sto)
    print(wbdata)
    while not wbdata.status_code==200:
        time.sleep(1)
        wbdata = requests.get(url, headers=headers_sto)
    else:
        info = json.loads(wbdata.text)
        print(info)









# 查询顺丰快递信息 有动态token, 暂时搁置
def get_sf_info(num):
    url = 'https://ccsp-egmas.sf-express.com/cx-app-query/query/app/waybillNo/queryWaybillByBNo'
    data = {
	"isHtml": "",
	"clientCode": "18053138878",
	"userId": "5CD69222DDBC45D7B5DF487FC51DBC19",
	"wayBillNos": "SF1015130242451"}

    wbdata = requests.post(url=url, data=data, headers=headers_sf)
    print(wbdata)
    print(json.loads(wbdata.text))




start = time.time()

# 测试 20 次查询所需时间, 圆通 5 秒左右, 中通 3 秒
# for i in range(20):
#     num = '78118941001359'
#
#     get_zto_info(num)

num = 777006771712031
get_sto_info(num)




end = time.time()

print(end-start)

