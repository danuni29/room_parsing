import requests
import pandas as pd
import geohash2
import os


def parsing_zigbang(addr):

    url = f"https://apis.zigbang.com/v2/search?leaseYn=N&q={addr}&serviceType=원룸"
    response = requests.get(url)
    # print(response.json()["items"])
    data = response.json()["items"][0]
    lat, lng = data["lat"], data["lng"]

    geohash = geohash2.encode(lat, lng, precision=5)
    # print(geohash)
    url = f"https://apis.zigbang.com/v2/items?deposit_gteq=0&domain=zigbang&geohash={geohash}&needHasNoFiltered=true&rent_gteq=0&sales_type_in=전세|월세&service_type_eq=원룸"
    response = requests.get(url)
    items = response.json()["items"]
    # print(items)
    ids = [item["item_id"] for item in items]


    # Post 방식 -> url 안에 데이터가 없기 때문에 params로 따로 데이터를 만들어서 설정해줘야 함
    url = "https://apis.zigbang.com/v2/items/list"
    params = {
        "domain": "zigbang",
        # "withCoalition": "true",
        "item_ids": ids[:900]
    }
    response = requests.post(url, json=params)
    # print(response.json())

    items = response.json()["items"]
    # print(items)


    colums = ["item_id", "sales_type", "deposit", "rent", "random_location", "manage_cost", 'images_thumbnail']
    df = pd.DataFrame(items)[colums]
    # df = df[df["address1"].str.contains(addr)].reset_index(drop=True)
    df = df.rename(columns={ "sales_type": "유형", "deposit": "보증금", "rent": "월세", "manage_cost": "관리비", 'images_thumbnail': "사진"})
    # random_location 에서 위경도를 분리하자!!!!!!!!
    df[['lat', 'lon']] = df['random_location'].apply(pd.Series)
    # random_location 열 제거
    df.drop('random_location', axis=1, inplace=True)
    # 다누니 폼 미춌다잉

    output_dir = "../output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, f'zigbang_parsing_data_{addr}.xlsx')
    df.to_excel(output_filename, index=False)



