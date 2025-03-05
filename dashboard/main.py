import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
combined_df = pd.read_csv(f"{script_dir}/combined_df.csv") 

# Load Data
@st.cache_data
def load_data():
    combined_df = pd.read_csv("combined_df.csv", parse_dates=["datetime"])
    combined_df["year"] = combined_df["datetime"].dt.year
    combined_df["Rain Condition"] = combined_df["RAIN"].apply(lambda x: "No Rain" if x == 0 else "Rain")
    return combined_df

combined_df = load_data()
stations = combined_df["station"].unique()

# Dashboard Title
st.title("📊 Dashboard Kualitas Udara dan Kondisi Hujan")

# Pilihan Stasiun
selected_station = st.selectbox("Pilih Stasiun:", stations)
filtered_df = combined_df[combined_df["station"] == selected_station]

# Boxplot PM2.5
st.subheader("Perbandingan PM2.5 Saat Hujan dan Tidak Hujan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x="Rain Condition", y="PM2.5", data=filtered_df, palette={"No Rain": "orange", "Rain": "skyblue"}, ax=ax)
ax.set_ylabel("Konsentrasi PM2.5 (µg/m³)")
ax.set_xlabel("Kondisi Hujan")
st.pyplot(fig)

# Boxplot PM10
st.subheader("Perbandingan PM10 Saat Hujan dan Tidak Hujan")
fig, ax = plt.subplots(figsize=(10, 5))
sns.boxplot(x="Rain Condition", y="PM10", data=filtered_df, palette={"No Rain": "orange", "Rain": "skyblue"}, ax=ax)
ax.set_ylabel("Konsentrasi PM10 (µg/m³)")
ax.set_xlabel("Kondisi Hujan")
st.pyplot(fig)

# Tren PM2.5 & PM10 per Tahun
st.subheader("📈 Tren Polusi Udara (2013-2017)")
pm_yearly_avg = combined_df.groupby(["station", "year"])[["PM2.5", "PM10"]].mean().reset_index()
subset = pm_yearly_avg[pm_yearly_avg["station"] == selected_station]

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(subset["year"], subset["PM2.5"], marker="o", linestyle="-", label="PM2.5", color="red")
ax.plot(subset["year"], subset["PM10"], marker="s", linestyle="--", label="PM10", color="orange")
ax.set_xticks([2013, 2014, 2015, 2016, 2017])
ax.set_xlim(2013, 2017)
ax.set_ylim(0, 150)
ax.set_xlabel("Tahun")
ax.set_ylabel("Konsentrasi (µg/m³)")
ax.legend()
ax.grid(True)
st.pyplot(fig)

st.write("Dashboard ini menampilkan analisis kualitas udara berdasarkan kondisi hujan dan tren polusi udara dari tahun 2013 hingga 2017.")
