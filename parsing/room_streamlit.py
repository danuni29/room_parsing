import streamlit as st
import pandas as pd
import folium
from folium import plugins
from folium import Marker
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium, folium_static

def add_dimensions(url, w=300, h=200):
    return f"{url}?w={w}&h={h}"

def main():
    st.title("방찾기")
    location = ["구정문", "사대부고", "신정문"]
    selected_location = st.selectbox("지역을 선택하세요", location)
    # st.write(f"{selected_location}선택")
    deposit_cost = st.slider('보증금 범위 선택해라', min_value=0, value= 200, max_value=1000)
    monthly_cost = st.slider('월세 범위 선택해라', min_value=0, value= 50, max_value=100)

    df = pd.read_excel('output/zigbang_parsing_data_2.xlsx')
    # st.map(df, zoom=15)

    m = folium.Map(location=[35.8440159, 127.127327], zoom_start=15, tiles="cartodbpositron")

    df['image_url'] = df['사진'].apply(add_dimensions)
    print(df)
    for i, row in df.iterrows():
        # iframe = f"이름: <strong>{row['name']}</strong><br>국가격자번호: <strong>{row['gloc']}</strong><br> 위경도: {row['lat']:.4f}, {row['lon']:.4f}<br> 주소: {row['addr_name']}"
        iframe = f"{row['image_url']}"
        # popup = folium.Popup(row['image_url'], min_width=200, max_width=200)
        # popup = f'<img src="{row['사진']}" width="300" height="200">'
        tooltip = '<i>title</i>'
        folium.Marker(location=[row['lat'], row['lon']], tooltip=tooltip).add_to(m)
        st.title('tilte')
        st.image(row['image_url'])

    # cluster = MarkerCluster()
    # for _, i in df.iterrows():
    #     cluster.add_child(
    #         Marker(location=[i['lat'], i['lon']])
    #     ).add_to(map)
    folium_static(m, width=700, height=650)

    # m.add_child(cluster)


if __name__ == '__main__':
    main()