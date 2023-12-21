FROM python:3
WORKDIR /usr/src/app


## Copy all src files
COPY .. /usr/src/app

## Install packages
RUN pip install -r requirements.txt

CMD streamlit run room_streamlit.py