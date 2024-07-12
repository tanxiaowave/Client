from DrissionPage import WebPage, ChromiumOptions, SessionOptions
import configparser
import logging
import time


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


class Log:
    Enable = True
    LogName = "RBL"
    DateFormat = "%Y-%m-%d %H:%M:%S"
    Format = "%(asctime)s - %(levelname)s - %(threadName)s - %(filename)s - %(lineno)d -> %(message)s"

    FileEnable = True
    # Path = "./log/{int(time.time())}-runtime.log"
    Path = "./log/{int(time.time())}-runtime.log"
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


co = ChromiumOptions().set_local_port(9113)
co.set_argument('--disable-background-timer-throttling')
page = WebPage(chromium_options=co)

time.sleep(3)
url = 'https://merchant-uk.hungrypanda.co/goods/list'
page.get(url)
time.sleep(3)
page.get('https://merchant-uk.hungrypanda.co/order/ordermanage')
# page.listen.set_targets('POST')
# page.listen.start('https://merchant-uk.hungrypanda.co/order/ordermanage')

page.change_mode()
print(page.mode)

page.cookies_to_session()

headers = {
    'authority': 'uk-gateway.hungrypanda.co',
    'Referer': url,
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'countrycode': 'GB',
    'lang': 'en-US',
    'origin': 'https://merchant-uk.hungrypanda.co',
    'platform': 'H5',
    'pragma': 'no-cache',
    'referer': 'https://merchant-uk.hungrypanda.co/',
    'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'token': '1a40f31fe79a9bafe4b861bd13e8bfa7',
    'uniquetoken': 'fe33fe5a-92b0-4fe8-b3fd-7e700701b93f',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
}

json_data = {
    'orderSn': '8627085170122727331158',
}

response = page.post('https://uk-gateway.hungrypanda.co/api/merchant/order/detail', headers=headers, json=json_data)
print(response.text)
# res = page.listen.wait()
# page.listen.pause()
# print(res)
time.sleep(40)