
import requests
import pandas as pd
import os

def dabang_parsing(url, region):

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
  # print(len(data))


  colums = ["seq", "id", "room_type_str", "location" ,"selling_type_str", "title", "price_title", "img_url", "img_urls", 'room_desc2']
  df = pd.DataFrame(data)[colums]
  # df1 = df.rename(columns={"seq": "id", "room_type_str": "방 유형", "selling_type_str": "판매 유형", "price_title": "가격", "img_url": "대표사진", "img_urls": "사진", 'room_desc2': "상세내용"})
  #
  # df1 = pd.DataFrame(data)[colums]
  df[['lon', 'lat']] = df['location'].apply(pd.Series)
  df.drop('location', axis=1, inplace=True)
  # print(df['lat'])



  output_dir = "../output/"
  if not os.path.exists(output_dir):
      os.makedirs(output_dir)

  output_filename = os.path.join(output_dir, f'dabang_parsing_data_{region}.xlsx')
  df.to_excel(output_filename, index=False)


