import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def eda():
    # Menampilkan informasi di bagian atas
    st.info("Ini adalah Bagian EDA! Dimana EDA ini akan menampilkan terkait tabel data Food Time Delivery seperti apa, kemudian heatmap correlation, scatterplot, dan distribusi data dari variabel numerik")
    
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

        st.markdown("""
        <style>
        .insight-box {
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 6px solid #007acc;
            margin-bottom: 15px;
        }
        .insight-box ul {
            list-style-type: none;
            padding-left: 20px;
        }
        .insight-box h4 {
            color: #007acc;
            font-size: 16px;
            font-weight: bold;
        }
        .insight-box li {
            font-size: 14px;
            font-weight: normal;
            color: #555;
        }
        </style>

        <div class="insight-box">
            <strong> Insight: </strong>
            <h4>Data Food Time Delivery tersebut merupakan data yang didapatkan dari Kaggle dengan rincian variabel-variabelnya:</h4>
            <ul>
                <li><strong>Weather</strong>: Kondisi cuaca pada saat pengiriman (misalnya: Clear, Rainy, etc.)</li>
                <li><strong>Traffic_Level</strong>: Tingkat kemacetan lalu lintas (misalnya: Low, Moderate, High)</li>
                <li><strong>Time_of_Day</strong>: Waktu pengiriman dilakukan (misalnya: Morning, Afternoon, Evening)</li>
                <li><strong>Vehicle_Type</strong>: Jenis kendaraan yang digunakan oleh kurir untuk pengiriman (misalnya: Motor, Car, etc.)</li>
                <li><strong>Distance_km</strong>: Jarak yang ditempuh oleh kurir dalam kilometer untuk pengiriman</li>
                <li><strong>Courier_Experience_yrs</strong>: Pengalaman kurir dalam tahun</li>
                <li><strong>Delivery_Time_min</strong>: Waktu yang dibutuhkan untuk pengiriman dalam menit</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)
    # Statistik Deskriptif
    with st.expander("Descriptive Statistics"):
        st.write(df.describe())

        st.markdown("""
        <style>
        .insight-box {
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 6px solid #007acc;
            margin-bottom: 15px;
        }
        .insight-box ul {
            list-style-type: none;
            padding-left: 20px;
        }
        .insight-box li {
            font-size: 14px;
            font-weight: normal;
            color: #555;
        }
        </style>
        
        <div class="insight-box">
            <strong>Insight:</strong>
            <ul>
                <li><strong>Waktu persiapan rata-rata</strong> (10 menit) dan <strong>waktu pengantaran rata-rata</strong> (56 menit) menunjukkan bahwa sistem umumnya berjalan cukup efisien, tetapi ada variasi yang signifikan.</li>
                <li><strong>Jarak pengantaran</strong> sangat bervariasi, dengan beberapa pengantaran sangat dekat (1 km) dan beberapa lainnya cukup jauh (hingga 19.9 km).</li>
                <li><strong>Pengalaman kurir rata-rata</strong> adalah 4.5 tahun, tetapi ada beberapa kurir baru, yang tercermin dari pengalaman minimum 0 tahun.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
    # Pilih kolom numerik untuk analisis
    numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns

    # Menampilkan Korelasi antar variabel menggunakan Heatmap hanya untuk variabel numerik
    with st.expander("Correlation Heatmap (Klik untuk melihat)"):
        corr = df[numeric_columns].corr()  # Menghitung korelasi hanya untuk kolom numerik
        fig, ax = plt.subplots(figsize=(4, 3))  # Menyesuaikan ukuran lebih kecil
        sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        st.markdown("""
        <style>
        .insight-box {
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 6px solid #007acc;
            margin-bottom: 15px;
        }
        .insight-box ul {
            list-style-type: none;
            padding-left: 20px;
        }
        .insight-box h4 {
            color: #007acc;
            font-size: 16px;
            font-weight: bold;
        }
        .insight-box li {
            font-size: 14px;
            font-weight: normal;
            color: #555;
        }
        </style>

        <div class="insight-box">
            <strong>Insight:</strong>
            <h4>Berdasarkan korelasi heatmap antara variabel Fitur dengan variabel Target, yaitu 'Preparation_Time_min', 'Courier_Experience_yrs', 'Distance_km' vs 'Delivery_Time_min':</h4>
            <ul>
                <li><strong>Nilai korelasi yang paling lemah</strong> adalah variabel 'Courier_Experience_yrs' terhadap 'Delivery_Time_min', yaitu mendekati 0 (-0.09). Make sense, jika scatterplotnya tidak membentuk korelasi positif/negatif.</li>
                <li><strong>Nilai korelasi yang lemah</strong> adalah variabel 'Preparation_Time_min' terhadap 'Delivery_Time_min', yaitu mendekati 0 (0.31). Make sense, jika scatterplotnya tidak membentuk korelasi positif/negatif.</li>
                <li><strong>Nilai korelasi yang cukup kuat</strong> adalah variabel 'Distance_km' terhadap 'Delivery_Time_min', yaitu mendekati 0 (0.79). Make sense, jika membentuk korelasi positif, karena memang ada indikasi hubungan yang cukup kuat.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # EDA Visualizations (Boxplot, Histogram, Scatter Plot)
    with st.expander("Scatter Plot (Klik untuk melihat)"):
        selected_x = st.selectbox("Pilih variabel untuk sumbu X", numeric_columns)
        selected_y = 'Delivery_Time_min'  # Y tetap pada 'Delivery_Time_min'
        fig, ax = plt.subplots(figsize=(4, 3))  # Ukuran kecil
        sns.scatterplot(data=df, x=selected_x, y=selected_y, ax=ax)
        ax.set_title(f'Scatter Plot: {selected_x} vs {selected_y}')
        st.pyplot(fig)
        st.markdown(f"""
        <style>
        .insight-box {{
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 6px solid #007acc;
            margin-bottom: 15px;
        }}
        .insight-box p {{
            font-size: 14px;
            font-weight: normal;
            color: #555;
        }}
        </style>

        <div class="insight-box">
            <strong>Insight:</strong>
            <p>Hanya variabel <strong>Distance_km</strong> yang cenderung memiliki hubungan cukup kuat dengan variabel Target ('Delivery_time_min') karena korelasinya positif linear ke atas. Sedangkan variabel lainnya, tidak adanya hubungan yang cukup kuat (alias lemah) karena korelasinya menyebar dan tidak membentuk garis linear ke atas/ke bawah.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Boxplot (Klik untuk melihat) "):
        selected_boxplot = st.selectbox("Pilih variabel untuk Boxplot", numeric_columns)
        fig, ax = plt.subplots(figsize=(4, 3))  # Ukuran kecil
        sns.boxplot(data=df, x=selected_boxplot, ax=ax)
        ax.set_title(f'Boxplot: {selected_boxplot}')
        st.pyplot(fig)

        st.markdown(f"""
        <style>
        .insight-box {{
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 6px solid #007acc;
            margin-bottom: 15px;
        }}
        .insight-box p {{
            font-size: 14px;
            font-weight: normal;
            color: #555;
        }}
        </style>

        <div class="insight-box">
            <strong>Insight:</strong>
            <p>Boxplot pada <strong>{selected_boxplot}</strong> tidak ada indikasi nilai ekstrem dan variasinya cukup ragam karena lebar boxplotnya cukup besar. Sehingga tidak ada indikasi outlier. Namun, sebenarnya ini data sudah bersih dalam artian sudah mengalami cleaning data.</p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Histogram (Klik untuk melihat)"):
        selected_hist = st.selectbox("Pilih variabel untuk Histogram", numeric_columns)
        fig, ax = plt.subplots(figsize=(4, 3))  # Ukuran kecil
        sns.histplot(df[selected_hist], kde=True, ax=ax)
        ax.set_title(f'Histogram: {selected_hist}')
        st.pyplot(fig)

        st.markdown(f"""
        <style>
        .insight-box {{
            padding: 15px;
            background-color: #f9f9f9;
            border-left: 6px solid #007acc;
            margin-bottom: 15px;
        }}
        .insight-box p {{
            font-size: 14px;
            font-weight: normal;
            color: #555;
        }}
        </style>

        <div class="insight-box">
            <strong>Insight:</strong>
            <p>Histogram pada <strong>{selected_hist}</strong> menunjukkan bahwa distribusinya cenderung membentuk simetris, tidak ada indikasi skewness. Sehingga, mendekati normal datanya. Selain itu, memang datanya ini sudah mengalami tahap cleaning data sehingga bersih datanya.</p>
        </div>
        """, unsafe_allow_html=True)


