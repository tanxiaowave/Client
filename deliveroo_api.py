import requests
import json
import tkinter as tk
import pymssql
import logging
import time
import configparser
from datetime import datetime

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
try:
    brandId = reader.get("Deliveroo_Branch", "brandId")
except:
    pass
try:
    database_flag = eval(reader.get("Database", "flag"))
except:
    database_flag = True

def deliveroo_API():
    logging.basicConfig(level='INFO', filename='test.log',
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filemode='a')

    # exchange credentials to get token
    try:
        url = "https://auth.developers.deliveroo.com/oauth2/token"
        payload = "grant_type=client_credentials"
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "authorization": "Basic N2VjdWZiajhyYTI2OXJsNDkxZzdrZTRjbnE6dG1zbmlhNmcwcTNtdmE3c2o3cjhkdmJ1NWQzdDhjczZvZGJhNG03cXI3aXVlNGZtbWRl"
        }
        response = requests.post(url, data=payload, headers=headers)
        token = json.loads(response.text)['access_token']

        # Then use the token to get orders
        iso_date = datetime.now().isoformat()[:11]
        url = f"https://api.developers.deliveroo.com/order/v2/brand/{brandId}/restaurant/{branchId}/orders?start_date={iso_date}00:00:00Z"
        headers = {
            "accept": "application/json",
            "authorization": "Bearer " + token
        }
        response = json.loads(requests.get(url, headers=headers).text)
    except Exception as e:
        logging.exception(e)
        return

    # deliveroo api limit: 10 times per minute
    try:
        if response['error']['code'] == 'too_many_requests':
            return
    except Exception as e:
        pass

    # 返回的订单列表是从老到新的，逆序一下再拿前十条
    try:
        orders = response['orders'][::-1][:10]
    except:
        print("No order today")
        return

    if len(orders) >= 1:
        # 读取旧订单
        try:
            with open("deliveroo_api_lastorder.txt", 'r') as f:
                old_orders = f.readlines()
            for i in range(len(old_orders)):
                old_orders[i] = old_orders[i].replace("\n", "")
            f.close()
        except:
            old_orders = []
            f = open('deliveroo_api_lastorder.txt', 'w')
            f.close()

        order_id = ""
        for o in orders:
            # 不是旧订单
            if o['id'] not in old_orders:
                try:
                    # status_log包含了整个过程的状态，例如10分已接受，15分配送中，20分送达，那会有三个状态在里面
                    status_list = o['status_log']
                    flag = False
                    for i in status_list:
                        # 如果状态是接受或确认，那就能发送
                        if i['status'] == 'accepted' or i['status'] == 'confirmed':
                            flag = True
                            break
                        elif i['status'] == 'canceled' or i['status'] == 'rejected':
                            old_orders.insert(0, o['id'])
                            old_orders = old_orders[:20]
                            with open("deliveroo_api_lastorder.txt", "w") as f:
                                for line in old_orders:
                                    f.write(str(line) + "\n")
                                f.close()
                            return
                    if flag == False:
                        continue
                except:
                    pass

                if o['asap'] == True:
                    # asap order
                    order_id = o['id']
                    display_id = o['display_id']
                    break
                else:
                    # schedule order
                    if datetime.now().isoformat() > o['start_preparing_at']:
                        # schedule order but already need to start preparing
                        order_id = o['id']
                        display_id = o['display_id']
                        break
                    else:
                        # schedule for later, store in txt file
                        old_orders.insert(0, o['id'])
                        old_orders = old_orders[:20]
                        with open("deliveroo_api_lastorder.txt", "w") as f:
                            for line in old_orders:
                                f.write(str(line) + "\n")
                            f.close()
                        try:
                            with open('deliveroo_schedule.txt', 'r') as f:
                                schedule_orders = f.readlines()
                                for i in range(len(schedule_orders)):
                                    schedule_orders[i] = schedule_orders[i].replace("\n", "")
                                f.close()
                        except FileNotFoundError:
                            schedule_orders = []
                            f = open('deliveroo_schedule.txt', 'w')
                            f.close()
                        schedule_orders.insert(0, o['id'])
                        msg = "Scheduled order " + o['id']
                        logging.info(msg)
                        with open("deliveroo_schedule.txt", "w") as f:
                            for o in schedule_orders:
                                f.write(str(o) + "\n")

        # if no new order in recent orders, check if there is any scheduled old order
        if order_id == "":
            try:
                with open('deliveroo_schedule.txt', 'r') as f:
                    schedule_orders = f.readlines()
                    for i in range(len(schedule_orders)):
                        schedule_orders[i] = schedule_orders[i].replace("\n", "")
                    f.close()
            except FileNotFoundError:
                schedule_orders = []
                f = open('deliveroo_schedule.txt', 'w')
                f.close()
            try:
                for o in schedule_orders:
                    # look up every schedule order
                    url = "https://auth.developers.deliveroo.com/oauth2/token"
                    payload = "grant_type=client_credentials"
                    headers = {
                        "accept": "application/json",
                        "content-type": "application/x-www-form-urlencoded",
                        "authorization": "Basic N2VjdWZiajhyYTI2OXJsNDkxZzdrZTRjbnE6dG1zbmlhNmcwcTNtdmE3c2o3cjhkdmJ1NWQzdDhjczZvZGJhNG03cXI3aXVlNGZtbWRl"
                    }
                    response = requests.post(url, data=payload, headers=headers)
                    token = json.loads(response.text)['access_token']
                    headers = {
                        "accept": "application/json",
                        "authorization": "Bearer " + token
                    }
                    url = f"https://api.developers.deliveroo.com/order/v2/orders/{o}"
                    response = json.loads(requests.get(url, headers=headers).text)
                    # if scheduled order is due, remove it from scheduled orders list and make it the one this loop is going to sent
                    if datetime.now().isoformat() > response['start_preparing_at']:
                        order_id = response['id']
                        display_id = response['display_id']
                        schedule_orders.remove(o)
                        msg = "Get out scheduled order " + o['id']
                        logging.info(msg)
                        with open("deliveroo_schedule.txt", "w") as f:
                            for oo in schedule_orders:
                                f.write(str(oo) + "\n")
                        break
            except Exception as e:
                logging.exception(e)
                return
            # no due scheduled order either, return
            if order_id == "":
                print("Deliveroo: No new order in recent 10 orders")
                return

    # 没有新订单的话上面就return了，能运行到这里就是有新订单(order_id 不为空)
    try:
        url = "https://auth.developers.deliveroo.com/oauth2/token"
        payload = "grant_type=client_credentials"
        headers = {
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded",
            "authorization": "Basic N2VjdWZiajhyYTI2OXJsNDkxZzdrZTRjbnE6dG1zbmlhNmcwcTNtdmE3c2o3cjhkdmJ1NWQzdDhjczZvZGJhNG03cXI3aXVlNGZtbWRl"
        }
        response = requests.post(url, data=payload, headers=headers)
        token = json.loads(response.text)['access_token']
        headers = {
            "accept": "application/json",
            "authorization": "Bearer " + token
        }
        url = f"https://api.developers.deliveroo.com/order/v2/orders/{order_id}"
        response = json.loads(requests.get(url, headers=headers).text)

        # 下面的获取订单内容，发送给H5，保存到数据库，跟fantuan里的差不多
        menu = response['items']
        items = []
        for item in menu:
            menu_id = item['operational_name'][item['operational_name'].find("[")+1:item['operational_name'].find("]")]
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

            i = {
                "ParentID": "SP1010",  # 随便，但不能为空
                "MenuID": menu_id,
                "MenuName": menu_name,
                "MenuUnit": ".",
                "MenuPrice": item['total_price']['fractional'] * 0.01,
                "MenuPriceOld": item['total_price']['fractional'] * 0.01,
                "MenuQty": item['quantity'],
                "MenuAmt": item['total_price']['fractional'] * 0.01 * item['quantity'],
                "MenuService": 0,
                "SumOfService": 0,
                "CookList": [],
                "MenuList": []
            }
            if 'modifiers' in item.keys() and len(item['modifiers']) > 0:
                CookList = []
                for modifier in item['modifiers']:
                    l = {
                        "id": "AutoIn",
                        "name": modifier['name'],
                        "price": 0,
                        "qty": modifier['quantity']
                    }
                    CookList.append(l)
                i["CookList"] = CookList
            items.append(i)
    except Exception as e:
        logging.exception(e)
        logging.exception(menu)
        return

    try:
        price_type = str(reader.get("Deliveroo_Branch", "price_type"))
    except:
        price_type = 'total_price'
    price = response[price_type]['fractional'] * 0.01

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
        "Remark": response['order_notes'] + " " + response['cutlery_notes'],
        "ServiceRate": 0,
        "SumOfService": 0,
        "TotalAmt": price * commission,
        "TotalPoint": 0,
        "MemberCardID": "888",  # 换成给每个平台创建的会员的会员号
        "MemberName": f"Deliveroo: {display_id}",
        "Items": items,
        "CompanyID": merch_id,
        "UserID": "167225002936801673"
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

    r2 = requests.post(url="http://tg2.weimember.cn/mb/member.api.ljson?api=mn.order&act=pay", json=data2,
                       headers=headers)
    logging.info(r2.text)
    print(f"Deliveroo: {display_id} is sent to JZZP.")
    old_orders.insert(0, order_id)
    old_orders = old_orders[:20]
    with open("deliveroo_api_lastorder.txt", "w") as f:
        for line in old_orders:
            f.write(str(line) + "\n")
        f.close()
    try:
        with open('deliveroo_lastorder.txt', 'r') as f:
            old_orders = f.readlines()
            for i in range(len(old_orders)):
                old_orders[i] = old_orders[i].replace("\n", "")
            old_orders.insert(0, '#' + display_id)
            old_orders = old_orders[:20]
            f.close()
    except FileNotFoundError:
        old_orders = []
        f = open('deliveroo_lastorder.txt', 'w')
        f.close()

    with open('deliveroo_lastorder.txt', 'w') as f:
        for l in old_orders:
            f.write(str(l) + "\n")
        f.close()

    try:
        data = dict()
        data["order_id"] = order_id
        data["platform"] = "deliveroo"
        data["displayed_id"] = display_id
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