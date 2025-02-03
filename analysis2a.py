import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# load, clean, and merge data
table1 = pd.read_csv("table1.csv")
table2 = pd.read_csv("table2.csv")
table1.columns = [
    "area", "pop", "acres", "pop_density", "avg_hh_size",
    "pct_0_vehicles", "pct_1_vehicle", "pct_2_plus_vehicles",
]
table2.columns = [
    "area", "age_0_19", "age_20_34", "age_35_44", "age_45_64",
    "age_65_plus", "unemployment_rate", "poverty_rate", "mhi"
]
df = pd.merge(table1, table2, on="area", how="inner")
full_names = {
    "unemployment_rate": "Unemployment Rate",
    "poverty_rate": "Poverty Rate",
    "mhi": "Median Household Income",
    "pop": "Population",
    "acres": "Size (acres)",
    "pop_density": "Population Density",
    "avg_hh_size": "Average Household Size",
    "pct_0_vehicles": "%HH 0 Vehicles",
    "pct_1_vehicle": "%HH 1 Vehicle",
    "pct_2_plus_vehicles": "%HH 2+ Vehicles",
    "age_0_19": "% Age 0-19",
    "age_20_34": "% Age 20-34",
    "age_35_44": "% Age 35-44",
    "age_45_64": "% Age 45-64",
    "age_65_plus": "% Age 65+"
}


# define socioeconomic indicators and demographic metrics
socioeconomic_indicators = ["unemployment_rate", "poverty_rate", "mhi"]
demographic_stats = [
    "pop", "acres", "pop_density", "avg_hh_size",
    "pct_0_vehicles", "pct_1_vehicle", "pct_2_plus_vehicles",
    "age_0_19", "age_20_34", "age_35_44", "age_45_64", "age_65_plus"
]


# calculate correlations
correlations = df[socioeconomic_indicators + demographic_stats].corr()
correlations_display = correlations.rename(index=full_names, columns=full_names)


# generate plot
plt.figure(figsize=(12, 8))
heatmap = sns.heatmap(correlations_display.loc[list(full_names.values())[:3], list(full_names.values())[3:]],
                                               annot=True,
                                               cmap="coolwarm",
                                               annot_kws={"size": 8},
                                               cbar_kws={"orientation": "horizontal", "pad": 0.25})
plt.suptitle("Chart 2a", fontsize=16, y=0.95)
plt.title("Correlation between Socioeconomic Indicators and Demographic Metrics", fontsize=10, pad=10)
plt.xticks(rotation=45, ha='right', wrap=True)
plt.yticks(rotation=0)
heatmap.set_yticklabels(heatmap.get_yticklabels(), rotation=0, ha='right', wrap=True)
plt.savefig("chart2a.png", dpi=300, bbox_inches='tight')
