import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
combined_df = pd.read_csv(f"{script_dir}/combined_df.csv") 

combined_df.to_parquet("combined_df.parquet")
combined_df = pd.read_parquet("combined_df.parquet")

# Load Data
@st.cache_data
def load_data():
    combined_df = pd.read_parquet("combined_df.parquet")
    combined_df["datetime"] = pd.to_datetime(combined_df["datetime"])
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
    st.subheader("🌧️Perbandingan Rata-rata PM2.5 Saat Hujan dan Tidak Hujan")
    grouped_pm25 = filtered_df.groupby(["station", "Rain Condition"])["PM2.5"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    custom_palette = {"No Rain": "orange", "Rain": "skyblue"}
    sns.barplot(x="station", y="PM2.5", hue="Rain Condition", data=grouped_pm25, palette=custom_palette, ax=ax)
    ax.set_ylim(0, 120)
    ax.set_yticks(range(0, 121, 10))
    for y in range(0, 121, 10):
        ax.axhline(y=y, color='gray', linestyle='--', alpha=0.5, zorder=0)
    ax.set_xlabel("Stasiun")
    ax.set_ylabel("Rata-rata Konsentrasi PM2.5 (µg/m³)")
    ax.set_title("Perbandingan Rata-rata PM2.5 Saat Hujan dan Tidak Hujan")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.legend(title="Kondisi Hujan")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    st.pyplot(fig)

    # Bar Chart PM10
    st.subheader("🌧️Perbandingan Rata-rata PM10 Saat Hujan dan Tidak Hujan")
    grouped_pm10 = filtered_df.groupby(["station", "Rain Condition"])["PM10"].mean().reset_index()
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.barplot(x="station", y="PM10", hue="Rain Condition", data=grouped_pm10, palette=custom_palette, ax=ax)
    ax.set_ylim(0, 150)
    ax.set_yticks(range(0, 151, 10))
    for y in range(0, 151, 10):
        ax.axhline(y=y, color='gray', linestyle='--', alpha=0.5, zorder=0)
    ax.set_xlabel("Stasiun")
    ax.set_ylabel("Rata-rata Konsentrasi PM10 (µg/m³)")
    ax.set_title("Perbandingan Rata-rata PM10 Saat Hujan dan Tidak Hujan")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.legend(title="Kondisi Hujan")
    ax.grid(axis='y', linestyle='--', alpha=0.7)
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
