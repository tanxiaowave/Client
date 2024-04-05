from selenium import webdriver
import time
import json
import requests
import os
import threading
import pymssql
import logging
import configparser


reader = configparser.ConfigParser()
reader.read("settings.INI")
server = reader.get("Database", "server")
user = reader.get("Database", "user")
sql_password = reader.get("Database", "password")
database = reader.get("Database", "database")
commission = float(reader.get("Commission", "ubereats"))
merch_id = reader.get("Store", "merchid")
branch_id = reader.get("Store", "branchid")
address = reader.get("UberEats_Branch", "address")
headless_flag = reader.get("Flag", "headless_flag")
try:
    database_flag = eval(reader.get("Database", "flag"))
except:
    database_flag = True

def uberScrape():
    logging.basicConfig(level='INFO', filename='test.log',
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filemode='a')
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-data-dir={os.getcwd()}/selenium')
    if headless_flag == 'True':
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--log-level=3")
    options.add_argument("--silent")
    driver = webdriver.Chrome('chromedriver', options=options)

    # ubereats管理页面加载很慢，所以sleep5秒
    driver.get(f"https://merchants.ubereats.com/manager/orders?start={time.localtime().tm_year}-{'%02d'%time.localtime().tm_mon}-{'%02d'%time.localtime().tm_mday}&end={time.localtime().tm_year}-{'%02d'%time.localtime().tm_mon}-{'%02d'%time.localtime().tm_mday}")
    time.sleep(5)
    if not driver.current_url.startswith("https://merchants.ubereats.com/manager/orders"):
        return False

    # 新增的UberEats提示信息，有的话先点击关掉
    try:
        driver.find_element('xpath', '//*[@id="bui10"]/div[2]/div/button').click()
    except:
        pass

    # 分店选择
    if address != "":
        try:
            # 餐厅 Stores 按钮
            restaurant_btn = driver.find_element('xpath', '//*[@id="wrapper"]/div/div/div[2]/div[2]/div[2]/div[4]/div/div[1]/button')
            restaurant_btn.click()
            time.sleep(1)
            try:
                # 分店 Stores 按钮
                driver.find_element('xpath', '//*[@id="bui11"]/div/div/div[1]/button[2]').click()
                time.sleep(1)
            except:
                try:
                    driver.find_element('xpath', '//*[@id="bui10"]/div/div/div[1]/button[2]').click()
                    time.sleep(1)
                except Exception as e:
                    logging.exception(e)
                    return

            # 循环分店选项，小字地址里包含了settings.ini里写的uber address的话就选中，所有包含的都会选中
            branch_num = 1
            while True:
                try:
                    branch_btn = driver.find_element('xpath', f'//*[@id="bui11"]/div/div/div[1]/div[3]/div[1]/div/div/div[{branch_num}]')
                except:
                    try:                                           
                        branch_btn = driver.find_element('xpath', f'//*[@id="bui10"]/div/div/div[1]/div[3]/div[1]/div/div/div[{branch_num}]')
                    except:
                        break
                if branch_btn.text.__contains__(address):
                    branch_btn.click()
                branch_num += 1
            time.sleep(1)
            # 选完分店后的确认按钮
            branch_confirm_btn = driver.find_element('xpath', '/html/body/div[1]/div/div/div[2]/div[2]/div/div/div/div/div/div[2]/button')
            branch_confirm_btn.click()

            time.sleep(3)
        except Exception as e:
            logging.exception(e)
            return
    # id = driver.find_element('xpath', '//*[@id="wrapper"]/div[1]/div/div[2]/div[2]/div/div[6]/div/table/tbody/tr[2]/td[2]/div/div').text
    # store_name = driver.find_element('xpath', '//*[@id="wrapper"]/div[1]/div/div[2]/div[2]/div/div[6]/div/table/tbody/tr[2]/td[4]/div/div/div/div[1]').text
    # eater_name = driver.find_element('xpath', '//*[@id="wrapper"]/div[1]/div/div[2]/div[2]/div/div[6]/div/table/tbody/tr[2]/td[1]/div/div/div[2]/div[1]/div').text
    # placed_at = driver.find_element('xpath', '//*[@id="wrapper"]/div[1]/div/div[2]/div[2]/div/div[6]/div/table/tbody/tr[2]/td[4]/div/div/div/div[2]').text.split(" ")
    # date = placed_at[0].split("/")
    # YYYY = date[2]
    # MM = date[0]
    # DD = date[1]
    # if len(DD) < 2:
    #   DD = '0' + DD
    # t = placed_at[1].split(":")
    # HH = t[0]
    # M = t[1]
    # placed_at = YYYY + '-' + MM + '-' + DD + ' ' + HH + ':' + M

    # 订单列表元素
    order_path = '//*[@id="wrapper"]/div[1]/div/div[2]/div[2]/div[2]/div[6]/div/table/tbody/'
    try:
        # 1是表头，所以从[2]开始找
        # 先看一下2存不存在
        driver.find_element('xpath', f'{order_path}tr[2]/td[2]')
    except:
        # 2不存在的话，有可能是还没加载好，刷新一下
        driver.refresh()
        time.sleep(4)
        try:
            # 如果2还是不存在，说明一条单都没有，return
            driver.find_element('xpath',
                                f'{order_path}tr[2]/td[2]')
        except Exception as e:
            return

    # 运行到这里说明至少有一条单
    try:
        with open('ubereats_lastorder.txt', 'r') as f:
            old_orders = f.readlines()
            for i in range(len(old_orders)):
                old_orders[i] = old_orders[i].replace("\n", "")
            f.close()
    except:
        old_orders = []
        f = open('ubereats_lastorder.txt', 'w')
        f.close()

    # 查看订单列表里的前五条单，顺序是从新到旧的
    for i in range(2,7):
        try:
            order_id = driver.find_element('xpath',
                                           f'{order_path}tr[{i}]/td[1]/div/div/div[2]/div[2]').text
            if order_id not in old_orders:
                # 不是旧订单，点击查看是不是已接受，因为会有已取消的单
                order_btn = driver.find_element('xpath',
                                        f'{order_path}tr[{i}]')
                order_btn.click()
                time.sleep(3)
                # 整条订单的内容
                all_text = driver.find_element('xpath', '//*[@id="wrapper"]/div[2]/div[2]/div/div/div/div[2]/div[1]/div[1]').text
                # 订单内容里不包括分店地址，说明分店选择失败，可能是加载慢导致的，返回，直到正确选择分店
                if not all_text.__contains__(address):
                    return
                # 已接受的订单，退出循环
                if all_text.__contains__("accepted") or all_text.__contains__("已接受"):
                    break
                # 如果已经是第五条单，都不是新订单，返回
                elif i == 6:
                    return
                else:
                    # 如果不是第五条单，点击订单界面的X关掉，看下一条
                    driver.find_element("xpath", '//*[@id="wrapper"]/div[2]/div[2]/div/div/div/div[2]/div[2]/button/svg').click()
                    continue
        except Exception as e:
            return

    # 双重检测
    if order_id in old_orders:
        print("UberEats: No new order")
        return
    try:
        all_text = driver.find_element('xpath',
                                       '//*[@id="wrapper"]/div[2]/div[2]/div/div/div/div[2]/div[1]/div[1]').text
        # 非已接受的订单，返回
        if all_text.__contains__("accepted") or all_text.__contains__("已接受"):
            pass
        else:
            return
    except:
        return

    # 运行到这里说明是有效新订单
    try:
        price = driver.find_element('xpath', '//*[@id="wrapper"]/div[2]/div[2]/div/div/div/div[2]/div[1]/div[1]/ul/li/div[2]/div/div[2]/div[last()]/div[2]').text[1:]
        price = float(price)
        menu = driver.find_element('xpath', '//*[@id="wrapper"]/div[2]/div[2]/div/div/div/div[2]/div[1]/div[1]/ul/li/div[2]/div/div[1]').text
    except Exception as e:
        logging.exception(e)
        return

    menu = menu.split("\n")
    # 每个菜的套餐或者做法上面会有一行"Choice of Toppings"，去掉
    for m in menu:
        if m.startswith("Choice") or m.startswith("Choose"):
            menu.remove(m)
    # for i in range(0, len(menu), 3):
    #     item = dict()
    #     item['id'] = "" # 等菜单更新，在前面加上[0000]的id后可以改为 item['id'] = menu[i][1:5]
    #     item['title'] = menu[i+1] # 菜单更新后改为 items['title'] = menu[i][6:]
    #     item['quantity'] = menu[i]
    #     item['price'] = menu[i+2]
    #     item['seleted_modifies_groups'] = ""
    #     price += float(menu[i]) * float(menu[i+2][1:])
    #     items.append(item)
    items = []
    i = 0
    try:
        while i < len(menu):
            # 每次循环第一个i都必是新菜的数量，用i+1的第一个字符确定是不是菜品，是[的话就是菜，不是的话就是套餐内容
            if i+1 < len(menu) and menu[i+1][0] == '[':
                menu_id = menu[i+1][menu[i+1].find('[')+1:menu[i+1].find(']')]
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
                item = {
                    "ParentID": "SP1010",  # 随便，但不能为空
                    "MenuID": menu_id,
                    "MenuName": menu_name,
                    "MenuUnit": ".",
                    "MenuPrice": float(menu[i+2][1:]),
                    "MenuPriceOld": float(menu[i+2][1:]),
                    "MenuQty": int(menu[i]),
                    "MenuAmt": float(menu[i+2][1:]) * int(menu[i]),
                    "MenuService": 0,
                    "SumOfService": 0,
                    "CookList": [],
                    "MenuList": []
                }
                items.append(item)
                i += 3
            # 菜名开头不是[的话，就是套餐
            # 如果报错在这附近说list index error，说明菜单id没加好，第一个菜就没有id不是[开头，被识别成做法或口味，当要把这个“做法”赋给items[-1]的时候就报错了
            else:
                option_price = 0.
                if i+1 < len(menu) and menu[i + 1][0] == '£':
                    # 有价格
                    l = {
                        "id": "TGDelivery",
                        "name": menu[i],
                        "price": float(menu[i + 1][1:]),
                        "qty": 1
                    }
                    option_price += float(menu[i + 1][1:])
                    i += 2
                else:
                    # 没价格
                    l = {
                        "id": "TGDelivery",
                        "name": menu[i],
                        "price": 0.,
                        "qty": 1
                    }
                    i += 1
                items[-1]["CookList"].append(l)
                items[-1]['MenuPriceOld'] += option_price
                items[-1]['MenuPrice'] += option_price
                items[-1]['MenuAmt'] = items[-1]['MenuPrice'] * items[-1]['MenuQty']
    except Exception as e:
        if len(menu) > 1:
            logging.exception(e)
        return

    if float(price) == 0:
        price = 0.01

    # 发送post请求给H5下单
    d = {
        "AppID": "web",
        "AppType": "web",
        "PayType": "mbpay",
        "BranchID": branch_id,
        "TableID": "991",
        "TableName": "UberEats",
        "BillType": 3,  # 盲猜3代指会员支付
        "Remark": "",
        "ServiceRate": 0,
        "SumOfService": 0,
        "TotalAmt": price * commission,
        "TotalPoint": 0,
        "MemberCardID": "888",  # 换成给每个平台创建的会员的会员号
        "MemberName": f"UberEats: {order_id}",
        "Items": items,
        "CompanyID": merch_id,
        "UserID": "167225002936801673"
    }

    headers = {"Cookie": "user_app_id=web; user_web=167225002936801673; hash_web=5d95b5c7e70cdc9b799d918e52ee167b"}
    # 第一次post创建订单
    r = requests.post(url="http://tg2.weimember.cn/mb/member.api.ljson?api=mn.order&act=create", json=d,
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
    print(f"UberEats: Order {order_id} is sent to JZZP.")
    old_orders.insert(0, order_id)
    old_orders = old_orders[:10]
    with open('ubereats_lastorder.txt', 'w') as f:
        for l in old_orders:
            f.write(str(l) + "\n")
        f.close()

    try:
        data = dict()
        data["order_id"] = order_id
        data["platform"] = "ubereats"
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
        response = requests.post(url='http://autoin.trinalgenius.co.uk:8000/order/new',headers=header,data=json.dumps(data), timeout=5)
        # response = requests.post(url='http://3.11.136.6:8000/order/new',json=data)
    except:
        pass
