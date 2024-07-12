async function fetchOrderDetails() {
    const url = 'https://uk-gateway.hungrypanda.co/api/merchant/order/detail';
    const headers = {
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
        'token': '{tokenst}',
        // 'cookie':'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221904045081412-0ca68084712dcd-26021e51-786432-190404508151e4%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%221904045081412-0ca68084712dcd-26021e51-786432-190404508151e4%22%7D; _cfuvid=mnXRCp_Ay_V.fYPa.BUxtwq3CmAB1v9wO3gRUrNF4OY-1720081668902-0.0.1.1-604800000; __cf_bm=gpR0R7j8dsXq6xemnRN5bIs8U5ijg8f6xna7V9hoZhc-1720083156-1.0.1.1-3ixrKtvjyLOdIoEhojCdW7d2TA_dvmWfxAmkOumMAq.kpa.1RtCeJ1PZflAyjgEw83f1cNo7gmAR35VX.1RZsg',
        'uniquetoken': 'fe33fe5a-92b0-4fe8-b3fd-7e700701b93f',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    };

    const requestData = {
        orderSn: '{ordersnst}'
    };

    const fetchData = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(requestData),
        compress: true
    };

    try {
        const response = await fetch(url, fetchData);
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Response:', data);
        return data;
    } catch (error) {
        console.error('Error:', error);
    }
}

return fetchOrderDetails();