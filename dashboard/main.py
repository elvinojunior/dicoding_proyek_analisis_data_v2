import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
combined_df = pd.read_csv(f"{script_dir}/combined_df.csv") 

combined_df.to_parquet("combined_df.parquet", engine="pyarrow")
combined_df = pd.read_parquet("combined_df.parquet")

# Load Data
@st.cache_data
def load_data():
    combined_df = pd.read_parquet("combined_df.csv", parse_dates=["datetime"])
    combined_df["year"] = combined_df["datetime"].dt.year
    combined_df["Rain Condition"] = combined_df["RAIN"].apply(lambda x: "No Rain" if x == 0 else "Rain")
    return combined_df

combined_df = load_data()
stations = combined_df["station"].unique()

# Dashboard Title
st.title("📊 Dashboard Kualitas Udara di berbagai Stasiun Beijing")
st.write("Dashboard ini menampilkan analisis perbedaan kualitas udara berdasarkan kondisi hujan dan tren polusi udara dari tahun 2013 hingga 2017")

# Pilihan Stasiun
selected_stations = st.multiselect("Pilih Stasiun:", stations, default=stations)

if not selected_stations:
    st.warning("Tidak ada lokasi yang dipilih. Silakan pilih setidaknya satu lokasi untuk melihat data.")
else:
    filtered_df = combined_df[combined_df["station"].isin(selected_stations)]

    # Bar Chart PM2.5
    st.subheader("Perbandingan Produksi PM2.5 Saat Hujan dan Tidak Hujan")
    fig, ax = plt.subplots(figsize=(10, 5))
    mean_pm25 = filtered_df.groupby("Rain Condition")["PM2.5"].mean()
    mean_pm25.plot(kind='bar', color=["orange", "skyblue"], ax=ax)
    ax.set_ylabel("Konsentrasi PM2.5 (µg/m³)")
    ax.set_xlabel("Kondisi Hujan")
    ax.set_ylim(0, 120)
    ax.set_xticklabels(mean_pm25.index, rotation=0)
    st.pyplot(fig)

    # Bar Chart PM10
    st.subheader("Perbandingan Produksi PM10 Saat Hujan dan Tidak Hujan")
    fig, ax = plt.subplots(figsize=(10, 5))
    mean_pm10 = filtered_df.groupby("Rain Condition")["PM10"].mean()
    mean_pm10.plot(kind='bar', color=["orange", "skyblue"], ax=ax)
    ax.set_ylabel("Konsentrasi PM10 (µg/m³)")
    ax.set_xlabel("Kondisi Hujan")
    ax.set_ylim(0, 140)
    ax.set_xticklabels(mean_pm10.index, rotation=0)
    st.pyplot(fig)

    # Tren PM2.5 & PM10 per Tahun
    st.subheader("📈 Tren Polusi Udara (2013-2017)")
    pm_yearly_avg = combined_df.groupby(["station", "year"])[["PM2.5", "PM10"]].mean().reset_index()
    subset = pm_yearly_avg[pm_yearly_avg["station"].isin(selected_stations)]

    for station in selected_stations:
        station_data = subset[subset["station"] == station]
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=station_data, x="year", y="PM2.5", marker="o", linestyle="-", label="PM2.5", linewidth=2)
        sns.lineplot(data=station_data, x="year", y="PM10", marker="s", linestyle="--", label="PM10", linewidth=2)
        ax.set_xticks([2013, 2014, 2015, 2016, 2017])
        ax.set_xlim(2013, 2017)
        ax.set_ylim(0, 150)
        ax.set_title(f"Tren Polusi Udara untuk {station}")
        ax.set_xlabel("Tahun")
        ax.set_ylabel("Konsentrasi (µg/m³)")
        ax.legend(title="Polutan")
        ax.grid(True)
        st.pyplot(fig)
