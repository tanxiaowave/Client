import json
import logging
import hashlib

import openai as openai
import requests
import tkinter as tk
import tkinter.font
import threading
import pymssql
import rsa
import requests
import json
import time
from selenium import webdriver

# 启动Chrome浏览器
driver = webdriver.Chrome()

# 打开网站
driver.get("https://tg2.weimember.cn/lightea/mn/lighteaub/101")

# 添加Cookie
driver.add_cookie({
    'name': 'user_app_id',
    'value': 'web',
    'domain': 'tg2.weimember.cn',
    'path': '/lightea/mn/lighteaub/101',
})
driver.add_cookie({
    'name': 'user_web',
    'value': '167225002936801673',
    'domain': 'tg2.weimember.cn',
    'path': '/lightea/mn/lighteaub/101',
})
driver.add_cookie({
    'name': 'hash_web',
    'value': '5d95b5c7e70cdc9b799d918e52ee167b',
    'domain': 'tg2.weimember.cn',
    'path': '/lightea/mn/lighteaub/101',
})

driver.refresh()
time.sleep(5000000)
# # 人工运行一下，检查账号密码文件
# pri = rsa.PrivateKey(
#             10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
#             65537,
#             7002712700928804011838917939227853273317722595990151016778949911089213823265260722795698382337717248876309656289331967090125041513510782458343001103454593,
#             7165380796988618938065214954530466870443807483684172787495616047866899293086811303,
#             1492014128088262667286826329565602575995354986910798283007464819843657741)
# with open("panda_username_info.txt", "rb") as f:
#     username = f.readline()
#     f.close()
# with open("panda_password_info.txt", "rb") as f:
#     password = f.readline()
#     f.close()
# username = rsa.decrypt(username, pri).decode('utf-8')
# password = rsa.decrypt(password, pri).decode('utf-8')
# print(username, password)

# 人工运行一下，制造账号密码文件，因为软件的录入有时候会不生效不知道为什么
# pub = rsa.PublicKey(
#             10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
#             65537)
# # 生成的时候改掉里面的账号密码
# username = bytes('7859999838', 'utf-8')
# password = bytes('R1uBSO469', 'utf-8')
# print(username, password)
# e_username = rsa.encrypt(username, pub)
# e_password = rsa.encrypt(password, pub)
# with open("panda_username_info.txt", "wb") as f:
#     f.write(e_username)
#     f.close()
# with open("panda_password_info.txt", "wb") as f:
#     f.write(e_password)
#     f.close()

