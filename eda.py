import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def eda():
    st.info("Ini adalah Bagian EDA!")
    # URL Dropbox yang telah diubah menjadi link langsung
    url = 'https://www.dropbox.com/scl/fi/n5zlvmvafydjweliu55f8/Data-FTD-Clean.csv?rlkey=fax9s8fnda5gxdnfh9y4guzu2&st=eq0a6s5v&dl=1'

    try:
        # Membaca file CSV dari Dropbox
        df = pd.read_csv(url)

        # Pastikan data berhasil dimuat
        st.write("Dataset successfully loaded!")
        st.write(df.head())  # Menampilkan 5 baris pertama untuk verifikasi
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return

    # Statistik Deskriptif
    st.write("Descriptive Statistics:")
    st.write(df.describe())

    # Menampilkan Korelasi antar variabel menggunakan Heatmap
    st.write("Correlation Heatmap:")
    corr = df.corr()
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
    st.pyplot(fig)

    # Distribusi Data untuk setiap variabel numerik
    st.write("Distribution of Numerical Variables:")
    fig, ax = plt.subplots(figsize=(10, 6))
    for column in df.select_dtypes(include=['float64', 'int64']).columns:
        sns.histplot(df[column], kde=True, ax=ax, label=column)
    st.pyplot(fig)

    # Boxplot untuk melihat distribusi Delivery Time berdasarkan Traffic Level
    st.write("Boxplot: Traffic Level vs Delivery Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='Traffic_Level', y='Delivery_Time_min', ax=ax)
    st.pyplot(fig)

    # Scatter plot antara Distance dan Delivery Time
    st.write("Scatter Plot: Distance vs Delivery Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='Distance_km', y='Delivery_Time_min', ax=ax)
    st.pyplot(fig)

    # Visualisasi hubungan antara Preparation Time dan Delivery Time
    st.write("Scatter Plot: Preparation Time vs Delivery Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=df, x='Preparation_Time_min', y='Delivery_Time_min', ax=ax)
    st.pyplot(fig)

    # Visualisasi boxplot antara Time of Day dan Delivery Time
    st.write("Boxplot: Time of Day vs Delivery Time")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(data=df, x='Time_of_Day', y='Delivery_Time_min', ax=ax)
    st.pyplot(fig)
