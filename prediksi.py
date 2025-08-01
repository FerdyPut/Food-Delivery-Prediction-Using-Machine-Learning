import pickle
import requests
import pandas as pd
import streamlit as st
from io import BytesIO

# Fungsi untuk mengunduh dan memuat pickle dari Dropbox
def load_pickle_from_dropbox(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pickle.load(BytesIO(response.content))  # Memuat pickle dari response content
    else:
        st.error(f"Error: {response.status_code}")
        return None

def prediksi():
    st.title('Food Time Delivery Prediction')
    st.info("Prediction Tools ini digunakan untuk menguji dari variabel-variabel yang ada berkaitan dengan faktor pengantaran makanan nantinya didapatkan berapa perkiraan estimasi waktu pengantarannya. Hal ini, berguna untuk meminimalisisr resiko pengantaran.")

    # Input variabel dari pengguna
    st.warning("Masukkan data untuk memprediksi waktu pengantaran:")
    
    # Input untuk variabel-variabel prediksi
    distance_km = st.number_input("Jarak Pengantaran (km)", min_value=0.0, value=5.0, step=0.1)
    courier_experience_yrs = st.number_input("Pengalaman Kurir (tahun)", min_value=0, value=3, step=1)
    preparation_time_min = st.number_input("Waktu Persiapan (menit)", min_value=0, value=10, step=1)
    weather = st.selectbox("Kondisi Cuaca", ['Clear', 'Rainy', 'Foggy', 'Snowy', 'Windy'])  # Kategorik
    traffic_level = st.selectbox("Tingkat Lalu Lintas", ['Low', 'Medium', 'High'])  # Kategorik
    time_of_day = st.selectbox("Waktu Pengiriman", ['Morning', 'Afternoon', 'Evening', 'Night'])  # Kategorik
    vehicle_type = st.selectbox("Jenis Kendaraan", ['Bike', 'Car', 'Scooter'])  # Kategorik

    # Membuat DataFrame untuk input pengguna
    input_data = pd.DataFrame([[weather, traffic_level, vehicle_type, time_of_day, preparation_time_min, courier_experience_yrs, distance_km]],
                              columns=['Weather', 'Traffic_Level', 'Vehicle_Type', 'Time_of_Day', 'Preparation_Time_min', 'Courier_Experience_yrs', 'Distance_km'])

    # Memuat model Linear Regression yang telah disimpan
    model_url = "https://dl.dropboxusercontent.com/scl/fi/hfj45bbigcyvsup9aeipf/Model-Linear-Regression.pkl?rlkey=vggmunmapqzgthbcj2puiohu6"
    model = load_pickle_from_dropbox(model_url)

    # Memuat scaler untuk normalisasi data
    scaler_url = "https://dl.dropboxusercontent.com/scl/fi/bzuklawrhusvzw1blbozq/scaler.pkl?rlkey=wi6cqgkcrm94du7ce4qt5fx8e"
    scaler = load_pickle_from_dropbox(scaler_url)

    # Memuat OneHotEncoder untuk kolom-kolom kategorik yang telah disimpan
    weather_ohe_url = "https://dl.dropboxusercontent.com/scl/fi/fnjz9ovnvs66cut7e8jig/Weather_ohe.pkl?rlkey=2my2uri7b7fgcmrdtrt2eoak4"
    weather_ohe = load_pickle_from_dropbox(weather_ohe_url)

    vehicle_type_ohe_url = "https://dl.dropboxusercontent.com/scl/fi/nnsljx70zjg3evnd51zxy/Vehicle_Type_ohe.pkl?rlkey=sc6giyo06e7yia0flfrtuxj5m"
    vehicle_type_ohe = load_pickle_from_dropbox(vehicle_type_ohe_url)

    time_of_day_ohe_url = "https://dl.dropboxusercontent.com/scl/fi/e3d20osm0tjnnbtp7ry71/Time_of_Day_ohe.pkl?rlkey=u22cw4pa4h1xsd08dwxit8z7s"
    time_of_day_ohe = load_pickle_from_dropbox(time_of_day_ohe_url)

    traffic_level_ohe_url = "https://dl.dropboxusercontent.com/scl/fi/7mj2z6piodp0x9p6y1sq2/Traffic_Level_ohe.pkl?rlkey=pbs9e5d7xvlow74tyt01d7rng"
    traffic_level_ohe = load_pickle_from_dropbox(traffic_level_ohe_url)

    # Menambahkan tombol Submit dan proses loading
    submit_button = st.button("Submit")

    if submit_button:
        # Menampilkan progress loading dengan spinner
        with st.spinner('Memproses data...'):
            # Melakukan One-Hot Encoding untuk kolom 'Weather' menggunakan encoder yang sudah dilatih
            encoded_data_weather = weather_ohe.transform(input_data[['Weather']])
            encoded_columns_weather = weather_ohe.get_feature_names_out(['Weather'])

            # Membuat DataFrame hasil encoding untuk 'Weather'
            df_encoded_weather = pd.DataFrame(encoded_data_weather, columns=encoded_columns_weather, index=input_data.index)

            # Menambahkan hasil encoding ke DataFrame input
            input_data = pd.concat([input_data, df_encoded_weather], axis=1)
            input_data = input_data.drop(columns=['Weather'])

            # Melakukan One-Hot Encoding untuk kolom 'Traffic_Level' menggunakan encoder yang sudah dilatih
            encoded_data_traffic_level = traffic_level_ohe.transform(input_data[['Traffic_Level']])
            encoded_columns_traffic_level = traffic_level_ohe.get_feature_names_out(['Traffic_Level'])
            df_encoded_traffic_level = pd.DataFrame(encoded_data_traffic_level, columns=encoded_columns_traffic_level, index=input_data.index)
            input_data = pd.concat([input_data, df_encoded_traffic_level], axis=1)
            input_data = input_data.drop(columns=['Traffic_Level'])

            # Melakukan One-Hot Encoding untuk kolom 'Vehicle_Type' menggunakan encoder yang sudah dilatih
            encoded_data_vehicle_type = vehicle_type_ohe.transform(input_data[['Vehicle_Type']])
            encoded_columns_vehicle_type = vehicle_type_ohe.get_feature_names_out(['Vehicle_Type'])
            df_encoded_vehicle_type = pd.DataFrame(encoded_data_vehicle_type, columns=encoded_columns_vehicle_type, index=input_data.index)
            input_data = pd.concat([input_data, df_encoded_vehicle_type], axis=1)
            input_data = input_data.drop(columns=['Vehicle_Type'])

            # Melakukan One-Hot Encoding untuk kolom 'Time_of_Day' menggunakan encoder yang sudah dilatih
            encoded_data_time_of_day = time_of_day_ohe.transform(input_data[['Time_of_Day']])
            encoded_columns_time_of_day = time_of_day_ohe.get_feature_names_out(['Time_of_Day'])
            df_encoded_time_of_day = pd.DataFrame(encoded_data_time_of_day, columns=encoded_columns_time_of_day, index=input_data.index)
            input_data = pd.concat([input_data, df_encoded_time_of_day], axis=1)
            input_data = input_data.drop(columns=['Time_of_Day'])

            # Pilih kolom numerik yang perlu diskalakan
            numerik_scale = ['Preparation_Time_min', 'Courier_Experience_yrs', 'Distance_km']

            # Lakukan scaling hanya pada kolom numerik
            input_data[numerik_scale] = scaler.transform(input_data[numerik_scale])

            # Kolom yang benar-benar digunakan saat pelatihan (harus sama persis dengan yang ada saat pelatihan)
            correct_column_order = [
                'Weather_Clear', 'Weather_Foggy', 'Weather_Rainy', 'Weather_Snowy', 'Weather_Windy','Traffic_Level_High', 
                'Traffic_Level_Low', 'Traffic_Level_Medium', 
                'Vehicle_Type_Bike', 'Vehicle_Type_Car', 'Vehicle_Type_Scooter', 
                'Time_of_Day_Afternoon', 'Time_of_Day_Evening', 'Time_of_Day_Morning', 'Time_of_Day_Night',
                'Preparation_Time_min', 'Courier_Experience_yrs', 'Distance_km'
            ]

            # Menyusun kolom input_data agar sesuai dengan urutan yang benar
            input_data = input_data[correct_column_order]

            # Lakukan prediksi
            prediction = model.predict(input_data)

            # Menampilkan hasil prediksi dengan style
            predicted_time = prediction[0] if prediction.ndim == 1 else prediction[0][0]

            # Membuat box untuk prediksi
            st.markdown(f"""
                <div style="background-color: #f9f9f9; border: 2px solid #007acc; padding: 20px; border-radius: 10px; text-align: center; transition: transform 0.3s ease-in-out; cursor: pointer;" 
                    onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                    <h3 style="font-size: 24px; color: #007acc;">Prediksi Waktu Pengantaran (Delivery Time):</h3>
                    <h2 style="font-size: 36px; color: #333; font-weight: bold;">{predicted_time:.2f} menit</h2>
                </div>
            """, unsafe_allow_html=True)