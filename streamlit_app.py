import streamlit as st
import pandas as pd
import numpy as np


st.title('Uber pickups in NYC 📍🗺🚗')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

 # <----
data_load_state = st.text('Loading data...🟢')
data = load_data(10000)
data_load_state.text(f"Loaded records #{len(data.index)}")
# ---->

# ------
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data.head())
# ------
st.subheader('Number of pickups by hour')
# Use NumPy to generate a histogram that breaks down pickup times binned by hour
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)


# ----
st.subheader('Map of all pickups')

st.map(data)

# ------

hour_to_filter = st.sidebar.slider('hour', 0, 23, 17)
