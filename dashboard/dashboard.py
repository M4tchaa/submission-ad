import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='dark')

# Helper Functions
def create_weather_group_data(df):
    return df.groupby("weather_group")["cnt"].mean().sort_values(ascending=False)

def create_total_weather_group_data(df):
    return df.groupby("weather_group")["cnt"].sum().sort_values(ascending=False)

def create_season_group_data(df):
    return df.groupby("season_group")["cnt"].sum().reindex(["Spring", "Summer", "Fall", "Winter"])

def create_season_group_average_data(df):
    return df.groupby("season_group")["cnt"].mean().reindex(["Spring", "Summer", "Fall", "Winter"])

def create_correlation_matrix(df):
    return df[["temp", "atemp", "hum", "windspeed", "cnt"]].corr()

def create_hourly_rentals_data(df):
    hourly_avg = df.groupby("hr")["cnt"].mean()
    hourly_avg = hourly_avg.reindex(range(24), fill_value=0)
    return hourly_avg


# Load Data
bike_data = pd.read_csv("dashboard/main_data.csv")

# Data Preparation
bike_data["dteday"] = pd.to_datetime(bike_data["dteday"])
bike_data["weather_group"] = bike_data["weathersit"].map({
    1: "Clear",
    2: "Mist",
    3: "Rain",
    4: "Thunderstorm"
})
bike_data["season_group"] = bike_data["season"].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})

# Sidebar Date Filter
min_date = bike_data["dteday"].min()
max_date = bike_data["dteday"].max()

with st.sidebar:
    st.image("dashboard/logo.jpg")
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

filtered_data = bike_data[(bike_data["dteday"] >= str(start_date)) & 
                          (bike_data["dteday"] <= str(end_date))]

# Prepare Data Using Helper Functions
weather_group_data = create_weather_group_data(filtered_data)
total_weather_group_data = create_total_weather_group_data(filtered_data)
season_group_data = create_season_group_data(filtered_data)
season_group_average_data = create_season_group_average_data(filtered_data)  # Pastikan ini untuk rata-rata
corr_matrix = create_correlation_matrix(filtered_data)
hourly_rentals_data = create_hourly_rentals_data(filtered_data)

# Calculate Total Orders
total_orders = filtered_data['cnt'].sum()

# Streamlit Visualizations
st.title("Arliyandi Bike Rentals Dashboard")
st.header(f"Total Orders: {total_orders:,.0f}")

# Total Weather Group Analysis
st.subheader("Total Bike Rentals by Weather Condition")
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(total_weather_group_data.index, total_weather_group_data.values, color=['skyblue', 'orange', 'red', 'black'])

for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        yval + 5000,
        f'{yval:,.0f}',
        ha='center',
        va='bottom',
        fontsize=10
    )

ax.set_title('Total Bike Rentals by Weather Condition', fontsize=14, fontweight='bold')
ax.set_xlabel('Weather Condition', fontsize=12)
ax.set_ylabel('Total Rentals', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

# Weather Group Analysis
st.subheader("Bike Rentals by Weather Condition")
fig, ax = plt.subplots()
weather_group_data.plot(kind='bar', color=['skyblue', 'orange', 'red', 'black'], ax=ax)
ax.set_title('Average Bike Rentals by Weather Condition')
ax.set_xlabel('Weather Condition')
ax.set_ylabel('Average Rentals')
st.pyplot(fig)

# **Correlation Heatmap**
st.subheader("Correlation Heatmap")
plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix for Weather and Bike Rentals', fontsize=14, fontweight='bold')
st.pyplot(plt)

# Visualisasi Total Rentals By Season
st.subheader("Total Bike Rentals by Season")
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(season_group_data.index, season_group_data.values, color='skyblue')

for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        yval + 5000,
        f'{yval:,.0f}',
        ha='center',
        va='bottom',
        fontsize=10
    )

ax.set_title('Total Bike Rentals by Season', fontsize=14, fontweight='bold')
ax.set_xlabel('Season', fontsize=12)
ax.set_ylabel('Total Rentals', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

# Visualisasi Average Rentals By Season
st.subheader("Average Bike Rentals by Season")
fig, ax = plt.subplots(figsize=(8, 6))
bars = ax.bar(season_group_average_data.index, season_group_average_data.values)

ax.set_title('Average Bike Rentals by Season', fontsize=14, fontweight='bold')
ax.set_xlabel('Season', fontsize=12)
ax.set_ylabel('Average Rentals', fontsize=12)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
st.pyplot(fig)

# **Peak Hourly Rentals**
st.subheader("Peak Hourly Rentals")
fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.bar(hourly_rentals_data.index, hourly_rentals_data.values, color='lightblue')

for bar in bars:
    yval = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2, 
        yval + 1, 
        f'{yval:,.0f}', 
        ha='center', 
        va='bottom', 
        fontsize=9
    )

# Garis threshold untuk rata-rata
mean_value = hourly_rentals_data.mean()
ax.axhline(mean_value, color='red', linestyle='--', label=f"Average Rentals: {mean_value:,.0f}")
ax.legend()

# Label
ax.set_title("Average Bike Rentals by Hour of the Day", fontsize=14, fontweight='bold')
ax.set_xlabel("Hour of the Day (24-Hour Format)", fontsize=12)
ax.set_ylabel("Average Rentals", fontsize=12)
ax.set_xticks(range(0, 24))
ax.set_xticklabels(range(0, 24))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

st.pyplot(fig)

st.caption('Copyright © itsMatcha 2024')