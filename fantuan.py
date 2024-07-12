import requests
import json
import tkinter as tk
import tkinter.messagebox
import rsa
import pymssql
import logging
import time
import configparser


reader = configparser.ConfigParser()
reader.read("settings.INI")
server = reader.get("Database", "server")
user = reader.get("Database", "user")
sql_password = reader.get("Database", "password")
database = reader.get("Database", "database")
commission = float(reader.get("Commission", "fantuan"))
merch_id = reader.get("Store", "merchid")
branch_id = reader.get("Store", "branchid")
try:
    price_type = reader.get("Fantuan", "pricetype")
    database_flag = eval(reader.get("Database", "flag"))
except:
    price_type = ""
    database_flag = True

def fantuanScrape():
    logging.basicConfig(level='INFO', filename='test.log',
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filemode='a')
    current = time.time()
    pri = rsa.PrivateKey(
        10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
        65537,
        7002712700928804011838917939227853273317722595990151016778949911089213823265260722795698382337717248876309656289331967090125041513510782458343001103454593,
        7165380796988618938065214954530466870443807483684172787495616047866899293086811303,
        1492014128088262667286826329565602575995354986910798283007464819843657741)
    # 从文件读取key和饭团商户id
    try:
        # with open("fantuan_appkey.txt", "rb") as f:
        #     username = f.readline()
        #     f.close()
        # with open("fantuan_shopid.txt", "rb") as f:
        #     password = f.readline()
        #     f.close()
        appkey = '1b44a528-58de-4f07-b842-31cc492f0ede'
        shop_id = 2277
    except:
        ftlogin = tk.Toplevel()
        ftlogin.resizable(False, False)
        ftlogin.grab_set()
        ftlogin.wm_attributes("-topmost", 1)
        ftlogin.title("Error!")
        ftlogin.geometry(
            f'{280}x{80}+{round(ftlogin.winfo_screenwidth() / 2 - 280 / 2)}+{round(ftlogin.winfo_screenheight() / 2 - 80 / 2)}')
        tk.Label(ftlogin,
                 text='The information for \nFantuan API is not valid, \nplease log your \nFantuan API info again.',
                 font=tk.font.Font(size=13), fg='red').pack()
        return False

    # 调用api获取最近7天前十条订单
    headers = {
        "Content-Type": "application/json",
        "appKey": appkey,
        "timestamp": "{{$timestamp}}",
    }
    data = {
        "shopId": shop_id,
        "page": {
            "pageNum": 1,
            "pageSize": 10
        }
    }
    url = "https://openapi.fantuan.ca/api/v1/order/page"
    response = json.loads(requests.post(url, json=data, headers=headers).text)

    # 文档没写错误码，700和2001应该是自己摸索的，只记得2001是饭团系统错误，这两个不是严重错误，重试就行
    if response['code'] == 700 or response['code'] == 2001:
        logging.info(response)
        return
    # 严重的错误直接返回False
    if response['code'] != 0:
        logging.exception(response)
        ftlogin = tk.Toplevel()
        ftlogin.resizable(False, False)
        ftlogin.grab_set()
        ftlogin.title("Error!")
        ftlogin.geometry(
            f'{280}x{80}+{round(ftlogin.winfo_screenwidth() / 2 - 280 / 2)}+{round(ftlogin.winfo_screenheight() / 2 - 80 / 2)}')
        tk.Label(ftlogin, text='The information for Fantuan API is not valid,\n please log your Fantuan API info again.',
                 font=tk.font.Font(size=13), fg='red').pack()
        return False

    # 如果至少有一条订单
    if len(response['data']['rows']) > 0:
        # 读取旧订单
        try:
            with open("fantuan_lastorder.txt", 'r') as f:
                old_orders = f.readlines()
            for i in range(len(old_orders)):
                old_orders[i] = old_orders[i].replace("\n", "")
            f.close()
        except:
            old_orders = []
            f = open('fantuan_lastorder.txt', 'w')
            f.close()

        order_id = ""
        for row in response['data']['rows']:
            # 3 已接单 7 配送中
            if row['status'] == 3 or row['status'] == 7:
                if row['orderId'] not in old_orders:
                    # 如果是预约单，要看进入到20分钟内没有
                    if row['appointedDelivery'] == 1:
                        # 大于20分钟，存入预约单列表和旧订单列表
                        if (row['estimatedArrivalTime'] - current) / 60 > 30:
                            old_orders.insert(0, row['orderId'])
                            old_orders = old_orders[:20]
                            with open("fantuan_lastorder.txt", "w") as f:
                                for line in old_orders:
                                    f.write(str(line) + "\n")
                                f.close()
                            try:
                                with open('fantuan_schedule.txt', 'r') as f:
                                    schedule_orders = f.readlines()
                                    for i in range(len(schedule_orders)):
                                        schedule_orders[i] = schedule_orders[i].replace("\n", "")
                                    f.close()
                            except FileNotFoundError:
                                schedule_orders = []
                                f = open('fantuan_schedule.txt', 'w')
                                f.close()
                            schedule_orders.insert(0, row['orderId'] + " " + str(row['estimatedArrivalTime']))
                            with open("fantuan_schedule.txt", "w") as f:
                                for o in schedule_orders:
                                    f.write(str(o) + "\n")
                            continue
                    # 如果不是预约单，或者是预约单但已经在20分钟以内，准备发送这一订单
                    order_id = row['orderId']
                    break

        # 如果上面循环api返回的最近十条订单没有找到有效的可以发送的订单，检查记录了的预约单列表里有没有进入到20分钟内的预约单
        if order_id == "":
            try:
                with open('fantuan_schedule.txt', 'r') as f:
                    schedule_orders = f.readlines()
                    for i in range(len(schedule_orders)):
                        schedule_orders[i] = schedule_orders[i].replace("\n", "").split(" ")
                    f.close()
            except FileNotFoundError:
                schedule_orders = []
                f = open('fantuan_schedule.txt', 'w')
                f.close()
            for order in schedule_orders:
                if (float(order[1]) - current) / 60 < 30:
                    order_id = order[0]
                    schedule_orders.remove(order)
                    break
            with open("fantuan_schedule.txt", "w") as f:
                for o in schedule_orders:
                    f.write(str(o[0]) + " " + str(o[1]) + "\n")
            if order_id == "":
                print("Fantuan: No new order in recent 10 orders")
                return

        # 调用api搜索上面搜索到的可发送的订单的内容
        data = {
            "shopId": shop_id,
            "orderId": order_id
        }
        url = "https://openapi.fantuan.ca/api/v1/order/getOrder"
        response = json.loads(requests.post(url, json=data, headers=headers).text)
        if response['code'] != 0:
            print("Fantuan Failed: " + response)
            logging.exception(response)
            return
    else:
        print("Fantuan: No order in latest seven days")
        return

    try:
        menu = response['data']['details']
        items = []
        for item in menu:
            # 根据 [ 和 ] 来取出id
            menu_id = item['name'][item['name'].find("[")+1:item['name'].find("]")]
            try:
                # 到数据库搜索id对应的菜名
                if database_flag == True:
                    connect = pymssql.connect(server=server, user=user, password=sql_password, database=database,
                                              login_timeout=5,tds_version='7.0')
                    cur = connect.cursor()
                    sql = f'select MenuName from mn_Menu where MenuID={menu_id}'
                    cur.execute(sql)
                    sql_result = cur.fetchall()
                    menu_name = sql_result[0][0].encode('latin-1').decode('gbk')
                # 没有数据库就到txt搜索对应的菜名
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

            # 发送给H5接口的数据包 的菜单列表 的一个元素
            i = {
                "ParentID": "SP1010",  # 随便，但不能为空
                "MenuID": menu_id,
                "MenuName": menu_name,
                "MenuUnit": ".",
                "MenuPrice": item['price'],
                "MenuPriceOld": item['price'],
                "MenuQty": item['quantity'],
                "MenuAmt": item['price'] * item['quantity'],
                "MenuService": 0,
                "SumOfService": 0,
                "CookList": [],
                "MenuList": []
            }
            # 先不管有没有做法口味直接append，下面口味就可以append给items[-1]了
            items.append(i)
            if 'optionGroups' in item.keys():
                CookList = []
                option_price = 0.
                for o in item['optionGroups']:
                    for options in o['options']:
                        l = {
                            "id": "AutoIn",
                            "name": options['name'],
                            "price": options['price'],
                            "qty": 1
                        }
                        option_price += options['price']
                        CookList.append(l)
                items[-1]["CookList"] = CookList
    except Exception as e:
        logging.exception(e)
        logging.exception(menu)
        return

    price = response['data']['shopOrderRevenue']['fantuanTransfer']
    if price_type == "subtotal":
        price = response['data']['shopOrderRevenue']['subtotal']
    if price_type == "Net":
        price = response['data']['shopOrderRevenue']['subtotal'] + response['data']['shopOrderRevenue']['totalDiscount'] + response['data']['shopOrderRevenue']['activitySubsidy']

    # 如果发送了0金额给H5，jzzp会报错没有零支付或者H5会报错金额不能为0
    if float(price) == 0:
        price = 0.01

    # 发送给H5的数据包d，第一次发送，创建订单
    d = {
        "AppID": "web",
        "AppType": "web",
        "PayType": "mbpay",
        "BranchID": branch_id,
        "TableID": "994",
        "TableName": "Fantuan",
        "BillType": 3,  # 3可能是会员支付
        "Remark": response['data']['remark'],
        "ServiceRate": 0,
        "SumOfService": 0,
        "TotalAmt": price,
        "TotalPoint": 0,
        "MemberCardID": "888",  # JZZP里创建的会员的会员号
        "MemberName": f"Fantuan: {response['data']['orderNo']}", # Name不用跟JZZP对应所以填成短订单号，打出来的单就有写订单号了
        "Items": items,
        "CompanyID": merch_id,
        "UserID": "167225002936801673"
    }
    headers = {"Cookie": "user_app_id=web; user_web=167225002936801673; hash_web=5d95b5c7e70cdc9b799d918e52ee167b"}
    r = requests.post(url="http://tg2.weimember.cn/mb/member.api.ljson?api=mn.order&act=create", data=json.dumps(d),
                      headers=headers)
    # 第二次发送，支付，要用到第一次返回的JZZP生成的order id
    try:
        data2 = {"OrderID": json.loads(r.text)['data']['OrderID']}
    except Exception as e:
        logging.exception(d)
        logging.exception(r.text)
        if json.loads(r.text)['err'].__contains__("库存数量不足"):
            return json.loads(r.text)['err']
        return
    # r2 = requests.post(url="http://tg2.weimember.cn/mb/member.api.ljson?api=mn.order&act=pay", json=data2,
    #                    headers=headers)
    # logging.info(r2.text)
    print(f"Fantuan: Order {order_id} is sent to JZZP.")
    old_orders.insert(0, order_id)
    old_orders = old_orders[:20]
    with open("fantuan_lastorder.txt", "w") as f:
        for line in old_orders:
            f.write(str(line) + "\n")
        f.close()

    # 把订单保存到数据库
    try:
        data = dict()
        data["order_id"] = order_id
        data["platform"] = "fantuan"
        data["displayed_id"] = response['data']['orderNo']
        # data["store"] = dict(id="54321", name="Homelink Express")
        # data["eater"] = dict(name="", phone="", phone_code="", delivery = dict(location=dict(), type="", notes=""))
        data["cart"] = dict(items=items, products_quantity=len(items))
        # data["payment"] = dict(total=price.split("（")[0],delivery_fee="",tip="")
        data["placed_at"] = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        data["branch_id"] = branch_id
        data["merch_id"] = merch_id
        data["price"] = price
        header = {"Content-Type":"application/json"}
        response = requests.post(url='http://autoin.trinalgenius.co.uk:8000/order/new',headers=header,data=json.dumps(data), timeout=5)
        # response = requests.post(url='http://3.11.136.6:8000/order/new',json=data)
    except:
        pass