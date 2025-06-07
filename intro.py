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
    st.warning(f"{greeting} Diharapkan digunakan dengan baik! Food Time Delivery Prediction.")
    st.markdown(f"""
    <style>
        .hover-box {{
            background-color: #FFEB3B; /* Kuning */
            padding: 5px;
            margin-bottom: 10px;
            border-radius: 2px;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }}
        .hover-box:hover {{
            transform: scale(1.05); /* Zoom saat hover */
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); /* Efek bayangan */
        }}
        .content {{
            margin-left: 20px;
        }}
    </style>

    <div class="hover-box">
        <ul class="content">
            <li><b>Menu Tab</b> terdapat Exploratory Data Analysis (EDA) dan Prediction Test.</li>
        </ul>
    </div>
    <div class="hover-box">
        <ul class="content">
            <li>Pada Menu <b>EDA</b> sebagai visualisasi atau analisis statistik terkait kasus Food Time Delivery.</li>
        </ul>
    </div>
    <div class="hover-box">
        <ul class="content">
            <li>Pada Menu <b>Prediction Test</b> terdapat Prediction Test yang digunakan untuk menguji hasil prediksi waktu pengantaran (Food Time Delivery) dari variabel-variabel yang tersedia.</li>
        </ul>
    </div>
    <div class="hover-box">
        <ul class="content">
            <li><b>Tools ini dibuat oleh:</b> Ferdyansyah Permana Putra - DS30.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
