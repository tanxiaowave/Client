import imaplib
import email
from email.header import decode_header
import re
from datetime import datetime
import logging

def getmail():
    t=0
    email_password = "007"
    user_email = "sgzz1v7f1g7t@9m9.fun"
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
        # date_str = msg["Date"].replace("(UTC)", "").strip()
        # date_obj = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S %z")
        # t0 = date_obj.timestamp()
        # if t0 < t:
        #     print("没有最新邮件")
        #     # return None
        # 获取主题
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        # if subject != "HP SMS Verify":
        #     # return None

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
            pattern = r'Your verification code: (\d+)'
            match = re.search(pattern, body)

            if match:
                yzm = match.group(1)
                print(f"验证码：{yzm}")
                return yzm
            else:
                print("获取验证码失败。")
    except Exception as e:
        print(e)

    finally:
        # 关闭连接
        mail.logout()

yzmstr = getmail()
print(yzmstr)