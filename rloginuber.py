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


    def init_app(self):
        # self.page = None
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
        self.h2 = cfg["h2"]
        self.ids = load_json("ids") or []
        # self.get_cds()

        if cfg["headless"] == 1:
            headless = False
        else:
            headless = True
        chrome_base_path = cfg["chrome"]
        co = ChromiumOptions(read_file=False).set_paths(
            # local_port='9888',
            browser_path=f"{chrome_base_path}chrome.exe",user_data_path = f"{chrome_base_path}data_001",)
        co.headless(headless)
        self.page = WebPage(chromium_options=co, session_or_options=False)
        # Logger.debug(f'浏览器无头模式-{headless}')
        # 其他配置
        self.restaurantUUID = cfg["restaurantUUID"]
        self.orgUUID = ""
        self.login()

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
        return False
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
                time.sleep(80)
                yzm = get_mail_rs(self.email, t=t0)
                if not yzm or len(yzm) != 4:
                    continue
                if "输入发送至以下号码的 4 位代码" in page.html:
                    time.sleep(50)
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

        if __name__ == "__main__":
            APP()