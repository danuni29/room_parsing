import os
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from pprint import pprint
from selenium.webdriver.common.by import By
import pandas as pd
import openpyxl

url = 'https://new.land.naver.com/rooms?ms=35.8409376,127.1240086,16&a=APT:OPST:ABYG:OBYG:GM:OR:VL:DDDGG:JWJT:SGJT:HOJT&e=RETAIL&aa=SMALLSPCRENT&ae=ONEROOM'
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(1)
driver.minimize_window()
driver.get(url)


onerooms = driver.find_elements_by_class_name('item_inner')

for oneroom in onerooms:
    pprint(oneroom.text)

time.sleep(3)
data_list = []

for i in range(1,31):
    try:
        each_room_button = driver.find_element(By.XPATH, f'//*[@id="listContents1"]/div/div/div[1]/div[{i}]/div/a[2]')
        each_room = each_room_button.click()
        table = driver.find_element_by_class_name('info_table_wrap')
        tbody = table.find_element_by_tag_name("tbody")
        rows = tbody.find_elements_by_tag_name("tr")
        for index, value in enumerate(rows):
            cells = value.find_elements_by_tag_name("td")
            cell_data = [cell.text for cell in cells]
            data_list.append(cell_data)
        #     for cell in cells:
        #         print(cell.text)
        #
        # print("-------------------------------------------")

    except:
        pass

# print("-----------------------")
df = pd.DataFrame(data_list)
# print(df)
#
output_dir = "../output/"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_filename = os.path.join(output_dir, 'naver_parsing_data.xlsx')
# df.to_excel('naver.xlsx', index=False)



