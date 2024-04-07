from selenium import webdriver
import os
import time
import tkinter as tk
import tkinter.messagebox
import rsa
import threading
import json
import requests
import logging
import time
from datetime import datetime
import requests
import json
import tkinter as tk
import pymssql
import logging
import time
import configparser


# 录入熊猫账号密码
def pandaLogin(label):
    pri = rsa.PrivateKey(
        10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
        65537,
        7002712700928804011838917939227853273317722595990151016778949911089213823265260722795698382337717248876309656289331967090125041513510782458343001103454593,
        7165380796988618938065214954530466870443807483684172787495616047866899293086811303,
        1492014128088262667286826329565602575995354986910798283007464819843657741)
    try:
        with open("panda_username_info.txt", "rb") as f:
            password = f.readline()
            f.close()
        shop_id = rsa.decrypt(password, pri).decode('utf-8')
    except:
        shop_id = ""

    login = tk.Toplevel(bg="#272727")
    login.resizable(False, False)
    login.grab_set()
    login.iconbitmap("logo.ico")
    width, height = 300, 150
    login.title("Panda Login")
    login.geometry(
        f'{width}x{height}+{round(login.winfo_screenwidth() / 2 - width / 2)}+{round(login.winfo_screenheight() / 2 - height / 2)}')

    tk.Label(login, text=f'Current account username: {shop_id}', fg="white", bg="#272727").grid(row=0, columnspan=2, padx=10, pady=4)
    tk.Label(login, text='Username:', fg="white", bg="#272727").grid(row=1, padx=10)
    tk.Label(login, text='Password:', fg="white", bg="#272727").grid(row=2, padx=10)

    u = tk.Entry(login)
    u.grid(row=1, column=1, pady=10)
    p = tk.Entry(login)
    p.grid(row=2, column=1, pady=10)

    # 检查输入是否有效，有效的话调用加密保存函数
    def check_panda():
        nonlocal u, p
        username = u.get()
        password = p.get()
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument("--proxy-server='direct://'")
        options.add_argument("--proxy-bypass-list=*")
        options.add_argument('window-size=1920x1080')
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        driver = webdriver.Chrome('chromedriver', options=options)
        driver.get("https://merchant-uk.hungrypanda.co/login")
        time.sleep(1)
        _u = driver.find_element('id', 'phone')
        _u.send_keys(username)
        _p = driver.find_element('id', 'password')
        _p.send_keys(password)
        b = driver.find_element('xpath', '//*[@id="root"]/div/div/div/div/div/div/div/form/div[5]/div/div/div/button')
        b.click()
        time.sleep(1)
        if driver.current_url != "https://merchant-uk.hungrypanda.co/login":
            driver.quit()

            # 调用加密保存函数
            encrypt_and_store_p()

            label.config(text=" Logged In ", foreground="white", bg="#47A57D", bd=0)
        else:
            driver.quit()
            tk.messagebox.showinfo(title='Wrong account',
                                   message="The account information you have input for HungryPanda is not valid, please check and try again.")

    def encrypt_and_store_p():
        nonlocal u, p
        pub = rsa.PublicKey(
            10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
            65537)
        username = bytes(u.get(), 'utf-8')
        password = bytes(p.get(), 'utf-8')
        print(username, password)
        e_username = rsa.encrypt(username, pub)
        e_password = rsa.encrypt(password, pub)
        with open("panda_username_info.txt", "wb") as f:
            f.write(e_username)
            f.close()
        with open("panda_password_info.txt", "wb") as f:
            f.write(e_password)
            f.close()
        login.destroy()
        tk.messagebox.showinfo(title='Success!',
                               message="Login information for HungryPanda has been recorded.")

    tk.Button(login, fg="white", bg="#47A57D", text="    Enter    ", command=check_panda).grid(row=3, column=1)

    login.mainloop()


# 录入deliveroo登录账号密码，接了API之后没什么用了
def deliverooLogin(label):
    # pri = rsa.PrivateKey(
    #     10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
    #     65537,
    #     7002712700928804011838917939227853273317722595990151016778949911089213823265260722795698382337717248876309656289331967090125041513510782458343001103454593,
    #     7165380796988618938065214954530466870443807483684172787495616047866899293086811303,
    #     1492014128088262667286826329565602575995354986910798283007464819843657741)
    # try:
    #     with open("deliveroo_username_info.txt", "rb") as f:
    #         password = f.readline()
    #         f.close()
    #     shop_id = rsa.decrypt(password, pri).decode('utf-8')
    # except:
    #     shop_id = ""
    # login = tk.Toplevel(bg="#272727")
    # login.grab_set()
    # login.iconbitmap("logo.ico")
    # login.resizable(False, False)
    # width, height = 350, 150
    # login.title("Deliveroo Login")
    # login.geometry(
    #     f'{width}x{height}+{round(login.winfo_screenwidth() / 2 - width / 2)}+{round(login.winfo_screenheight() / 2 - height / 2)}')
    #
    # tk.Label(login, text=f'Current account username: {shop_id}', fg="white", bg="#272727").grid(row=0, columnspan=2, padx=10, pady=4)
    # tk.Label(login, text='Username:', fg="white", bg="#272727").grid(row=1, padx=10)
    # tk.Label(login, text='Password:', fg="white", bg="#272727").grid(row=2, padx=10)
    #
    # u = tk.Entry(login)
    # u.grid(row=1, column=1, pady=10)
    # p = tk.Entry(login)
    # p.grid(row=2, column=1, pady=10)
    #
    # # password = tk.Entry(login, textvariable=p, show="*")
    # # password.grid(row=1, column=1, pady=10)
    logging.basicConfig(level='INFO', filename='test.log',
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filemode='a')

    # exchange credentials to get token

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
        tk.messagebox.showinfo(title='Success!',
                                message="Login information for Deliveroo has been recorded.")
        label.config(text=" Logged In ", foreground="white", bg="#47A57D", bd=0)
    except Exception as e:
        logging.exception(e)
        # driver.quit()
        tk.messagebox.showinfo(title='Wrong account',
                                message="The account information you have input for Deliveroo is not valid, please check and try again.")
        return

    # def check_deliveroo():
    #     nonlocal u, p
    #     username = u.get()
    #     password = p.get()
    #     options = webdriver.ChromeOptions()
    #     options.add_argument(f'--headless')
    #     options.add_argument('--no-sandbox')
    #     options.add_argument("--proxy-server='direct://'")
    #     options.add_argument("--proxy-bypass-list=*")
    #     options.add_argument('window-size=1920x1080')
    #     options.add_argument("--log-level=3")
    #     options.add_argument("--silent")
    #     driver = webdriver.Chrome('chromedriver', options=options)
    #     driver.get("https://restaurant-hub.deliveroo.net/login")
    #     time.sleep(1)
    #     try:
    #         cookie_btn = driver.find_element('xpath', "//*[@id='onetrust-accept-btn-handler']")
    #         cookie_btn.click()
    #     except:
    #         print("Already accept cookies.")
    #     _u = driver.find_element('xpath', '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/label[1]/span/div/input')
    #     _u.send_keys(username)
    #     _p = driver.find_element('xpath', '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/label[2]/span/div/input')
    #     _p.send_keys(password)
    #     b = driver.find_element('xpath', '//*[@id="__next"]/div[1]/div[1]/div/form/div[2]/button')
    #     b.click()
    #     time.sleep(2)
    #     if driver.current_url != "https://restaurant-hub.deliveroo.net/login":
    #         driver.quit()
    #         encrypt_and_store_d()
    #         tk.messagebox.showinfo(title='Success!',
    #                                message="Login information for Deliveroo has been recorded.")
    #         label.config(text=" Logged In ", foreground="white", bg="#47A57D", bd=0)
    #     else:
    #         driver.quit()
    #         tk.messagebox.showinfo(title='Wrong account',
    #                                message="The account information you have input for Deliveroo is not valid, please check and try again.")
    #
    # def encrypt_and_store_d():
    #     nonlocal u, p
    #     pub = rsa.PublicKey(
    #         10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
    #         65537)
    #     username = bytes(u.get(), 'utf-8')
    #     password = bytes(p.get(), 'utf-8')
    #     print(username, password)
    #     e_username = rsa.encrypt(username, pub)
    #     e_password = rsa.encrypt(password, pub)
    #     with open("deliveroo_username_info.txt", "wb") as f:
    #         f.write(e_username)
    #         f.close()
    #     with open("deliveroo_password_info.txt", "wb") as f:
    #         f.write(e_password)
    #         f.close()
    #     login.destroy()
    #
    # tk.Button(login, fg="white", bg="#47A57D", text="   Enter   ", command=check_deliveroo).grid(row=3, column=1)

    login.mainloop()


# 录入api-key和商户id
def fantuanLogin(label):
    pri = rsa.PrivateKey(
        10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
        65537,
        7002712700928804011838917939227853273317722595990151016778949911089213823265260722795698382337717248876309656289331967090125041513510782458343001103454593,
        7165380796988618938065214954530466870443807483684172787495616047866899293086811303,
        1492014128088262667286826329565602575995354986910798283007464819843657741)
    try:
        with open("fantuan_shopid.txt", "rb") as f:
            password = f.readline()
            f.close()
        shop_id = rsa.decrypt(password, pri).decode('utf-8')
    except:
        shop_id = ""

    login = tk.Toplevel(bg="#272727")
    login.grab_set()
    login.resizable(False, False)
    width, height = 250, 150
    login.title("Fantuan Login")
    login.iconbitmap("logo.ico")
    login.geometry(
        f'{width}x{height}+{round(login.winfo_screenwidth() / 2 - width / 2)}+{round(login.winfo_screenheight() / 2 - height / 2)}')
    tk.Label(login, text=f'Current ShopID: {shop_id}', fg="white", bg="#272727").grid(row=0, columnspan=2, padx=10, pady=3)
    tk.Label(login, text='AppKey:', fg="white", bg="#272727").grid(row=2, padx=10)
    tk.Label(login, text='ShopID:', fg="white", bg="#272727").grid(row=1, padx=10)

    u = tk.Entry(login)
    u.grid(row=2, column=1, pady=10)
    p = tk.Entry(login)
    p.grid(row=1, column=1, pady=10)

    # password = tk.Entry(login, textvariable=p, show="*")
    # password.grid(row=1, column=1, pady=10)

    def check_fantuan():
        nonlocal u, p
        username = u.get()
        password = p.get()
        headers = {
            "Content-Type": "application/json",
            "appKey": username,
            "timestamp": "{{$timestamp}}",
        }
        data = {
            "shopId": password,
            "page": {
                "pageNum": 1,
                "pageSize": 5
            }
        }
        url = "https://openapi.fantuan.ca/api/v1/order/page"
        response = json.loads(requests.post(url, json=data, headers=headers).text)
        if response['code'] == 0:
            encrypt_and_store_f()
            tk.messagebox.showinfo(title='Success!',
                                   message="API information for Fantuan has been recorded.")
            label.config(text=" Logged In ", foreground="white", bg="#47A57D", bd=0)
        else:
            tk.messagebox.showinfo(title='Invalid!',
                                   message='The information for Fantuan API is not valid, please check and try again.')

    def encrypt_and_store_f():
        nonlocal u, p
        pub = rsa.PublicKey(
            10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
            65537)
        username = bytes(u.get(), 'utf-8')
        password = bytes(p.get(), 'utf-8')
        print(username, password)
        e_username = rsa.encrypt(username, pub)
        e_password = rsa.encrypt(password, pub)
        with open("fantuan_appkey.txt", "wb") as f:
            f.write(e_username)
            f.close()
        with open("fantuan_shopid.txt", "wb") as f:
            f.write(e_password)
            f.close()
        login.destroy()

    tk.Button(login, fg="white", bg="#47A57D", text="   Enter   ", command=check_fantuan).grid(row=3, column=1)

    # login.mainloop()


# 打开uberEats登录页面手动登录
def uberLogin(label, ublog):
    options = webdriver.ChromeOptions()
    options.add_argument(f'user-data-dir={os.getcwd()}/selenium')
    options.add_argument("--log-level=3")
    options.add_argument("--silent")
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get("https://merchants.ubereats.com/manager/orders")
    while True:
        try:
            if driver.current_url == "https://merchants.ubereats.com/manager/orders?effect=" or driver.current_url == "https://merchants.ubereats.com/manager/orders":
                driver.quit()
                tk.messagebox.showinfo(title='Message',
                                       message="Already logged in!")
                label.config(text=" Logged In ", foreground="white", bg="#47A57D", bd=0)
                break
        except:
            break
