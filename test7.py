# 定义要替换的新的 token 和 order_sn 值
new_token = '99aa24a203b107d41ab461f7def13146'
new_order_sn = '462511524052176362624'

# 定义 JavaScript 文件路径
js_file_path = 'get_json_data.js'

try:
    # 打开 JavaScript 文件进行读取
    with open(js_file_path, 'r') as file:
        js_code = file.read()

        # 替换 token 和 order_sn 的值
        js_code = js_code.replace('{tokens}', new_token)
        js_code = js_code.replace('{ordersns}', new_order_sn)

    # 打开 JavaScript 文件进行写入，写入替换后的内容
    with open(js_file_path, 'w') as file:
        file.write(js_code)

    print(f'Successfully replaced token and order_sn values in {js_file_path}.')

except FileNotFoundError:
    print(f'Error: File {js_file_path} not found.')

except Exception as e:
    print(f'Error: {e}')