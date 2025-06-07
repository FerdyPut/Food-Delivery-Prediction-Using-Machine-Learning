import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

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

    # Memuat encoder untuk kolom-kolom kategorik yang telah disimpan
    ohe_dict = {}  # Untuk menyimpan encoder per kolom
    for col in ['Weather', 'Traffic_Level', 'Vehicle_Type', 'Time_of_Day']:
        with open(f"{col}_ohe.pkl", "rb") as f:
            ohe_dict[col] = pickle.load(f)

    # Memproses data input:
    # 1. Melakukan One-Hot Encoding untuk kolom kategorik
    for col in ['Weather', 'Traffic_Level', 'Vehicle_Type', 'Time_of_Day']:
        ohe = ohe_dict[col]
        # Melakukan transformasi (encoding)
        encoded_data = ohe.transform(input_data[[col]])
        encoded_columns = ohe.get_feature_names_out([col])

        # Membuat DataFrame hasil encoding
        df_encoded = pd.DataFrame(encoded_data, columns=encoded_columns, index=input_data.index)

        # Menambahkan hasil encoding ke DataFrame input
        input_data = pd.concat([input_data, df_encoded], axis=1)

        # Menghapus kolom asli yang kategorikal
        input_data = input_data.drop(columns=[col])

    # 2. Melakukan scaling untuk kolom numerik
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
