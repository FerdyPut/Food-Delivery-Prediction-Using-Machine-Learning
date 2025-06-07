import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# Mendapatkan waktu Jakarta
jakarta_tz = pytz.timezone('Asia/Jakarta')
now = datetime.now(jakarta_tz)

# Menentukan waktu dalam kategori
if 5 <= now.hour < 11:
    greeting = "Selamat Pagi"
elif 11 <= now.hour < 15:
    greeting = "Selamat Siang"
elif 15 <= now.hour < 18:
    greeting = "Selamat Sore"
else:
    greeting = "Selamat Malam"

def tampilkan_halaman_umum():
    st.info("Selamat datang di Prediction Tools!")
    st.markdown(f"""
    - **{greeting}**, Diharapkan digunakan dengan baik!
                **Food Time Delivery Prediction**.    
    - **Menu Tab terdapat Exploratory Data Analysis (EDA) dan Prediction Test**.
    - Pada Menu EDA sebagai visualisasi atau analisis statistik terkait kasus Food Time Delivery.
    - Pada Menu Prediction Test terdapat Prediction Test yang digunakan untuk menguji hasil prediksi waktu pengantaran (Food Time Delivery) dari variabel-variabel yang tersedia
    - Tools ini dibuat oleh: Ferdyansyah Permana Putra - DS30.
    """)

