from DrissionPage import ChromiumPage,ChromiumOptions
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
page = ChromiumPage(co)

time.sleep(3)
url = 'https://merchant-uk.hungrypanda.co/goods/list'
page.get(url)
time.sleep(3)
page.get('https://merchant-uk.hungrypanda.co/order/ordermanage')



# dg=page.run_js('get_json_data.js','fetchOrderDetails(arguments[0]+arguments[1]);','99aa24a203b107d41ab461f7def13146','462511524052176362624')


# 替换token和order_sn
token = '1432d7c58741ac88141af5131a3a0de3'
order_sn = '462511524052176362624'

# 定义要替换的新的 token 和 order_sn 值
new_token = token
new_order_sn = order_sn

# 定义 JavaScript 文件路径
js_file_path = 'get_json_data.js'

#     # 打开 JavaScript 文件进行读取
with open(js_file_path, 'r') as file:
    js_code = file.read()

js_code = js_code.replace('{tokenst}', new_token)
js_code = js_code.replace('{ordersnst}', new_order_sn)

print(js_code)


dg = page.run_js(js_code)




time.sleep(60)

