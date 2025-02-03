import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import cm


# load data and rename columns
df = pd.read_csv("table1.csv")
df.columns = [
    "area",
    "pop",
    "acres",
    "pop_density",
    "avg_hh_size",
    "pct_0_vehicles",
    "pct_1_vehicle",
    "pct_2_plus_vehicles",
]


# ensure vehicle ownership types sum to 100%
vehicle_pct_sum = df["pct_0_vehicles"] + df["pct_1_vehicle"] + df["pct_2_plus_vehicles"]
df.loc[vehicle_pct_sum < 1, ["pct_0_vehicles", "pct_1_vehicle", "pct_2_plus_vehicles"]] = (
    df.loc[vehicle_pct_sum < 1, ["pct_0_vehicles", "pct_1_vehicle", "pct_2_plus_vehicles"]].div(vehicle_pct_sum, axis=0)
)


# calculate vehicle ownership
TWO_PLUS_VEHICLE_ESTIMATE = 2.5
df["avg_num_vehicles"] = df["pct_2_plus_vehicles"] * TWO_PLUS_VEHICLE_ESTIMATE + df["pct_1_vehicle"]
df["avg_num_vehicles_per_person"] = df["avg_num_vehicles"] / df["avg_hh_size"]


# calculate benefit score
pop_density_norm = (df["pop_density"] - df["pop_density"].min()) / (df["pop_density"].max() - df["pop_density"].min())
vehicles_per_person_norm = (df["avg_num_vehicles_per_person"] - df["avg_num_vehicles_per_person"].min()) / (df["avg_num_vehicles_per_person"].max() - df["avg_num_vehicles_per_person"].min())
benefit_score = pop_density_norm - vehicles_per_person_norm


# generate plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(df["pop_density"],
                      df["avg_num_vehicles_per_person"],
                      c=benefit_score,
                      cmap=cm.Blues,
                      norm=Normalize(vmin=benefit_score.min(), vmax=benefit_score.max()),
                      edgecolors='black',
                      s=100)
for i in range(df.shape[0]):
    plt.text(df["pop_density"].iloc[i] + 0.01,
             df["avg_num_vehicles_per_person"].iloc[i] + 0.02,
             df["area"].iloc[i], 
             fontsize=10, 
             fontweight='light', 
             fontname="Arial",
             color='black')
plt.suptitle("Chart 1", fontsize=16, y=1.02)
plt.title("Which Area Would Most Benefit from Transit Investment?", fontsize=10, pad=15)
plt.xlabel("Population Density (people per acre)", fontsize=12, fontweight='bold')
plt.ylabel("Average Number of Vehicles per Person", fontsize=12, fontweight='bold')
plt.colorbar(scatter, label='Benefit Score')
plt.grid(True)
plt.savefig("chart1.png", dpi=300, bbox_inches='tight')
