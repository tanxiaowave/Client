import requests

cookies = {
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%221904045081412-0ca68084712dcd-26021e51-786432-190404508151e4%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221904045081412-0ca68084712dcd-26021e51-786432-190404508151e4%22%7D',
    '_cfuvid': 'mnXRCp_Ay_V.fYPa.BUxtwq3CmAB1v9wO3gRUrNF4OY-1720081668902-0.0.1.1-604800000',
    '__cf_bm': 'gpR0R7j8dsXq6xemnRN5bIs8U5ijg8f6xna7V9hoZhc-1720083156-1.0.1.1-3ixrKtvjyLOdIoEhojCdW7d2TA_dvmWfxAmkOumMAq.kpa.1RtCeJ1PZflAyjgEw83f1cNo7gmAR35VX.1RZsg',
}

headers = {
    'authority': 'track-eu.hungrypanda.co',
    'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'accept-language': 'zh-CN,zh;q=0.9',
    # 'cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221904045081412-0ca68084712dcd-26021e51-786432-190404508151e4%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221904045081412-0ca68084712dcd-26021e51-786432-190404508151e4%22%7D; _cfuvid=mnXRCp_Ay_V.fYPa.BUxtwq3CmAB1v9wO3gRUrNF4OY-1720081668902-0.0.1.1-604800000; __cf_bm=gpR0R7j8dsXq6xemnRN5bIs8U5ijg8f6xna7V9hoZhc-1720083156-1.0.1.1-3ixrKtvjyLOdIoEhojCdW7d2TA_dvmWfxAmkOumMAq.kpa.1RtCeJ1PZflAyjgEw83f1cNo7gmAR35VX.1RZsg',
    'referer': 'https://merchant-uk.hungrypanda.co/',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'image',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

params = {
    'project': 'production',
    'data': 'eyJkaXN0aW5jdF9pZCI6IjE5MDQwNDUwODE0MTItMGNhNjgwODQ3MTJkY2QtMjYwMjFlNTEtNzg2NDMyLTE5MDQwNDUwODE1MWU0IiwibGliIjp7IiRsaWIiOiJqcyIsIiRsaWJfbWV0aG9kIjoiY29kZSIsIiRsaWJfdmVyc2lvbiI6IjEuMTUuMjcifSwicHJvcGVydGllcyI6eyIkdGltZXpvbmVfb2Zmc2V0IjotNjAsIiRzY3JlZW5faGVpZ2h0Ijo3NjgsIiRzY3JlZW5fd2lkdGgiOjEwMjQsIiRsaWIiOiJqcyIsIiRsaWJfdmVyc2lvbiI6IjEuMTUuMjciLCIkbGF0ZXN0X3RyYWZmaWNfc291cmNlX3R5cGUiOiLnm7TmjqXmtYHph48iLCIkbGF0ZXN0X3NlYXJjaF9rZXl3b3JkIjoi5pyq5Y+W5Yiw5YC8X+ebtOaOpeaJk+W8gCIsIiRsYXRlc3RfcmVmZXJyZXIiOiIiLCJwcm9kdWN0X2lkIjo0LCJwbGF0Zm9ybV9pZCI6MywiY291bnRyeV9uYW1lIjoi6Iux5Zu9IiwiY2l0eV9uYW1lIjoiIiwic3lzdGVtX2xhbmd1YWdlIjoiQ04iLCJhcHBfbGFuZ3VhZ2UiOiJDTiIsIiRlbGVtZW50X3R5cGUiOiJhIiwiJGVsZW1lbnRfY2xhc3NfbmFtZSI6IiIsIiRlbGVtZW50X2NvbnRlbnQiOiJWaWV3IiwiJHVybCI6Imh0dHBzOi8vbWVyY2hhbnQtdWsuaHVuZ3J5cGFuZGEuY28vb3JkZXIvb3JkZXJtYW5hZ2UiLCIkdXJsX3BhdGgiOiIvb3JkZXIvb3JkZXJtYW5hZ2UiLCIkdGl0bGUiOiJPcmRlcnMiLCIkdmlld3BvcnRfd2lkdGgiOjQ0MSwiJGVsZW1lbnRfc2VsZWN0b3IiOiIjcm9vdCA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgyKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgyKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgyKSA+IGRpdjpudGgtb2YtdHlwZSgyKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IGRpdjpudGgtb2YtdHlwZSgxKSA+IHRhYmxlOm50aC1vZi10eXBlKDEpID4gdGJvZHk6bnRoLW9mLXR5cGUoMSkgPiB0cjpudGgtb2YtdHlwZSgxKSA+IHRkOm50aC1vZi10eXBlKDYpID4gYTpudGgtb2YtdHlwZSgxKSIsIiRpc19maXJzdF9kYXkiOmZhbHNlfSwiYW5vbnltb3VzX2lkIjoiMTkwNDA0NTA4MTQxMi0wY2E2ODA4NDcxMmRjZC0yNjAyMWU1MS03ODY0MzItMTkwNDA0NTA4MTUxZTQiLCJ0eXBlIjoidHJhY2siLCJldmVudCI6IiRXZWJDbGljayIsIl90cmFja19pZCI6MzkwNzg0NDgwfQ==',
    'ext': 'crc=-859354530',
}

response = requests.get('https://track-eu.hungrypanda.co/sa.gif', params=params, cookies=cookies, headers=headers)


headers = {
    'authority': 'uk-gateway.hungrypanda.co',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'countrycode': 'GB',
    'lang': 'en-US',
    'origin': 'https://merchant-uk.hungrypanda.co',
    'platform': 'H5',
    'referer': 'https://merchant-uk.hungrypanda.co/',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'token': '9531bb9a5320a79d0cafe74034df2c08',
    'uniquetoken': '90fccb9c-7466-457a-b035-ff9828cc746f',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

json_data = {
    'orderSn': '015899164901175329590',
}

response = requests.post('https://uk-gateway.hungrypanda.co/api/merchant/order/detail', headers=headers, json=json_data)
time.sleep(60)