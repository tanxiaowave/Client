# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : stk.py
# Time       ：2024/1/28 12:43
# Author     ：Aodic8
# version    ：python 3.6
# Description：
"""

import time
import urllib3
from typing import Optional
from datetime import timedelta
from DrissionPage import WebPage, ChromiumOptions
# from curl_cffi import requests
import  requests
import logging
import json
from datetime import datetime
import imaplib
import email
from email.header import decode_header
import re
import pymssql
urllib3.disable_warnings()
import configparser


# 这段代码定义了一个函数get_str_from_stamp，用于将时间戳转换为指定格式的时间字符串。如果没有传入时间戳和格式参数，
# 函数会使用当前时间和默认的时间格式"%Y-%m-%d %H:%M:%S"。
# 需要注意的是，代码中使用了time模块，但是在代码中并未导入该模块。因此在使用该函数之前，需要导入time模块。可以在代码
# 的开头添加import time语句。



def get_str_from_stamp(stamp=None, _format=None):
    stamp = stamp or time.time()
    _format = _format or "%Y-%m-%d %H:%M:%S"
    return time.strftime(_format, time.localtime(stamp))

# 这段代码定义了一个函数get_txt，用于从指定的文本文件中读取非空行且不以"#"开头的文本内容，并将其存储在列表中返回。
# 该函数接受一个名为name的参数，如果未提供该参数，则默认为"cfg"。函数首先构建了文本文件的路径p，然后打开文件进行读
# 取操作。在逐行读取文件内容后，会去除每行两边的空白字符，并检查是否为非空行且不以"#"开头，符合条件的行将被添加到结果
# 列表rs中。最后返回处理后的文本内容列表。需要注意的是，函数中使用了文件处理操作，如果文件不存在或者无法打开，会导致程
# 序报错。在调用这个函数之前，需要确保文件存在且具有读取权限。


def get_txt(name="cfg"):
    p = f"./{name}.txt"
    rs = []
    with open(p, "r", encoding="UTF-8") as f:
        lines = f.readlines()
        for i in lines:
            i = i.strip()
            if i and i[0] != "#":
                rs.append(i.strip())
        return rs



# 这段代码定义了一个函数load_json，用于从指定的JSON文件中加载数据并返回。如果未提供文件名参数，则默认为"data"。
# 函数中使用了try-except块，尝试打开指定的JSON文件进行读取操作，并使用json.load()方法加载文件内容。如果文件读取
# 或解析过程中出现异常，会捕获异常并使用Logger.error()记录异常信息。

def load_json(name="data"):
    p = f"./{name}.json"
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        Logger.error(e)


def dump_json(data, name="data"):
    p = f"./{name}.json"
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 这段代码定义了一个函数get_str_d，用于获取前n天的日期并将其以字符串形式返回。

# 在函数内部，首先通过datetime.now()获取当前日期时间，然后通过timedelta(days=n)计算前n天的日期。
# 接着使用strftime("%Y-%m-%d")
# 将前一天的日期转换为指定格式的字符串"%Y-%m-%d"，最后将转换后的日期字符串返回。
def get_str_d(n=1):
    # 获取当前日期
    current_date = datetime.now()
    # 计算前一天的日期
    previous_date = current_date - timedelta(days=n)
    # 将前一天的日期转换为字符串
    previous_date_string = previous_date.strftime("%Y-%m-%d")
    return previous_date_string


class Log:
    Enable = True
    LogName = "RBL"
    DateFormat = "%Y-%m-%d %H:%M:%S"
    Format = "%(asctime)s - %(levelname)s - %(threadName)s - %(filename)s - %(lineno)d -> %(message)s"

    FileEnable = True
    Path = f"./log/{int(time.time())}-runtime.log"
    ClearFile = True
    FileLevel = "DEBUG"

    ConsoleEnable = True
    ConsoleLevel = "DEBUG"


def get_logger(name=None):
    if not Log.Enable:
        return None

    if not name:
        name = __name__

    logger = logging.getLogger(name)
    logger.setLevel(Log.ConsoleLevel)
    formatter = logging.Formatter(fmt=Log.Format, datefmt=Log.DateFormat)

    # 输出到控制台
    if Log.ConsoleEnable:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level=Log.ConsoleLevel)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    # 输出到文件
    if Log.Enable:
        # 先清空日志文件
        if Log.ClearFile:
            with open(Log.Path, "a+", encoding="utf-8") as f:
                f.truncate(0)
        file_handler = logging.FileHandler(Log.Path, encoding="utf-8")
        file_handler.setLevel(level=Log.FileLevel)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

Logger = get_logger(Log.LogName)


def get_mail_rs(user_email, t=0):
    """
    获取验证码
    :param user_email:
    :return:
    """
    email_password = "007"

    # 搜索邮件

    mail = imaplib.IMAP4_SSL("9m9.fun")
    try:
        mail.login(user_email, email_password)
        mail.select("inbox")

        status, messages = mail.search(None, "ALL")
        last_msg_id = messages[0].split()[-1]
        # 获取邮件
        _, msg_data = mail.fetch(last_msg_id, "(RFC822)")
        raw_email = msg_data[0][1]

        msg = email.message_from_bytes(raw_email)

        # 获取邮件时间
        # 获取邮件的时间
        date_str = msg["Date"].replace("(UTC)", "").strip()
        date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        t0 = date_obj.timestamp()
        if t0 < t:
            Logger.debug("没有最新邮件")
            return None
        # 获取主题
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        if subject != "您的优步账号验证码":
            return None

        # 获取邮件正文
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode("utf-8")
                elif part.get_content_type() == "text/html":
                    # 如果存在HTML格式的正文，你也可以解析HTML
                    body = part.get_payload(decode=True).decode("utf-8")
        else:
            body = msg.get_payload(decode=True).decode("utf-8")

        if body:
            pattern = r'<td class="p2b".*?>(.*?)</td>'
            matches = re.findall(pattern, body)

            if matches:
                yzm = matches[0]
                Logger.debug(f"验证码：{yzm}")
                return yzm
            else:
                Logger.error("获取验证码失败。")
    except Exception as e:
        Logger.error(e)

    finally:
        # 关闭连接
        mail.logout()


# 主程序
class APP:
    def __init__(self):
        self.cfg: Optional[dict] = None
        self.ids: Optional[list] = None
        self.cds: Optional[dict] = None

        self.proxy: Optional[str] = None
        self.proxies: Optional[dict] = None
        self.page: Optional[WebPage] = None

        self.email: Optional[str] = None
        self.req_count = 0
        self.cookies: Optional[dict] = None

        self.h2: Optional[dict] = None
        self.t0 = 0
        self.restaurantUUID: Optional[str] = None
        self.orgUUID: Optional[str] = None
        self.init_app()
        self.run()

    def init_app(self):
        """

        :return:
        """
        Logger.debug("程序正在初始化，请等待。。。。。。")

        self.cfg = cfg = load_json("cfg")
        proxy = cfg["proxy"]
        proxies = {
            "http": proxy,
            "https": proxy,
        }
        self.proxy = proxy
        self.proxies = proxies
        self.email = cfg["email"]
        # self.porty = cfg["port"]
        self.h2 = cfg["h2"]
        self.ids = load_json("ids") or []
        self.get_cds()

        if cfg["headless"] == 1:
            headless = False
        else:
            headless = True
        for i in range(3):
            try:
                chrome_base_path = cfg["chrome"]
                co = ChromiumOptions(read_file=False).set_paths(
                    # local_port=self.porty,
                    browser_path=f"{chrome_base_path}chrome.exe",
                    user_data_path=f"{chrome_base_path}data_001",
                )
                co.headless(headless)
                self.page = WebPage(chromium_options=co, session_or_options=False)
                self.restaurantUUID = cfg["restaurantUUID"]
                self.orgUUID = ""
                return True
            except:
                time.sleep(20)
                print("-----------20------------")
                # Logger.debug(f'浏览器无头模式-{headless}')
                # 其他配置


    def add_ids(self, order_id):
        """
        控制最新的10个订单号
        :return:
        """
        ids = self.ids
        ids.append(order_id)
        if len(ids) > 1000:
            ids.pop()
        dump_json(ids, "ids")

    def run(self):
        """
        重复5次
        :return:
        """
        self.login()
        start_day = get_str_d()

        total = 0
        while True:
            self.t0 = int(time.time())
            orders = self.getOrders(start_day)
            if orders:
                self.submitOrders(orders)
                Logger.debug("-------------60-------------")
                time.sleep(60)
                total += 1
                if total > 1500:
                    total = 0
                    start_day = get_str_d()

    def login(self):
        """
        检查是否过期
        :return:
        """
        for i in range(3):
            if self.getUsers():
                Logger.debug("登录未过期")
                self.page.quit()
                return True
            elif self._login():
                Logger.debug("重新登录成功")
                self.page.quit()
                return True
        Logger.error("登录失败")
        self.page.quit()
        quit()

    def getUsers(self):
        """
        查询个人信息
        :return:
        """
        if "merchants.ubereats.com" not in self.page.url:
            self.page.get("https://merchants.ubereats.com/manager/stores")
        self.cookies = self.page.cookies(as_dict=True)
        restaurantUUID = self.restaurantUUID
        headers = {
            "Host": "merchants.ubereats.com",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "content-type": "application/json",
            "x-csrf-token": "x",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": '"Windows"',
            "accept": "*/*",
            "origin": "https://merchants.ubereats.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": f"https://merchants.ubereats.com/manager/users?restaurantUUID={restaurantUUID}",
            "accept-language": "zh-CN,zh;q=0.9",
        }

        url = "https://merchants.ubereats.com/manager/api/getUsers"
        params = {"localeCode": "zh-CN"}
        data = {}
        time.sleep(15)
        for i in range(3):
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    cookies=self.cookies,
                    params=params,
                    json=data,
                    # impersonate="chrome110",
                    verify=False,
                    proxies=self.proxies,
                )
                if response.status_code == 200:
                    rs = response.json()
                    status = rs["status"]
                    if status == "success":
                        Logger.debug("获取用户成功")
                        return True
                else:
                    if response.status_code == 404 and response.text == "Not Found":
                        Logger.debug("登录过期")
                        return False
                    else:
                        Logger.error(f"{response.status_code}")
            except Exception as e:
                Logger.error(e)

        Logger.error(f"获取用户失败")

    def _login(self):
        """
        登录
        :return:
        """
        page = self.page
        url = "https://merchants.ubereats.com/manager/stores"
        for i in range(5):
            try:
                # 登录
                page.get(url)
                # page.wait.load_start()
                # 重新登录
                t0 = int(time.time())
                page.actions.move_to("#PHONE_NUMBER_or_EMAIL_ADDRESS").type(
                    f"{self.email}\n"
                )
                # page.wait.load_start()
                time.sleep(50)
                yzm = get_mail_rs(self.email, t=t0)
                if not yzm or len(yzm) != 4:
                    continue
                if "输入发送至以下号码的 4 位代码" in page.html:
                    eles = page.eles("@aria-label=输入一次性密码")
                    if len(eles) == 4:
                        for idx, ele in enumerate(eles):
                            ele.input(yzm[idx])
                        page.wait.load_start()
                        if self.getUsers():
                            return True
            except Exception as e:
                Logger.error(e)

        Logger.error("登录失败，程序退出")
        quit()

    def getOrders(self, start_day):
        """
        获取订单-按收入明细
        :return:
        """
        current_date = datetime.now().strftime("%Y-%m-%d")
        restaurantUUID = self.restaurantUUID

        headers = {
            "Host": "merchants.ubereats.com",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "accept": "*/*",
            "content-type": "application/json",
            "x-csrf-token": "x",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": '"Windows"',
            "origin": "https://merchants.ubereats.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": f"https://merchants.ubereats.com/manager/payments/payouts-by-order?restaurantUUID={restaurantUUID}",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        }

        url = "https://merchants.ubereats.com/manager/graphql"
        data = {
            "operationName": "ordersBreakdown",
            "variables": {
                "filters": {
                    "dateRange": {"start": start_day, "end": current_date},
                    "orderIssues": [],
                    "search": "",
                    "locationConstraints": {
                        "cities": [],
                        "countries": [],
                        "locationUUIDs": [self.restaurantUUID],
                    },
                    "displayCurrencyCode": "GBP",
                    "orgUUID": self.orgUUID,
                },
                "pagination": {"limit": 20, "nextTable": "liveOrders"},
            },
            "query": "fragment Orders_LastMessageFragment on Orders_LastMessage {\n  sender\n  content\n  promoAmount\n  promoCurrency\n  __typename\n}\n\nfragment OrdersBreakdown_OrderBreakDownRowFragment on Orders_OrderBreakdownRow {\n  orderId\n  workflowUuid\n  currencyCode\n  restaurant {\n    uuid\n    name\n    countryCode\n    __typename\n  }\n  eater {\n    uuid\n    name\n    profileURL\n    numOrders\n    isEatsPassSubscriber\n    subscriptionPass\n    __typename\n  }\n  orderTag\n  orderChannel\n  fulfillmentType\n  chargebackTotal\n  salesTotal\n  requestedAt\n  netPayout\n  lastMessage {\n    ...Orders_LastMessageFragment\n    __typename\n  }\n  checkoutInfo {\n    key\n    amount\n    label\n    descriptionKey\n    __typename\n  }\n  orderStatus\n  canceledBy\n  missedBy\n  orderUuid\n  possibleChargebackAmount\n  possibleChargebackAmountFormatted\n  chargebackProcessingTimeFormatted\n  __typename\n}\n\nquery ordersBreakdown($filters: Orders_OrdersFiltersInput!, $pagination: Orders_OrdersPaginationInput, $sort: Orders_OrdersSortInput) {\n  ordersBreakdown(filters: $filters, pagination: $pagination, sort: $sort) {\n    lastUpdatedAtUtc\n    rows {\n      ...OrdersBreakdown_OrderBreakDownRowFragment\n      __typename\n    }\n    isUserAuthorizedToDispute\n    paginationResult {\n      nextCursor\n      nextTable\n      __typename\n    }\n    ordersCount\n    ordersIssueCount {\n      missedCount\n      canceledCount\n      disputeInProgressCount\n      disputeAcceptedCount\n      disputeRejectedCount\n      issueChargedCount\n      issueReportedCount\n      potentialDeductionCount\n      __typename\n    }\n    __typename\n  }\n}\n",
        }
        data = json.dumps(data, separators=(",", ":"))

        for i in range(3):
            try:
                response = requests.post(
                    url,
                    cookies=self.cookies,
                    headers=headers,
                    data=data,
                    # impersonate="chrome110",
                    verify=False,
                    proxies=self.proxies,
                )
                if response.status_code == 200:
                    rs = response.json()
                    time.sleep(3)
                    orders = rs["data"]["ordersBreakdown"]
                    return orders
                else:
                    self.deal_err(response)
            except Exception as e:
                Logger.error(e)

        Logger.error(f"获取订单数据失败")

    def getOrderDetails(self, workflowUUID):
        """
        获取订单详情
        :return:
        """
        restaurantUUID = self.restaurantUUID
        headers = {
            "Host": "merchants.ubereats.com",
            "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
            "accept": "*/*",
            "content-type": "application/json",
            "x-csrf-token": "x",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": '"Windows"',
            "origin": "https://merchants.ubereats.com",
            "sec-fetch-site": "same-origin",
            "sec-fetch-mode": "cors",
            "sec-fetch-dest": "empty",
            "referer": f"https://merchants.ubereats.com/manager/payments/payouts-by-order/{workflowUUID}?effect=&restaurantUUID={restaurantUUID}&activeOrder=1",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        }

        url = "https://merchants.ubereats.com/manager/graphql"
        data = {
            "operationName": "LiveOrderDetails",
            "variables": {
                "workflowUUID": workflowUUID,
                "metadata": {"isEatsPassSubscriber": True},
            },
            "query": "fragment customizationFields on Orders_Customization {\n  name\n  uuid\n  __typename\n}\n\nfragment customizationOptionFields on Orders_Option {\n  name\n  quantity\n  price\n  uuid\n  support {\n    issueType\n    itemIssueType\n    __typename\n  }\n  __typename\n}\n\nquery LiveOrderDetails($workflowUUID: ID!, $metadata: Orders_OrderDetailsMetadataInput) {\n  liveOrderDetails(workflowUUID: $workflowUUID, metadata: $metadata) {\n    requestedAt\n    orderId\n    orderStateChanges {\n      changedAt\n      orderState\n      __typename\n    }\n    orderUUID\n    eater {\n      isEatsPassSubscriber\n      name\n      numOrders\n      profileURL\n      uuid\n      phone\n      phonePinCode\n      deliveryAddress\n      __typename\n    }\n    restaurant {\n      name\n      address\n      currencyCode\n      uuid\n      __typename\n    }\n    checkoutInfo {\n      key\n      amount\n      label\n      descriptionKey\n      __typename\n    }\n    marketplaceFeeRate\n    netPayout\n    issueSummary {\n      adjustmentAmount\n      customerRefund\n      failureReason\n      issueType\n      orderJobState\n      numMissingItems\n      __typename\n    }\n    items {\n      customizations {\n        ...customizationFields\n        options {\n          ...customizationOptionFields\n          customizations {\n            ...customizationFields\n            options {\n              ...customizationOptionFields\n              customizations {\n                ...customizationFields\n                options {\n                  ...customizationOptionFields\n                  customizations {\n                    ...customizationFields\n                    options {\n                      ...customizationOptionFields\n                      customizations {\n                        ...customizationFields\n                        options {\n                          ...customizationOptionFields\n                          customizations {\n                            ...customizationFields\n                            options {\n                              ...customizationOptionFields\n                              customizations {\n                                ...customizationFields\n                                options {\n                                  ...customizationOptionFields\n                                  customizations {\n                                    ...customizationFields\n                                    options {\n                                      ...customizationOptionFields\n                                      customizations {\n                                        ...customizationFields\n                                        options {\n                                          ...customizationOptionFields\n                                          customizations {\n                                            ...customizationFields\n                                            options {\n                                              ...customizationOptionFields\n                                              customizations {\n                                                ...customizationFields\n                                                options {\n                                                  ...customizationOptionFields\n                                                  customizations {\n                                                    ...customizationFields\n                                                    options {\n                                                      ...customizationOptionFields\n                                                      customizations {\n                                                        ...customizationFields\n                                                        options {\n                                                          ...customizationOptionFields\n                                                          customizations {\n                                                            ...customizationFields\n                                                            options {\n                                                              ...customizationOptionFields\n                                                              customizations {\n                                                                ...customizationFields\n                                                                options {\n                                                                  ...customizationOptionFields\n                                                                  customizations {\n                                                                    ...customizationFields\n                                                                    options {\n                                                                      ...customizationOptionFields\n                                                                      customizations {\n                                                                        ...customizationFields\n                                                                        options {\n                                                                          ...customizationOptionFields\n                                                                          customizations {\n                                                                            ...customizationFields\n                                                                            options {\n                                                                              ...customizationOptionFields\n                                                                              customizations {\n                                                                                ...customizationFields\n                                                                                options {\n                                                                                  ...customizationOptionFields\n                                                                                  customizations {\n                                                                                    ...customizationFields\n                                                                                    options {\n                                                                                      ...customizationOptionFields\n                                                                                      customizations {\n                                                                                        ...customizationFields\n                                                                                        options {\n                                                                                          ...customizationOptionFields\n                                                                                          customizations {\n                                                                                            ...customizationFields\n                                                                                            options {\n                                                                                              ...customizationOptionFields\n                                                                                              customizations {\n                                                                                                ...customizationFields\n                                                                                                options {\n                                                                                                  ...customizationOptionFields\n                                                                                                  customizations {\n                                                                                                    ...customizationFields\n                                                                                                    options {\n                                                                                                      ...customizationOptionFields\n                                                                                                      customizations {\n                                                                                                        ...customizationFields\n                                                                                                        options {\n                                                                                                          ...customizationOptionFields\n                                                                                                          customizations {\n                                                                                                            ...customizationFields\n                                                                                                            options {\n                                                                                                              ...customizationOptionFields\n                                                                                                              customizations {\n                                                                                                                ...customizationFields\n                                                                                                                options {\n                                                                                                                  ...customizationOptionFields\n                                                                                                                  customizations {\n                                                                                                                    ...customizationFields\n                                                                                                                    options {\n                                                                                                                      ...customizationOptionFields\n                                                                                                                      customizations {\n                                                                                                                        ...customizationFields\n                                                                                                                        options {\n                                                                                                                          ...customizationOptionFields\n                                                                                                                          customizations {\n                                                                                                                            ...customizationFields\n                                                                                                                            options {\n                                                                                                                              ...customizationOptionFields\n                                                                                                                              customizations {\n                                                                                                                                ...customizationFields\n                                                                                                                                options {\n                                                                                                                                  ...customizationOptionFields\n                                                                                                                                  customizations {\n                                                                                                                                    ...customizationFields\n                                                                                                                                    options {\n                                                                                                                                      ...customizationOptionFields\n                                                                                                                                      customizations {\n                                                                                                                                        ...customizationFields\n                                                                                                                                        options {\n                                                                                                                                          ...customizationOptionFields\n                                                                                                                                          customizations {\n                                                                                                                                            ...customizationFields\n                                                                                                                                            options {\n                                                                                                                                              ...customizationOptionFields\n                                                                                                                                              customizations {\n                                                                                                                                                ...customizationFields\n                                                                                                                                                options {\n                                                                                                                                                  ...customizationOptionFields\n                                                                                                                                                  customizations {\n                                                                                                                                                    ...customizationFields\n                                                                                                                                                    options {\n                                                                                                                                                      ...customizationOptionFields\n                                                                                                                                                      customizations {\n                                                                                                                                                        ...customizationFields\n                                                                                                                                                        options {\n                                                                                                                                                          ...customizationOptionFields\n                                                                                                                                                          customizations {\n                                                                                                                                                            ...customizationFields\n                                                                                                                                                            options {\n                                                                                                                                                              ...customizationOptionFields\n                                                                                                                                                              customizations {\n                                                                                                                                                                ...customizationFields\n                                                                                                                                                                options {\n                                                                                                                                                                  ...customizationOptionFields\n                                                                                                                                                                  customizations {\n                                                                                                                                                                    ...customizationFields\n                                                                                                                                                                    options {\n                                                                                                                                                                      ...customizationOptionFields\n                                                                                                                                                                      customizations {\n                                                                                                                                                                        ...customizationFields\n                                                                                                                                                                        options {\n                                                                                                                                                                          ...customizationOptionFields\n                                                                                                                                                                          customizations {\n                                                                                                                                                                            ...customizationFields\n                                                                                                                                                                            options {\n                                                                                                                                                                              ...customizationOptionFields\n                                                                                                                                                                              customizations {\n                                                                                                                                                                                ...customizationFields\n                                                                                                                                                                                options {\n                                                                                                                                                                                  ...customizationOptionFields\n                                                                                                                                                                                  customizations {\n                                                                                                                                                                                    ...customizationFields\n                                                                                                                                                                                    options {\n                                                                                                                                                                                      ...customizationOptionFields\n                                                                                                                                                                                      customizations {\n                                                                                                                                                                                        ...customizationFields\n                                                                                                                                                                                        options {\n                                                                                                                                                                                          ...customizationOptionFields\n                                                                                                                                                                                          customizations {\n                                                                                                                                                                                            ...customizationFields\n                                                                                                                                                                                            options {\n                                                                                                                                                                                              ...customizationOptionFields\n                                                                                                                                                                                              customizations {\n                                                                                                                                                                                                ...customizationFields\n                                                                                                                                                                                                options {\n                                                                                                                                                                                                  ...customizationOptionFields\n                                                                                                                                                                                                  customizations {\n                                                                                                                                                                                                    ...customizationFields\n                                                                                                                                                                                                    options {\n                                                                                                                                                                                                      ...customizationOptionFields\n                                                                                                                                                                                                      customizations {\n                                                                                                                                                                                                        ...customizationFields\n                                                                                                                                                                                                        options {\n                                                                                                                                                                                                          ...customizationOptionFields\n                                                                                                                                                                                                          customizations {\n                                                                                                                                                                                                            ...customizationFields\n                                                                                                                                                                                                            options {\n                                                                                                                                                                                                              ...customizationOptionFields\n                                                                                                                                                                                                              __typename\n                                                                                                                                                                                                            }\n                                                                                                                                                                                                            __typename\n                                                                                                                                                                                                          }\n                                                                                                                                                                                                          __typename\n                                                                                                                                                                                                        }\n                                                                                                                                                                                                        __typename\n                                                                                                                                                                                                      }\n                                                                                                                                                                                                      __typename\n                                                                                                                                                                                                    }\n                                                                                                                                                                                                    __typename\n                                                                                                                                                                                                  }\n                                                                                                                                                                                                  __typename\n                                                                                                                                                                                                }\n                                                                                                                                                                                                __typename\n                                                                                                                                                                                              }\n                                                                                                                                                                                              __typename\n                                                                                                                                                                                            }\n                                                                                                                                                                                            __typename\n                                                                                                                                                                                          }\n                                                                                                                                                                                          __typename\n                                                                                                                                                                                        }\n                                                                                                                                                                                        __typename\n                                                                                                                                                                                      }\n                                                                                                                                                                                      __typename\n                                                                                                                                                                                    }\n                                                                                                                                                                                    __typename\n                                                                                                                                                                                  }\n                                                                                                                                                                                  __typename\n                                                                                                                                                                                }\n                                                                                                                                                                                __typename\n                                                                                                                                                                              }\n                                                                                                                                                                              __typename\n                                                                                                                                                                            }\n                                                                                                                                                                            __typename\n                                                                                                                                                                          }\n                                                                                                                                                                          __typename\n                                                                                                                                                                        }\n                                                                                                                                                                        __typename\n                                                                                                                                                                      }\n                                                                                                                                                                      __typename\n                                                                                                                                                                    }\n                                                                                                                                                                    __typename\n                                                                                                                                                                  }\n                                                                                                                                                                  __typename\n                                                                                                                                                                }\n                                                                                                                                                                __typename\n                                                                                                                                                              }\n                                                                                                                                                              __typename\n                                                                                                                                                            }\n                                                                                                                                                            __typename\n                                                                                                                                                          }\n                                                                                                                                                          __typename\n                                                                                                                                                        }\n                                                                                                                                                        __typename\n                                                                                                                                                      }\n                                                                                                                                                      __typename\n                                                                                                                                                    }\n                                                                                                                                                    __typename\n                                                                                                                                                  }\n                                                                                                                                                  __typename\n                                                                                                                                                }\n                                                                                                                                                __typename\n                                                                                                                                              }\n                                                                                                                                              __typename\n                                                                                                                                            }\n                                                                                                                                            __typename\n                                                                                                                                          }\n                                                                                                                                          __typename\n                                                                                                                                        }\n                                                                                                                                        __typename\n                                                                                                                                      }\n                                                                                                                                      __typename\n                                                                                                                                    }\n                                                                                                                                    __typename\n                                                                                                                                  }\n                                                                                                                                  __typename\n                                                                                                                                }\n                                                                                                                                __typename\n                                                                                                                              }\n                                                                                                                              __typename\n                                                                                                                            }\n                                                                                                                            __typename\n                                                                                                                          }\n                                                                                                                          __typename\n                                                                                                                        }\n                                                                                                                        __typename\n                                                                                                                      }\n                                                                                                                      __typename\n                                                                                                                    }\n                                                                                                                    __typename\n                                                                                                                  }\n                                                                                                                  __typename\n                                                                                                                }\n                                                                                                                __typename\n                                                                                                              }\n                                                                                                              __typename\n                                                                                                            }\n                                                                                                            __typename\n                                                                                                          }\n                                                                                                          __typename\n                                                                                                        }\n                                                                                                        __typename\n                                                                                                      }\n                                                                                                      __typename\n                                                                                                    }\n                                                                                                    __typename\n                                                                                                  }\n                                                                                                  __typename\n                                                                                                }\n                                                                                                __typename\n                                                                                              }\n                                                                                              __typename\n                                                                                            }\n                                                                                            __typename\n                                                                                          }\n                                                                                          __typename\n                                                                                        }\n                                                                                        __typename\n                                                                                      }\n                                                                                      __typename\n                                                                                    }\n                                                                                    __typename\n                                                                                  }\n                                                                                  __typename\n                                                                                }\n                                                                                __typename\n                                                                              }\n                                                                              __typename\n                                                                            }\n                                                                            __typename\n                                                                          }\n                                                                          __typename\n                                                                        }\n                                                                        __typename\n                                                                      }\n                                                                      __typename\n                                                                    }\n                                                                    __typename\n                                                                  }\n                                                                  __typename\n                                                                }\n                                                                __typename\n                                                              }\n                                                              __typename\n                                                            }\n                                                            __typename\n                                                          }\n                                                          __typename\n                                                        }\n                                                        __typename\n                                                      }\n                                                      __typename\n                                                    }\n                                                    __typename\n                                                  }\n                                                  __typename\n                                                }\n                                                __typename\n                                              }\n                                              __typename\n                                            }\n                                            __typename\n                                          }\n                                          __typename\n                                        }\n                                        __typename\n                                      }\n                                      __typename\n                                    }\n                                    __typename\n                                  }\n                                  __typename\n                                }\n                                __typename\n                              }\n                              __typename\n                            }\n                            __typename\n                          }\n                          __typename\n                        }\n                        __typename\n                      }\n                      __typename\n                    }\n                    __typename\n                  }\n                  __typename\n                }\n                __typename\n              }\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      name\n      price\n      quantity\n      support {\n        issueType\n        itemIssueType\n        __typename\n      }\n      uuid\n      __typename\n    }\n    fulfillmentType\n    hasOrderCompleted\n    estimatedDeliveryTime\n    estimatedPickupTime\n    attachments {\n      prescriptionInfo {\n        prescriptionUUID\n        details {\n          imageFileObjectIDs\n          patientFullName\n          patientNationalID\n          signedImageURLs\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n",
        }

        data = json.dumps(data, separators=(",", ":"))
        for i in range(3):
            try:
                response = requests.post(
                    url,
                    cookies=self.cookies,
                    headers=headers,
                    data=data,
                    # impersonate="chrome110",
                    verify=False,
                    proxies=self.proxies,
                )
                if response.status_code == 200:
                    rs = response.json()
                    orderDetails = rs["data"]["liveOrderDetails"]
                    return orderDetails
                else:
                    self.deal_err(response)
            except Exception as e:
                Logger.error(e)

        Logger.error(f"获取订单详情失败")

    def get_cds(self):
        """获取菜单"""
        cfg = self.cfg
        self.cds = cds = {}
        if cfg["db_enable"] is False:
            Logger.error("未请用数据库")
            return False

        try:
            conn = pymssql.connect(
                server=cfg["server"],
                user=cfg["user"],
                password=cfg["password"],
                database=cfg["database"],
                login_timeout=5,
                tds_version='7.0',
            )
            cur = conn.cursor()
            sql = "select MenuID,MenuName from mn_Menu"
            cur.execute(sql)
            for row in cur.fetchall():
                MenuID = row[0]
                MenuName = row[1].encode("latin-1").decode("gbk")
                # MenuNameEN=row[2].encode('latin-1').decode('gbk')
                cds[MenuID] = {
                    "MenuID": MenuID,
                    "MenuName": MenuName,
                    # 'MenuNameEN': MenuName,
                }
                Logger.debug(f"{MenuID},{MenuName}")
            # menu_name = sql_result[0][0].encode('latin-1').decode('gbk')
            Logger.debug(f"菜单总数->{len(cds)}")

            self.cds = cds

        except Exception as e:
            print(e)
            time.sleep(10)
            Logger.error("获取菜单失败")

    def check_order(self, order):
        """
        确认订单
        'ACCEPTED'
        'BEGINTRIP'
        'COMPLETED'
        InProgress
        """
        order_id = order["orderId"]
        orderStatus = order.get("orderStatus", "")

        Logger.debug(f"订单状态->{order_id},{orderStatus}")
        if orderStatus != "InProgress" or order_id in self.ids:
            # 非InProgress订单，已添加订单，都不添加系统
            return None

        # 获取订单详情
        OrderDetails = self.getOrderDetails(order["workflowUuid"])
        items = OrderDetails.get("items")

        if not items:
            Logger.debug("获取订单详情失败")
            return None

        # 构建菜品
        Items = []
        TotalAmt = float(order["salesTotal"][1:])





        for item in items:

            # def get_name_quantity_list(item):
            #     name_quantity_list = []
            #
            #     if 'customizations' in item and item['customizations']:
            #         optionstopping = item['customizations'][0]['options']
            #         for option in optionstopping:
            #             name = option['name']
            #             quantity = option['quantity']
            #             name_quantity_dict = {'name': name, 'quantity': quantity}
            #             name_quantity_list.append(name_quantity_dict)
            #     return name_quantity_list
            #
            # name_quantity_list = get_name_quantity_list(item)
            # print(name_quantity_list)


            # def get_name_quantity_stri(item):
            #     name_quantity_str = ""
            #     if 'customizations' in item and item['customizations']:
            #         print(item)
            #         print(item['customizations'])
            #         optionstopping = item['customizations'][0]['options']
            #
            #         for option in optionstopping:
            #             name = option['name']
            #             quantity = option['quantity']
            #             name_quantity_str += f"{name}: {quantity}, "

                # return name_quantity_str

            def extract_customizations_as_list(item):
                customizations_list = []  # 创建空列表来存储定制字符串
                options = []
                for customization in item['customizations']:
                    for option in customization['options']:
                        op = option['name']  # 获取选项的名称

                        options = {
                            "id": "AutoIn",
                            "name": op,
                            "price": 0,
                            "qty": 1
                        }

                        customizations_list.append(options)  # 将定制字符串添加到列表中

                return customizations_list

            name_quantity_list = []
            name_quantity_list = extract_customizations_as_list(item)
            print(name_quantity_list)
            # name_quantity_list = name_quantity_string.split(',')
            # print(name_quantity_list)

            name = item["name"]
            MenuID = name[1:5]
            cp = self.cds.get(MenuID) or {"MenuName": "未知菜品"}
            price = float(item["price"][1:])
            quantity = item["quantity"]
            item0 = {
                "ParentID": "SP1001",  # 固定
                "MenuID": MenuID,  # 要求取"name": "[5006]中括号里面的数据
                "MenuName": cp["MenuName"],  # 根据MenuID到本都sqlexpress数据库里面查询相应的Menuname
                # "MenuNameEN": 'meu',  # 根据MenuID到本都sqlexpress数据库里面查询相应的MenunameEN
                "MenuUnit": ".",  # 固定
                # "UnitID": "1",  # 固定
                "PicImg": "",
                "MenuQty": quantity,  # "quantity":
                "MenuPriceOld": price/quantity,  # "price"
                "MenuPrice": price/quantity,  # "price"name_quantity_dict
                "MenuAmt": price,  # MenuPrice * MenuQty
                "MenuPoint": 0,  # 固定
                "MenuService": 0,  # 固定
                "SumOfService": 0,  # 固定
                "CookList": name_quantity_list,  # 固定
                "MenuList": []  # 固定
                # "Remark": "NO CUTLERY"  # 固定
            }
            # TotalAmt += 1
            Items.append(item0)
            print(item0)
        reader = configparser.ConfigParser()
        reader.read("settings.INI")
        commission = float(reader.get("Commission", "ubereats"))

        dd = {
            "AppID": "web",  # 固定
            "AppType": "web",  # 固定
            "PayType": "mbpay",  # 固定
            "BranchID": self.cfg["BranchID"],  # 读取setting配置文件
            "TableID": "991",  # 固定
            "TableName": "UberEats",  # 固定
            "BillType": 3,  # 固定
            "ServiceRate": 0,  # 固定
            "SumOfService": 0,  # 固定
            "TotalPoint": 0,  # 固定
            "TotalAmt": TotalAmt*commission,  # netPayout
            "MemberCardID": "888",  # 固定
            "MemberName": "Uber Eats",  # 固定
            # "Mobile": "0788888888",  # 固定
            # "PeopleCount": 0,  # 固定
            "Items": Items,
            # "Coupons": [],  # 固定
            "Remark": "NO CUTLERY",  # 固定
            "CompanyID": self.cfg["CompanyID"],  # 固定
            "UserID": self.cfg["UserID"] # 固定
        }
        print(dd)
        return dd


    def submitOrders(self, orders):
        """
        提交订单
        :param orders:
        :return:
        """
        rows = orders["rows"]
        for order in rows:
            try:
                dd = self.check_order(order)
                if dd:
                    if self.submitOrder(dd):
                        self.add_ids(order["orderId"])
            except Exception as e:
                Logger.error(e)

    def submitOrder(self, dd):
        """
        提交订单至服务器
        :param dd:
        :return:
        """

        url = "http://tg2.weimember.cn/mb/member.api.ljson?api=mn.order&act=create"
        for i in range(3):
            try:
                res = requests.post(url, json=dd, headers=self.h2)
                print(res.text)
                if res.status_code == 200:
                    rs = res.json()
                    ok = rs.get("ok")
                    if ok:
                        order_id = rs["data"]["OrderID"]
                        print(order_id)
                        Logger.debug(f"提交订单->{order_id}")
                        if self.submitPay(order_id):
                            return True
                    else:
                        Logger.error(f"请求错误->{rs}")
                else:
                    Logger.error(res.status_code)
            except Exception as e:
                Logger.error(e)

        Logger.error(f"提交订单失败->{dd}")
        # quit()

    def submitPay(self, order_id):
        """
        构造支付订单时的服务器需要的数据
        :param:
        :return:
        """

        url = "http://tg2.weimember.cn/mb/member.api.ljson?api=mn.order&act=pay"
        data = {
            "OrderID": order_id,
            "CompanyID": self.cfg["CompanyID"],
            "UserID": self.cfg["UserID"]
        }

        for i in range(3):
            try:
                res = requests.post(url, json=data, headers=self.h2)
                if res.status_code == 200:
                    rs = res.json()
                    ok = rs.get("ok")
                    if ok:
                        order_id = rs["data"]["OrderID"]
                        Logger.debug(f"支付提交->{order_id}")
                        time.sleep(5)
                        return True
                    else:
                        Logger.error(f"请求错误->{rs}")
                else:
                    Logger.error(res.status_code)
            except Exception as e:
                Logger.error(e)

        Logger.error(f"提交订单失败->{data}")
        quit()

    def deal_err(self, response):
        if response.status_code == 404 and response.text == "Not Found":
            self.login()
        else:
            Logger.error(f"未知错误->{response.status_code}")


if __name__ == "__main__":
    APP()
