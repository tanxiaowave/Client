# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : xmwm.py
# Time       ：2024/3/15 22:07
# Author     ：Aodic8
# version    ：python 3.6
# Description：
"""
import time

from DrissionPage import ChromiumPage, ChromiumOptions
import json
def get_token():
    print("===========程序正在初始化，请等待===========")

    co = ChromiumOptions().set_local_port(9222)
    page = ChromiumPage(addr_or_opts=co)
    # page.get('https://merchant-uk.hungrypanda.co/goods/list')

    while True:
        try:
            rs=page.run_js('return localStorage.getItem("LOCALSTORE_USERINFOTABLE") ')
            if rs:
                ss=json.loads(rs)
                token=ss["token"]
                print(f'获取Token成功->{token}')
                time.sleep(1)
                return token
            else:
                yy=input(f'登录已过期，期重新登录。')
                if yy[0] =='q':
                    print('程序退出了')
                    quit()
        except Exception as e:
            print('未知错误')


if __name__ == "__main__":
    get_token()
