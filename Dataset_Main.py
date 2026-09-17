import streamlit as st
import pandas as pd
import numpy as np

st.title('Persebaran & Analisis Gempa Bumi')

DATE_COLUMN = 'date/time'
DATA_FILE = 'earthquake_clean.csv'

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_FILE, nrows=nrows)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data gempa...')
data = load_data(10000)
data_load_state.text("Data gempa berhasil dimuat! (menggunakan st.cache_data)")

st.subheader("Pengaturan Kekuatan Gempa")
kategori_gempa = st.selectbox(
    "Pilih Kategori Kekuatan:",
    ["Semua Kategori", "Ringan (Mag < 5.0)", "Sedang (Mag 5.0 - 6.0)", "Besar (Mag > 6.0)"]
)

if kategori_gempa == "Ringan (Mag < 5.0)":
    data_filtered = data[data['magnitude'] < 5.0]
elif kategori_gempa == "Sedang (Mag 5.0 - 6.0)":
    data_filtered = data[(data['magnitude'] >= 5.0) & (data['magnitude'] <= 6.0)]
elif kategori_gempa == "Besar (Mag > 6.0)":
    data_filtered = data[data['magnitude'] > 6.0]
else:
    data_filtered = data

st.subheader("Ringkasan Data")
col1, col2, col3 = st.columns(3)
col1.metric("Total Kejadian", f"{len(data_filtered)} Gempa")
col2.metric("Rata-rata Magnitudo", f"{data_filtered['magnitude'].mean():.2f}")
col3.metric("Maksimum Magnitudo", f"{data_filtered['magnitude'].max():.1f}")

if st.checkbox('Tampilkan data mentah'):
    st.subheader('Tabel Data Gempa')
    st.write(data_filtered)

st.subheader('Distribusi Jam Terjadinya Gempa (UTC)')
hist_values = np.histogram(data_filtered[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

hour_to_filter = st.slider('Pilih Jam Gempa (0-23)', 0, 23, 12)
final_data = data_filtered[data_filtered[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader(f'Titik Pusat Gempa pada Jam {hour_to_filter}:00')
st.map(final_data[['lat', 'lon']])