from DrissionPage import ChromiumOptions, ChromiumPage
import time
import pymssql
import requests
import configparser
import json
import logging

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

def initial_panda():
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

    co = ChromiumOptions().set_local_port(9132)
    # 用 d 模式创建页面对象（默认模式）
    if headless_flag == "True":
        co = ChromiumOptions().headless()
        page = ChromiumPage(co)
        # page.quit()
    else:
        page = ChromiumPage(co)

    time.sleep(5)

    page.get('https://merchant-uk.hungrypanda.co/login')
    time.sleep(15)
    try:
        if page.url != "https://merchant-uk.hungrypanda.co/goods/list":
            print(page.url)
            page.ele('#phone').clear()
            page.ele('#password').clear()
            page.ele('#phone').input(username)
            time.sleep(2)
            page.ele('#password').input(password)
            time.sleep(2)
            page.ele('.ant-btn ant-btn-primary ant-btn-lg ant-btn-block').click()

        else:
            page.get('https://merchant-uk.hungrypanda.co/order/ordermanage')
            time.sleep(5)
            return True
    except:
        print("HungryPanda is not valid, \n please log your \nHungryPanda info again.")
        return False

def panda_drAPI():

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

    co = ChromiumOptions().set_local_port(9132)
    # 用 d 模式创建页面对象（默认模式）
    if headless_flag == "True":
        co = ChromiumOptions().headless()
        page = ChromiumPage(co)
        # page.quit()
    else:
        page = ChromiumPage(co)

    time.sleep(5)

    page.get('https://merchant-uk.hungrypanda.co/login')
    time.sleep(15)
    try:
        if page.url != "https://merchant-uk.hungrypanda.co/goods/list":
            print(page.url)
            page.ele('#phone').clear()
            page.ele('#password').clear()
            page.ele('#phone').input(username)
            time.sleep(2)
            page.ele('#password').input(password)
            time.sleep(2)
            page.ele('.ant-btn ant-btn-primary ant-btn-lg ant-btn-block').click()

        else:
            page.get('https://merchant-uk.hungrypanda.co/order/ordermanage')
            time.sleep(5)
    except:
        print("HungryPanda is not valid, \n please log your \nHungryPanda info again.")


    page.ele('.ant-menu-title-content').click()
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


    try:
        for i in range(1, 11):
            for j in range(3):
                try:
                    order_id=page.ele('xpath=//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr['+str(i)+']/td[1]').text
                    status_id=page.ele('xpath=//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr['+str(i)+']/td[5]').text
                    break
                except Exception as e:
                    Logger.error(e)
                    time.sleep(5)

            print(order_id,status_id)
            if order_id not in old_orders and status_id == "Done" and order_id != "No Data":
                vbtn= page.ele('xpath=//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr['+str(i)+']/td[6]/a')
                vbtn.click()
                divs = page.eles('.goods-detail')
                items = []
                for div in divs:
                    product_name = div.ele('.product-name').text
                    # 定位方括号的位置
                    start_index = product_name.find("[")
                    end_index = product_name.find("]")

                    # 如果找到方括号，则提取方括号内的内容（字母部分）
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


                    else:
                        menu_id = int(menu_id) if menu_id.isdigit() else 1990  # 如果 menu_id 不是数字，则初始值为 1990
                        menu_name = product_name

                    for n in range(3):
                        try:
                            menucountstr = div.ele('.product-count').text
                            menucount = int(menucountstr.replace('*', ''))
                            menupricestr = div.ele('.product-price').text
                            menuprice = float(menupricestr.replace('£', ''))
                            menuamtstr = page.ele('.ant-collapse-extra').text
                            menuamt = float(menuamtstr.replace('£', ''))
                            break
                        except Exception as e:
                            Logger.error(e)
                            time.sleep(5)
                    try:
                        # total_amount += float(menu[i + 2][1:])
                        item = {
                            "ParentID": "SP1010",  # 随便，但不能为空
                            "MenuID": menu_id,
                            "MenuName": menu_name,
                            "MenuUnit": ".",
                            "MenuPrice": menuprice/menucount,
                            "MenuPriceOld": menuprice/menucount,
                            "MenuQty": menucount,
                            "MenuAmt": menuamt,
                            "MenuService": 0,
                            "SumOfService": 0,
                            "CookList": [],
                            "MenuList": []
                        }
                        items.append(item)
                    except Exception as e:
                        logging.exception(e)
                        # logging.exception(menu)
                vbtn_order = page.ele('@data-icon=close')
                vbtn_order.click()
                dd = {
                    "AppID": "web",  # 固定
                    "AppType": "web",  # 固定
                    "PayType": "mbpay",  # 固定
                    "BranchID": branch_id,  # 读取setting配置文件
                    "TableID": "992",  # 固定
                    "TableName": "Panda",  # 固定
                    "BillType": 3,  # 固定
                    "ServiceRate": 0,  # 固定
                    "SumOfService": 0,  # 固定
                    "TotalPoint": 0,  # 固定
                    "TotalAmt": menuamt * commission,  # netPayout
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
                print(dd)
                headers = {"Cookie": "user_app_id=web; user_web=167225002936801673; hash_web=5d95b5c7e70cdc9b799d918e52ee167b"}
                r = requests.post(url="http://tg2.weimember.cn/mb/member.api.ljson?api=mn.order&act=create",
                                  data=json.dumps(dd), headers=headers)
                print(r.text)
                try:
                    data2 = {"OrderID": json.loads(r.text)['data']['OrderID']}
                except Exception as e:
                    logging.exception(e)
                    logging.exception(r.text)
                    if json.loads(r.text)['err'].__contains__("库存数量不足"):
                        print("库存数量不足")

                r2 = requests.post(url="http://tg2.weimember.cn/mb/member.api.ljson?api=mn.order&act=pay", json=data2,
                                   headers=headers)
                print(r2.text)
                print(f"HungryPanda: Order {order_id} is sent to JZZP.")
                time.sleep(5)
                old_orders.insert(0, order_id)
                old_orders = old_orders[:30]
                with open("hungrypanda_lastorder.txt", "w") as f:
                    for l in old_orders:
                        f.write(str(l) + "\n")
                    f.close()


    except Exception as e:
        print(e)
        print("失败")







# for i in range(1, 11):
#     # 构造XPath
#     # xpath = '//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]'
#
#     # 定位到元素并点击
#     element = page.ele('xpath//*[@id="root"]/div/div[2]/div/div/div[2]/div/div[2]/div[2]/div/div/div/div/div/div/table/tbody/tr[1]/td[6]/a')
#     element.click()
#     time.sleep(3)




