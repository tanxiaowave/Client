import pymssql
import winreg


def get_sql_aliases():
    aliases = []
    reg_path = r"SOFTWARE\Microsoft\MSSQLServer\Client\ConnectTo"

    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
        index = 0
        while True:
            try:
                sub_key_name = winreg.EnumKey(key, index)
                sub_key_path = reg_path + "\\" + sub_key_name
                sub_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key_path)
                server_name, _ = winreg.QueryValueEx(sub_key, "Server")
                port, _ = winreg.QueryValueEx(sub_key, "ServerPort")
                protocol, _ = winreg.QueryValueEx(sub_key, "ServerType")
                connection_options, _ = winreg.QueryValueEx(sub_key, "ConnectionOptions")

                alias_info = {
                    "Alias": sub_key_name,
                    "ServerName": server_name,
                    "Port": port,
                    "Protocol": protocol,
                    "ConnectionOptions": connection_options
                }
                aliases.append(alias_info)

                index += 1
            except FileNotFoundError:
                break
    except FileNotFoundError:
        pass

    return aliases


def connect_to_alias(alias_info, user, password, database):
    server = alias_info["ServerName"]
    port = alias_info["Port"]

    try:
        conn = pymssql.connect(server=f"{server}:{port}", user = user, password = password, database = database)
        print(f"成功连接到别名 {alias_info['Alias']}")
        conn.close()
    except pymssql.Error as ex:
        print(f"连接别名 {alias_info['Alias']} 失败: {str(ex)}")  # 获取并显示 SQL Server 别名信息


aliases = get_sql_aliases()
if aliases:
    for alias in aliases:
        print("别名: ", alias["Alias"])
        print("服务器名: ", alias["ServerName"])
        print("端口号: ", alias["Port"])
        print("协议: ", alias["Protocol"])
        print("其他连接参数: ", alias["ConnectionOptions"])
        print("---------------------")

        # 尝试连接到别名
        connect_to_alias(alias, user="sa", password="pos", database="rms_db")
else:
    print("未找到 SQL Server 别名信息。")