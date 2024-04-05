# not completed
import pymssql
import configparser
import requests
import json

reader = configparser.ConfigParser()
reader.read("settings.INI")
server = reader.get("Database", "server")
user = reader.get("Database", "user")
sql_password = reader.get("Database", "password")
database = reader.get("Database", "database")
orgId = reader.get("Deliveroo_Branch", "orgId")
branchId = reader.get("Deliveroo_Branch", "branchId")

connect = pymssql.connect(server=server, user=user, password=sql_password, database=database,
                                              login_timeout=5)
cur = connect.cursor()
sql = f'select MenuID, menuname, menuprice4 from mn_Menu where menuid >= 1000'
cur.execute(sql)
sql_result = cur.fetchall()
# {
#     "name": { "1001": "name1" },
#     "price_info": { "price": 1380 },
#     "contains_alcohol": False,
#     "tax_rate": "20",
#     "id": "1001",
#     "operational_name": "[1001] name1"
# }
items = []
for line in sql_result:
    item = {}
    item['name'] = {line[0]:line[1].encode('latin-1').decode('gbk')}
    item['price_info'] = {'price': int(float(line[2]) * 100)}
    item['contains_alcohol'] = False
    item['tax_rate'] = "20"
    item['id'] = line[0]
    item['operational_name'] = "[" + line[0] + "] " + line[1].encode('latin-1').decode('gbk')
    items.append(item)

print(json.dumps(items, indent=2))
print(items)

# sql = f'select menutypeid, Menutypename from mn_Menutype'
# cur.execute(sql)
# sql_result = cur.fetchall()
# print(sql_result)
# print(sql_result[0][0])

# url = "https://auth.developers.deliveroo.com/oauth2/token"
# payload = "grant_type=client_credentials"
# headers = {
#     "accept": "application/json",
#     "content-type": "application/x-www-form-urlencoded",
#     "authorization": "Basic N2VjdWZiajhyYTI2OXJsNDkxZzdrZTRjbnE6dG1zbmlhNmcwcTNtdmE3c2o3cjhkdmJ1NWQzdDhjczZvZGJhNG03cXI3aXVlNGZtbWRl"
# }
# response = requests.post(url, data=payload, headers=headers)
# token = json.loads(response.text)['access_token']
#
# url = "https://api.developers.deliveroo.com/menu/v1/brands/ricecoming-gb/menus/8888"
#
# payload = {
#     "menu": { "items": items},
#     "name": "test menu",
#     "site_ids": ["243097"]
# }
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     "authorization": "Bearer " + token
# }
#
# response = requests.put(url, json=payload, headers=headers)
#
# print(response.text)
