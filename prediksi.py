import pickle
import requests
import pandas as pd
import streamlit as st
from io import BytesIO

# Fungsi untuk mengunduh dan memuat pickle dari Dropbox
def load_pickle_from_dropbox(url):
    # Mengunduh file pickle dari URL Dropbox
    response = requests.get(url)
    if response.status_code == 200:
        return pickle.load(BytesIO(response.content))  # Memuat pickle dari response content
    else:
        st.error(f"Error: {response.status_code}")
        return None

def prediksi():
    st.title('Food Time Delivery Prediction')

    # Input variabel dari pengguna
    st.write("Masukkan data untuk memprediksi waktu pengantaran:")
    
    # Input untuk variabel-variabel prediksi
    distance_km = st.number_input("Jarak Pengantaran (km)", min_value=0.0, value=5.0, step=0.1)
    courier_experience_yrs = st.number_input("Pengalaman Kurir (tahun)", min_value=0, value=3, step=1)
    preparation_time_min = st.number_input("Waktu Persiapan (menit)", min_value=0, value=10, step=1)
    weather = st.selectbox("Kondisi Cuaca", ['Clear', 'Rainy', 'Cloudy'])  # Kategorik
    traffic_level = st.selectbox("Tingkat Lalu Lintas", ['Low', 'Moderate', 'High'])  # Kategorik
    time_of_day = st.selectbox("Waktu Pengiriman", ['Morning', 'Afternoon', 'Evening'])  # Kategorik
    vehicle_type = st.selectbox("Jenis Kendaraan", ['Motor', 'Car', 'Bicycle'])  # Kategorik

    # Membuat DataFrame untuk input pengguna
    input_data = pd.DataFrame([[distance_km, courier_experience_yrs, preparation_time_min, weather, traffic_level, time_of_day, vehicle_type]],
                              columns=['Distance_km', 'Courier_Experience_yrs', 'Preparation_Time_min', 'Weather', 'Traffic_Level', 'Time_of_Day', 'Vehicle_Type'])

    # Memuat model, scaler dan encoder yang telah disimpan
    model = pickle.load(open('food_delivery_model.pkl', 'rb'))

    # Memuat scaler untuk normalisasi data
    scaler = pickle.load(open('scaler.pkl', 'rb'))

    # Memuat OneHotEncoder untuk kolom-kolom kategorik yang telah disimpan
    weather_ohe_url = "https://dl.dropboxusercontent.com/scl/fi/fnjz9ovnvs66cut7e8jig/Weather_ohe.pkl?rlkey=2my2uri7b7fgcmrdtrt2eoak4"
    weather_ohe = load_pickle_from_dropbox(weather_ohe_url)

    # Memuat OneHotEncoder untuk Vehicle_Type dari Dropbox
    vehicle_type_ohe_url = "https://dl.dropboxusercontent.com/scl/fi/nnsljx70zjg3evnd51zxy/Vehicle_Type_ohe.pkl?rlkey=sc6giyo06e7yia0flfrtuxj5m"
    vehicle_type_ohe = load_pickle_from_dropbox(vehicle_type_ohe_url)

    # Memuat OneHotEncoder untuk Time_of_Day dari Dropbox
    time_of_day_ohe_url = "https://dl.dropboxusercontent.com/scl/fi/e3d20osm0tjnnbtp7ry71/Time_of_Day_ohe.pkl?rlkey=u22cw4pa4h1xsd08dwxit8z7s"
    time_of_day_ohe = load_pickle_from_dropbox(time_of_day_ohe_url)

    # Memuat OneHotEncoder untuk Traffic_Level dari Dropbox
    traffic_level_ohe_url = "https://dl.dropboxusercontent.com/scl/fi/7mj2z6piodp0x9p6y1sq2/Traffic_Level_ohe.pkl?rlkey=pbs9e5d7xvlow74tyt01d7rng"
    traffic_level_ohe = load_pickle_from_dropbox(traffic_level_ohe_url)

    # Menambahkan tombol Submit dan proses loading
    submit_button = st.button("Submit")

    if submit_button:
        # Menampilkan progress loading dengan spinner
        with st.spinner('Memproses data...'):
            # Memproses data input:
            # 1. Melakukan One-Hot Encoding untuk kolom 'Weather'
            encoded_data_weather = weather_ohe.transform(input_data[['Weather']])
            encoded_columns_weather = weather_ohe.get_feature_names_out(['Weather'])

            # Membuat DataFrame hasil encoding untuk 'Weather'
            df_encoded_weather = pd.DataFrame(encoded_data_weather, columns=encoded_columns_weather, index=input_data.index)

            # Menambahkan hasil encoding ke DataFrame input
            input_data = pd.concat([input_data, df_encoded_weather], axis=1)

            # Menghapus kolom asli yang kategorikal
            input_data = input_data.drop(columns=['Weather'])

            # 2. Melakukan One-Hot Encoding untuk kolom 'Vehicle_Type'
            encoded_data_vehicle_type = vehicle_type_ohe.transform(input_data[['Vehicle_Type']])
            encoded_columns_vehicle_type = vehicle_type_ohe.get_feature_names_out(['Vehicle_Type'])

            # Membuat DataFrame hasil encoding untuk 'Vehicle_Type'
            df_encoded_vehicle_type = pd.DataFrame(encoded_data_vehicle_type, columns=encoded_columns_vehicle_type, index=input_data.index)

            # Menambahkan hasil encoding ke DataFrame input
            input_data = pd.concat([input_data, df_encoded_vehicle_type], axis=1)

            # Menghapus kolom asli yang kategorikal
            input_data = input_data.drop(columns=['Vehicle_Type'])

            # 3. Melakukan One-Hot Encoding untuk kolom 'Time_of_Day'
            encoded_data_time_of_day = time_of_day_ohe.transform(input_data[['Time_of_Day']])
            encoded_columns_time_of_day = time_of_day_ohe.get_feature_names_out(['Time_of_Day'])

            # Membuat DataFrame hasil encoding untuk 'Time_of_Day'
            df_encoded_time_of_day = pd.DataFrame(encoded_data_time_of_day, columns=encoded_columns_time_of_day, index=input_data.index)

            # Menambahkan hasil encoding ke DataFrame input
            input_data = pd.concat([input_data, df_encoded_time_of_day], axis=1)

            # Menghapus kolom asli yang kategorikal
            input_data = input_data.drop(columns=['Time_of_Day'])

            # 4. Melakukan One-Hot Encoding untuk kolom 'Traffic_Level'
            encoded_data_traffic_level = traffic_level_ohe.transform(input_data[['Traffic_Level']])
            encoded_columns_traffic_level = traffic_level_ohe.get_feature_names_out(['Traffic_Level'])

            # Membuat DataFrame hasil encoding untuk 'Traffic_Level'
            df_encoded_traffic_level = pd.DataFrame(encoded_data_traffic_level, columns=encoded_columns_traffic_level, index=input_data.index)

            # Menambahkan hasil encoding ke DataFrame input
            input_data = pd.concat([input_data, df_encoded_traffic_level], axis=1)

            # Menghapus kolom asli yang kategorikal
            input_data = input_data.drop(columns=['Traffic_Level'])

            # 5. Melakukan scaling untuk kolom numerik
            input_data_numeric = input_data[['Distance_km', 'Courier_Experience_yrs', 'Preparation_Time_min']]

            # Melakukan scaling menggunakan StandardScaler yang telah dilatih
            input_data_scaled = scaler.transform(input_data_numeric)

            # Menyusun kembali DataFrame setelah scaling
            input_data_scaled_df = pd.DataFrame(input_data_scaled, columns=input_data_numeric.columns, index=input_data.index)

            # Menambahkan hasil scaling ke input_data yang sudah diencoding
            input_data = pd.concat([input_data_scaled_df, input_data.drop(columns=['Distance_km', 'Courier_Experience_yrs', 'Preparation_Time_min'])], axis=1)

            # Melakukan prediksi menggunakan model yang sudah dilatih
            prediction = model.predict(input_data)

            # Menampilkan hasil prediksi
            st.write(f"Prediksi waktu pengantaran (Delivery Time) adalah: {prediction[0]:.2f} menit")

            # Metrik evaluasi prediksi (optional jika tersedia data test)
            rmse = 5.0  # Placeholder, replace with actual RMSE calculation
            mae = 3.2   # Placeholder, replace with actual MAE calculation
            mape = 12.5  # Placeholder, replace with actual MAPE calculation
            r2 = 0.85    # Placeholder, replace with actual R^2 calculation

            # Tampilkan metrik evaluasi
            st.subheader("Metrik Evaluasi:")
            st.write(f"RMSE: {rmse:.2f}")
            st.write(f"MAE: {mae:.2f}")
            st.write(f"MAPE: {mape:.2f}%")
            st.write(f"R²: {r2:.2f}")

            # Line chart untuk visualisasi perbandingan antara prediksi dan actual (jika data tersedia)
            st.subheader("Prediksi vs Actual")
            actual_values = [10, 12, 14, 15, 13]  # Example, replace with actual values
            predicted_values = [prediction[0]] * len(actual_values)  # Example for visualization
            st.line_chart({"Actual": actual_values, "Predicted": predicted_values})

