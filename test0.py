import json

# Sample data
data = {
    'details': [
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
}

# Dictionary to store categorized items
categorized_items = {}

# Process each item in 'details'
for item in data['details']:
    productName = item['productName']
    split_name = productName.split('@', 1)
    if len(split_name) == 2:
        category = split_name[1].strip()  # Extract the category after '@'
        memuid = productName.split(']')[0][1:]  # Extract memuid from '[XXXX]' part
        productPrice = item['productPrice']
        productCount = item['productCount']

        # Prepare the item in the required format
        formatted_item = {
            "ParentID": "SP1010",
            "MenuID": memuid,
            "MenuName": productName,
            "MenuUnit": ".",
            "PicImg": "",
            "MenuPrice": productPrice / productCount,
            "MenuPriceOld": productPrice / productCount,
            "MenuQty": productCount,
            "MenuPoint": 0,
            "MenuService": 0,
            "SumOfService": 0,
            "MenuAmt": productPrice,
            "CookList": "",
            "MenuList": []
        }

        # Add the formatted item to the corresponding category
        if category in categorized_items:
            categorized_items[category].append(formatted_item)
        else:
            categorized_items[category] = [formatted_item]

# Print categorized items
print(json.dumps(categorized_items, indent=4, ensure_ascii=False))