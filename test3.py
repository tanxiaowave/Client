from DrissionPage import ChromiumOptions, ChromiumPage
import base64
import requests,json
from DrissionPage.common import Actions

co = ChromiumOptions().set_local_port(9113)
# 用 d 模式创建页面对象（默认模式）
page = ChromiumPage(co)
ac = Actions(page)
# time.sleep(5)
page.get('file:///C:/Users/X/Downloads/Merchant%20login.html')

def img_download():

    img = page('.geetest_bg_73e850cf geetest_bg')
    img.get_screenshot(path='tmp', name='pic.png')

def img_data():

    url = "https://api.jfbym.com/api/YmServer/customApi"

    with open(r'.\tmp\pic.png','rb') as f:
        im = base64.b64encode(f.read()).decode()


    data = {
        "token":"PvnOdYXAPcAspNnvqSBIPugniFrpnjCchn0WyohgZTU",  #输入自己的token
        "type":"22222",
        "image":im,#待识别图的base64

    }


    _headers = {
            'Content-Type': 'application/json'
        }
    response = requests.request("POST", url, headers=_headers, json=data)
    if response.status_code == 200:
        # Extract JSON data from the response
        response_data = response.json()

        # Access 'data' field from the JSON response
        data_value = response_data['data']['data']
        print(response_data)
        # Now you can work with 'data_value'
        print(data_value)
        return data_value
    else:
        print(f"Request failed with status code {response.status_code}")


def ac_hold():
    img_download()
    data_value = img_data()
    ac.hold('.geetest_arrow_73e850cf geetest_arrow geetest_arrow_1')
    # 向右移动鼠标300像素
    ac.right(int(data_value))
    # 释放左键
    ac.release()

ac_hold()


