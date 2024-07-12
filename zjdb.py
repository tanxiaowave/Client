import sqlite3
import pymssql
import configparser

reader = configparser.ConfigParser()
reader.read("settings.INI")
server = reader.get("Database", "server")
user = reader.get("Database", "user")
sql_password = reader.get("Database", "password")
database = reader.get("Database", "database")

#连接到数据库
connect = pymssql.connect(server=server, user=user, password=sql_password, database=database,
                          login_timeout=5, tds_version='7.0')
cur = connect.cursor()

# 检查并填充数据
for i in range(9950, 1000000):
    cur.execute("SELECT COUNT(*) FROM mn_Menu WHERE MenuID=%s", (i,))
    if cur.fetchone()[0] == 0:
        insert_query = "INSERT INTO mn_Menu (MenuID, MenuName, ToSpell, MenuTypeID, MenuUnit) VALUES (%s, 'other_values', 'other_values', 30, '')"
        cur.execute(insert_query, (i,))
    else:
        print(f"id 为 {i} 的数据已存在，无需修改")

# 提交并关闭连接
connect.commit()
connect.close()