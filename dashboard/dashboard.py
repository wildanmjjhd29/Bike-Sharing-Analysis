import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Membaca data dari file CSV
df_hour = pd.read_csv('hour.csv')
df_day = pd.read_csv('day.csv')

# Fungsi untuk menghitung rata-rata harian
def calculate_daily_average(data):
    return data.groupby('dteday')['cnt'].mean()

# Fungsi untuk menghitung rata-rata per jam
def calculate_hourly_average(data):
    return data.groupby('hr')['cnt'].mean()

# Fungsi untuk membuat plot
def create_plot(data, x_label, y_label, title):
    plt.figure(figsize=(10, 6))
    plt.plot(data.index, data.values, marker='o', linestyle='-')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(True)
    plt.gca().xaxis.set_major_locator(plt.MultipleLocator(7))
    plt.xticks(rotation=45)
    return plt

# Judul dasbor
st.title('Bike Sharing Data Dashboard')

# Sidebar untuk pemilihan pertanyaan
question = st.sidebar.selectbox(
    'Pilih Pertanyaan:',
    ('Pola Harian Peminjaman Sepeda (Musim Dingin 2011)', 
     'Rata-rata Peminjaman Sepeda per Jam (2012)', 
     'Peminjaman Sepeda pada Hari-hari dengan Cuaca Buruk (2011)', 
     'Hubungan Suhu dengan Peminjaman Sepeda (Musim Panas 2012)'
    ))

# Menampilkan visualisasi sesuai pertanyaan yang dipilih
if question == 'Pola Harian Peminjaman Sepeda (Musim Dingin 2011)':
    winter_2011_data = df_hour[(df_hour['season'] == 4) & (df_hour['yr'] == 0)]
    average_daily_cnt_winter_2011 = calculate_daily_average(winter_2011_data)
    st.pyplot(create_plot(average_daily_cnt_winter_2011, 'Tanggal', 'Jumlah Peminjaman Sepeda (cnt)', 'Pola Harian Peminjaman Sepeda (Musim Dingin 2011)'))

elif question == 'Rata-rata Peminjaman Sepeda per Jam (2012)':
    year_2012_data = df_hour[df_hour['yr'] == 1]
    average_hourly_cnt_weekday = calculate_hourly_average(year_2012_data[year_2012_data['workingday'] == 1])
    average_hourly_cnt_weekend = calculate_hourly_average(year_2012_data[year_2012_data['workingday'] == 0])
    st.pyplot(create_plot(average_hourly_cnt_weekday, 'Jam (hr)', 'Rata-rata Peminjaman Sepeda (cnt)', 'Rata-rata Peminjaman Sepeda per Jam (Hari Kerja 2012)'))
    st.pyplot(create_plot(average_hourly_cnt_weekend, 'Jam (hr)', 'Rata-rata Peminjaman Sepeda (cnt)', 'Rata-rata Peminjaman Sepeda per Jam (Akhir Pekan 2012)'))

elif question == 'Peminjaman Sepeda pada Hari-hari dengan Cuaca Buruk (2011)':
    bad_weather_2011_data = df_hour[(df_hour['yr'] == 0) & (df_hour['weathersit'] == 3)]
    average_daily_cnt_bad_weather_2011 = calculate_daily_average(bad_weather_2011_data)
    st.pyplot(create_plot(average_daily_cnt_bad_weather_2011, 'Tanggal', 'Jumlah Peminjaman Sepeda (cnt)', 'Peminjaman Sepeda pada Hari-hari dengan Cuaca Buruk (2011)'))

elif question == 'Hubungan Suhu dengan Peminjaman Sepeda (Musim Panas 2012)':
    summer_2012_data = df_hour[(df_hour['yr'] == 1) & (df_hour['season'] == 2)]
    correlation_temp_atemp = summer_2012_data[['temp', 'atemp', 'cnt']].corr()
    st.write('Korelasi antara Suhu Aktual (temp) dan Suhu Perasaan (atemp) dengan Jumlah Peminjaman Sepeda (cnt) (Musim Panas 2012):')
    st.dataframe(correlation_temp_atemp)

