from http.server import BaseHTTPRequestHandler, HTTPServer
from json import loads

# 初始化服务器的IP地址和端口号，这里使用了0.0.0.0，这样服务器可以在任何网络接口上监听。
server_address = ("127.0.0.1", 8000)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 处理POST请求
        content_length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(content_length)

        # 数据格式化为json
        json_data = loads(data.decode())

        # 打印接收到的数据
        print(f"Received data: {json_data}")

        self.send_response(200)
        self.end_headers()
        # 返回一段简单的响应体
        self.wfile.write(b"Data received successfully!")

if __name__ == '__main__':
    # 创建服务器实例
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Server running on port {server_address[1]}")
    # 开始监听
    httpd.serve_forever()