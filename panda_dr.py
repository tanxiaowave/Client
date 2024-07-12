from DrissionPage import ChromiumOptions,ChromiumPage
from DrissionPage import SessionPage, SessionOptions
import time
import pymssql
import requests
import configparser
import json
import logging
import base64
import requests,json
from DrissionPage.common import Actions
import imaplib
import email
from email.header import decode_header
import re
import winsound


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

# def dura_fre():#定义蜂鸣
#     # 初始化 pygame
#     pygame.init()
#
#     # 设置蜂鸣声音频率和持续时间
#     frequency = 1000  # Hz
#     duration = 500  # 毫秒
#
#     # 发出蜂鸣声
#     pygame.mixer.Sound(frequency, duration)

def initial_panda():
    print("子程序已运行")
    with open("panda_username_info.txt", "rb") as f:
        username = f.readline().decode('utf-8')
        f.close()
    with open("panda_password_info.txt", "rb") as f:
        password = f.readline().decode('utf-8')
        f.close()
    co = ChromiumOptions().set_local_port(9113)
    # co = ChromiumOptions().arguments("--disable-background-timer-throttling")
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
        ac.right(int(data_value)-92)
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

    # time.sleep(2)
    page.get('https://merchant-uk.hungrypanda.co/login')
    time.sleep(1)
    try:
        if page.url != "https://merchant-uk.hungrypanda.co/goods/list":
            print(page.url)
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
                # if page.address == "https://merchant-uk.hungrypanda.co/order/ordermanage":
                #     print("登录成功")
                #     rs = page.run_js('return localStorage.getItem("LOCALSTORE_USERINFOTABLE") ')
                #     if rs:
                #         ss = json.loads(rs)
                #         token = ss["token"]
                #         print(token)
                #     # page.quit()
                # else:
                #     print("登录失败")
                #     # page.quit()
            else:
                time.sleep(8)
                page.get('https://merchant-uk.hungrypanda.co/order/ordermanage')
                print("登录成功")
                rs = page.run_js('return localStorage.getItem("LOCALSTORE_USERINFOTABLE") ')
                if rs:
                    ss = json.loads(rs)
                    token = ss["token"]
                    print(token)
                # page.quit()
                return True
    except:
        print("HungryPanda is not valid, \n please log your \nHungryPanda info again.")
        return False
        print("子程序已运行4")
def panda_drAPI():

    class Log:
        Enable = True
        LogName = "RBL"
        DateFormat = "%Y-%m-%d %H:%M:%S"
        Format = "%(asctime)s - %(levelname)s - %(threadName)s - %(filename)s - %(lineno)d -> %(message)s"

        FileEnable = True
        # Path = "./log/{int(time.time())}-runtime.log"
        Path = f"./log/{int(time.time())}-runtime.log"
        ClearFile = True
        FileLevel = "DEBUG"

        ConsoleEnable = True
        ConsoleLevel = "DEBUG"




    def get_logger(name=None):
        if not Log.Enable:
            return None

        if not name:
            name = __name__

        logger = logging.getLogger(name)
        logger.setLevel(Log.ConsoleLevel)
        formatter = logging.Formatter(fmt=Log.Format, datefmt=Log.DateFormat)

        # 输出到控制台
        if Log.ConsoleEnable:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(level=Log.ConsoleLevel)
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        # 输出到文件
        if Log.Enable:
            # 先清空日志文件
            if Log.ClearFile:
                with open(Log.Path, "a+", encoding="utf-8") as f:
                    f.truncate(0)
            file_handler = logging.FileHandler(Log.Path, encoding="utf-8")
            file_handler.setLevel(level=Log.FileLevel)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    Logger = get_logger(Log.LogName)

    with open("panda_username_info.txt", "rb") as f:
        username = f.readline().decode('utf-8')
        f.close()
    with open("panda_password_info.txt", "rb") as f:
        password = f.readline().decode('utf-8')
        f.close()

    try:
        database_flag = eval(reader.get("Database", "flag"))
    except:
        database_flag = True

    co = ChromiumOptions().set_local_port(9113)
    co.set_argument('--disable-background-timer-throttling')
    # 用 d 模式创建页面对象（默认模式）
    if headless_flag == "True":
        co = ChromiumOptions().headless()
        page = ChromiumPage(co)
        # page.quit()
    else:
        page = ChromiumPage(co)

    time.sleep(3)
    url = f'https://merchant-uk.hungrypanda.co/goods/list'
    page.get(url)
    time.sleep(30)
    try:
        if page.url != "https://merchant-uk.hungrypanda.co/goods/list":
            print("密码失败")
            print(page.url)
            page.ele('#phone').clear()
            page.ele('#password').clear()
            # print("syy")
            page.ele('#phone').input(username)
            time.sleep(8)
            page.ele('#password').input(password)
            time.sleep(8)
            page.ele('.ant-btn ant-btn-primary ant-btn-lg ant-btn-block').click()
            # print("syy1")

        else:
            page.get('https://merchant-uk.hungrypanda.co/order/ordermanage')
            print("登录成功")
            time.sleep(3)
    except:
        print("HungryPanda is not valid, \n please log your \nHungryPanda info again.")

    time.sleep(5)
    # page.set.window.size(2, 2)
    while True:
        # page.scroll.to_bottom()
        # page.reconnect()
        # page.get('https://merchant-uk.hungrypanda.co/order/ordermanage', retry=3, interval=2, timeout=1.5)
        # time.sleep(5)
        for n in range(3):
            try:
                page.ele('.ant-menu-title-content').click()
                break
            except Exception as e:
                Logger.error(e)
                print("断开5")
                page.reconnect()
                time.sleep(15)


        # 读取旧订单
        try:
            with open("hungrypanda_lastorder.txt", 'r+') as f:
                old_orders = f.readlines()
            for i in range(len(old_orders)):
                old_orders[i] = old_orders[i].replace("\n", "")
            f.close()
        except:
            old_orders = []
            f = open('hungrypanda_lastorder.txt', 'w')
            f.close()
            print("断开4")
            page.reconnect()


        try:
            for i in range(1, 11):
                for j in range(3):
                    try:
                        order_id=page.ele('xpath=//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr['+str(i)+']/td[1]').text
                        status_id=page.ele('xpath=//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr['+str(i)+']/td[5]').text
                        break
                    except Exception as e:
                        Logger.error(e)
                        print("断开6")
                        page.reconnect()
                        time.sleep(5)

                # Logger.debug(order_id)
                # Logger.debug(status_id)
                print(order_id,status_id)
                time.sleep(1)
                if order_id not in old_orders:
                    vbtn= page.ele('xpath=//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr['+str(i)+']/td[6]/a')
                    Logger.debug(vbtn.text)
                    # // *[ @ id = "root"] / div / div[2] / div / div / div[2] / div / div[2] / div[2] / div / div / div / div / div / div / table / tbody / tr[1] / td[6] / a
                    vbtn.click()
                    time.sleep(1)
                    divs = page.eles('.goods-detail')
                    Logger.debug(divs)
                    items = []
                    total_amount = 0
                    k = 0
                    for div in divs:
                        try:
                            # time.sleep(3)
                            product_name = div.ele('.product-name').text
                            # 定位方括号的位置
                            start_index = product_name.find("[")
                            end_index = product_name.find("]")
                        except Exception as e:
                            Logger.error(e)
                            time.sleep(4)
                            page.reconnect()

                        # 如果找到方括号，则提取方括号内的内容（字母部分）
                        # time.sleep(4)
                        if start_index != -1 and end_index != -1:
                            menu_id = product_name[start_index + 1: end_index]
                            try:
                                if database_flag == True:
                                    connect = pymssql.connect(server=server, user=user, password=sql_password, database=database,
                                                              login_timeout=5,tds_version='7.0')
                                    cur = connect.cursor()
                                    sql = f'select MenuName from mn_Menu where MenuID={menu_id}'
                                    cur.execute(sql)
                                    sql_result = cur.fetchall()
                                    menu_name = ""
                                    menu_name = sql_result[0][0].encode('latin-1').decode('gbk')
                                else:
                                    with open(f"{branch_id}.txt", "r+") as f:
                                        d = f.read()
                                        f.close()
                                    result = json.loads(d)
                                    menu_name = result.get(str(menu_id))
                            except:
                                print('sql connection failed...')
                                menu_id = "1990"
                                menu_name = product_name
                                # page.reconnect()


                        else:
                            # menust_id = int(menu_id) if menu_id.isdigit() else 1990  # 如果 menu_id 不是数字，则初始值为 1990
                            menu_id = 1990
                            print(menu_id)
                            # chinese_chars_str = ''.join(chinese_chars)
                            additional_string = "-G"
                            result_str = product_name + additional_string
                            menu_name = result_str
                            if database_flag == True:
                                connect = pymssql.connect(server=server, user=user, password=sql_password,
                                                          database=database,
                                                          login_timeout=5, tds_version='7.0')
                                cur = connect.cursor()
                                sql = 'UPDATE mn_Menu SET MenuName = %s WHERE MenuID = %s'
                                cur.execute(sql, (menu_name, menu_id))

                                # 更新操作执行成功，提交事务
                                connect.commit()

                                # 关闭游标和数据库连接
                                cur.close()
                                connect.close()

                        for n in range(3):
                                menucountstr = div.ele('.product-count').text
                                menucount = int(menucountstr.replace('*', ''))
                                menupricestr = div.ele('.product-price').text
                                menuprice = float(menupricestr.replace('£', ''))
                                # 播放系统默认蜂鸣声音（持续 500 毫秒）
                                winsound.Beep(1000, 1200)
                                # menuamtstr = page.ele('xpath=/html/body/div[2]/div/div[2]/div/div[2]/div[2]/div/div[4]/div[1]/div[2]').text
                                # try:
                                #     menuamtstr = page.ele('.ant-collapse-extra').text
                                #     # if not menuamtstr:  # Check if menuamtstr is empty or evaluates to False
                                #
                                # except Exception as e:
                                #     Logger.error(e)
                                #     menuamtstr = page.ele('.count').text
                                #     time.sleep(5)
                                Logger.debug(menu_id)
                                Logger.debug(menu_name)
                                print(menucountstr)
                                Logger.debug(menucount)
                                print(menupricestr)
                                Logger.debug(menuprice)
                                # print(menuamtstr)
                                break

                        # menuamt = float(menuamtstr.replace('£', ''))
                        try:
                            total_amount += menuprice
                            menu_id = str(menu_id)
                            item = {
                                "ParentID": "SP1010",  # 随便，但不能为空
                                "MenuID": menu_id,
                                "MenuName": menu_name,
                                "MenuUnit": ".",
                                "MenuPrice": menuprice/menucount,
                                "MenuPriceOld": menuprice/menucount,
                                "MenuQty": menucount,
                                "MenuAmt": menuprice,
                                "MenuService": 0,
                                "SumOfService": 0,
                                "CookList": [],
                                "MenuList": []
                            }
                            # items.append(item)

                            rs = page.run_js('return localStorage.getItem("LOCALSTORE_USERINFOTABLE") ')
                            if rs:
                                ss = json.loads(rs)
                                token = ss["token"]
                                print(token)
                            # #
                            # # page1 = SessionPage()
                            # #
                            # # cookies = {
                            # #     'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%221904045081412-0ca68084712dcd-26021e51-786432-190404508151e4%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221904045081412-0ca68084712dcd-26021e51-786432-190404508151e4%22%7D',
                            # #     '_cfuvid': 'mnXRCp_Ay_V.fYPa.BUxtwq3CmAB1v9wO3gRUrNF4OY-1720081668902-0.0.1.1-604800000',
                            # #     '__cf_bm': 'gpR0R7j8dsXq6xemnRN5bIs8U5ijg8f6xna7V9hoZhc-1720083156-1.0.1.1-3ixrKtvjyLOdIoEhojCdW7d2TA_dvmWfxAmkOumMAq.kpa.1RtCeJ1PZflAyjgEw83f1cNo7gmAR35VX.1RZsg',
                            # # }
                            # #
                            # # params = {
                            # #     'project': 'production',
                            # #     'data': 'eyJkaXN0aW5jdF9pZCI6IjE5MDQwNDUwODE0MTItMGNhNjgwODQ3MTJkY2QtMjYwMjFlNTEtNzg2NDMyLTE5MDQwNDUwODE1MWU0IiwibGliIjp7IiRsaWIiOiJqcyIsIiRsaWJfbWV0aG9kIjoiY29kZSIsIiRsaWJfdmVyc2lvbiI6IjEuMTUuMjcifSwicHJvcGVydGllcyI6eyIkdGltZXpvbmVfb2Zmc2V0IjotNjAsIiRzY3JlZW5faGVpZ2h0Ijo3NjgsIiRzY3JlZW5fd2lkdGgiOjEwMjQsIiRsaWIiOiJqcyIsIiRsaWJfdmVyc2lvbiI6IjEuMTUuMjciLCIkbGF0ZXN0X3RyYWZmaWNfc291cmNlX3R5cGUiOiLnm7TmjqXmtYHph48iLCIkbGF0ZXN0X3NlYXJjaF9rZXl3b3JkIjoi5pyq5Y+W5Yiw5YC8X+ebtOaOpeaJk+W8gCIsIiRsYXRlc3RfcmVmZXJyZXIiOiIiLCJwcm9kdWN0X2lkIjo0LCJwbGF0Zm9ybV9pZCI6MywiY291bnRyeV9uYW1lIjoi6Iux5Zu9IiwiY2l0eV9uYW1lIjoiIiwic3lzdGVtX2xhbmd1YWdlIjoiQ04iLCJhcHBfbGFuZ3VhZ2UiOiJDTiIsIiRlbGVtZW50X3R5cGUiOiJhIiwiJGVsZW1lbnRfY2xhc3NfbmFtZSI6IiIsIiRlbGVtZW50X2NvbnRlbnQiOiJWaWV3IiwiJHVybCI6Imh0dHBzOi8vbWVyY2hhbnQtdWsuaHVuZ3J5cGFuZGEuY28vb3JkZXIvb3JkZXJtYW5hZ2UiLCIkdXJsX3BhdGgiOiIvb3JkZXIvb3JkZXJtYW5hZ2UiLCIkdGl0bGUiOiJPcmRlcnMiLCIkdmlld3BvcnRfd2lkdGgiOjQ0MSwiJGVsZW1lbnRfc2VsZWN0b3IiOiIjcm9vdCA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgyKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgyKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgyKSA+IGRpdjpudGgtb2YtdHlwZSgyKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IHRhYmxlOm50aC1vZi10eXBlKDEpID4gdGJvZHk6bnRoLW9mLXR5cGUoMSkgPiB0cjpudGgtb2YtdHlwZSgxKSA+IHRkOm50aC1vZi10eXBlKDYpID4gYTpudGgtb2YtdHlwZSgxKSIsIiRpc19maXJzdF9kYXkiOmZhbHNlfSwiYW5vbnltb3VzX2lkIjoiMTkwNDA0NTA4MTQxMi0wY2E2ODA4NDcxMmRjZC0yNjAyMWU1MS03ODY0MzItMTkwNDA0NTA4MTUxZTQiLCJ0eXBlIjoidHJhY2siLCJldmVudCI6IiRXZWJDbGljayIsIl90cmFja19pZCI6MzkwNzg0NDgwfQ==',
                            # #     'ext': 'crc=-859354530',
                            # # }
                            # #
                            # # headers = {
                            # #     'authority': 'uk-gateway.hungrypanda.co',
                            # #     'accept': 'application/json, text/plain, */*',
                            # #     'accept-language': 'zh-CN,zh;q=0.9',
                            # #     'content-type': 'application/json',
                            # #     'countrycode': 'GB',
                            # #     'lang': 'en-US',
                            # #     'origin': 'https://merchant-uk.hungrypanda.co',
                            # #     'platform': 'H5',
                            # #     'referer': 'https://merchant-uk.hungrypanda.co/',
                            # #     'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
                            # #     'sec-ch-ua-mobile': '?0',
                            # #     'sec-ch-ua-platform': '"Windows"',
                            # #     'sec-fetch-dest': 'empty',
                            # #     'sec-fetch-mode': 'cors',
                            # #     'sec-fetch-site': 'same-site',
                            # #     'token': token,
                            # #     'uniquetoken': '90fccb9c-7466-457a-b035-ff9828cc746f',
                            # #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
                            # # }
                            # #
                            # # json_data = {
                            # #     'orderSn': order_id,
                            # # }
                            # #
                            # # res = page1.post('https://uk-gateway.hungrypanda.co/api/merchant/order/detail',
                            # #                       headers=headers, json=json_data,params=params, cookies=cookies)
                            # #
                            # # 替换token和order_sn
                            # # token = '1432d7c58741ac88141af5131a3a0de3'
                            # # order_sn = '462511524052176362624'
                            #
                            # 定义要替换的新的 token 和 order_sn 值
                            new_token = token
                            new_order_sn = order_id

                            # 定义 JavaScript 文件路径
                            js_file_path = 'get_json_data.js'

                            #     # 打开 JavaScript 文件进行读取
                            with open(js_file_path, 'r') as file:
                                js_code = file.read()

                            js_code = js_code.replace('{tokenst}', new_token)
                            js_code = js_code.replace('{ordersnst}', new_order_sn)

                            # print(js_code)
                            # time.sleep(4)
                            # dg = page.run_js(js_code)
                            for g in range(3):
                                try:
                                    # rus = dg.json
                                    dg = page.run_js(js_code)
                                    details = dg['data']['details']
                                    CookList = []
                                    detail = details[k]
                                    lt = []
                                    lt = {
                                        "id": "AutoIn",
                                        "name": detail['skuName'],
                                        "price": 0,  # 这里可以根据需要修改价格的逻辑
                                        "qty": detail['productCount']
                                        }
                                    break
                                except Exception as e:
                                    Logger.error(e)
                                    print("断开9")
                                    time.sleep(15)

                            CookList.append(lt)
                            item["CookList"] = CookList
                            k = k + 1
                            items.append(item)


                        except Exception as e:
                            Logger.error(e)
                            print("断开3")
                            page.reconnect()
                            # logging.exception(menu)
                    vbtn_order = page.ele('@data-icon=close')
                    vbtn_order.click()
                    # menuamtint = 0.01
                    # try:
                    #     menuamtint = float(rus['data']['feeInfoResqDTOList'][0]['feePrice'])
                    # except:
                    #     menuamtint = float(rus['data']['fixedPrice'])
                    # menuamt = menuamtint
                    dd = {
                        "AppID": "web",  # 固定
                        "AppType": "web",  # 固定
                        "PayType": "mbpay",  # 固定
                        "BranchID": branch_id,  # 读取setting配置文件
                        "TableID": "992",  # 固定
                        "TableName": "HungryPanda",  # 固定
                        "BillType": 3,  # 固定
                        "ServiceRate": 0,  # 固定
                        "SumOfService": 0,  # 固定
                        "TotalPoint": 0,  # 固定
                        "TotalAmt": total_amount * commission,  # netPayout
                        "MemberCardID": "888",  # 固定
                        "MemberName": "Panda"+order_id[-4:],  # 固定
                        # "Mobile": "0788888888",  # 固定
                        # "PeopleCount": 0,  # 固定
                        "Items": items,
                        # "Coupons": [],  # 固定
                        "Remark": "NO CUTLERY",  # 固定
                        "CompanyID": merch_id,  # 固定
                        "UserID": user_id  # 固定
                    }
                    Logger.debug(dd)
                    headers = {"Cookie": "user_app_id=web; user_web=167225002936801673; hash_web=5d95b5c7e70cdc9b799d918e52ee167b"}
                    r = requests.post(url="http://tg2.weimember.cn/mb/member.api.ljson?api=mn.order&act=create",
                                      data=json.dumps(dd), headers=headers)
                    Logger.debug(r.text)
                    try:
                        data2 = {"OrderID": json.loads(r.text)['data']['OrderID']}
                    except Exception as e:
                        Logger.error(e)
                        print("断开2")
                        page.reconnect()
                        Logger.error(r.text)
                        if json.loads(r.text)['err'].__contains__("库存数量不足"):
                            print("库存数量不足")

                    r2 = requests.post(url="http://tg2.weimember.cn/mb/member.api.ljson?api=mn.order&act=pay", json=data2,
                                       headers=headers)
                    Logger.debug(r2.text)
                    print(f"HungryPanda: Order {order_id} is sent to JZZP.")
                    # page.scroll.to_top()

                    # time.sleep(2)
                    old_orders.insert(0, order_id)
                    old_orders = old_orders[:30]
                    with open("hungrypanda_lastorder.txt", "w") as f:
                        for l in old_orders:
                            f.write(str(l) + "\n")
                        f.close()


        except Exception as e:
            print(e)
            print("断开1")
            vbtn_order = page.ele('@data-icon=close')
            vbtn_order.click()
            page.reconnect()
            print("失败")
        print("-------------------")
        time.sleep(2)







# for i in range(1, 11):
#     # 构造XPath
#     # xpath = '//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]'
#
#     # 定位到元素并点击
#     element = page.ele('xpath//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/a')
#     element.click()
#     time.sleep(3)




