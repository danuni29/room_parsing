import requests
import pandas as pd
import os


# 피터팬의 좋은방 구하기~
def peterpan_parsing(url, region):


    response_1 = requests.get(url)
    # print(response)
    houses = response_1.json()["houses"]["withoutFee"]["image"]

    # print(len(houses))

    info_list = []
    type_list = []
    price_list = []
    location_list = []

    for i in range(len(houses)):
        info_list.append(houses[i]['info'])

    for i in range(len(houses)):
        type_list.append(houses[i]['type'])

    for i in range(len(houses)):
        price_list.append(houses[i]['price'])

    for i in range(len(houses)):
        location_list.append(houses[i]['location']["coordinate"])



    colums = ['subject', 'thumbnail', 'livingroom_text']
    colums1 = ['contract_type', 'building_type']
    colums2 = ['monthly_fee', 'deposit', 'maintenance_cost']
    colums3 = ['latitude', 'longitude']
    df = pd.DataFrame(info_list)[colums]
    df1 = pd.DataFrame(type_list)[colums1]
    df2 = pd.DataFrame(price_list)[colums2]
    df3 = pd.DataFrame(location_list)[colums3]

    total_df = pd.concat([df, df1, df2, df3], axis=1)
    # print(total_df)

    output_dir = "../output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, f'peterpan_parsing_data_{region}.xlsx')
    total_df.to_excel(output_filename, index=False)


url_geumam = 'https://api.peterpanz.com/houses/area?zoomLevel=15&center=%7B%22y%22:35.837424,%22_lat%22:35.837424,%22x%22:127.133088,%22_lng%22:127.133088%7D&dong=%EA%B8%88%EC%95%941%EB%8F%99&gungu=%EC%A0%84%EC%A3%BC%EC%8B%9C%20%EB%8D%95%EC%A7%84%EA%B5%AC&filter=latitude:35.8231411~35.8517043%7C%7Clongitude:127.1204923~127.1456837%7C%7CcontractType;%5B%22%EC%9B%94%EC%84%B8%22%5D%7C%7CroomType;%5B%22%EC%98%A4%ED%94%88%ED%98%95%20%EC%9B%90%EB%A3%B8%22,%22%EB%B6%84%EB%A6%AC%ED%98%95%20%EC%9B%90%EB%A3%B8%22%5D&&pageSize=90&pageIndex=1&order_id=1703077104&search=&response_version=5.2&filter_version=5.1&order_by=random'
url_dukjin = 'https://api.peterpanz.com/houses/area?zoomLevel=17&center=%7B%22y%22:35.8442803,%22_lat%22:35.8442803,%22x%22:127.1255069,%22_lng%22:127.1255069%7D&dong=%EB%8D%95%EC%A7%84%EB%8F%991%EA%B0%80&gungu=%EC%A0%84%EC%A3%BC%EC%8B%9C%20%EB%8D%95%EC%A7%84%EA%B5%AC&filter=latitude:35.8407101~35.8478503%7C%7Clongitude:127.122358~127.1286558%7C%7CcontractType;%5B%22%EC%9B%94%EC%84%B8%22%5D%7C%7CroomType;%5B%22%EC%98%A4%ED%94%88%ED%98%95%20%EC%9B%90%EB%A3%B8%22,%22%EB%B6%84%EB%A6%AC%ED%98%95%20%EC%9B%90%EB%A3%B8%22%5D&&pageSize=90&pageIndex=1&order_id=1702364791&search=&response_version=5.2&filter_version=5.1&order_by=random'

peterpan_parsing(url_geumam, 'geumam')
peterpan_parsing(url_dukjin, 'dukjin')

file1 = pd.read_excel('../output/peterpan_parsing_data_geumam.xlsx')
file2 = pd.read_excel('../output/peterpan_parsing_data_dukjin.xlsx')

peterpan_df = pd.concat([file1, file2])

output_dir = "../output/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_filename = os.path.join(output_dir, f'peterpan_total_data.xlsx')
peterpan_df.to_excel(output_filename, index=False)



