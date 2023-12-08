
import requests
import pandas as pd
import os


url = """https://www.dabangapp.com/api/3/room/new-list/multi-room/region?api_version=3.0.1&call_type=web&code=45113105&filters=%7B%22multi_room_type%22%3A%5B0%5D%2C%22selling_type%22%3A%5B0%5D%2C%22deposit_range%22%3A%5B0%2C999999%5D%2C%22price_range%22%3A%5B0%2C999999%5D%2C%22trade_range%22%3A%5B0%2C999999%5D%2C%22maintenance_cost_range%22%3A%5B0%2C999999%5D%2C%22room_size%22%3A%5B0%2C999999%5D%2C%22supply_space_range%22%3A%5B0%2C999999%5D%2C%22room_floor_multi%22%3A%5B1%2C2%2C3%2C4%2C5%2C6%2C7%2C-1%2C0%5D%2C%22division%22%3Afalse%2C%22duplex%22%3Afalse%2C%22room_type%22%3A%5B%5D%2C%22use_approval_date_range%22%3A%5B0%2C999999%5D%2C%22parking_average_range%22%3A%5B0%2C999999%5D%2C%22household_num_range%22%3A%5B0%2C999999%5D%2C%22parking%22%3Afalse%2C%22short_lease%22%3Afalse%2C%22full_option%22%3Afalse%2C%22elevator%22%3Afalse%2C%22balcony%22%3Afalse%2C%22safety%22%3Afalse%2C%22pano%22%3Afalse%2C%22is_contract%22%3Afalse%2C%22deal_type%22%3A%5B0%2C1%5D%2C%22animal%22%3Afalse%2C%22loan%22%3Afalse%7D&page=1&version=1&zoom=14"""

headers = {
  "authority": "www.dabangapp.com",
  "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
  "accept-language": "ko-KR,ko;q=0.9",
  "cache-control": "max-age=0",
  "sec-ch-ua": '"Google Chrome";v="119",,"Chromium";v="119",,"Not?A_Brand^";v="24"',
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": '"Windows"',
  "sec-fetch-dest": "document",
  "sec-fetch-mode": "navigate",
  "sec-fetch-site": "none",
  "sec-fetch-user": "?1",
  "upgrade-insecure-requests": "1",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
}


response = requests.get(url, verify=False, headers=headers)
data = response.json()["rooms"]
print(len(data))


colums = ["seq", "room_type_str", "location" ,"selling_type_str", "title", "price_title", "img_url", "img_urls", 'room_desc2']
df = pd.DataFrame(data)[colums]
df = df.rename(columns={"seq": "id", "room_type_str": "방 유형", "selling_type_str": "판매 유형", "price_title": "가격", "img_url": "대표사진", "img_urls": "사진", 'room_desc2': "상세내용"})

df = pd.DataFrame(data)[colums]
df[['lat', 'lng']] = df['location'].apply(pd.Series)
df.drop('location', axis=1, inplace=True)
print(response.text)
print(data)


output_dir = "../output/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_filename = os.path.join(output_dir, 'dabang_parsing_data.xlsx')
df.to_excel(output_filename, index=False)