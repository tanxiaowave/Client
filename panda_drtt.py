from collections import defaultdict
import json

# 假设这是你的产品数据列表
products = [
    {
        'productName': '[2204]清汤光头粉@米齐临',
        'productImg': '',
        'skuName': '[3918] 白米饭',
        'productPrice': 3.5,
        'productCount': 1
    },
    {
        'productName': '[3001]fried Chicken Breast@台湾炸鸡HB',
        'productImg': '',
        'skuName': '可加料',
        'productPrice': 33.2,
        'productCount': 1
    },
    {
        'productName': '[2125]笋干猪肚粉@米齐临',
        'productImg': '',
        'skuName': '可加料',
        'productPrice': 33.2,
        'productCount': 1
    },
    {
        'productName': '[2301]五香牛肉粉@米齐临',
        'productImg': '',
        'skuName': '可加料',
        'productPrice': 33.2,
        'productCount': 1
    },
    {
        'productName': '[1101]Breast&popcorn@台湾炸鸡HB',
        'productImg': '',
        'skuName': '可加料',
        'productPrice': 33.2,
        'productCount': 1
    },
    {
        'productName': '[1101]Black tea milk tea@台湾炸鸡HB',
        'productImg': '',
        'skuName': '可加料',
        'productPrice': 33.2,
        'productCount': 1
    },
    {
        'productName': '[3005]Popcorn Chicken脆皮鸡米花@台湾炸鸡HB',
        'productImg': '',
        'skuName': '可加料',
        'productPrice': 33.2,
        'productCount': 1
    }
]

# 使用 defaultdict 来按照分类整理产品
classified_items = defaultdict(list)

for product in products:
    # 解析产品名称字段，按@后面的名字分类
    name_parts = product['productName'].split('@')
    category = name_parts[1] if len(name_parts) > 1 else '未分类'

    # 构建每个产品的 item 字典
    item = {
        "ParentID": "SP1010",
        "MenuID": "some_unique_id",  # 需要为每个菜单项生成或提供唯一的ID
        "MenuName": product['productName'],
        "MenuUnit": ".",
        "PicImg": product['productImg'],
        "MenuPrice": product['productPrice'] / product['productCount'],
        "MenuPriceOld": product['productPrice'] / product['productCount'],
        "MenuQty": product['productCount'],
        "MenuPoint": 0,
        "MenuService": 0,
        "SumOfService": 0,
        "MenuAmt": product['productPrice'],
        "CookList": [],  # 暂时空列表，如有需要可添加具体内容
        "MenuList": []  # 空列表，如有需要可添加具体内容
    }

    # 将 item 添加到对应的分类列表中
    classified_items[category].append(item)

# 将分类结果转换为 JSON 格式并打印输出
classified_items_json = json.dumps(classified_items, ensure_ascii=False, indent=2)
print(classified_items_json)