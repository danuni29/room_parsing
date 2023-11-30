import streamlit as st

def main():
    st.title("방찾기")
    location = ["구정문", "사대부고", "신정문"]
    selected_location = st.selectbox("지역을 선택하세요", location)
    # st.write(f"{selected_location}선택")
    deposit_cost = st.slider('보증금 범위 선택해라', min_value=0, value= 200, max_value=1000)
    monthly_cost = st.slider('월세 범위 선택해라', min_value=0, value= 50, max_value=100)



if __name__ == '__main__':
    main()