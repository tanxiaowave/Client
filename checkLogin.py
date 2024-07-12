import time
import os
import rsa
import json
from DrissionPage import ChromiumOptions, ChromiumPage
import time
import pymssql
import requests
import configparser
import base64
import requests,json
from DrissionPage.common import Actions
import imaplib
import email
from email.header import decode_header
import re

reader = configparser.ConfigParser()
reader.read("settings.INI")
server = reader.get("Database", "server")
user = reader.get("Database", "user")
sql_password = reader.get("Database", "password")
database = reader.get("Database", "database")
commission = float(reader.get("Commission", "hungrypanda"))
merch_id = reader.get("Store", "merchid")
branch_id = reader.get("Store", "branchid")
user_id = reader.get("Store", "userid")
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
    #     with open("panda_username_info.txt", "rb") as f:
    #         username = f.readline().decode('utf-8')
    #         f.close()
    #     with open("panda_password_info.txt", "rb") as f:
    #         password = f.readline().decode('utf-8')
    #         f.close()
    #     co = ChromiumOptions().set_local_port(9113)
    #     # 用 d 模式创建页面对象（默认模式）
    #     page = ChromiumPage(co)
    #     time.sleep(5)
    #     page.get('https://merchant-uk.hungrypanda.co/login')
    #     time.sleep(3)
    #     try:
    #         if page.url != "https://merchant-uk.hungrypanda.co/goods/list":
    #             print(page.url)
    #             page.ele('#phone').clear()
    #             time.sleep(2)
    #             page.ele('#password').clear()
    #             page.ele('#phone').input(username)
    #             time.sleep(12)
    #             page.ele('#password').input(password)
    #             time.sleep(12)
    #             page.ele('.ant-btn ant-btn-primary ant-btn-lg ant-btn-block').click()
    #             time.sleep(30)
    #             if page.address == "https://merchant-uk.hungrypanda.co/order/ordermanage":
    #                 print("登录成功")
    #                 panda = True
    #                 # page.quit()
    #             else:
    #                 print("登录失败")
    #                 panda = False
    #                 # page.quit()
    #         else:
    #             time.sleep(15)
    #             page.get('https://merchant-uk.hungrypanda.co/order/ordermanage')
    #             print("登录成功")
    #             panda = True
    #             # page.quit()
    #             # return True
    #     except:
    #         print("HungryPanda is not valid, \n please log your \nHungryPanda info again.")
    #         panda = False


        # driver.get("https://merchant-uk.hungrypanda.co/order/ordermanage")
        # time.sleep(2)
        # if driver.current_url != 'https://merchant-uk.hungrypanda.co/order/ordermanage':
        #     driver.get("https://merchant-uk.hungrypanda.co/login")
        #     time.sleep(1)
        #     # 写死的rsa钥
        #     pri = rsa.PrivateKey(
        #         10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
        #         65537,
        #         7002712700928804011838917939227853273317722595990151016778949911089213823265260722795698382337717248876309656289331967090125041513510782458343001103454593,
        #         7165380796988618938065214954530466870443807483684172787495616047866899293086811303,
        #         1492014128088262667286826329565602575995354986910798283007464819843657741)
        #     try:
        #         with open("panda_username_info.txt", "rb") as f:
        #             username = f.readline()
        #             f.close()
        #         with open("panda_password_info.txt", "rb") as f:
        #             password = f.readline()
        #             f.close()
        #         # 用密钥解密账号密码文件
        #         username = rsa.decrypt(username, pri).decode('utf-8')
        #         password = rsa.decrypt(password, pri).decode('utf-8')
        #         # 找到账号密码元素，填入账号密码
        #         u = driver.find_element('id', 'phone')
        #         u.send_keys(username)
        #         p = driver.find_element('id', 'password')
        #         p.send_keys(password)
        #         # 找到登录按钮，点击登录
        #         btn = driver.find_element('xpath', '//*[@id="root"]/div/div/div/div/div/div/div/form/div[5]/div/div/div/button')
        #         btn.click()
        #         time.sleep(1)
        #         # 睡眠一秒后检查是否还在登录界面，还在登录界面说明登陆失败，登陆状态返回false
        #         if driver.current_url == "https://merchant-uk.hungrypanda.co/login":
        #             panda = False
        #         else:
        #             panda = True
        #     except:
        #         panda = False
        # else:
        #     panda = True

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

def checklogin_hun(hun):

    panda = False
    if hun:
        print("子程序已运行")
        with open("panda_username_info.txt", "rb") as f:
            username = f.readline().decode('utf-8')
            f.close()
        with open("panda_password_info.txt", "rb") as f:
            password = f.readline().decode('utf-8')
            f.close()
        co = ChromiumOptions().set_local_port(9113)
        # 用 d 模式创建页面对象（默认模式）
        page = ChromiumPage(co)
        ac = Actions(page)

        def img_download():

            img = page('.^geetest_bg')
            img.get_screenshot(path='tmp', name='pic.png')

        def img_data():

            url = "https://api.jfbym.com/api/YmServer/customApi"

            with open(r'.\tmp\pic.png', 'rb') as f:
                im = base64.b64encode(f.read()).decode()

            data = {
                "token": "PvnOdYXAPcAspNnvqSBIPugniFrpnjCchn0WyohgZTU",  # 输入自己的token
                "type": "22222",
                "image": im,  # 待识别图的base64

            }

            _headers = {
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=_headers, json=data)
            if response.status_code == 200:
                # Extract JSON data from the response
                response_data = response.json()

                # Access 'data' field from the JSON response
                data_value = response_data['data']['data']
                print(response_data)
                # Now you can work with 'data_value'
                print(data_value)
                return data_value
            else:
                print(f"Request failed with status code {response.status_code}")


                def ac_hold():
                    img_download()
                    data_value = img_data()
                    ac.hold('.^geetest_arrow')
                    # 向右移动鼠标300像素
                    ac.right(int(data_value) - 92)
                    # 释放左键
                    time.sleep(3)
                    ac.release()
                    # time.sleep(2)
                    # 获取邮件验证码

                def getmail():
                    time.sleep(60)
                    t = 0
                    email_password = "007"
                    user_email = "sgzz1v7f1g7t@9m9.fun"
                    # 搜索邮件

                    mail = imaplib.IMAP4_SSL("9m9.fun")
                    try:
                        mail.login(user_email, email_password)
                        mail.select("inbox")

                        status, messages = mail.search(None, "ALL")
                        last_msg_id = messages[0].split()[-1]
                        # 获取邮件
                        _, msg_data = mail.fetch(last_msg_id, "(RFC822)")
                        raw_email = msg_data[0][1]

                        msg = email.message_from_bytes(raw_email)

                        # 获取邮件时间
                        # 获取邮件的时间
                        # date_str = msg["Date"].replace("(UTC)", "").strip()
                        # date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
                        # t0 = date_obj.timestamp()
                        # if t0 < t:
                        #     print("没有最新邮件")
                        #     # return None
                        # 获取主题
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            subject = subject.decode(encoding if encoding else "utf-8")

                        # if subject != "HP SMS Verify":
                        #     # return None

                        # 获取邮件正文
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                if part.get_content_type() == "text/plain":
                                    body = part.get_payload(decode=True).decode("utf-8")
                                elif part.get_content_type() == "text/html":
                                    # 如果存在HTML格式的正文，你也可以解析HTML
                                    body = part.get_payload(decode=True).decode("utf-8")
                        else:
                            body = msg.get_payload(decode=True).decode("utf-8")

                        if body:
                            pattern = r'Your verification code: (\d+)'
                            match = re.search(pattern, body)

                            if match:
                                yzm = match.group(1)
                                # print(f"验证码：{yzm}")
                                return yzm
                            else:
                                print("获取验证码失败。")
                    except Exception as e:
                        print(e)

                    finally:
                        # 关闭连接
                        mail.logout()

        # time.sleep(5)
        page.get('https://merchant-uk.hungrypanda.co/login')
        time.sleep(8)
        try:
            # if page.url != "https://merchant-uk.hungrypanda.co/goods/list":
            print(page.url)
            if page.url == "https://merchant-uk.hungrypanda.co/login":
                page.ele('#phone').clear()
                time.sleep(2)
                page.ele('#password').clear()
                page.ele('#phone').input(username)
                time.sleep(12)
                page.ele('#password').input(password)
                time.sleep(12)
                page.ele('.ant-btn ant-btn-primary ant-btn-lg ant-btn-block').click()
                time.sleep(15)
                if page.url != "https://merchant-uk.hungrypanda.co/goods/list":
                    ac_hold()
                    time.sleep(15)
                    yzmstr = getmail()
                    page.ele('.ant-input ant-input-borderless').input(yzmstr)
                    time.sleep(3)
            else:
                time.sleep(15)
                page.get('https://merchant-uk.hungrypanda.co/order/ordermanage')
                print("登录成功")
                # rs = page.run_js('return localStorage.getItem("LOCALSTORE_USERINFOTABLE") ')
                # if rs:
                #     ss = json.loads(rs)
                #     token = ss["token"]
                #     print(token)
                # page.quit()
                return panda
        except:
            print("HungryPanda is not valid, \n please log your \nHungryPanda info again.")
            return False
            print("子程序已运行4")

