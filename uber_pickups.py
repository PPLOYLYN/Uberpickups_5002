import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.title('Uber pickups in NYC')

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

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

st.bar_chart(hist_values)

st.subheader('Map of all pickups')
st.map(data)


hour_to_filter = 17
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

hour_to_filter2 = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter2]
st.subheader(f'Map of all pickups at {hour_to_filter2}:00')
st.map(filtered_data)


#MAP 3D
import pydeck as pdk

st.subheader("Uber pickups in NYC")


data_clean = data.dropna(subset=['lat', 'lon'])

st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=data_clean['lat'].mean(),
            longitude=data_clean['lon'].mean(),
            zoom=11,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data_clean,
                get_position='[lon, lat]',
                radius=100,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            
        ],
    )
)

# Date input
st.subheader("Select a Date")
selected_date = st.date_input("Pick a date")
st.write(f"You selected: {selected_date}")

# Selectbox
st.subheader("Selectbox - pick hour")
selected_hour = st.selectbox(
    'Which hour do you want to see pickups?',
    list(range(24))
)
filtered_by_selectbox = data[data[DATE_COLUMN].dt.hour == selected_hour]
st.subheader(f'Map of pickups at {selected_hour}:00 selected from selectbox')
st.map(filtered_by_selectbox)

# Plotly
st.subheader(" Plotly Chart : Number of pickups by hour")
hist_data = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
fig = px.bar(x=list(range(24)), y=hist_data,
             labels={'x':'Hour of Day', 'y':'Number of Pickups'},
             title='Pickups by Hour')
st.plotly_chart(fig)

# Click button to increase the number
st.subheader(" Click to Count Page Runs")
if 'count' not in st.session_state:
    st.session_state.count = 0

if st.button('Click me!'):
    st.session_state.count += 1

st.write(f"This page has run {st.session_state.count} times.")