import requests
import json

appkey = '1b44a528-58de-4f07-b842-31cc492f0ede'
headers = {
        "Content-Type": "application/json",
        "appKey": appkey,
        "timestamp": "{{$timestamp}}",
}
data = {
  "shopId": "724",
  "categories": [
    {
      "id": "c1",
      "name": "啤酒 Beer",
      "sequence": 1,
    },
    {
      "id": "c2",
      "name": "软饮 Soft Drinks",
      "sequence": 2,
    },
    {
      "id": "c3",
      "name": "热饮 Hot Drinks",
      "sequence": 3,
    },
    {
      "id": "c4",
      "name": "头盘 Appertizer",
      "sequence": 4,
    },
    {
      "id": "c5",
      "name": "湘味热卤 Hunan Style Braised Stew",
      "sequence": 5,
    },
    {
      "id": "c6",
      "name": "主食 Main Food",
      "sequence": 6,
    },
    {
      "id": "c7",
      "name": "加码 Extra Topping",
      "sequence": 7,
    },
    {
      "id": "c8",
      "name": "加菜 Extra Side Dishes",
      "sequence": 8,
    },
    {
      "id": "c9",
      "name": "蒸菜 Steamed Dishes",
      "sequence": 9,
    },
    {
      "id": "c10",
      "name": "炒饭面 Stir Fried Rice and Noodles",
      "sequence": 10,
    },
    {
      "id": "c11",
      "name": "点心 Dimsum",
      "sequence": 11,
    },
    {
      "id": "c12",
      "name": "甜点 Dessert",
      "sequence": 12,
    },
  ],
  "products": [
    {
      "id": "p1",
      "categoryId": "c1",
      "name": "[1101] 百威 Budweiser",
      "nameEn": "[1101] 百威 Budweiser",
      "price": 3.8,
      "sequence": 1,
    },
    {
      "id": "p2",
      "categoryId": "c1",
      "name": "[1102] 青岛啤酒 Tsingtao",
      "nameEn": "[1102] 青岛啤酒 Tsingtao",
      "price": 3.8,
      "sequence": 1,
    },
    {
      "id": "p3",
      "categoryId": "c1",
      "name": "[1103] 扎啤 (Half Pint) Tiger Beer",
      "nameEn": "[1103] 扎啤 (Half Pint) Tiger Beer",
      "price": 4.5,
      "sequence": 1,
    },
    {
      "id": "p4",
      "categoryId": "c1",
      "name": "[1104] 扎啤 (Pint) Tiger Beer",
      "nameEn": "[1104] 扎啤 (Pint) Tiger Beer",
      "price": 6.5,
      "sequence": 1,
    },
    {
      "id": "p5",
      "categoryId": "c2",
      "name": "[2001] 有机米浆 Rice Juice",
      "nameEn": "[2001] 有机米浆 Rice Juice",
      "price": 3,
      "sequence": 1,
    },
    {
      "id": "p6",
      "categoryId": "c2",
      "name": "[2002] 鲜榨豆浆 Fresh Soy Milk",
      "nameEn": "[2002] 鲜榨豆浆 Fresh Soy Milk",
      "price": 3,
      "sequence": 1,
    },
    {
      "id": "p7",
      "categoryId": "c2",
      "name": "[2003] 王老吉 Herbal Tea",
      "nameEn": "[2003] 王老吉 Herbal Tea",
      "price": 3,
      "sequence": 1,
    },
    {
      "id": "p8",
      "categoryId": "c2",
      "name": "[2004] 酸梅汤 Sour Plum",
      "nameEn": "[2004] 酸梅汤 Sour Plum",
      "price": 3,
      "sequence": 1,
    },
    {
      "id": "p9",
      "categoryId": "c2",
      "name": "[2005] 绿茶 Green Tea",
      "nameEn": "[2005] 绿茶 Green Tea",
      "price": 3,
      "sequence": 1,
    },
    {
      "id": "p10",
      "categoryId": "c2",
      "name": "[2006] 红茶 Red Tea",
      "nameEn": "[2006] 红茶 Red Tea",
      "price": 3,
      "sequence": 1,
    },
    {
      "id": "p11",
      "categoryId": "c2",
      "name": "[2007] 可乐 Coke",
      "nameEn": "[2007] 可乐 Coke",
      "price": 2.5,
      "sequence": 1,
    },
    {
      "id": "p12",
      "categoryId": "c2",
      "name": "[2008] 健怡可乐 Diet Coke",
      "nameEn": "[2008] 健怡可乐 Diet Coke",
      "price": 2.5,
      "sequence": 1,
    },
    {
      "id": "p13",
      "categoryId": "c2",
      "name": "[2009] 雪碧 7up",
      "nameEn": "[2009] 雪碧 7up",
      "price": 2.5,
      "sequence": 1,
    },

    {
      "id": "p14",
      "categoryId": "c2",
      "name": "[2010] 芬达 Fanta",
      "nameEn": "[2010] 芬达 Fanta",
      "price": 2.5,
      "sequence": 1,
    },

    {
      "id": "p15",
      "categoryId": "c2",
      "name": "[2011] 矿泉水 Still Water",
      "nameEn": "[2011] 矿泉水 Still Water",
      "price": 2.5,
      "sequence": 1,
    },

    {
      "id": "p16",
      "categoryId": "c2",
      "name": "[2012] 气泡水 Sparkling Water",
      "nameEn": "[2012] 气泡水 Sparkling Water",
      "price": 2.5,
      "sequence": 1,
    },
    {
      "id": "p17",
      "categoryId": "c3",
      "name": "[2101] 茉莉花茶 Jasmine Flower Tea",
      "nameEn": "[2101] 茉莉花茶 Jasmine Flower Tea",
      "price": 2.5,
      "sequence": 1,
    },
    {
      "id": "p18",
      "categoryId": "c3",
      "name": "[2102] 乌龙茶 Uoolong Tea",
      "nameEn": "[2102] 乌龙茶 Uoolong Tea",
      "price": 2.5,
      "sequence": 1,
    },
    {
      "id": "p19",
      "categoryId": "c3",
      "name": "[2103] 绿茶 Green Tea",
      "nameEn": "[2103] 绿茶 Green Tea",
      "price": 2.5,
      "sequence": 1,
    },
    {
      "id": "p20",
      "categoryId": "c3",
      "name": "[2104] 菊花茶 Chrysanthemum Tea",
      "nameEn": "[2104] 菊花茶 Chrysanthemum Tea",
      "price": 3,
      "sequence": 1,
    },
    {
      "id": "p21",
      "categoryId": "c3",
      "name": "[2106] 鲜榨热豆浆 Hot Soy Milk",
      "nameEn": "[2106] 鲜榨热豆浆 Hot Soy Milk",
      "price": 3,
      "sequence": 1,
    },
    {
      "id": "p22",
      "categoryId": "c3",
      "name": "[2107] 蜂蜜柚子茶 Honey Citron Tea",
      "nameEn": "[2107] 蜂蜜柚子茶 Honey Citron Tea",
      "price": 4.8,
      "sequence": 1,
    },
    {
      "id": "p23",
      "categoryId": "c4",
      "name": "[4301] 红薯片 Crisps",
      "nameEn": "[4301] 红薯片 Crisps",
      "price": 4.8,
      "sequence": 1,
    },
    {
      "id": "p24",
      "categoryId": "c4",
      "name": "[3003] 素春卷 Spring Roll",
      "nameEn": "[3003] 素春卷 Spring Roll",
      "price": 4.8,
      "sequence": 1,
    },

    {
      "id": "p25",
      "categoryId": "c4",
      "name": "[3004] 湘味小酥肉 Crispy Pork",
      "nameEn": "[3004] 湘味小酥肉 Crispy Pork",
      "price": 5.8,
      "sequence": 1,
    },

    {
      "id": "p26",
      "categoryId": "c4",
      "name": "[3005] 椒盐魷鱼 Squid",
      "nameEn": "[3005] 椒盐魷鱼 Squid",
      "price": 5.8,
      "sequence": 1,
    },

    {
      "id": "p27",
      "categoryId": "c4",
      "name": "[3008] 虾春卷 Prawn Spring Roll",
      "nameEn": "[3008] 虾春卷 Prawn Spring Roll",
      "price": 5.8,
      "sequence": 1,
    },

    {
      "id": "p28",
      "categoryId": "c4",
      "name": "[3009] 葱油粑粑 Spring Onion Rice Pancake",
      "nameEn": "[3009] 葱油粑粑 Spring Onion Rice Pancake",
      "price": 4.8,
      "sequence": 1,
    },

    {
      "id": "p29",
      "categoryId": "c5",
      "name": "[3101] 混拼(猪脚牛肉鱼丸香干萝卜) trotter+beef+fish+tofu+radish",
      "nameEn": "[3101] 混拼(猪脚牛肉鱼丸香干萝卜) trotter+beef+fish+tofu+radish",
      "price": 5.8,
      "sequence": 1,
    },
    {
      "id": "p30",
      "categoryId": "c5",
      "name": "[3102] 湘卤单拼(猪脚x3) Braised Stew (pork trotter x3)",
      "nameEn": "[3102] 湘卤单拼(猪脚x3) Braised Stew (pork trotter x3)",
      "price": 6.8,
      "sequence": 1,
    },

    {
      "id": "p31",
      "categoryId": "c5",
      "name": "[3103] 湘卤单拼(牛肉丸x4) Braised Stew (beef ball x4)",
      "nameEn": "[3103] 湘卤单拼(牛肉丸x4) Braised Stew (beef ball x4)",
      "price": 6.8,
      "sequence": 1,
    },

    {
      "id": "p32",
      "categoryId": "c5",
      "name": "[3104] 湘卤单拼(鱼丸x4) Braised Stew (fish ball x4)",
      "nameEn": "[3104] 湘卤单拼(鱼丸x4) Braised Stew (fish ball x4)",
      "price": 6.8,
      "sequence": 1,
    },

    {
      "id": "p33",
      "categoryId": "c5",
      "name": "[3105] 湘卤单拼(三角香干x3) Braised Stew (triangular dried tofu x3)",
      "nameEn": "[3105] 湘卤单拼(三角香干x3) Braised Stew (triangular dried tofu x3)",
      "price": 6.8,
      "sequence": 1,
    },

    {
      "id": "p34",
      "categoryId": "c5",
      "name": "[3106] 湘卤单拼(白萝卜x5) Braised Stew (radish x5)",
      "nameEn": "[3106] 湘卤单拼(白萝卜x5) Braised Stew (radish x5)",
      "price": 6.8,
      "sequence": 1,
    },

    {
      "id": "p35",
      "categoryId": "c6",
      "name": "[4201] 碟头饭套餐 Steamed Rice + One Topping",
      "nameEn": "[4201] 碟头饭套餐 Steamed Rice + One Topping",
      "price": 10.8,
      "sequence": 1,
    },
    {
      "id": "p36",
      "categoryId": "c6",
      "name": "[4202] 汤米粉套餐 Rice Noodle Soup + One Topping",
      "nameEn": "[4202] 汤米粉套餐 Rice Noodle Soup + One Topping",
      "price": 10.8,
      "sequence": 1,
    },
    {
      "id": "p37",
      "categoryId": "c6",
      "name": "[4204] 汤面套餐 Noodle Soup + One Topping",
      "nameEn": "[4204] 汤面套餐 Noodle Soup + One Topping",
      "price": 10.8,
      "sequence": 1,
    },
    {
      "id": "p38",
      "categoryId": "c6",
      "name": "[4206] 白米饭 Rice",
      "nameEn": "[4206] 白米饭 Rice",
      "price": 2,
      "sequence": 2,
    },
    {
      "id": "p100",
      "categoryId": "c6",
      "name": "[4207] 清汤米粉 Rice Noodle",
      "nameEn": "[4207] 清汤米粉 Rice Noodle",
      "price": 2,
      "sequence": 2,
    },
    {
      "id": "p101",
      "categoryId": "c6",
      "name": "[4208] 清汤面 Noodle",
      "nameEn": "[4208] 清汤面 Noodle",
      "price": 2,
      "sequence": 2,
    },

    {
      "id": "p39",
      "categoryId": "c7",
      "name": "[4101] 素三鲜 Mixed Vegetable",
      "nameEn": "[4101] 素三鲜 Mixed Vegetable",
      "price": 4,
      "sequence": 1,
    },
    {
      "id": "p40",
      "categoryId": "c7",
      "name": "[4102] 一品牛腩 Braised Beef Brisket",
      "nameEn": "[4102] 一品牛腩 Braised Beef Brisket",
      "price": 4,
      "sequence": 1,
    },

    {
      "id": "p41",
      "categoryId": "c7",
      "name": "[4103] 五香牛肉 Five-spiced Sliced Beef",
      "nameEn": "[4103] 五香牛肉 Five-spiced Sliced Beef",
      "price": 4,
      "sequence": 1,
    },

    {
      "id": "p42",
      "categoryId": "c7",
      "name": "[4104] 酸辣鸡丁 Hot Sour Diced Chicken",
      "nameEn": "[4104] 酸辣鸡丁 Hot Sour Diced Chicken",
      "price": 4,
      "sequence": 1,
    },

    {
      "id": "p43",
      "categoryId": "c7",
      "name": "[4105] 农家小炒肉 Sliced Pork Belly",
      "nameEn": "[4105] 农家小炒肉 Sliced Pork Belly",
      "price": 4,
      "sequence": 1,
    },

    {
      "id": "p44",
      "categoryId": "c7",
      "name": "[4106] 酸豆角肉末 Pork Mince",
      "nameEn": "[4106] 酸豆角肉末 Pork Mince",
      "price": 4,
      "sequence": 1,
    },

    {
      "id": "p45",
      "categoryId": "c7",
      "name": "[4108] 笋干肚丝 Pig Stomach",
      "nameEn": "[4108] 笋干肚丝 Pig Stomach",
      "price": 4,
      "sequence": 1,
    },

    {
      "id": "p46",
      "categoryId": "c8",
      "name": "[5001] 绝味鸭脖 Duck Neck",
      "nameEn": "[5001] 绝味鸭脖 Duck Neck",
      "price": 5.8,
      "sequence": 1,
    },
    {
      "id": "p47",
      "categoryId": "c8",
      "name": "[5002] 绝味鸭翅 Duck Wing",
      "nameEn": "[5002] 绝味鸭翅 Duck Wing",
      "price": 5.8,
      "sequence": 1,
    },

    {
      "id": "p48",
      "categoryId": "c8",
      "name": "[4303] 剁椒牙白 Chinese Leaf",
      "nameEn": "[4303] 剁椒牙白 Chinese Leaf",
      "price": 6.8,
      "sequence": 1,
    },

    {
      "id": "p49",
      "categoryId": "c8",
      "name": "[5004] 酱焗猪手 Pork Trotters",
      "nameEn": "[5004] 酱焗猪手 Pork Trotters",
      "price": 6.8,
      "sequence": 1,
    },

    {
      "id": "p50",
      "categoryId": "c8",
      "name": "[5005] 姜辣凤爪 Chicken Feet",
      "nameEn": "[5005] 姜辣凤爪 Chicken Feet",
      "price": 6.8,
      "sequence": 1,
    },

    {
      "id": "p51",
      "categoryId": "c8",
      "name": "[5006] 卤猪耳 Pork Ear",
      "nameEn": "[5006] 卤猪耳 Pork Ear",
      "price": 6.8,
      "sequence": 1,
    },

    {
      "id": "p52",
      "categoryId": "c8",
      "name": "[5007] 卤牛腱子肉 Beef Tendon",
      "nameEn": "[5007] 卤牛腱子肉 Beef Tendon",
      "price": 8.8,
      "sequence": 1,
    },

    {
      "id": "p53",
      "categoryId": "c8",
      "name": "[5011] 农家小炒肉（大份） Pork Belly (Big)",
      "nameEn": "[5011] 农家小炒肉（大份） Pork Belly (Big)",
      "price": 9.8,
      "sequence": 1,
    },

    {
      "id": "p54",
      "categoryId": "c8",
      "name": "[5013] 香煎荷包蛋 Fried Egg",
      "nameEn": "[5013] 香煎荷包蛋 Fried Egg",
      "price": 1.5,
      "sequence": 1,
    },

    {
      "id": "p55",
      "categoryId": "c9",
      "name": "[5101] 湘味豉椒排骨 Steamed Pork Ribs with Black Bean Pepper",
      "nameEn": "[5101] 湘味豉椒排骨 Steamed Pork Ribs with Black Bean Pepper",
      "price": 8.8,
      "sequence": 1,
    },
    {
      "id": "p56",
      "categoryId": "c9",
      "name": "[5102] 腊味双蒸（腊肉、腊排骨） Steamed Preserved Pork Belly and Ribs",
      "nameEn": "[5102] 腊味双蒸（腊肉、腊排骨） Steamed Preserved Pork Belly and Ribs",
      "price": 8.8,
      "sequence": 1,
    },

    {
      "id": "p57",
      "categoryId": "c9",
      "name": "[5103] 香干蒸腊肉 Steamed Preserved Pork Belly with Dried Tofu",
      "nameEn": "[5103] 香干蒸腊肉 Steamed Preserved Pork Belly with Dried Tofu",
      "price": 8.8,
      "sequence": 1,
    },

    {
      "id": "p58",
      "categoryId": "c9",
      "name": "[5104] 湘味蒸腊鸭 Steamed Preserved Duck",
      "nameEn": "[5104] 湘味蒸腊鸭 Steamed Preserved Duck",
      "price": 8.8,
      "sequence": 1,
    },

    {
      "id": "p59",
      "categoryId": "c9",
      "name": "[5105] 湘味扣肉 Braised Pork with Preserved Vegetables",
      "nameEn": "[5105] 湘味扣肉 Braised Pork with Preserved Vegetables",
      "price": 9.8,
      "sequence": 1,
    },

    {
      "id": "p60",
      "categoryId": "c10",
      "name": "[5201] 蛋炒饭 Egg Fried Rice",
      "nameEn": "[5201] 蛋炒饭 Egg Fried Rice",
      "price": 6.8,
      "sequence": 1,
    },
    {
      "id": "p61",
      "categoryId": "c10",
      "name": "[5202] 鸡丝炒面 Chicken Chow Mein",
      "nameEn": "[5202] 鸡丝炒面 Chicken Chow Mein",
      "price": 8.8,
      "sequence": 1,
    },

    {
      "id": "p62",
      "categoryId": "c10",
      "name": "[5203] 鸡丝炒饭 Chicken Fried Rice",
      "nameEn": "[5203] 鸡丝炒饭 Chicken Fried Rice",
      "price": 8.8,
      "sequence": 1,
    },

    {
      "id": "p63",
      "categoryId": "c10",
      "name": "[5204] 什菜炒面 Stir Fried Mixed Vegetable Fried Noodles",
      "nameEn": "[5204] 什菜炒面 Stir Fried Mixed Vegetable Fried Noodles",
      "price": 8.8,
      "sequence": 1,
    },

    {
      "id": "p64",
      "categoryId": "c10",
      "name": "[5205] 什菜炒饭 Stir Fried Mixed Vegetable Fried Rice",
      "nameEn": "[5205] 什菜炒饭 Stir Fried Mixed Vegetable Fried Rice",
      "price": 8.8,
      "sequence": 1,
    },

    {
      "id": "p65",
      "categoryId": "c10",
      "name": "[5206] 农家小炒肉炒面 Stir Fried Pork Belly Fried Noodles",
      "nameEn": "[5206] 农家小炒肉炒面 Stir Fried Pork Belly Fried Noodles",
      "price": 10.8,
      "sequence": 1,
    },

    {
      "id": "p66",
      "categoryId": "c10",
      "name": "[5207] 农家小炒肉炒饭 Stir Fried Pork Belly Fried Rice",
      "nameEn": "[5207] 农家小炒肉炒饭 Stir Fried Pork Belly Fried Rice",
      "price": 10.8,
      "sequence": 1,
    },

    {
      "id": "p67",
      "categoryId": "c10",
      "name": "[5208] 大虾炒面 Stir Fried King Prawn Fried Noodles",
      "nameEn": "[5208] 大虾炒面 Stir Fried King Prawn Fried Noodles",
      "price": 11.8,
      "sequence": 1,
    },

    {
      "id": "p68",
      "categoryId": "c10",
      "name": "[5209] 大虾炒饭 Stir Fried King Prawn Fried Rice",
      "nameEn": "[5209] 大虾炒饭 Stir Fried King Prawn Fried Rice",
      "price": 11.8,
      "sequence": 1,
    },

    {
      "id": "p69",
      "categoryId": "c11",
      "name": "[7001] 虾饺(4) Prawn Dumpling",
      "nameEn": "[7001] 虾饺(4) Prawn Dumpling",
      "price": 4.8,
      "sequence": 1,
    },
    {
      "id": "p70",
      "categoryId": "c11",
      "name": "[7003] 叉烧包(3) Char Siew Bun",
      "nameEn": "[7003] 叉烧包(3) Char Siew Bun",
      "price": 4.8,
      "sequence": 1,
    },

    {
      "id": "p71",
      "categoryId": "c11",
      "name": "[7004] 烧卖(4) Siomai",
      "nameEn": "[7004] 烧卖(4) Siomai",
      "price": 4.8,
      "sequence": 1,
    },

    {
      "id": "p72",
      "categoryId": "c11",
      "name": "[7007] 猪肉大包(1) Large Pork Bun",
      "nameEn": "[7007] 猪肉大包(1) Large Pork Bun",
      "price": 3,
      "sequence": 1,
    },

    {
      "id": "p73",
      "categoryId": "c11",
      "name": "[7008] 湘味烧麦(1) Siomai in Hunan Style",
      "nameEn": "[7008] 湘味烧麦(1) Siomai in Hunan Style",
      "price": 3,
      "sequence": 1,
    },

    {
      "id": "p74",
      "categoryId": "c12",
      "name": "[8001] 糖油粑粑 Rice Pancake",
      "nameEn": "[8001] 糖油粑粑 Rice Pancake",
      "price": 4.8,
      "sequence": 1,
    },
    {
      "id": "p75",
      "categoryId": "c12",
      "name": "[4302] 米酒汤圆 Glugtinous Rice Ball",
      "nameEn": "[4302] 米酒汤圆 Glugtinous Rice Ball",
      "price": 5.8,
      "sequence": 1,
    },

    {
      "id": "p76",
      "categoryId": "c12",
      "name": "[8004] 南瓜饼 Pumpkin Cake",
      "nameEn": "[8004] 南瓜饼 Pumpkin Cake",
      "price": 4.8,
      "sequence": 1,
    },

  ],
  "optionGroups": [
    {
      "id": "op11",
      "name": "码头",
      "nameEn": "Topping",
      "required": True,
      "multiSelected": False,
      "min": 0,
      "max": 1,
      "options": [
        {
          "id": "o11",
          "name": "素三鲜 Mixed Vegetable",
          "nameEn": "素三鲜 Mixed Vegetable",
          "price": 0,
        },
        {
          "id": "o12",
          "name": "一品牛腩 Braised Beef Brisket",
          "nameEn": "一品牛腩 Braised Beef Brisket",
          "price": 0,
        },
        {
          "id": "o13",
          "name": "五香牛肉 Five-spiced Sliced Beef",
          "nameEn": "五香牛肉 Five-spiced Sliced Beef",
          "price": 0,
        },
        {
          "id": "o14",
          "name": "酸辣鸡丁 Hot Sour Diced Chicken",
          "nameEn": "酸辣鸡丁 Hot Sour Diced Chicken",
          "price": 0,
        },
        {
          "id": "o15",
          "name": "农家小炒肉 Sliced Pork Belly",
          "nameEn": "农家小炒肉 Sliced Pork Belly",
          "price": 0,
        },
        {
          "id": "o16",
          "name": "酸豆角肉末 Pork Mince",
          "nameEn": "酸豆角肉末 Pork Mince",
          "price": 0,
        },
        {
          "id": "o17",
          "name": "笋干肚丝 Pig Stomach",
          "nameEn": "笋干肚丝 Pig Stomach",
          "price": 0,
        },
      ],
      "productIds": [
        "p35","p36","p37"
      ]
    }
  ]
}
url = "https://openapi.fantuan.ca/api/v1/menu/uploadMenu"
response = json.loads(requests.post(url, json=data, headers=headers).text)
print(response)