from datetime import date
from selenium import webdriver
import requests
import time
import json
import tkinter as tk
import threading
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
commission = float(reader.get("Commission", "deliveroo"))
merch_id = reader.get("Store", "merchid")
branch_id = reader.get("Store", "branchid")
orgId = reader.get("Deliveroo_Branch", "orgId")
branchId = reader.get("Deliveroo_Branch", "branchId")
headless_flag = reader.get("Flag", "headless_flag")
try:
    database_flag = eval(reader.get("Database", "flag"))
except:
    database_flag = True



def deliverooScrape():
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

    driver.get(f"https://restaurant-hub.deliveroo.net/live-orders?orgId={orgId}&branchId={branchId}")
    time.sleep(3)

    if driver.current_url != f"https://restaurant-hub.deliveroo.net/live-orders?orgId={orgId}&branchId={branchId}":
        pri = rsa.PrivateKey(
            10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
            65537,
            7002712700928804011838917939227853273317722595990151016778949911089213823265260722795698382337717248876309656289331967090125041513510782458343001103454593,
            7165380796988618938065214954530466870443807483684172787495616047866899293086811303,
            1492014128088262667286826329565602575995354986910798283007464819843657741)
        try:
            with open("deliveroo_username_info.txt", "rb") as f:
                username = f.readline()
                f.close()
            with open("deliveroo_password_info.txt", "rb") as f:
                password = f.readline()
                f.close()
            username = rsa.decrypt(username, pri).decode('utf-8')
            password = rsa.decrypt(password, pri).decode('utf-8')
        except:
            drlogin = tk.Toplevel(bg="#272727")
            drlogin.resizable(False, False)
            drlogin.grab_set()
            drlogin.wm_attributes("-topmost", 1)
            drlogin.title("Error!")
            drlogin.geometry(
                f'{250}x{80}+{round(drlogin.winfo_screenwidth() / 2 - 250 / 2)}+{round(drlogin.winfo_screenheight() / 2 - 80 / 2)}')
            tk.Label(drlogin,
                     text='The login information for \nDeliveroo is not valid,\n please log your \nDeliveroo info again.',
                     font=tk.font.Font(family="Arial", size=12), fg='#F37249', bg="#272727").pack()
            return False
        try:
            cookie_btn = driver.find_element('xpath', "//*[@id='onetrust-accept-btn-handler']")
            cookie_btn.click()
        except:
            pass
        u = driver.find_element('xpath', '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/label[1]/span/div/input')
        u.send_keys(username)
        p = driver.find_element('xpath', '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/label[2]/span/div/input')
        p.send_keys(password)
        btn = driver.find_element('xpath', '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/button')
        btn.click()
        time.sleep(3)
        if driver.current_url != f"https://restaurant-hub.deliveroo.net/live-orders?orgId={orgId}&branchId={branchId}":
            driver.get("https://www.google.com")
            driver.get(f"https://restaurant-hub.deliveroo.net/live-orders?orgId={orgId}&branchId={branchId}")
            time.sleep(3)

    if driver.current_url != f'https://restaurant-hub.deliveroo.net/live-orders?orgId={orgId}&branchId={branchId}':
        return

    try:
        with open('deliveroo_lastorder.txt', 'r') as f:
            old_orders = f.readlines()
            for i in range(len(old_orders)):
                old_orders[i] = old_orders[i].replace("\n", "")
            f.close()
    except FileNotFoundError:
        old_orders = []
        f = open('deliveroo_lastorder.txt', 'w')
        f.close()

    try:
        driver.find_element("xpath", '//*[@id="survey-wrapper"]/form/footer/div[1]/div[1]/button').click()
    except:
        pass


    try:
        for i in range(1, 30, 2):
            try:
                detail_btn = driver.find_element('xpath',
                                                 f'//*[@id="__next"]/div[1]/div/main/div[2]/div/div[2]/div[1]/div[2]/div/div[{i}]')
            except:
                return
            order_id = detail_btn.text.split('\n')[0]
            if order_id in old_orders:
                continue
            if detail_btn.text.split('\n')[2].__contains__(':'):
                continue
            break
        detail_btn.click()
        time.sleep(1)
    # placed_at = driver.find_element('xpath', '//*[@id="__next"]/div[1]/main/div[2]/div/div[2]/div/div/dl/div[2]/dd/span').text.split(" ")
    # YYYY = placed_at[2]
    # MM = str(list(calendar.month_abbr).index(placed_at[1]))
    # DD = placed_at[0]
    # if len(DD) <2:
    #     DD = '0' + DD
    # HH = placed_at[4][:2]
    # M = placed_at[4][-2:]
    # placed_at = YYYY + '-' + MM + '-' + DD + ' ' + HH + ':' + M
        remark = ""
        num_of_text = driver.find_elements('xpath',
                                           "//*[@class='tcl__Text-03d692ab tcl__Text-267ecb65 tcl__Text-b0b3d22f tcl__Text-c49192dd']")
        if len(num_of_text) == 2:
            remark = num_of_text[0].text
        if len(num_of_text) == 4:
            remark = num_of_text[1].text
        if remark.startswith("为此"):
            remark = ""
        print(remark)
        price = driver.find_elements("xpath",
                                     "//*[@class='tcl__Heading-2a4b5924 tcl__Heading-c8c7e524 tcl__Heading-e7d4fe35']")
        price = float(price[1].text[1:])
        menu = driver.find_elements("xpath", "//*[@class='tcl__LayoutBox-832894ed styles_categories__SPo9P']")

        menu = menu[:int(len(menu)/2)]
    except Exception as e:
        logging.exception(e)
        return

    temp = []
    for i in menu:
        i = i.text.split("\n")
        for j in i[1:]:
            temp.append(j)
    menu = temp
    items = []
    i = 0
    while i < len(menu):
        # item = dict()
        # item['id'] = menu[i+1][1:5] # 等菜单更新，在前面加上[0000]的id后可以改为 item['id'] = menu[i][1:5]
        # item['title'] = menu[i+1][7:] # 菜单更新后改为 items['title'] = menu[i][6:]
        # item['quantity'] = menu[i][:-1]
        # item['price'] = menu[i+2]
        # item['seleted_modifies_groups'] = ""

        # 数量+名字前有id+价格 = 单品或菜单里的主菜，i是数量，i+1是名字，i+2是价格
        try:
            if menu[i][-1] == 'x' and i+1 < len(menu) and menu[i+1][0] == '[':
                menu_id = menu[i+1][menu[i+1].find("[")+1:menu[i+1].find("]")]
                # menu_name = menu[i+1][menu[i+1].find("]")+1:]
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

                if menu[i + 1][0] == '-':
                    item_price = 0.
                else:
                    # 0块商品网页上显示的价格为 '-' 而不是 '£0'
                    item_price = float(menu[i+2][1:])

                item = {
                    "ParentID": "SP1010",  # 随便，但不能为空
                    "MenuID": menu_id,
                    "MenuName": menu_name,
                    "MenuUnit": ".",
                    "MenuPrice": item_price / int(menu[i][:-1]),
                    "MenuPriceOld": item_price / int(menu[i][:-1]),
                    "MenuQty": int(menu[i][:-1]),
                    "MenuAmt": item_price,
                    "MenuService": 0,
                    "SumOfService": 0,
                    "CookList": [],
                    "MenuList": []
                    # ,
                    # "CookList": [
                    #     {
                    #         "id": "",
                    #         "name": "",
                    #         "price": 0,
                    #         "qty": 1
                    #     },
                    # ],
                    # "MenuList": [
                    #     {
                    #         "id": "",
                    #         "name": "",
                    #         "qty": 1,
                    #         "unit": ".",
                    #         "price": 0,
                    #     }
                    # ]
                }
                items.append(item)
                i += 3
            # 否则就是套餐
            else:
                option_price = 0.
                if menu[i+1][0] == '£':
                    # 有价格
                    l = {
                        "id": "TGDelivery",
                        "name": menu[i],
                        "price": float(menu[i + 1][1:]),
                        "qty": 1
                    }
                    option_price += float(menu[i+1][1:])
                else:
                    # 没价格， 但因为还是会在价格位置显示'-'，i也是加2
                    l = {
                        "id": "TGDelivery",
                        "name": menu[i],
                        "price": 0.,
                        "qty": 1
                    }
                i += 2
                items[-1]["CookList"].append(l)
                items[-1]['MenuPriceOld'] += option_price
                items[-1]['MenuPrice'] += option_price
                items[-1]['MenuAmt'] = items[-1]['MenuPrice'] * items[-1]['MenuQty']
        except Exception as e:
            logging.exception(e)
            logging.exception(menu)
            return

    if float(price) == 0:
        price = 0.01

    d = {
        "AppID": "web",
        "AppType": "web",
        "PayType": "mbpay",
        "BranchID": branch_id,
        "TableID": "993",
        "TableName": "Deliveroo",
        "BillType": 3,  # 盲猜3代指会员支付
        "Remark": remark,
        "ServiceRate": 0,
        "SumOfService": 0,
        "TotalAmt": price * commission,
        "TotalPoint": 0,
        "MemberCardID": "888",  # 换成给每个平台创建的会员的会员号
        "MemberName": f"Deliveroo: {order_id}",
        "Items": items,
        "CompanyID": merch_id,
        "UserID": "167225002936801673"
    }

    headers = {"Cookie": "user_app_id=web; user_web=167225002936801673; hash_web=5d95b5c7e70cdc9b799d918e52ee167b"}
    # 第一次post创建订单
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

    r2 = requests.post(url="http://tg2.weimember.cn/mb/member.api.ljson?api=mn.order&act=pay", json=data2,
                       headers=headers)
    logging.info(r2.text)
    print(f"Deliveroo: Order {order_id} is sent to JZZP.")

    old_orders.insert(0, order_id)
    old_orders = old_orders[:10]
    with open('deliveroo_lastorder.txt', 'w') as f:
        for l in old_orders:
            f.write(str(l) + "\n")
        f.close()

    try:
        data = dict()
        data["order_id"] = order_id
        data["platform"] = "deliveroo"
        data["displayed_id"] = order_id
        # data["store"] = dict(id="54321", name="Homelink Express")
        # data["eater"] = dict(name="", phone="", phone_code="", delivery = dict(location=dict(), type="", notes=""))
        data["cart"] = dict(items=items, products_quantity=len(items))
        # data["payment"] = dict(total=price.split("（")[0],delivery_fee="",tip="")
        data["placed_at"] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        data["branch_id"] = branch_id
        data["merch_id"] = merch_id
        data["price"] = price * commission
        header = {"Content-Type":"application/json"}
        response = requests.post(url='http://3.11.136.6:8000/order/new',headers=header,data=json.dumps(data), timeout=5)
        # response = requests.post(url='http://3.11.136.6:8000/order/new',json=data)
    except:
        pass