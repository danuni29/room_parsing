import requests
import pandas as pd
import os


# 피터팬의 좋은방 구하기~
def peterpan_parsing(url, region):


    response_1 = requests.get(url)
    # print(response)
    houses = response_1.json()["houses"]["withoutFee"]["image"]

    # print(len(houses))
    id_list = []
    info_list = []
    type_list = []
    price_list = []
    location_list = []
    for i in range (len(houses)):
        id_list.append(houses[i])
        # print(id_list)

    for i in range(len(houses)):
        info_list.append(houses[i]['info'])

    for i in range(len(houses)):
        type_list.append(houses[i]['type'])

    for i in range(len(houses)):
        price_list.append(houses[i]['price'])

    for i in range(len(houses)):
        location_list.append(houses[i]['location']["coordinate"])


    colums0 = ['hidx']
    colums = ['subject', 'thumbnail', 'livingroom_text']
    colums1 = ['contract_type', 'building_type']
    colums2 = ['monthly_fee', 'deposit', 'maintenance_cost']
    colums3 = ['latitude', 'longitude']
    df0 = pd.DataFrame(id_list)[colums0]
    df = pd.DataFrame(info_list)[colums]
    df1 = pd.DataFrame(type_list)[colums1]
    df2 = pd.DataFrame(price_list)[colums2]
    df3 = pd.DataFrame(location_list)[colums3]

    total_df = pd.concat([df0, df, df1, df2, df3], axis=1)
    # print(total_df)

    output_dir = "../output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, f'peterpan_parsing_data_{region}.xlsx')
    total_df.to_excel(output_filename, index=False)


