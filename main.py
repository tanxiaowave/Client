import hashlib
import random
import signal
import subprocess
import tkinter as tk
import tkinter.font
import pymssql
import pyqrcode
import tempfile
from shutil import rmtree
from tkinter import StringVar, OptionMenu
from hungrypanda import hungrypandaScrape
from panda_dr import panda_drAPI, initial_panda
from deliveroo import deliverooScrape
from deliveroo_api import deliveroo_API
from fantuan import fantuanScrape
from ubereats import uberScrape
# from login import pandaLogin, deliverooLogin, fantuanLogin, uberLogin
from checkLogin import checklogin,checklogin_hun
import requests
import json
import threading
import time
from selenium import webdriver
import os
import logging
import configparser
from PIL import ImageTk, Image
from datetime import datetime
import datetime as dt
from win32event import CreateMutex
from win32api import CloseHandle, GetLastError
from winerror import ERROR_ALREADY_EXISTS
import sys
from run import APP


# 不知道从哪抄的
class singleinstance:
    # Limits application to single instance

    def __init__(self):
        self.mutexname = "testmutex_{D0E858DF-985E-4907-B7FB-8D732C3FC3B9}"
        self.mutex = CreateMutex(None, False, self.mutexname)
        self.lasterror = GetLastError()

    def alreadyrunning(self):
        return (self.lasterror == ERROR_ALREADY_EXISTS)

    def __del__(self):
        if self.mutex:
            CloseHandle(self.mutex)


# current version number
version = "1.2.1"
# Limits application to single instance
myapp = singleinstance()
if myapp.alreadyrunning():
    tk.messagebox.showinfo(title="Already running!",
                           message='You are trying to open a second instance of this software, please check if there is already one running!')
    sys.exit(1)
reader = configparser.ConfigParser()
reader.read("settings.INI")
server = reader.get("Database", "server")
user = reader.get("Database", "user")
sql_password = reader.get("Database", "password")
database = reader.get("Database", "database")
merch_id = reader.get("Store", "merchid")
branch_id = reader.get("Store", "branchid")
autostart_hp = eval(reader.get("Autostart", "HungryPanda"))
autostart_dr = eval(reader.get("Autostart", "Deliveroo"))
autostart_ue = eval(reader.get("Autostart", "UberEats"))
autostart_ft = eval(reader.get("Autostart", "Fantuan"))
try:
    deliveroo_mode = reader.get("Deliveroo_Branch", "mode")
except:
    deliveroo_mode = "Web"
try:
    frequency = int(reader.get("Frequency", "Frequency"))
except:
    if deliveroo_mode == "API":
        frequency = 5
    else:
        frequency = 1
try:
    server_address = reader.get("Server", "server_address")
    analysis_address = reader.get("Server", "analysis_address")
except:
    try:
        reader.add_section('Server')
    except:
        pass


logging.basicConfig(level='INFO', filename='test.log',
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', filemode='a')
# 这一句跟后面有句差不多的Program Closed很关键，因为很多店员明明自己早上不小心关了，快午休了才重新打开，然后说不出单的时候嘴硬说一直没关
logging.info("Program Start--------------version="+version)
# get latest version from server
# 尝试五次每次隔几秒，因为刚开机可能没网
count = 5
while count > 0:
    try:
        response = requests.get(url='http://autoin.trinalgenius.co.uk:8000/version')
        ver = response.text
        break
    except requests.exceptions.ConnectionError:
        count -= 1
        time.sleep(2)
if count == 0:
    tk.messagebox.showinfo(title="Connection Error!",
                               message='Connection to server failed! Please check your internet connection or contact us!')
    quit()


# get valid info from server
data = {
    'MerchID': merch_id,
    'BranchID': branch_id,
}
try:
    today = datetime.today().strftime("%Y-%m-%d")
    response = requests.post(url='http://autoin.trinalgenius.co.uk:8000/validate/validate', json=data)
    valid = json.loads(response.content)['ValidUntil']
    try:
        # xx_valid are the "valid until" text displayed on software interface
        hp_valid = json.loads(response.content)['HP_Valid']
        # xx are variables used in later code as flags
        hun = True
        if hp_valid < today:
            hun = False
    except:
        hp_valid = 'Not Valid'
        hun = False
    try:
        dr_valid = json.loads(response.content)['DR_Valid']
        de = True
        if dr_valid < today:
            de = False
    except:
        dr_valid = 'Not Valid'
        de = False
    try:
        ue_valid = json.loads(response.content)['UE_Valid']
        ub = True
        if ue_valid < today:
            ub = False
    except:
        ue_valid = 'Not Valid'
        ub = False
    try:
        ft_valid = json.loads(response.content)['FT_Valid']
        fan = True
        if ft_valid < today:
            fan = False
    except:
        ft_valid = 'Not Valid'
        fan = False
except Exception as e:
    # merch_id or branch_id doesn't exist
    valid = False
    hun, de, fan, ub = False, False, False, False

# 充值页面用的充值金额的下拉框选项
topup_options = ["One Month £15", "Half Year £72 (£12 Monthly)", "One Year £120 (£10/Monthly)"]
# 充值页面用的充值平台的下拉框选项
valid_channel = []
if hp_valid != "Not Valid":
    valid_channel.append("HungryPanda")
if dr_valid != "Not Valid":
    valid_channel.append("Deliveroo")
if ue_valid != "Not Valid":
    valid_channel.append("UberEats")
if ft_valid != "Not Valid":
    valid_channel.append("Fantuan")

# loopxx: controls if xx channel is monitored
# ublog: uberEat login status
loopde, loophun, loopfan, loopub, ublog = False, False, False, False, True

def loop():
    global loopde, loophun, loopfan, loopub, ublog
    global monitor_hungry, monitor_deliveroo, monitor_uber, monitor_fantuan
    while True:
        # 每次开始循环的时候更新一下last.txt，Autoin_Monitor会用到
        with open("last.txt", "w") as f:
            f.write(str(datetime.now()))
            f.write("\n")
            f.close()
        try:
            if loophun:
                # xxScrape()函数：搜一次xx平台的订单，只有登录信息失效了的时候会返回False
                # temp = initial_panda()
                # if temp == False:
                #     loophun = False
                #     login_hungry.config(text=" Log Now ", foreground="white", bg="#F36249")
                #     monitor_hungry.config(text="Stopped", foreground="#F36249")
                # 如果在发送订单给金字招牌H5的时候错误了返回了报错信息，返回值temp会是H5的报错信息
                try:
                    # 如果是库存数量不足，出一个置在最顶层的提示框
                    if temp.__contains__("库存数量不足"):
                        try:
                            top.destroy()
                        except:
                            pass
                        top = tk.Toplevel(wd)
                        top.title("线上库存不足！")
                        top.wm_attributes("-topmost", 1)
                        top.config(bg="#272727")
                        top.geometry(
                            f'{top.winfo_screenwidth()}x{40}+{round(top.winfo_screenwidth() / 2 - top.winfo_screenwidth() / 2)}+{round(top.winfo_screenheight() / 2 - 40 / 2)}')
                        label = tk.Label(top, text=temp, fg="#F36249", bg="#272727",
                                         font=tk.font.Font(size=12))
                        label.pack()
                except:
                    pass
        except Exception as e:
            logging.exception(e)

        try:
            if loopde:
                # 可以通过Settings.INI里的参数设置deliveroo_mode，也可以用advanced settings里的功能设置deliveroo_mode
                # 默认使用API，因为爬虫没更新了
                try:
                    deliveroo_mode = reader.get("Deliveroo_Branch", "mode")
                except:
                    deliveroo_mode = "API"
                if deliveroo_mode == "API":
                    temp = deliveroo_API()
                    time.sleep(40)
                    print("--------------")
                else:
                    temp = deliverooScrape()
                if temp == False:
                    login_deliveroo.config(text=" Log Now ", foreground="white", bg="#F36249")
                    loopde = False
                    monitor_deliveroo.config(text="Stopped", foreground="#F36249")
                try:
                    if temp.__contains__("库存数量不足"):
                        try:
                            top.destroy()
                        except:
                            pass
                        top = tk.Toplevel(wd)
                        top.title("线上库存不足！")
                        top.wm_attributes("-topmost", 1)
                        top.config(bg="#272727")
                        top.geometry(
                            f'{280}x{40}+{round(top.winfo_screenwidth() / 2 - 280 / 2)}+{round(top.winfo_screenheight() / 2 - 40 / 2)}')
                        label = tk.Label(top, text=temp, fg="#F36249", bg="#272727",
                                         font=tk.font.Font(size=12))
                        label.pack()
                except:
                    pass
        except Exception as e:
            logging.exception(e)

        # try:
        #     if loopub:
        #         temp = APP()
        #         if temp == False:
        #             loopub = False
        #             ublog = False
        #             login_uber.config(text=" Log Now ", foreground="white", bg="#F36249")
        #             monitor_uber.config(text="Stopped", foreground="#F36249")
        #             # login_status.tag_config("u", foreground="red")
        #             ublogin = tk.Toplevel(bg="#272727")
        #             ublogin.resizable(False, False)
        #             ublogin.grab_set()
        #             ublogin.focus_force()
        #             ublogin.wm_attributes("-topmost", 1)
        #             ublogin.title("Uber Eats logged out!")
        #             ublogin.geometry(
        #                 f'{280}x{80}+{round(ublogin.winfo_screenwidth() / 2 - 280 / 2)}+{round(ublogin.winfo_screenheight() / 2 - 80 / 2)}')
        #             tk.Label(ublogin, text='Uber Eats has logged out!\n Please manually login\n to Uber Eats platform again!', font=tk.font.Font(family="Arial", size=13), fg='#F37249', bg="#272727").pack()
        #         try:
        #             if temp.__contains__("库存数量不足"):
        #                 try:
        #                     top.destroy()
        #                 except:
        #                     pass
        #                 top = tk.Toplevel(wd)
        #                 top.title("线上库存不足！")
        #                 top.wm_attributes("-topmost", 1)
        #                 top.config(bg="#272727")
        #                 top.geometry(
        #                     f'{280}x{40}+{round(top.winfo_screenwidth() / 2 - 280 / 2)}+{round(top.winfo_screenheight() / 2 - 40 / 2)}')
        #                 label = tk.Label(top, text=temp, fg="#F36249", bg="#272727",
        #                                  font=tk.font.Font(size=12))
        #                 label.pack()
        #         except:
        #             pass
        # except Exception as e:
        #     logging.exception(e)

        try:
            if loopfan:
                temp = fantuanScrape()
                if temp == False:
                    loopfan = False
                    login_fantuan.config(text=" Log Now ", foreground="white", bg="#F36249")
                    monitor_fantuan.config(text="Stopped", foreground="#F36249")
                try:
                    if temp.__contains__("库存数量不足"):
                        try:
                            top.destroy()
                        except:
                            pass
                        top = tk.Toplevel(wd)
                        top.title("线上库存不足！")
                        top.wm_attributes("-topmost", 1)
                        top.config(bg="#272727")
                        top.geometry(
                            f'{280}x{40}+{round(top.winfo_screenwidth() / 2 - 280 / 2)}+{round(top.winfo_screenheight() / 2 - 40 / 2)}')
                        label = tk.Label(top, text=temp, fg="#F36249", bg="#272727",
                                         font=tk.font.Font(size=12))
                        label.pack()
                except:
                    pass
        except Exception as e:
            logging.exception(e)
        time.sleep(frequency)

# 各个平台的开始暂停函数，会绑定在 start 和 stop 按钮上
# 还有两个给start all 和 stop all
def startloophungry():
    global loophun, hun,loophun_thread
    loophun = hun
    # looppdt()
    loophun_thread=threading.Thread(target=looppdt, daemon=True)
    loophun_thread.start()
    time.sleep(5)
    # loophun_thread.join()
    if loophun:
        monitor_hungry.config(text="Monitoring", foreground="#47A57D")
    else:
        pass


def stoploophungry():
    global loophun
    loophun = False
    monitor_hungry.config(text="Stopped", foreground="#F36249")


def startloopdeliveroo():
    global loopde, de
    loopde = de
    # threading.Thread(target=loopdeliveroo, daemon=True).start()
    if loopde:
        monitor_deliveroo.config(text="Monitoring", foreground="#47A57D")
    else:
        pass


def stoploopdeliveroo():
    global loopde
    loopde = False
    monitor_deliveroo.config(text="Stopped", foreground="#F36249")


def startloopuber():
    global loopub, ub, ublog,ubereats_button

    loopub = ub
    # while True:
    if ubereats_button['state'] == 'normal':
        threading.Thread(target=loopubt, daemon=True).start()
    ubereats_button = tk.Button(wd, text=" Start ", command=startloopuber, font=fontStyle, fg='white', bg="#999999", state='disabled')
    # thread1.start()
        # thread1.join()
        # time.sleep(30)
        # print("-------------30-------------")
    if loopub:
        monitor_uber.config(text="Monitoring", foreground="#47A57D")

    else:
        pass


def stoploopuber():
    global loopub
    loopub = False
    monitor_uber.config(text="Stopped", foreground="#F36249")


def startloopfantuan():
    global loopfan, fan
    loopfan = fan
    # threading.Thread(target=loopfantuan, daemon=True).start()
    if fan:
        monitor_fantuan.config(text="Monitoring", foreground="#47A57D")
    else:
        pass


def stoploopfantuan():
    global loopfan
    loopfan = False
    monitor_fantuan.config(text="Stopped", foreground="#F36249")


def startloopall():
    global loophun, loopde, loopub, loopfan, hun, de, ub, fan, ublog
    # if not loophun:
    loophun = hun
    # threading.Thread(target=loophungry, daemon=True).start()
    if loophun:
        monitor_hungry.config(text="Monitoring", foreground="#47A57D")
    # if not loopde:
    loopde = de
        # threading.Thread(target=loopdeliveroo, daemon=True).start()
    if loopde:
        monitor_deliveroo.config(text="Monitoring", foreground="#47A57D")
    # if not loopub:
    loopub = ub and ublog and ue_valid
    if ublog == False:
        pass
        # threading.Thread(target=loopuber, daemon=True).start()
    if loopub:
        monitor_uber.config(text="Monitoring", foreground="#47A57D")
    # if not loopfan:
    loopfan = fan and ft_valid
        # threading.Thread(target=loopfantuan, daemon=True).start()
    if loopfan:
        monitor_fantuan.config(text="Monitoring", foreground="#47A57D")


def stoploopall():
    global loophun, loopde, loopub, loopfan
    loophun, loopde, loopub, loopfan = False, False, False, False
    if hun:
        monitor_hungry.config(text="Stopped", foreground="#F36249")
    if ub:
        monitor_uber.config(text="Stopped", foreground="#F36249")
    if de:
        monitor_deliveroo.config(text="Stopped", foreground="#F36249")
    if fan:
        monitor_fantuan.config(text="Stopped", foreground="#F36249")


# main window
wd = tk.Tk()
width, height = 970, 555
wd.title("AutoIn"+str(version))
wd.resizable(False, False)
wd.iconbitmap("logo.ico")
wd.config(background="#272727")
# set to be in the middle of the screen
wd.geometry(
    f'{width}x{height}+{round(wd.winfo_screenwidth() / 2 - width / 2)}+'
    f'{round(wd.winfo_screenheight() / 2 - height / 2)}')

# font style
fontStyle = tk.font.Font(family="Arial", size=12)
fontStyle_bold = tk.font.Font(family="Arial", size=15, weight="bold")

# 定义登录状态按钮，只是先定义，位置在最后设置
# hun 是在上面读取数据库里的有效信息的时候定义的，存在且没过期就是true
# 没过期就先放个checking，后面setlogin调用checklogin会再次设置各个 login_xx 按钮，过期了直接not valid
if hun:
    login_hungry = tk.Button(wd, text="Checking...", fg="#999999", background="#272727", font=fontStyle, bd=0)
else:
    login_hungry = tk.Button(wd, text=" Not Valid ", fg="white", background="#797979", font=fontStyle)
if ub:
    login_uber = tk.Button(wd, text="Checking...", fg="#999999", background="#272727", font=fontStyle, bd=0)
else:
    login_uber = tk.Button(wd, text=" Not Valid ", fg="white", background="#797979", font=fontStyle)
if de:
    login_deliveroo = tk.Button(wd, text="Checking...", fg="#999999", background="#272727", font=fontStyle, bd=0)
else:
    login_deliveroo = tk.Button(wd, text=" Not Valid ", fg="white", background="#797979", font=fontStyle)
if fan:
    login_fantuan = tk.Button(wd, text="Checking...", fg="#999999", background="#272727", font=fontStyle, bd=0)
else:
    login_fantuan = tk.Button(wd, text=" Not Valid ", fg="white", background="#797979", font=fontStyle)

def set_login():
    global login_hungry, login_fantuan, login_deliveroo, login_uber

    # 只有uber和hungrypanda要检查登录状态，因为饭团和deliveroo已经接入api
    if ub or hun:
        # checklogin 返回四个boolean值，对应四个平台登录信息
        h, u, d, f = checklogin(hun, ub, de, fan)
    else:
        # 不用检查登录状态（有效平台不包括uber和hungrypanda）的时候默认登录状态等于对应通道的有效信息
        h, u, d, f = hun, ub, de, fan

    if hun:
        # 除了设置文本，还设置了按钮绑定的函数

        # checklogin_hun(hun)

        if h:
            login_hungry.config(text=" Logged In ", foreground="white", bg="#47A57D", command=lambda: checklogin_hun(hun))
        else:
            login_hungry.config(text=" Log Now ", foreground="white", bg="#F37249",command=lambda: handle_login_hun(hun))

            def handle_login_hun(hun):
                result = checklogin_hun(hun)
                # 在这里处理返回的结果，可以根据需要进行其他操作
                print(result)
                if result:
                    # print("success")
                    login_hungry.config(text=" Logged In ", foreground="white", bg="#47A57D")
                else:
                    print("登录失败")

    if ub:
        if u:
            login_uber.config(text=" Logged In ", foreground="white", bg="#47A57D", command=lambda: uberLogin(login_uber, ublog))
        else:
            login_uber.config(text=" Log Now ", foreground="white", bg="#F37249", command=lambda: uberLogin(login_uber, ublog), bd=1)

    if de:
        if d:
            login_deliveroo.config(text=" Logged In ", foreground="white", bg="#47A57D", command=lambda: deliverooLogin(login_deliveroo))
        else:
            login_deliveroo.config(text=" Log Now ", foreground="white", bg="#F37249", command=lambda: deliverooLogin(login_deliveroo), bd=1)

    if fan:
        if f:
            login_fantuan.config(text=" Logged In ", foreground="white", bg="#47A57D", command=lambda: fantuanLogin(login_fantuan))
        else:
            login_fantuan.config(text=" Log Now ", foreground="white", bg="#F37249", command=lambda: fantuanLogin(login_fantuan), bd=1)

# 定义按钮右边的显示monitor状态的label，默认stopped，无效通道的monitor状态显示not valid
if hun:
    monitor_hungry = tk.Label(wd, text="Stopped", foreground="#F36249", background="#272727", font=fontStyle, width=10)
else:
    monitor_hungry = tk.Label(wd, text="Not Valid", foreground="#797979", background="#272727", font=fontStyle)
if ub:
    monitor_uber = tk.Label(wd, text="Stopped", foreground="#F36249", background="#272727", font=fontStyle, width=10)
else:
    monitor_uber = tk.Label(wd, text="Not Valid", foreground="#797979",
                            background="#272727", font=fontStyle)
if de:
    monitor_deliveroo = tk.Label(wd, text="Stopped", foreground="#F36249",
                                 background="#272727", font=fontStyle, width=10)
else:
    monitor_deliveroo = tk.Label(wd, text="Not Valid", foreground="#797979",
                                 background="#272727", font=fontStyle)
if fan:
    monitor_fantuan = tk.Label(wd, text="Stopped", foreground="#F36249",
                               background="#272727", font=fontStyle, width=10)
else:
    monitor_fantuan = tk.Label(wd, text="Not Valid", foreground="#797979",
                               background="#272727", font=fontStyle)

# 定义按钮
all_button = tk.Button(wd, text=f"Start All", command=startloopall, font=fontStyle, fg='white', bg="#47A57D")
all_stop_button = tk.Button(wd, text=f"Stop All", command=stoploopall, font=fontStyle, fg='white', bg="#F37249")
panda_button = tk.Button(wd, text=" Start ", command=startloophungry, font=fontStyle, fg='white', bg="#47A57D")
panda_stop_button = tk.Button(wd, text=" Stop ", command=stoploophungry, font=fontStyle, fg='white', bg="#F37249")
deliveroo_button = tk.Button(wd, text=" Start ", command=startloopdeliveroo, font=fontStyle, fg='white', bg="#47A57D")
deliveroo_stop_button = tk.Button(wd, text=" Stop ", command=stoploopdeliveroo, font=fontStyle, fg='white', bg="#F37249")
ubereats_button = tk.Button(wd, text=" Start ", command=startloopuber, font=fontStyle, fg='white', bg="#47A57D")
ubereats_stop_button = tk.Button(wd, text=" Stop ", command=stoploopuber, font=fontStyle, fg='white', bg="#F37249")
fantuan_button = tk.Button(wd, text=" Start ", command=startloopfantuan, font=fontStyle, fg='white', bg="#47A57D")
fantuan_stop_button = tk.Button(wd, text=" Stop ", command=stoploopfantuan, font=fontStyle, fg='white', bg="#F37249")

# 如果通道无效，把按钮设置成灰色
if not hun:
    panda_button = tk.Button(wd, text=" Start ", command=startloophungry, font=fontStyle, fg='white', bg="#999999")
    panda_stop_button = tk.Button(wd, text=" Stop ", command=startloophungry, font=fontStyle, fg='white', bg="#999999")
if not ub:
    ubereats_button = tk.Button(wd, text=" Start ", command=startloopuber, font=fontStyle, fg='white', bg="#999999")
    ubereats_stop_button = tk.Button(wd, text=" Stop ", command=startloopuber, font=fontStyle, fg='white', bg="#999999")
if not de:
    deliveroo_button = tk.Button(wd, text=" Start ", command=startloopdeliveroo, font=fontStyle, fg='white', bg="#999999")
    deliveroo_stop_button = tk.Button(wd, text=" Stop ", command=startloopdeliveroo, font=fontStyle, fg='white', bg="#999999")
if not fan:
    fantuan_button = tk.Button(wd, text=" Start ", command=startloopfantuan, font=fontStyle, fg='white', bg="#999999")
    fantuan_stop_button = tk.Button(wd, text=" Stop ", command=startloopfantuan, font=fontStyle, fg='white', bg="#999999")


#定义线程开始函数

def loopubt():

    # for i in range(700):
    app_instance = APP()
        # time.sleep(60)
        # print("-------------60-------------")
def looppdt():
    print("looppdt thread started")
    app_instance = panda_drAPI()




# 设置循环频率
def frequency_setting(root):
    global frequency
    login = tk.Toplevel(bg="#272727")
    login.grab_set()
    login.focus_force()
    login.resizable(False, False)
    width, height = 280, 120
    login.title("Frequency Setting")
    login.geometry(
        f'{width}x{height}+{round(login.winfo_screenwidth() / 2 - width / 2)}+{round(login.winfo_screenheight() / 2 - height / 2)}')
    tk.Label(login, text=f'Current Frequency: {frequency} second(s)', fg="white", bg="#272727").grid(row=0, columnspan=2, pady=5)
    tk.Label(login, text='New Frequency:', fg="white", bg="#272727").grid(row=1, padx=10)

    u = tk.Entry(login)
    u.grid(row=1, column=1, pady=5)

    # 保存
    def keep_frequency():
        global frequency
        nonlocal u
        frequency = int(u.get())
        if frequency > 60:
            frequency = 60
            tk.messagebox.showinfo(title='Bad frequency',
                                   message="Frequency should not be larger than 60 seconds.\n"
                                           "It has now been set to 60 seconds.")
        try:
            reader.add_section('Frequency')
        except:
            pass
        reader.set('Frequency', 'frequency', frequency)
        with open('settings.INI', 'w+') as configfile:  # save
            reader.write(configfile)
        login.destroy()
        root.destroy()

    tk.Button(login, text="   Enter   ", command=keep_frequency).grid(row=2, column=1, pady=5)
    login.mainloop()


# advance setting 里的 open a browser
def open_browser():

    def op():
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-data-dir={os.getcwd()}/selenium')
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        driver = webdriver.Chrome('chromedriver', options=options)
        while True:
            try:
                driver.current_url
            except:
                break

    threading.Thread(target=op, daemon=True).start()


# advance settings 里的测试数据库连接
def testSQL():
    try:
        connect = pymssql.connect(server=server, user=user, password=sql_password, database=database,tds_version='7.0',)
        tk.messagebox.showinfo(title='SQL connection Succeeded!',
                               message='SQL connection Succeeded!')
    except:
        logging.exception([server, user, sql_password, database])
        tk.messagebox.showinfo(title='SQL connection Failed!',
                               message='SQL connection Failed!')


# advanced settings 里的设置deliveroo_mode， API或者Web
def deliveroo_setting():
    deliveroo_choose = tk.Toplevel()
    deliveroo_choose.config(background="#272727")
    deliveroo_choose.grab_set()
    deliveroo_choose.focus_force()
    deliveroo_choose.wm_title("Choose")
    deliveroo_choose.iconbitmap("logo.ico")
    width, height = 400, 160
    deliveroo_choose.geometry(
        f'{width}x{height}+{round(deliveroo_choose.winfo_screenwidth() / 2 - width / 2)}+{round(deliveroo_choose.winfo_screenheight() / 2 - height / 2)}')
    tk.Label(deliveroo_choose, text="Chosse how to inquire Deliveroo orders", fg="white", bg="#272727", width=40,
             font=tk.font.Font(size=12, weight="bold", family="Arial")).grid(row=0, column=0, pady=10)

    choice_v = StringVar(deliveroo_choose)
    try:
        mode = reader.get("Deliveroo_Branch", "mode")
    except:
        mode = ""
    choice_v.set(mode)
    choice_e = OptionMenu(deliveroo_choose, choice_v, 'Web', 'API')
    choice_e.config(width=20, font=tk.font.Font(size=10, family="Arial"))
    choice_e.grid(row=1, column=0, pady=8)

    def save():
        nonlocal choice_v, deliveroo_choose
        global reader

        try:
            reader.add_section('Deliveroo_Branch')
        except:
            pass
        reader.set('Deliveroo_Branch', 'mode', choice_v.get())
        with open('settings.INI', 'w+') as configfile:  # save
            reader.write(configfile)

        deliveroo_choose.destroy()

    tk.Button(deliveroo_choose, text=" Confirm ", width=8, fg="white", bg="#47A57D",
              font=tk.font.Font(size=12, family="Arial"),
              command=save).grid(row=2, pady=10)


# advanced settings 界面
def settings():
    login = tk.Toplevel()
    login.resizable(False, False)
    login.grab_set()
    login.focus_force()
    w, h = 250, 250
    login.title("Advanced Settings")
    login.config(background="#272727")
    login.geometry(
        f'{w}x{h}+{round(login.winfo_screenwidth() / 2 - w / 2)}+{round(login.winfo_screenheight() / 2 - h / 2)}')
    frequency_btn = tk.Button(login, fg="white", bg="#47A57D", text="Frequency setting", command=lambda: frequency_setting(login), font=fontStyle)
    frequency_btn.grid(row=0, padx=0, pady=15)
    browser_btn = tk.Button(login, fg="white", bg="#47A57D", text="Open a browser", command=open_browser, font=fontStyle)
    browser_btn.grid(row=1, padx=20, pady=15)
    browser_btn = tk.Button(login, fg="white", bg="#47A57D", text="Test SQL Connection", command=testSQL, font=fontStyle)
    browser_btn.grid(row=2, padx=50, pady=15)
    deliveroo_choosing_btn = tk.Button(login, fg="white", bg="#47A57D", text="Deliveroo Setting", command=deliveroo_setting,
                            font=fontStyle)
    deliveroo_choosing_btn.grid(row=3, padx=50, pady=15)


# 打开AutoIn的后台管理页面
def open_analysis_website():
    def o():
        options = webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--silent")
        driver = webdriver.Chrome('chromedriver', options=options)
        driver.get("http://autoin.trinalgenius.co.uk:9528/")
        # driver.execute_script(f"sessionStorage.setItem('username', {merch_id});")
        # driver.execute_script(f"sessionStorage.setItem('branchname', {branch_id});")
        username = driver.find_element("xpath", '//*[@id="app"]/div/div[2]/div/div/div[2]/form/div[1]/div/div/input')
        username.send_keys(merch_id)
        branchname = driver.find_element("xpath", '//*[@id="app"]/div/div[2]/div/div/div[2]/form/div[2]/div/div[1]/input')
        branchname.send_keys(branch_id)
        password = driver.find_element("xpath", '//*[@id="app"]/div/div[2]/div/div/div[2]/form/div[3]/div/div[1]/input')
        password.send_keys(branch_id+"1001")
        driver.find_element("xpath", '//*[@id="app"]/div/div[2]/div/div/div[2]/form/div[4]/div/button').click()

        while True:
            try:
                driver.current_url
            except:
                break

    threading.Thread(target=o, daemon=True).start()


# 更新，打开更新程序，更新程序包含了关闭所有chrome和autoin
def update():
    subprocess.Popen("AutoIn_Update.exe")
    os.kill(os.getpid(), signal.SIGINT)


# 关闭一个窗口，不是关闭程序
def close(login):
    login.destroy()


# 检查更新
def check_update():
    if ver > version:
        update_info = requests.get(url='http://autoin.trinalgenius.co.uk:8000/version_info').text
        login = tk.Toplevel(bg="#272727")
        login.grab_set()
        login.focus_force()
        login.resizable(False, False)
        width, height = 480, 250
        login.title("Update Available!")
        update_info = requests.get(url='http://autoin.trinalgenius.co.uk:8000/version_info').text
        height = height + 20 * len(update_info) % 50 + 20
        login.geometry(
            f'{width}x{height}+{round(login.winfo_screenwidth() / 2 - width / 2)}+{round(login.winfo_screenheight() / 2 - height / 2)}')
        tk.Label(login, text='There is a new version of AutoIn.\n'
                             '有可用新版本更新！\n'
                             'Do you want to update to the latest version?'
                             ' It should take no more than 1 minute. (Suggested).\n'
                             '是否更新？仅需大约一分钟（建议更新）\n\n' + update_info,
                 wraplength=400, justify="left", fg="white", bg="#272727",
                 font=tk.font.Font(family="Arial", size=10)).grid(row=0, column=0, padx=30, pady=30, columnspan=4)
        # 更新
        tk.Button(login, text="Yes", command=update, fg="white", bg="#47A57D", width=15).grid(row=1, column=2)
        # 关闭“是否更新”的窗口
        tk.Button(login, text="No", command=lambda: close(login), fg="white", bg="#F37249", width=15).grid(row=1,
                                                                                                           column=3)
    else:
        tk.messagebox.showinfo('Lateset Version!',
                               'v' + ver +
                               '\nYou are runing the latest version.' +
                               '\n已是最新版本，暂无可用更新。')


# 二维码窗口
def topup(platform,months):
    # default price 15 for Top-up
    price = 15
    if months == "One Month £15":
        months = 1
        price = 15
    elif months == "Half Year £72 (£12 Monthly)":
        months = 6
        price = 72
    elif months == "One Year £120 (£10/Monthly)":
        months = 12
        price = 120

    # 生成12位随机字符串用作调用tgpay api时使用的交易号
    rand12nums = ""
    for i in range(12):
        rand12nums += str(random.randint(0, 9))

    # notify_url不知道干什么的，但是一定要有，其他参数可以看tgpay api文档
    args = "access_type=cashier" + \
           "&channel_type=online" + \
           "&goods_name=" + platform + str(months) + \
           "&language=cn" + \
           "&merchants_id=202109208001" + \
           "&notify_url=http://autoin.trinalgenius.co.uk:8000/validate/" + merch_id + "/" + branch_id + "/" + platform + "/" + str(months) + \
           "&out_trade_no=202109208001" + rand12nums + \
           "&pay_type=bankcard" + \
           "&redirect_url=http://autoin.trinalgenius.co.uk:8000/validate/" + merch_id + "/" + branch_id + "/" + platform + "/" + str(months) + \
           "&return_url=http://autoin.trinalgenius.co.uk:9528/" + \
           "&terminal_type=web" + \
           "&trans_amount=" + str(price) + "&trans_timeout=20"
    token = "f1s8fqxtkagtvodbsknbwuimog5wv58v"
    temp = args + token
    sign = hashlib.md5(temp.encode('utf-8')).hexdigest()
    url = "https://api.tgpaypro.com/v2/tgpaybankcard.php?" + args + "&sign=" + sign + "&sign_type=MD5"
    response = requests.get(url)
    data = response.text
    pay_url = data[data.find("<pay_url>") + 9:data.find("</pay_url>")]
    topup_win = tk.Toplevel()
    topup_win.grab_set()
    topup_win.focus_force()
    topup_win.iconbitmap("logo.ico")
    # topup_win.resizable(False,False)
    topup_win.geometry(
        f'{300}x{440}+{round(topup_win.winfo_screenwidth() / 2 - 300 / 2)}+{round(topup_win.winfo_screenheight() / 2 - 440 / 2)}')
    # 把付款页面做成png存到本地在展示出来
    pyqrcode.create(pay_url).png("top_up_QR_temp.png")
    img = ImageTk.PhotoImage(Image.open(r'top_up_QR_temp.png').resize([300, 300]))

    # month 跟 months 的区别而已
    if months == 1:
        tk.Label(topup_win, text="Prolong " + platform + " channel\nvalidation for " + str(months) + " month",
                 font=tk.font.Font(size=11, weight="bold", family="Arial")).pack(pady=10)
    else:
        tk.Label(topup_win, text="Prolong " + platform + " channel\nvalidation for " + str(months) + " months",
                 font=tk.font.Font(size=11, weight="bold", family="Arial")).pack(pady=10)

    tk.Label(topup_win, image=img).pack()
    topup_win.image = img
    tk.Label(topup_win, text="Price: £" + str(price), font=tk.font.Font(size=12, weight="bold", family="Arial")).pack()
    tk.Label(topup_win, fg="#F37249", text="After successful payment, please restart\nthe software to see updated valid info.", font=tk.font.Font(size=10, weight="bold", family="Arial")).pack()

    # 关闭二维码窗口时更新有效信息，所以要付完款才关闭二维码，才能刷新有效时间
    def topup_on_closing():
        global hun, de, ub, fan, valid, hp_valid, dr_valid, ue_valid, ft_valid
        global hun_valid_label, dr_valid_label, ue_valid_label, ft_valid_label
        global monitor_hungry, monitor_deliveroo, monitor_uber, monitor_fantuan
        global panda_button, panda_stop_button, deliveroo_button, deliveroo_stop_button
        global ubereats_button, ubereats_stop_button, fantuan_button, fantuan_stop_button
        nonlocal topup_win
        try:
            today = datetime.today().strftime("%Y-%m-%d")
            data_temp = {
                'MerchID': merch_id,
                'BranchID': branch_id,
            }
            response = requests.post(url='http://autoin.trinalgenius.co.uk:8000/validate/validate', json=data_temp)
            valid = json.loads(response.content)['ValidUntil']
            try:
                hp_valid = json.loads(response.content)['HP_Valid']
                hun = True
                if hp_valid < today:
                    hun = False
            except:
                hp_valid = 'Not Valid'
                hun = False
            try:
                dr_valid = json.loads(response.content)['DR_Valid']
                de = True
                if dr_valid < today:
                    de = False
            except:
                dr_valid = 'Not Valid'
                de = False
            try:
                ue_valid = json.loads(response.content)['UE_Valid']
                ub = True
                if ue_valid < today:
                    ub = False
            except:
                ue_valid = 'Not Valid'
                ub = False
            try:
                ft_valid = json.loads(response.content)['FT_Valid']
                fan = True
                if ft_valid < today:
                    fan = False
            except:
                ft_valid = 'Not Valid'
                fan = False
        except Exception as e:
            valid = False
            hun, de, fan, ub = False, False, False, False

        # 重新设置有效日期label
        hun_valid_label.config(text=hp_valid, fg="white")
        dr_valid_label.config(text=dr_valid, fg="white")
        ue_valid_label.config(text=ue_valid, fg="white")
        ft_valid_label.config(text=ft_valid, fg="white")

        # 重新设置登录按钮
        if hun:
            login_hungry.config(text=" Logged In ", foreground="white", bg="#47A57D",
                                command=lambda: pandaLogin(login_hungry))
            monitor_hungry.config(text="Stopped", foreground="#F36249")
            panda_button.config(text=" Start ", command=startloophungry, font=fontStyle, fg='white',
                                     bg="#47A57D")
            panda_stop_button.config(text=" Stop ", command=stoploophungry, font=fontStyle, fg='white',
                                          bg="#F37249")
        if de:
            login_deliveroo.config(text=" Logged In ", foreground="white", bg="#47A57D",
                                   command=lambda: deliverooLogin(login_deliveroo))
            monitor_deliveroo.config(text="Stopped", foreground="#F36249")
            deliveroo_button.config(text=" Start ", command=startloopdeliveroo, font=fontStyle, fg='white',
                                         bg="#47A57D")
            deliveroo_stop_button.config(text=" Stop ", command=stoploopdeliveroo, font=fontStyle, fg='white',
                                              bg="#F37249")
        if ub:
            login_uber.config(text=" Logged In ", foreground="white", bg="#47A57D",
                              command=lambda: uberLogin(login_uber, ublog))
            monitor_uber.config(text="Stopped", foreground="#F36249")
            ubereats_button.config(text=" Start ", command=startloopuber, font=fontStyle, fg='white',
                                        bg="#47A57D")
            ubereats_stop_button.config(text=" Stop ", command=stoploopuber, font=fontStyle, fg='white',
                                             bg="#F37249")
        if fan:
            login_fantuan.config(text=" Logged In ", foreground="white", bg="#47A57D", command=lambda: fantuanLogin(login_fantuan))
            monitor_fantuan.config(text="Stopped", foreground="#F36249")
            fantuan_button.config(text=" Start ", command=startloopfantuan, font=fontStyle, fg='white',
                                       bg="#47A57D")
            fantuan_stop_button.config(text=" Stop ", command=stoploopfantuan, font=fontStyle, fg='white',
                                            bg="#F37249")

        topup_win.destroy()

    topup_win.protocol("WM_DELETE_WINDOW", topup_on_closing)


# 用来预览充值后的有效期的
def increase_month(d, month):
    temp = d.split("-")
    d = dt.date(year=int(temp[0]), month=int(temp[1]), day=int(temp[2]))
    if d < dt.date.today():
        d = dt.date.today()
    month += d.month
    if month > 12:
        month -= 12
        year = d.year + 1
    else:
        year = d.year
    day = d.day
    try:
        res = dt.date(year=year, month=month, day=day)
    except:
        try:
            res = dt.date(year=year, month=month, day=30)
        except:
            res = dt.date(year=year, month=month, day=28)
    return res.strftime("%Y-%m-%d")


# 用来预览充值后的有效期的
def setValid(label1, label2, platform, option):
    if platform == "HungryPanda":
        label1.config(text=hp_valid)
    if platform == "Deliveroo":
        label1.config(text=dr_valid)
    if platform == "UberEats":
        label1.config(text=ue_valid)
    if platform == "Fantuan":
        label1.config(text=ft_valid)
    if option == topup_options[0]:
        if platform == "HungryPanda":
            current = hp_valid
        if platform == "Deliveroo":
            current = dr_valid
        if platform == "UberEats":
            current = ue_valid
        if platform == "Fantuan":
            current = ft_valid
        label2.config(text=increase_month(current, 1))
    if option == topup_options[1]:
        if platform == "HungryPanda":
            current = hp_valid
        if platform == "Deliveroo":
            current = dr_valid
        if platform == "UberEats":
            current = ue_valid
        if platform == "Fantuan":
            current = ft_valid
        label2.config(text=increase_month(current, 6))
    if option == topup_options[2]:
        if platform == "HungryPanda":
            current = hp_valid
        if platform == "Deliveroo":
            current = dr_valid
        if platform == "UberEats":
            current = ue_valid
        if platform == "Fantuan":
            current = ft_valid
        label2.config(text=increase_month(current, 12))


# 充值窗口，top up all
def customized_topup():
    advanced_topup = tk.Toplevel()
    advanced_topup.config(background="#272727")
    advanced_topup.grab_set()
    advanced_topup.focus_force()
    advanced_topup.wm_title("Customized Top Up")
    advanced_topup.iconbitmap("logo.ico")
    width, height = 490, 370
    advanced_topup.geometry(
        f'{width}x{height}+{round(advanced_topup.winfo_screenwidth() / 2 - width / 2)}+{round(advanced_topup.winfo_screenheight() / 2 - height / 2)}')
    tk.Label(advanced_topup, text="Customized Top Up", fg="white", bg="#272727", width=40,
             font=tk.font.Font(size=15, weight="bold", family="Arial")).grid(row=0, column=0, columnspan=2, pady=10)

    tk.Label(advanced_topup, text="Platform:", fg="white", bg="#272727", width=20,
             font=tk.font.Font(size=12, family="Arial")).grid(row=1, column=0, pady=10)
    # _e是组件，_v是_e绑定的变量
    platform_v = StringVar(advanced_topup)
    platform_v.set("")
    tk.Label(advanced_topup, text="Current Due:", fg="white", bg="#272727", font=fontStyle).grid(row=2, pady=10)
    current_valid = tk.Label(advanced_topup, text="", fg="#F37249", bg="#272727", font=fontStyle)
    current_valid.grid(row=2, column=1)
    platform_e = OptionMenu(advanced_topup, platform_v, *valid_channel, command=lambda x: setValid(current_valid, new_valid, x, period_v.get()))
    platform_e.config(width=25, font=tk.font.Font(size=10, family="Arial"))
    platform_e.grid(row=1, column=1, pady=10)

    tk.Label(advanced_topup, text="Top-up Options:", fg="white", bg="#272727", width=20,
             font=tk.font.Font(size=12, family="Arial")).grid(row=3, column=0, pady=10)
    period_v = StringVar(advanced_topup)
    period_v.set(topup_options[0])  # default value
    tk.Label(advanced_topup, text="New Due:", fg="white", bg="#272727", font=fontStyle).grid(row=4, pady=10)
    new_valid = tk.Label(advanced_topup, fg="#47D57A", bg="#272727", font=fontStyle)
    new_valid.grid(row=4, column=1)
    period_e = OptionMenu(advanced_topup, period_v, *topup_options, command=lambda x: setValid(current_valid, new_valid, platform_v.get(), x))
    period_e.config(width=25, font=tk.font.Font(size=10, family="Arial"))
    period_e.grid(row=3, column=1, pady=10)

    tk.Label(advanced_topup, text="Payment method:", fg="white", bg="#272727", width=20,
             font=tk.font.Font(size=12, family="Arial")).grid(row=5, column=0, pady=10)
    payment_v = StringVar(advanced_topup)
    payment_v.set("Bank Card")  # default value
    payment_e = OptionMenu(advanced_topup, payment_v, "Bank Card")
    payment_e.config(width=25, font=tk.font.Font(size=10, family="Arial"))
    payment_e.grid(row=5, column=1, pady=10)

    tk.Button(advanced_topup, text="  Pay Now  ", width=10, fg="white", bg="#47A57D", font=tk.font.Font(size=12, family="Arial"),
              command=lambda:topup(platform_v.get(), period_v.get())).grid(row=6, columnspan=2, pady=15)


# 用来当作间隔的空label，只占位
empty_label = tkinter.Label(wd,text="",width=3,bg="#272727").grid(row=4,column=3)
empty_label = tkinter.Label(wd,text="",width=8,bg="#272727").grid(row=4,column=7)
# 0th row title
tk.Button(wd, text="Check Update", command=check_update, font=tk.font.Font(family="Arial", size=10), fg="white", bg="#797979").grid(row=0, column=0, columnspan=1, padx=10, pady=10)
tkinter.Label(wd, text="  Delivery Platform Monitoring System", fg="white", bg="#272727", font=fontStyle_bold).grid(row=0, columnspan=8, pady=20)
img = ImageTk.PhotoImage(Image.open(r'logo.png').resize([150, 60]))
tk.Label(wd, image=img, bg="#272727").grid(row=0, column=6, columnspan=3)
tk.Label(wd, text=f"V{version}\n\n\n", fg="white", bg="#272727", font=tk.font.Font(size=10)).grid(row=1, column=6, columnspan=3)
tk.Label(wd, text=".", fg="#272727", bg="#272727").grid(row=1,pady=20)
# 1st row current branch
current_branch_label = tk.Label(wd, text=f'Current Branch ID: {branch_id}                              ', fg="white", bg="#272727", font=tk.font.Font(family="Arial", size=11, weight="bold"))
if not valid:
    current_branch_label.config(fg="#F37249")
current_branch_label.grid(row=2, columnspan=2, padx=10)
tk.Button(wd, text="  Analysis Web  ", command=open_analysis_website, width=15, font=fontStyle, fg="white", bg="#909090").grid(row=2, column=6, columnspan=2)
# 2nd row column title
tk.Label(wd, text="Platform Name", background="#404040", font=fontStyle, fg="white", width=23, height=2, bd=2, relief="groove").grid(row=3, column=0,pady=10)
tk.Label(wd, text="Valid Until", background="#404040", font=fontStyle, fg="white", width=15, height=2, bd=2, relief="groove").grid(row=3, column=1, pady=10)
tk.Label(wd, text="Valid Login", background="#404040", font=fontStyle, fg="white", width=15, height=2, bd=2, relief="groove").grid(row=3, column=2, pady=10)
tk.Label(wd, text="Monitoring Status", background="#404040", font=fontStyle, fg="white", width=37, height=2, bd=2, relief="groove").grid(row=3, column=3, columnspan=4, pady=10)
tk.Label(wd, text="Payment", background="#404040", font=fontStyle, fg="white", width=14, height=2, bd=2, relief="groove").grid(row=3, column=7, pady=10)
# 3rd-6th 4 platforms content
tk.Label(wd, text="HungryPanda", background="#272727", fg="white", font=fontStyle).grid(row=4, pady=10)
if hun:
    delta = datetime.strptime(hp_valid, '%Y-%m-%d') - datetime.strptime(datetime.today().strftime("%Y-%m-%d"),
                                                                        '%Y-%m-%d')
    # 过期前五天，有效日期显示成红色
    if delta.days > 5:
        hun_valid_label = tk.Label(wd, text=hp_valid, foreground="white", background="#272727", font=fontStyle)
    else:
        hun_valid_label = tk.Label(wd, text=hp_valid, foreground="#F37249", background="#272727", font=fontStyle)
else:
    try:
        hun_valid_label = tk.Label(wd, text=hp_valid, fg="#999999", background="#272727", font=fontStyle)
    except:
        hun_valid_label = tk.Label(wd, text="Not Valid", fg="#999999", background="#272727", font=fontStyle)
hun_valid_label.grid(row=4, column=1, pady=10)
login_hungry.grid(row=4, column=2)
monitor_hungry.grid(row=4, column=4, padx=0)
panda_button.grid(row=4, column=5, pady=10)
panda_stop_button.grid(row=4, column=6, pady=10)
if hp_valid != "Not Valid":
    tk.Button(wd, text="Top-up", command=lambda:topup("HungryPanda","1"), font=tk.font.Font(family="Arial", size=14, underline=1), fg='#FFC27B', bg="#272727", bd=0).grid(row=4, column=7, padx=10)
else:
    # 通道没开通的话不能充值，充值了也用不了因为菜单啊什么的都要我们改
    tk.Button(wd, text="Top-up", font=tk.font.Font(family="Arial", size=14, underline=1), fg='#999999', bg="#272727", bd=0).grid(row=4, column=7, padx=10)

tk.Label(wd, text="Deliveroo", background="#272727", fg="white", font=fontStyle).grid(row=5, pady=10)
if de:
    delta = datetime.strptime(dr_valid, '%Y-%m-%d') - datetime.strptime(datetime.today().strftime("%Y-%m-%d"),
                                                                        '%Y-%m-%d')
    if delta.days > 5:
        dr_valid_label = tk.Label(wd, text=dr_valid, foreground="white", background="#272727", font=fontStyle)
    else:
        dr_valid_label = tk.Label(wd, text=dr_valid, foreground="#F37249", background="#272727", font=fontStyle)
else:
    try:
        dr_valid_label = tk.Label(wd, text=dr_valid, fg="#999999", background="#272727", font=fontStyle)
    except:
        dr_valid_label = tk.Label(wd, text="Not Valid", fg="#999999", background="#272727", font=fontStyle)
dr_valid_label.grid(row=5, column=1, pady=10)
login_deliveroo.grid(row=5, column=2)
monitor_deliveroo.grid(row=5, column=4)
deliveroo_button.grid(row=5, column=5, pady=10)
deliveroo_stop_button.grid(row=5, column=6, pady=10)
if dr_valid != "Not Valid":
    tk.Button(wd, text="Top-up", command=lambda:topup("Deliveroo","1"), font=tk.font.Font(family="Arial", size=14, underline=1), fg='#FFC27B', bg="#272727", bd=0).grid(row=5, column=7, padx=10)
else:
    tk.Button(wd, text="Top-up", font=tk.font.Font(family="Arial", size=14, underline=1), fg='#999999', bg="#272727", bd=0).grid(row=5, column=7, padx=10)

tk.Label(wd, text="Uber Eats", background="#272727", fg="white", font=fontStyle).grid(row=6, pady=10)
if ub:
    delta = datetime.strptime(ue_valid, '%Y-%m-%d') - datetime.strptime(datetime.today().strftime("%Y-%m-%d"),
                                                                        '%Y-%m-%d')
    if delta.days > 5:
        ue_valid_label = tk.Label(wd, text=ue_valid, foreground="white", background="#272727", font=fontStyle)
    else:
        ue_valid_label = tk.Label(wd, text=ue_valid, foreground="#F37249", background="#272727", font=fontStyle)
else:
    try:
        ue_valid_label = tk.Label(wd, text=ue_valid, fg="#999999", background="#272727", font=fontStyle)
    except:
        ue_valid_label = tk.Label(wd, text="Not Valid", fg="#999999", background="#272727", font=fontStyle)
ue_valid_label.grid(row=6, column=1, pady=10)
login_uber.grid(row=6, column=2)
monitor_uber.grid(row=6, column=4)
ubereats_button.grid(row=6, column=5, pady=10)
ubereats_stop_button.grid(row=6, column=6, pady=10)
if ue_valid != "Not Valid":
    tk.Button(wd, text="Top-up", command=lambda:topup("UberEats","1"), font=tk.font.Font(family="Arial", size=14, underline=1), fg='#FFC27B', bg="#272727", bd=0).grid(row=6, column=7, padx=10)
else:
    tk.Button(wd, text="Top-up", font=tk.font.Font(family="Arial", size=14, underline=1), fg='#999999', bg="#272727", bd=0).grid(row=6, column=7, padx=10)

tk.Label(wd, text="Fantuan", background="#272727", fg="white", font=fontStyle).grid(row=7, pady=10)
if fan:
    delta = datetime.strptime(ft_valid, '%Y-%m-%d') - datetime.strptime(datetime.today().strftime("%Y-%m-%d"),
                                                                        '%Y-%m-%d')
    if delta.days > 5:
        ft_valid_label = tk.Label(wd, text=ft_valid, foreground="white", background="#272727", font=fontStyle)
    else:
        ft_valid_label = tk.Label(wd, text=ft_valid, foreground="#F37249", background="#272727", font=fontStyle)
else:
    try:
        ft_valid_label = tk.Label(wd, text=ft_valid, fg="#999999", background="#272727", font=fontStyle)
    except:
        ft_valid_label = tk.Label(wd, text="Not Valid", fg="#999999", background="#272727", font=fontStyle)
ft_valid_label.grid(row=7, column=1, pady=10)
login_fantuan.grid(row=7, column=2)
monitor_fantuan.grid(row=7, column=4)
fantuan_button.grid(row=7, column=5, pady=10)
fantuan_stop_button.grid(row=7, column=6, pady=10)
if ft_valid != "Not Valid":
    tk.Button(wd, text="Top-up", command=lambda:topup("Fantuan","1"), font=tk.font.Font(family="Arial", size=14, underline=1), fg='#FFC27B', bg="#272727", bd=0).grid(row=7, column=7, padx=10)
else:
    tk.Button(wd, text="Top-up", font=tk.font.Font(family="Arial", size=14, underline=1), fg='#999999', bg="#272727", bd=0).grid(row=7, column=7, padx=10)
# 8th row
tk.Button(wd, text="Advanced Settings", command=settings, font=tk.font.Font(family="Arial", size=10), fg="white", bg="#797979").grid(row=8, column=0, columnspan=1, padx=10, pady=10)
tk.Button(wd, text="Start All", command=startloopall, font=tk.font.Font(family="Arial", size=10), fg="white", bg="#47A57D").grid(row=8, column=5, columnspan=1, pady=10)
tk.Button(wd, text="Stop All", command=stoploopall, font=tk.font.Font(family="Arial", size=10), fg="white", bg="#F37249").grid(row=8, column=6, columnspan=1, pady=10)
tk.Button(wd, text="Top Up All", command=customized_topup, font=tk.font.Font(family="Arial", size=13, underline=1), fg='#FFC27B', bg="#272727", bd=0).grid(row=8, column=7, padx=10)
# 9th row
tk.Label(wd, text="状态为Monitoring时，新的外卖订单将在店家接受订单1-2分钟后自动发送至金字招牌，营业期间请保持软件开启。", font=tk.font.Font(family="Arial", size=12), fg="white", bg="#272727").grid(row=9,columnspan=8, pady=5)
# 10th row
tk.Label(wd, text="When monitoring, new orders from takeaway food platform(s) will be sent to JZZP automatically in 1-2 minutes after accepted.", font=tk.font.Font(family="Arial", size=11), fg="white", bg="#272727").grid(row=10,columnspan=8,pady=5)
for file in os.listdir(tempfile.gettempdir()):
    if file.startswith("_MEI"):
        try:
            rmtree(os.path.join(tempfile.gettempdir(), file))
        except PermissionError:  # mainly to allow simultaneous pyinstaller instances
            print(1)


# 根据settings.ini参数来自动开始monitor
def autostart():
    if autostart_hp and hun:
        startloophungry()
    if autostart_dr and de:
        startloopdeliveroo()
    if autostart_ue and ub:
        startloopuber()
    if autostart_ft and fan:
        startloopfantuan()


# 启动时自动检查一次有没有新版本
def thread_function():
    # ask if user want to update or not
    global wd

    if ver > version:
        update_info = requests.get(url='http://autoin.trinalgenius.co.uk:8000/version_info').text
        login = tk.Toplevel(bg="#272727")
        login.grab_set()
        login.focus_force()
        login.resizable(False, False)
        width, height = 480, 250
        login.title("Update Available!")
        update_info = requests.get(url='http://autoin.trinalgenius.co.uk:8000/version_info').text
        height = height + 20 * len(update_info) % 50 + 20
        login.geometry(
            f'{width}x{height}+{round(login.winfo_screenwidth() / 2 - width / 2)}+{round(login.winfo_screenheight() / 2 - height / 2)}')
        msg_box = tk.Label(login,
                           text='There is a new version of AutoIn.\n有可用新版本更新！\nDo you want to update to the latest version? It should take no more than 1 minute. (Suggested).\n是否更新？仅需大约一分钟（建议更新）\n\n'
                                + update_info, wraplength=400, justify="left", fg="white", bg="#272727",
                           font=tk.font.Font(family="Arial", size=10)).grid(row=0, column=0, padx=30, pady=30,
                                                                            columnspan=4)
        b1 = tk.Button(login, text="Yes", command=update, fg="white", bg="#47A57D", width=15).grid(row=1, column=2)
        b2 = tk.Button(login, text="No", command=lambda: close(login), fg="white", bg="#F37249", width=15).grid(row=1,
                                                                                                                column=3)

    set_login()
    autostart()
    wd.iconify()

# 线程运行循环，还有启动检查新版本
threading.Thread(target=loop, daemon=True).start()
threading.Thread(target=thread_function, daemon=True).start()


# 关闭前提醒，防止点错关闭
def on_closing():
    msg_box = tk.messagebox.askquestion('Exit Application', 'Are you sure you want to exit the application?\nNew takeaway orders will no longer be sent to JZZP automatically!',
                                        icon='warning')
    if msg_box == 'yes':
        wd.destroy()
        subprocess.call("TASKKILL /F /IM chromedriver.exe", shell=True)
        subprocess.call("TASKKILL /F /IM chrome.exe", shell=True)
        logging.info("Program Closed--------------")   # 这行上面说了很重要
        quit()


wd.protocol("WM_DELETE_WINDOW", on_closing)
wd.mainloop()
