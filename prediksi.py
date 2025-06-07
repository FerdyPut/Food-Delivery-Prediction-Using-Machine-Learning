import streamlit as st
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler

def prediksi():
    st.title('Food Time Delivery Prediction')

    # Input variabel dari pengguna
    st.write("Masukkan data untuk memprediksi waktu pengantaran:")
    
    distance_km = st.number_input("Jarak Pengantaran (km)", min_value=0.0, value=5.0, step=0.1)
    courier_experience_yrs = st.number_input("Pengalaman Kurir (tahun)", min_value=0, value=3, step=1)
    preparation_time_min = st.number_input("Waktu Persiapan (menit)", min_value=0, value=10, step=1)

    # Load model yang telah dilatih (model .pkl yang sudah disimpan)
    model = pickle.load(open('food_delivery_model.pkl', 'rb'))
    
    # Load scaler untuk normalisasi (jika diperlukan)
    scaler = pickle.load(open('scaler.pkl', 'rb'))

    # Menyiapkan input untuk prediksi
    input_features = pd.DataFrame([[distance_km, courier_experience_yrs, preparation_time_min]],
                                  columns=['Distance_km', 'Courier_Experience_yrs', 'Preparation_Time_min'])

    # Normalisasi data
    scaled_input = scaler.transform(input_features)

    # Melakukan prediksi menggunakan model
    prediction = model.predict(scaled_input)

    # Menampilkan hasil prediksi
    st.write(f"Prediksi waktu pengantaran (Delivery Time) adalah: {prediction[0]:.2f} menit")

    # Metrik evaluasi prediksi (optional jika tersedia data test)
    # Asumsi Anda memiliki data tes atau metrik lainnya
    # Example metrics (replace with actual metrics)
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
