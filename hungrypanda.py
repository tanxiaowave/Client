from selenium import webdriver
import time
import json
import requests
import threading
import tkinter as tk
import rsa
import pymssql
import logging
import configparser


reader = configparser.ConfigParser()
reader.read("settings.INI")
server = reader.get("Database", "server")
user = reader.get("Database", "user")
sql_password = reader.get("Database", "password")
database = reader.get("Database", "database")
commission = float(reader.get("Commission", "hungrypanda"))
merch_id = reader.get("Store", "merchid")
branch_id = reader.get("Store", "branchid")
headless_flag = reader.get("Flag", "headless_flag")
try:
    database_flag = eval(reader.get("Database", "flag"))
except:
    database_flag = True

def hungrypandaScrape():
    logging.basicConfig(level='INFO', filename='test.log',
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filemode='a')
    options = webdriver.ChromeOptions()
    if headless_flag == 'True':
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--log-level=3")
    options.add_argument("--silent")
    driver = webdriver.Chrome('chromedriver', options=options)

    driver.get("https://merchant-uk.hungrypanda.co/order/ordermanage")
    time.sleep(2)
    if driver.current_url != 'https://merchant-uk.hungrypanda.co/order/ordermanage':
        pri = rsa.PrivateKey(
            10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
            65537,
            7002712700928804011838917939227853273317722595990151016778949911089213823265260722795698382337717248876309656289331967090125041513510782458343001103454593,
            7165380796988618938065214954530466870443807483684172787495616047866899293086811303,
            1492014128088262667286826329565602575995354986910798283007464819843657741)
        try:
            with open("panda_username_info.txt", "rb") as f:
                username = f.readline()
                f.close()
            with open("panda_password_info.txt", "rb") as f:
                password = f.readline()
                f.close()
            username = rsa.decrypt(username, pri).decode('utf-8')
            password = rsa.decrypt(password, pri).decode('utf-8')
        except:
            hplogin = tk.Toplevel(bg="#272727")
            hplogin.resizable(False, False)
            hplogin.grab_set()
            hplogin.wm_attributes("-topmost", 1)
            hplogin.title("Error!")
            hplogin.geometry(
                f'{250}x{80}+{round(hplogin.winfo_screenwidth() / 2 - 250 / 2)}+{round(hplogin.winfo_screenheight() / 2 - 80 / 2)}')
            tk.Label(hplogin,
                     text='The login information for \nHungryPanda is not valid,\n please log your \nHungryPanda info again.',
                     font=tk.font.Font(family="Arial", size=12), fg='#F37249', bg="#272727").pack()
            return False
        driver.get("https://merchant-uk.hungrypanda.co/login")
        time.sleep(1)
        u = driver.find_element('id', 'phone')
        u.send_keys(username)
        p = driver.find_element('id', 'password')
        p.send_keys(password)
        btn = driver.find_element('xpath', '//*[@id="root"]/div/div/div/div/div/div/div/form/div[5]/div/div/div/button')
        btn.click()
        time.sleep(1)
        # # 按理来说不会出现密码能被解密但无法登陆的情况，因为记录的时候就会验证，只有对的密码才会被记录。除非文件被手动修改了
        # if driver.current_url == "https://merchant-uk.hungrypanda.co/login":
        #     tk.messagebox.showinfo(title='Invalid login info!',
        #                            message='The information for HungryPanda login is not valid, please log your account info again.')
        #     return False
        driver.get("https://merchant-uk.hungrypanda.co/order/ordermanage")

    time.sleep(1)

    # 进入到preparing orders界面，只看preparing的订单
    try:
        preparing_btn = driver.find_element('xpath', '//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[1]/div/ul/li[3]')
        preparing_btn.click()
        time.sleep(1)
        try:
            driver.find_element("xpath",
                                f"//*[@id='root']/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]")
        except:
            print("Hungrypanda: No preparing order")
            return
    except Exception as e:
        # logging.exception(e)
        return

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

    # 看前十条单，一页也只有十条
    for i in range(1,11):
        try:
            order_id = driver.find_element("xpath", f"//*[@id='root']/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr[{i}]/td[1]").text
            if order_id not in old_orders:
                status = driver.find_element("xpath", f"//*[@id='root']/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr[{i}]/td[5]").text
                if status != "Preparing" and status != "Delivering" and not status.startswith("To be picked"):
                    logging.exception(status)
                    logging.exception(order_id)
                    return
                view_btn = driver.find_element("xpath", f"//*[@id='root']/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr[{i}]/td[6]/a")
                break
        except:
            print("Hungrypanda: No new preparing order")
            return

    # 点击订单的view查看订单内容，下面的获取订单内容，发送到H5，保存到服务器数据库，都跟fantuan差不多了
    try:
        view_btn.click()
    except:
        return

    time.sleep(1)
    try:
        ordernum = driver.find_elements('class name', 'order-number')[0].text
        remark = driver.find_elements('class name', 'remark')[0].text
        order = driver.find_elements("class name", "modal-column")
    except:
        logging.exception(Exception)
    if not ordernum.__contains__(order_id):
        return
    # 细分订单详情
    items = []
    total_amount = 0.
    try:
        menu = order[1].text.split("\n")[1:]
    except Exception as e:
        logging.exception(e)
        logging.exception(menu)
        return
    for i in range(0, len(menu), 3):
        # item = dict()
        # item['id'] = "" # 等菜单更新，在前面加上[0000]的id后可以改为 item['id'] = menu[i][1:5]
        # item['title'] = menu[i] # 菜单更新后改为 items['title'] = menu[i][6:]
        # item['quantity'] = menu[i+1][1:]
        # item['price'] = menu[i+2]
        # item['seleted_modifies_groups'] = ""

        # # 去掉多余括号
        # index = menu[i].find("(")
        # if index == -1:
        #     index = len(menu[i])
        # menu[i] = menu[i][:index]
        menu_id = menu[i][menu[i].find('[')+1:menu[i].find(']')]

        try:
            if database_flag == True:
                connect = pymssql.connect(server=server, user=user, password=sql_password, database=database,
                                          login_timeout=5)
                cur = connect.cursor()
                sql = f'select MenuName from mn_Menu where MenuID={menu_id}'
                cur.execute(sql)
                sql_result = cur.fetchall()
                menu_name = sql_result[0][0].encode('latin-1').decode('gbk')
            else:
                with open(f"{branch_id}.txt", "r+") as f:
                    d = f.read()
                    f.close()
                result = json.loads(d)
                menu_name = result.get(str(menu_id))
        except:
            print('sql connection failed...')
            menu_id = "1999"
            menu_name = "编码出错！Code Error!"
        try:
            total_amount += float(menu[i + 2][1:])
            item = {
                "ParentID": "SP1010",  # 随便，但不能为空
                "MenuID": menu_id,
                "MenuName": menu_name,
                "MenuUnit": ".",
                "MenuPrice": float(menu[i + 2][1:]) / int(menu[i+1][1:]),
                "MenuPriceOld": float(menu[i + 2][1:]) / int(menu[i+1][1:]),
                "MenuQty": int(menu[i+1][1:]),
                "MenuAmt": float(menu[i + 2][1:]),
                "MenuService": 0,
                "SumOfService": 0,
                "CookList": [],
                "MenuList": []
            }
            items.append(item)
        except Exception as e:
            logging.exception(e)
            logging.exception(menu)
            return
    # 发送给服务器
    # data = dict()
    # data["id"] = order[0].text[9:]
    # data["platform"] = "hungrypanda"
    # data["displayed_id"] = ""
    # data["current_state"] = ""
    # data["store"] = dict(id="12345", name="")
    # data["eater"] = dict(name="", phone="", phone_code="", delivery = dict(location=dict(), type="", notes=""))
    # data["cart"] = dict(items=items, products_quantity=len(items))
    # data["payment"] = dict(total=order[2].text.split("\n")[1],delivery_fee="",tip="")
    # data["placed_at"] = order_time
    # print(data)
    # 发送post请求给TG服务器
    # header = {"Content-Type":"application/json"}
    # response = requests.post(url='http://3.11.136.6:8000/order/new',headers=header,data=json.dumps(data))
    # response = requests.post(url='http://3.11.136.6:8000/order/new',json=data)
    # print(response.content)
    # time.sleep(1)
    if float(total_amount) == 0:
        total_amount = 0.01
    # 发送post请求给H5进行下单
    d ={
        "AppID": "web",
        "AppType": "web",
        "PayType": "mbpay",
        "BranchID": branch_id,
        "TableID": "992",
        "TableName": "HungryPanda",
        "BillType": 3,                       # 盲猜3代指会员支付
        "Remark": remark,
        "ServiceRate": 0,
        "SumOfService": 0,
        "TotalAmt": float(total_amount) * commission,
        "TotalPoint": 0,
        "MemberCardID": "888",        # 换成给每个平台创建的会员的会员号
        "MemberName": f"HungryPanda: #{order_id[-8:-4]} {order_id[-4:]}",
        "Items": items,
        "CompanyID": merch_id,
        "UserID": "167225002936801673"       # 随便填
    }

    headers = {"Cookie": "user_app_id=web; user_web=167225002936801673; hash_web=5d95b5c7e70cdc9b799d918e52ee167b"}
    r = requests.post(url="http://tg2.weimember.cn/mb/member.api.ljson?api=mn.order&act=create", data=json.dumps(d),
                      headers=headers)

    try:
        data2 = {"OrderID": json.loads(r.text)['data']['OrderID']}
    except Exception as e:
        logging.exception(d)
        logging.exception(r.text)
        if json.loads(r.text)['err'].__contains__("库存数量不足"):
            return json.loads(r.text)['err']
        return

    r2 = requests.post(url="http://tg2.weimember.cn/mb/member.api.ljson?api=mn.order&act=pay", json=data2, headers=headers)
    logging.info(r2.text)
    print(f"HungryPanda: Order {order_id} is sent to JZZP.")
    old_orders.insert(0, order_id)
    old_orders = old_orders[:30]
    with open("hungrypanda_lastorder.txt", "w") as f:
        for l in old_orders:
            f.write(str(l) + "\n")
        f.close()

    try:
        data = dict()
        data["order_id"] = order_id
        data["platform"] = "hungrypanda"
        data["displayed_id"] = f"#{order_id[-8:-4]} {order_id[-4:]}"
        # data["store"] = dict(id="54321", name="Homelink Express")
        # data["eater"] = dict(name="", phone="", phone_code="", delivery = dict(location=dict(), type="", notes=""))
        data["cart"] = dict(items=items, products_quantity=len(items))
        # data["payment"] = dict(total=price.split("（")[0],delivery_fee="",tip="")
        data["placed_at"] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        data["branch_id"] = branch_id
        data["merch_id"] = merch_id
        data["price"] = float(total_amount) * commission
        header = {"Content-Type":"application/json"}
        response = requests.post(url='http://autoin.trinalgenius.co.uk:8000/order/new',headers=header,data=json.dumps(data), timeout=5)
        # response = requests.post(url='http://3.11.136.6:8000/order/new',json=data)
    except:
        pass