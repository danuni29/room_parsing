import requests
import pandas as pd
def main():

    # 피터팬의 좋은방 구하기~
    # 일단 덕진동1가
    url = 'https://api.peterpanz.com/houses/area?zoomLevel=17&center=%7B%22y%22:35.8442803,%22_lat%22:35.8442803,%22x%22:127.1255069,%22_lng%22:127.1255069%7D&dong=%EB%8D%95%EC%A7%84%EB%8F%991%EA%B0%80&gungu=%EC%A0%84%EC%A3%BC%EC%8B%9C%20%EB%8D%95%EC%A7%84%EA%B5%AC&filter=latitude:35.8407101~35.8478503%7C%7Clongitude:127.122358~127.1286558%7C%7CcontractType;%5B%22%EC%9B%94%EC%84%B8%22%5D%7C%7CroomType;%5B%22%EC%98%A4%ED%94%88%ED%98%95%20%EC%9B%90%EB%A3%B8%22,%22%EB%B6%84%EB%A6%AC%ED%98%95%20%EC%9B%90%EB%A3%B8%22%5D&&pageSize=90&pageIndex=1&order_id=1702364791&search=&response_version=5.2&filter_version=5.1&order_by=random'
    response = requests.get(url)
    # print(response)
    data = response.json()["houses"]["withoutFee"]["image"][0]
    print(data)

    colums = ['subject', 'thumbnail', 'livingroom_text', "contract_type", "monthly_Fee", "deposit", "maintenace_cost", "location" ]
    # df = pd.DataFrame(items)[colums]
if __name__ == '__main__':
    main()