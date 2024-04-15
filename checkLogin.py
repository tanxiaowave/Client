from selenium import webdriver
import time
import os
import rsa
import json
import requests
import configparser

reader = configparser.ConfigParser()
reader.read("settings.INI")
headless_flag = reader.get("Flag", "headless_flag")

def checklogin(hun, ub, de, fan):
    uber, panda, deliveroo, fantuan = False, False, False, False
    # options = webdriver.ChromeOptions()
    # # 如果通道开通了，检查该通道登陆状态
    # if ub:
    #     # 只有uber需要加之前保存的登录状态
    #     options.add_argument(f'user-data-dir={os.getcwd()}/selenium')
    # # if headless_flag = false, selenium activity will be visible
    # if headless_flag == 'True':
    #     options.add_argument('--headless')
    #     options.add_argument('--no-sandbox')
    # options.add_argument("--proxy-server='direct://'")
    # options.add_argument("--proxy-bypass-list=*")
    # options.add_argument("--log-level=3")
    # options.add_argument("--silent")
    # driver = webdriver.Chrome('chromedriver', options=options)
    #
    # if ub:
    #     driver.get("https://merchants.ubereats.com/manager/orders")
    #     # uber如果没登陆，会跳转到登录页面，url就不会是下面这个
    #     if driver.current_url != "https://merchants.ubereats.com/manager/orders":
    #         uber = False
    #     else:
    #         uber = True

    if ub:
        uber = True


    # if hun:
    #     driver.get("https://merchant-uk.hungrypanda.co/order/ordermanage")
    #     time.sleep(2)
    #     if driver.current_url != 'https://merchant-uk.hungrypanda.co/order/ordermanage':
    #         driver.get("https://merchant-uk.hungrypanda.co/login")
    #         time.sleep(1)
    #         # 写死的rsa钥
    #         pri = rsa.PrivateKey(
    #             10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
    #             65537,
    #             7002712700928804011838917939227853273317722595990151016778949911089213823265260722795698382337717248876309656289331967090125041513510782458343001103454593,
    #             7165380796988618938065214954530466870443807483684172787495616047866899293086811303,
    #             1492014128088262667286826329565602575995354986910798283007464819843657741)
    #         try:
    #             with open("panda_username_info.txt", "rb") as f:
    #                 username = f.readline()
    #                 f.close()
    #             with open("panda_password_info.txt", "rb") as f:
    #                 password = f.readline()
    #                 f.close()
    #             # 用密钥解密账号密码文件
    #             username = rsa.decrypt(username, pri).decode('utf-8')
    #             password = rsa.decrypt(password, pri).decode('utf-8')
    #             # 找到账号密码元素，填入账号密码
    #             u = driver.find_element('id', 'phone')
    #             u.send_keys(username)
    #             p = driver.find_element('id', 'password')
    #             p.send_keys(password)
    #             # 找到登录按钮，点击登录
    #             btn = driver.find_element('xpath', '//*[@id="root"]/div/div/div/div/div/div/div/form/div[5]/div/div/div/button')
    #             btn.click()
    #             time.sleep(1)
    #             # 睡眠一秒后检查是否还在登录界面，还在登录界面说明登陆失败，登陆状态返回false
    #             if driver.current_url == "https://merchant-uk.hungrypanda.co/login":
    #                 panda = False
    #             else:
    #                 panda = True
    #         except:
    #             panda = False
    #     else:
    #         panda = True

    # if de:
    #     driver.get("https://restaurant-hub.deliveroo.net/live-orders")
    #     time.sleep(1)
    #     if driver.current_url == 'https://restaurant-hub.deliveroo.net/login?redirect=/live-orders':
    #         pri = rsa.PrivateKey(
    #             10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
    #             65537,
    #             7002712700928804011838917939227853273317722595990151016778949911089213823265260722795698382337717248876309656289331967090125041513510782458343001103454593,
    #             7165380796988618938065214954530466870443807483684172787495616047866899293086811303,
    #             1492014128088262667286826329565602575995354986910798283007464819843657741)
    #         try:
    #             with open("deliveroo_username_info.txt", "rb") as f:
    #                 username = f.readline()
    #                 f.close()
    #             with open("deliveroo_password_info.txt", "rb") as f:
    #                 password = f.readline()
    #                 f.close()
    #             username = rsa.decrypt(username, pri).decode('utf-8')
    #             password = rsa.decrypt(password, pri).decode('utf-8')
    #             try:
    #                 cookie_btn = driver.find_element('xpath', "//*[@id='onetrust-accept-btn-handler']")
    #                 cookie_btn.click()
    #             except:
    #                 pass
    #             u = driver.find_element('xpath', '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/label[1]/span/div/input')
    #             u.send_keys(username)
    #             p = driver.find_element('xpath', '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/label[2]/span/div/input')
    #             p.send_keys(password)
    #             btn = driver.find_element('xpath', '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/button')
    #             btn.click()
    #             time.sleep(2)
    #             if driver.current_url == 'https://restaurant-hub.deliveroo.net/login?redirect=/live-orders':
    #                 deliveroo = False
    #             else:
    #                 deliveroo = True
    #         except Exception as e:
    #             deliveroo = False
    #     else:
    #         deliveroo = True

    # deliveroo用API了不用检查登陆
    if de:
        deliveroo = True

    # if fan:
    #     pri = rsa.PrivateKey(
    #         10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
    #         65537,
    #         7002712700928804011838917939227853273317722595990151016778949911089213823265260722795698382337717248876309656289331967090125041513510782458343001103454593,
    #         7165380796988618938065214954530466870443807483684172787495616047866899293086811303,
    #         1492014128088262667286826329565602575995354986910798283007464819843657741)
    #     try:
    #         with open("fantuan_appkey.txt", "rb") as f:
    #             username = f.readline()
    #             f.close()
    #         with open("fantuan_shopid.txt", "rb") as f:
    #             password = f.readline()
    #             f.close()
    #         appkey = rsa.decrypt(username, pri).decode('utf-8')
    #         shop_id = rsa.decrypt(password, pri).decode('utf-8')
    #         headers = {
    #             "Content-Type": "application/json",
    #             "appKey": appkey,
    #             "timestamp": "{{$timestamp}}",
    #         }
    #         data = {
    #             "shopId": shop_id,
    #             "page": {
    #                 "pageNum": 1,
    #                 "pageSize": 5
    #             }
    #         }
    #         url = "https://openapi.fantuan.ca/api/v1/order/page"
    #         response = json.loads(requests.post(url, json=data, headers=headers).text)
    #         if response['msg'] == 'Invalid AppKey!':
    #             fantuan = False
    #         if response['code'] == 0:
    #             fantuan = True
    #     except:
    #         fantuan = False

    # 饭团用API了不用检查登陆
    if fan:
        fantuan = True

    return panda, uber, deliveroo, fantuan