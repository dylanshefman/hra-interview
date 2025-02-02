import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load data and rename columns
table1 = pd.read_csv('table1.csv')
table2 = pd.read_csv('table2.csv')
table1.columns = [
    "area",
    "pop",
    "acres",
    "pop_density",
    "avg_hh_size",
    "pct_0_vehicles",
    "pct_1_vehicle",
    "pct_2_plus_vehicles",
]
table2.columns = [
    'area',
    'age_0_19',
    'age_20_34',
    'age_35_44',
    'age_45_64',
    'age_65_plus',
    'unemployment_rate',
    'poverty_rate',
    'mhi'
]
df = pd.merge(table1, table2, on='area', how='inner')

# ensure vehicle ownership types sum to 100%
vehicle_pct_sum = df["pct_0_vehicles"] + df["pct_1_vehicle"] + df["pct_2_plus_vehicles"]
df.loc[vehicle_pct_sum < 1, ["pct_0_vehicles", "pct_1_vehicle", "pct_2_plus_vehicles"]] = (
    df.loc[vehicle_pct_sum < 1, ["pct_0_vehicles", "pct_1_vehicle", "pct_2_plus_vehicles"]].div(vehicle_pct_sum, axis=0)
)

# calculate vehicle ownership
TWO_PLUS_VEHICLE_ESTIMATE = 2.5
df["avg_num_vehicles"] = df["pct_2_plus_vehicles"] * TWO_PLUS_VEHICLE_ESTIMATE + df["pct_1_vehicle"]
df["avg_num_vehicles_per_person"] = df["avg_num_vehicles"] / df["avg_hh_size"]

# plot average number of vehicles per person vs poverty rate, unemployment rate, and median household income
fig, ax1 = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(left=0.1, right=0.85, top=0.85, bottom=0.1)  # Adjust top to ensure title is not cut off

# Create a second y-axis for unemployment rate
ax2 = ax1.twinx()

# Create a third y-axis for median household income
ax3 = ax1.twinx()
ax3.spines["right"].set_position(("outward", 60))

sns.regplot(x="avg_num_vehicles_per_person", y="poverty_rate", data=df, ax=ax1, color="blue", label="Poverty Rate", scatter_kws={"s": 10}, line_kws={"color": "blue"}, ci=None, truncate=False)
sns.regplot(x="avg_num_vehicles_per_person", y="unemployment_rate", data=df, ax=ax2, color="green", label="Unemployment Rate", scatter_kws={"s": 10}, line_kws={"color": "green"}, ci=None, truncate=False)
sns.regplot(x="avg_num_vehicles_per_person", y="mhi", data=df, ax=ax3, color="red", label="Median Household Income", scatter_kws={"s": 10}, line_kws={"color": "red"}, ci=None, truncate=False)

# Add vertical lines and labels for each area
for i, area in enumerate(df['area']):
    x = df.loc[i, 'avg_num_vehicles_per_person']
    ax1.axvline(x=x, color='gray', linestyle='--', linewidth=0.5)
    if area == "Area 5":
        ax1.text(x - 0.005, ax1.get_ylim()[1] * 1.02, area, rotation=45, verticalalignment='bottom', fontsize=8, color='gray')
    elif area == "City":
        ax1.text(x + 0.005, ax1.get_ylim()[1] * 1.02, area, rotation=45, verticalalignment='bottom', fontsize=8, color='gray')
    else:
        ax1.text(x, ax1.get_ylim()[1] * 1.02, area, rotation=45, verticalalignment='bottom', fontsize=8, color='gray')

ax1.set_xlabel("Average Number of Vehicles per Person")
ax1.set_ylabel("Poverty Rate", color="blue")
ax1.tick_params(axis='y', colors='blue')
ax1.spines['left'].set_color('blue')
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x*100:.0f}%'))

ax2.set_ylabel("Unemployment Rate", color="green")
ax2.tick_params(axis='y', colors='green')
ax2.spines['right'].set_color('green')
ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x*100:.0f}%'))

ax3.set_ylabel("Median Household Income", color="red")
ax3.tick_params(axis='y', colors='red')
ax3.spines['right'].set_color('red')

plt.show()