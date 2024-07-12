import json
import requests

# 要发送的JSON数据
data = {
    "name": "John Doe",
    "age": 30,
    "city": "New York"
}

# 服务器地址和端口号
url = "http://127.0.0.1:8000"

# 使用requests库发送POST请求
response = requests.post(url, json=data)

# 打印服务器返回的响应体
print(response.text)