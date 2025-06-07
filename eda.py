import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def eda():
    # Menampilkan informasi di bagian atas
    st.info("Ini adalah Bagian EDA! Dimana EDA ini akan menampilkan terkait tabel data Food Time Delivery seperti apa, kemudian heatmap correlation, scatterplot, dan distribusik data dari variabel numerik")
    
    # URL Dropbox yang telah diubah menjadi link langsung
    url = 'https://www.dropbox.com/scl/fi/n5zlvmvafydjweliu55f8/Data-FTD-Clean.csv?rlkey=fax9s8fnda5gxdnfh9y4guzu2&st=eq0a6s5v&dl=1'

    try:
        # Membaca file CSV dari Dropbox
        df = pd.read_csv(url)

        # Menghapus kolom yang memiliki nama 'Unnamed' atau kolom tanpa nama yang tidak diperlukan
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

        # Pastikan data berhasil dimuat
        st.warning("Dataset berhasil dibaca!")
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return
        
    # Menampilkan DataFrame di dalam st.expander()
    with st.expander("Dataset Preview (Klik untuk melihat)"):
        st.write(df.head())  # Menampilkan 5 baris pertama untuk verifikasi

    # Statistik Deskriptif
    with st.expander("Descriptive Statistics"):
        st.write(df.describe())

    # Pilih kolom numerik untuk analisis
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

    # Menampilkan Korelasi antar variabel menggunakan Heatmap hanya untuk variabel numerik
    with st.expander("Correlation Heatmap (Numerical Variables Only)"):
        corr = df[numeric_columns].corr()  # Menghitung korelasi hanya untuk kolom numerik
        fig, ax = plt.subplots(figsize=(4, 3))  # Menyesuaikan ukuran lebih kecil
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

    # EDA Visualizations (Boxplot, Histogram, Scatter Plot)
    with st.expander("Boxplot: Pilih variabel untuk melihat Boxplot"):
        selected_boxplot = st.selectbox("Pilih variabel untuk Boxplot", numeric_columns)
        fig, ax = plt.subplots(figsize=(4, 3))  # Ukuran kecil
        sns.boxplot(data=df, x=selected_boxplot, ax=ax)
        ax.set_title(f'Boxplot: {selected_boxplot}')
        st.pyplot(fig)

    with st.expander("Histogram: Pilih variabel untuk melihat Histogram"):
        selected_hist = st.selectbox("Pilih variabel untuk Histogram", numeric_columns)
        fig, ax = plt.subplots(figsize=(4, 3))  # Ukuran kecil
        sns.histplot(df[selected_hist], kde=True, ax=ax)
        ax.set_title(f'Histogram: {selected_hist}')
        st.pyplot(fig)

    with st.expander("Scatter Plot: Pilih variabel untuk melihat Scatter Plot (Y = Delivery Time)"):
        selected_x = st.selectbox("Pilih variabel untuk sumbu X", numeric_columns)
        selected_y = 'Delivery_Time_min'  # Y tetap pada 'Delivery_Time_min'
        fig, ax = plt.subplots(figsize=(4, 3))  # Ukuran kecil
        sns.scatterplot(data=df, x=selected_x, y=selected_y, ax=ax)
        ax.set_title(f'Scatter Plot: {selected_x} vs {selected_y}')
        st.pyplot(fig)
