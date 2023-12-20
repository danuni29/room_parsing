import streamlit as st
import pandas as pd
import folium
from folium import plugins
from folium import Marker
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium, folium_static
from PIL import Image
import os

from parsing_dabang import dabang_parsing
from parsing_peterpan import peterpan_parsing
from parsing_zigbang import parsing_zigbang


def add_dimensions(url, w=300, h=200):
    return f"{url}?w={w}&h={h}"

def calculate_distance_gujung(lat, lon, df):
    df['gujung_lat'] = abs(df['lat'] - lat)
    df['gujung_lng'] = abs(df['lon'] - lon)

def calculate_distance_shin(lat, lon, df):
    df['shin_lat'] = abs(df['lat'] - lat)
    df['shin_lng'] = abs(df['lon'] - lon)

def calculate_distance_sadae(lat, lon, df):
    df['sadae_lat'] = abs(df['lat'] - lat)
    df['sadae_lng'] = abs(df['lon'] - lon)


def main():
    # 사이드바를 만들어보자

    st.sidebar.title('내방찾기🏡')

    gujung = 0
    sadae = 0
    shin = 0

    region = st.sidebar.radio(label='원하는 지역이 있나요?', options=['네', '아니요'])
    print(region)
    if region == '네':
        location = ["구정문", "사대부고", "신정문"]
        selected_location = st.sidebar.selectbox("원하는 지역을 알려주세요", location)
        print(selected_location)

    else:
        st.sidebar.write("당신에게 맞는 지역을 찾아드려요")
        quietness = st.sidebar.radio(label='조용한 곳을 선호하시나요?', options=['네', '상관없어요'])
        infra = st.sidebar.radio(label='주변에 놀거리가 많았으면 좋겠나요?', options=['네', '상관없어요'])
        importance = st.sidebar.radio(label='무엇을 가장 중요하게 생각하시나요?', options=['저렴한 월세', '넓은방', '과방과의 거리'])

        if quietness == '네':
            shin += 10
            sadae += 5
        else:
            pass

        if infra == '네':
            gujung += 10
            sadae += 5
        else:
            pass

        if importance == '저렴한 월세':
            sadae += 10
        elif importance == '넓은방':
            shin += 10
        else:
            gujung += 10

        region_list = [shin, gujung, sadae]
        btn_clicked = st.sidebar.button("제출")
        if btn_clicked:
            if max(region_list) == shin:
                st.sidebar.write("신정문 지역을 추천드려요!")
                st.sidebar.write("신정문으로부터 가까운 집을 찾아드릴게요")
                room = shin
            if max(region_list) == gujung:
                st.sidebar.write("구정문 지역을 추천드려요!")
                st.sidebar.write("구정문으로부터 가까운 집을 찾아드릴게요")
                room = gujung
            if max(region_list) == sadae:
                st.sidebar.write("사대부고 지역을 추천드려요!")
                st.sidebar.write("사대부고로부터 가까운 집을 찾아드릴게요")
                room = sadae

# ------
    gujung_location = [35.8440610, 127.127228]
    sadae_location = [35.8424118, 127.135472]
    shin_location = [35.8402431, 127.132479]

    # 직방 API로 부터 파싱
    parsing_zigbang('덕진동1가')
    parsing_zigbang('금암동')

    file1 = pd.read_excel('../output/zigbang_parsing_data_금암동.xlsx')
    file2 = pd.read_excel('../output/zigbang_parsing_data_덕진동1가.xlsx')

    zigbang_total_df = pd.concat([file1, file2])
    zigbang_total_df = zigbang_total_df.rename(columns={'lng': 'lon'}) # streamlit에서 lng안됨...lon으로 해야함.....하아
    calculate_distance_gujung(gujung_location[0], gujung_location[1], zigbang_total_df)
    calculate_distance_sadae(sadae_location[0], sadae_location[1], zigbang_total_df)
    calculate_distance_shin(shin_location[0], shin_location[1], zigbang_total_df)

    output_dir = "../output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, 'zigbang_total_data.xlsx')
    zigbang_total_df.to_excel(output_filename, index=False)

    # 다방 API로 부터 파싱
    dabang_url_dukjin = "https://www.dabangapp.com/api/3/room/new-list/multi-room/region?api_version=3.0.1&call_type=web&code=45113105&filters=%7B%22multi_room_type%22%3A%5B0%5D%2C%22selling_type%22%3A%5B0%5D%2C%22deposit_range%22%3A%5B0%2C999999%5D%2C%22price_range%22%3A%5B0%2C999999%5D%2C%22trade_range%22%3A%5B0%2C999999%5D%2C%22maintenance_cost_range%22%3A%5B0%2C999999%5D%2C%22room_size%22%3A%5B0%2C999999%5D%2C%22supply_space_range%22%3A%5B0%2C999999%5D%2C%22room_floor_multi%22%3A%5B1%2C2%2C3%2C4%2C5%2C6%2C7%2C-1%2C0%5D%2C%22division%22%3Afalse%2C%22duplex%22%3Afalse%2C%22room_type%22%3A%5B%5D%2C%22use_approval_date_range%22%3A%5B0%2C999999%5D%2C%22parking_average_range%22%3A%5B0%2C999999%5D%2C%22household_num_range%22%3A%5B0%2C999999%5D%2C%22parking%22%3Afalse%2C%22short_lease%22%3Afalse%2C%22full_option%22%3Afalse%2C%22elevator%22%3Afalse%2C%22balcony%22%3Afalse%2C%22safety%22%3Afalse%2C%22pano%22%3Afalse%2C%22is_contract%22%3Afalse%2C%22deal_type%22%3A%5B0%2C1%5D%2C%22animal%22%3Afalse%2C%22loan%22%3Afalse%7D&page=1&version=1&zoom=14"
    dabang_url_geumam = "https://www.dabangapp.com/api/3/room/new-list/multi-room/bbox?api_version=3.0.1&call_type=web&filters=%7B%22multi_room_type%22%3A%5B0%2C2%5D%2C%22selling_type%22%3A%5B0%2C1%2C2%5D%2C%22deposit_range%22%3A%5B0%2C999999%5D%2C%22price_range%22%3A%5B0%2C999999%5D%2C%22trade_range%22%3A%5B0%2C999999%5D%2C%22maintenance_cost_range%22%3A%5B0%2C999999%5D%2C%22room_size%22%3A%5B0%2C999999%5D%2C%22supply_space_range%22%3A%5B0%2C999999%5D%2C%22room_floor_multi%22%3A%5B1%2C2%2C3%2C4%2C5%2C6%2C7%2C-1%2C0%5D%2C%22division%22%3Afalse%2C%22duplex%22%3Afalse%2C%22room_type%22%3A%5B%5D%2C%22use_approval_date_range%22%3A%5B0%2C999999%5D%2C%22parking_average_range%22%3A%5B0%2C999999%5D%2C%22household_num_range%22%3A%5B0%2C999999%5D%2C%22parking%22%3Afalse%2C%22short_lease%22%3Afalse%2C%22full_option%22%3Afalse%2C%22elevator%22%3Afalse%2C%22balcony%22%3Afalse%2C%22safety%22%3Afalse%2C%22pano%22%3Afalse%2C%22is_contract%22%3Afalse%2C%22deal_type%22%3A%5B0%2C1%5D%7D&location=%5B%5B127.1296452%2C35.8380491%5D%2C%5B127.1382282%2C35.8450851%5D%5D&page=1&version=1&zoom=17"

    dabang_parsing(dabang_url_dukjin, 'geumam')
    dabang_parsing(dabang_url_geumam, 'dukjin')

    file1 = pd.read_excel('../output/dabang_parsing_data_geumam.xlsx')
    file2 = pd.read_excel('../output/dabang_parsing_data_dukjin.xlsx')

    dabang_total_df = pd.concat([file1, file2])
    print(dabang_total_df)
    calculate_distance_gujung(gujung_location[0], gujung_location[1], dabang_total_df)
    calculate_distance_sadae(sadae_location[0], sadae_location[1], dabang_total_df)
    calculate_distance_shin(shin_location[0], shin_location[1], dabang_total_df)


    output_dir = "../output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, 'dabang_total_data.xlsx')
    dabang_total_df.to_excel(output_filename, index=False)

    # 피터팬 API로 부터 파싱
    peter_url_geumam = 'https://api.peterpanz.com/houses/area?zoomLevel=15&center=%7B%22y%22:35.837424,%22_lat%22:35.837424,%22x%22:127.133088,%22_lng%22:127.133088%7D&dong=%EA%B8%88%EC%95%941%EB%8F%99&gungu=%EC%A0%84%EC%A3%BC%EC%8B%9C%20%EB%8D%95%EC%A7%84%EA%B5%AC&filter=latitude:35.8231411~35.8517043%7C%7Clongitude:127.1204923~127.1456837%7C%7CcontractType;%5B%22%EC%9B%94%EC%84%B8%22%5D%7C%7CroomType;%5B%22%EC%98%A4%ED%94%88%ED%98%95%20%EC%9B%90%EB%A3%B8%22,%22%EB%B6%84%EB%A6%AC%ED%98%95%20%EC%9B%90%EB%A3%B8%22%5D&&pageSize=90&pageIndex=1&order_id=1703077104&search=&response_version=5.2&filter_version=5.1&order_by=random'
    peter_url_dukjin = 'https://api.peterpanz.com/houses/area?zoomLevel=17&center=%7B%22y%22:35.8442803,%22_lat%22:35.8442803,%22x%22:127.1255069,%22_lng%22:127.1255069%7D&dong=%EB%8D%95%EC%A7%84%EB%8F%991%EA%B0%80&gungu=%EC%A0%84%EC%A3%BC%EC%8B%9C%20%EB%8D%95%EC%A7%84%EA%B5%AC&filter=latitude:35.8407101~35.8478503%7C%7Clongitude:127.122358~127.1286558%7C%7CcontractType;%5B%22%EC%9B%94%EC%84%B8%22%5D%7C%7CroomType;%5B%22%EC%98%A4%ED%94%88%ED%98%95%20%EC%9B%90%EB%A3%B8%22,%22%EB%B6%84%EB%A6%AC%ED%98%95%20%EC%9B%90%EB%A3%B8%22%5D&&pageSize=90&pageIndex=1&order_id=1702364791&search=&response_version=5.2&filter_version=5.1&order_by=random'

    peterpan_parsing(peter_url_geumam, 'geumam')
    peterpan_parsing(peter_url_dukjin, 'dukjin')

    file1 = pd.read_excel('../output/peterpan_parsing_data_geumam.xlsx')
    file2 = pd.read_excel('../output/peterpan_parsing_data_dukjin.xlsx')

    peterpan_total_df = pd.concat([file1, file2])
    peterpan_total_df.columns = ['subject', 'thumbnail','livingroom_text','contract_type','monthly_fee','building_type','deposit','maintenance_cost','latitude','longitude']
    peterpan_total_df = peterpan_total_df.rename(columns={'latitude': 'lat', 'longitude':'lon'})

    calculate_distance_gujung(gujung_location[0], gujung_location[1], peterpan_total_df)
    calculate_distance_sadae(sadae_location[0], sadae_location[1], peterpan_total_df)
    calculate_distance_shin(shin_location[0], shin_location[1], peterpan_total_df)


    output_dir = "../output/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_filename = os.path.join(output_dir, 'peterpan_total_data.xlsx')
    peterpan_total_df.to_excel(output_filename, index=False)


    st.title("방찾기")
    # st.header("직방, 다방, 피터팬의 좋은방 구하기 사이트로 ")
    img = Image.open('output/logo.png')
    st.image(img)

    deposit_cost = st.slider('보증금 범위를 설정하세요', min_value=0, value=200, max_value=1000)
    print(deposit_cost)
    monthly_cost = st.slider('월세 범위를 설정하세요', min_value=0, value=50, max_value=100)
    print(monthly_cost)
    site = st.radio(label='어느 사이트의 정보를 불러올까요?', options=['직방', '다방', '피터팬의 좋은방 구하기'])

    if site == '직방':
        df = zigbang_total_df
        # df.columns = ['lat', 'lon']
        m = folium.Map(location=[35.8440159, 127.127327], zoom_start=15, tiles="cartodbpositron")
        for i, row in df.iterrows():
            folium.Marker(location=[row['lat'], row['lon']]).add_to(m)
        folium_static(m, width=600, height=500)


    elif site == '다방':
        df = dabang_total_df
        print(df)
        # df.colums = ['lat', 'lon']
        m = folium.Map(location=[35.8440159, 127.127327], zoom_start=15, tiles="cartodbpositron")
        for i, row in df.iterrows():
            folium.Marker(location=[row['lat'], row['lon']]).add_to(m)
        folium_static(m, width=600, height=500)

    else:
        df = peterpan_total_df
        print(df)
        # df.colums = ['lat', 'lon']
        m = folium.Map(location=[35.8440159, 127.127327], zoom_start=15, tiles="cartodbpositron")
        for i, row in df.iterrows():
            folium.Marker(location=[row['lat'], row['lon']]).add_to(m)
        folium_static(m, width=600, height=500)




if __name__ == '__main__':
    main()