# holborn店有一段时间不记得是没了收单机还是什么，看不了饭团订单列表，这是写了个小程序给他们查看历史订单
import rsa
import json
import tkinter as tk
import requests


pri = rsa.PrivateKey(
        10690849382239354932069678647576775530502785728974248210646711710842662286687729661457284316695477606433550792821419683402634484378249872944165297782246523,
        65537,
        7002712700928804011838917939227853273317722595990151016778949911089213823265260722795698382337717248876309656289331967090125041513510782458343001103454593,
        7165380796988618938065214954530466870443807483684172787495616047866899293086811303,
        1492014128088262667286826329565602575995354986910798283007464819843657741)
try:
    with open("fantuan_appkey.txt", "rb") as f:
        username = f.readline()
        f.close()
    with open("fantuan_shopid.txt", "rb") as f:
        password = f.readline()
        f.close()
    appkey = rsa.decrypt(username, pri).decode('utf-8')
    shop_id = rsa.decrypt(password, pri).decode('utf-8')
except:
    pass

headers = {
    "Content-Type": "application/json",
    "appKey": appkey,
    "timestamp": "{{$timestamp}}",
}
data = {
    "shopId": shop_id,
    "page": {
        "pageNum": 1,
        "pageSize": 10
    }
}
url = "https://openapi.fantuan.ca/api/v1/order/page"
response = json.loads(requests.post(url, json=data, headers=headers).text)
text = ""


def settext():
    text = ""
    for row in response['data']['rows']:
        text += row['orderNo']
        text += "\n"
    textField.config(text=text)


wd = tk.Tk("饭团订单查询")
width, height = 150, 225
check = tk.Button(wd, text="查询近十条饭团订单")
check.config(command=settext)
check.pack()
wd.geometry(
    f'{width}x{height}+{round(wd.winfo_screenwidth() / 2 - width / 2)}+'
    f'{round(wd.winfo_screenheight() / 2 - height / 2)}')
textField = tk.Label(wd)
textField.config(text="请点击查询")
textField.pack()

wd.mainloop()
