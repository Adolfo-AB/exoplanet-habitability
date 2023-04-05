import pandas as pd
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
import seaborn as sns

FILENAME = "phl_exoplanet_catalog_2019.csv"
SELECTED_FEATURES = ("P_NAME", "S_NAME", "P_HABITABLE", "P_RADIUS", "P_PERIOD", "P_TEMP_EQUIL",
                     "P_TEMP_EQUIL_MIN", "P_TEMP_EQUIL_MAX", "P_DISTANCE", "S_MASS", "S_RADIUS",
                     "S_TEMPERATURE", "S_LUMINOSITY", "S_METALLICITY")

def clean_data():
    data = pd.read_csv(FILENAME)

    # Drop unused features
    data = data.drop([column for column in data.columns if column not in SELECTED_FEATURES], axis=1)

    # Raw data exploration
    print("Data info:")
    data.info()
    print(data.describe())
    print(data.head())
    print()

    print("Showing columns of the raw data:")
    for column_name, dtype in data.dtypes.items():
        print(f"{column_name}: {dtype}")
    print()

    # Check missing values from columns
    print("Showing count of missing values from features:")
    # Get a boolean mask indicating missing values in the DataFrame
    missing_data_mask = data.isnull()

    # Calculate the number of missing values for each column
    missing_data_counts = missing_data_mask.sum()

    # Calculate the percentage of missing values for each column
    missing_data_percent = missing_data_counts / len(data) * 100

    # Print columns with missing data, the count of missing values, and the percentage of missing values
    for column_name, missing_count in missing_data_counts.items():
        if missing_count > 0:
            print(f"{column_name}: {missing_count} missing values ({missing_data_percent[column_name]:.2f}%)")
    print()

    # Impute missing values with mean
    print("Imputing missing values with mean")
    mean_imputer = SimpleImputer(strategy="mean")
    data_imputed = pd.DataFrame(mean_imputer.fit_transform(data.select_dtypes(include=['float64', 'int64'])),
                                columns=data.select_dtypes(include=['float64', 'int64']).columns)
    data[data_imputed.columns] = data_imputed

    # Export preprocessed data to .csv
    data.to_csv("preprocessed_data.csv", index=False)

    # Show histogram for "P_HABITABLE"
    plt.figure(figsize=(10, 6))
    plt.hist(data["P_HABITABLE"], bins=[-0.5, 0.5, 1.5, 2.5], color="navy", alpha=0.7,
             rwidth=0.8)
    plt.xlabel("Habitability", fontsize=14)
    plt.ylabel("Frequency", fontsize=14)
    plt.title("Habitability Indicator", fontsize=16)
    plt.xticks([0, 1, 2], ['Non-habitable (0)', 'Conservatively Habitable (1)', 'Optimistically Habitable (2)'], fontsize=12)
    plt.yticks(fontsize=12)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()

    # Plot correlation heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(data.select_dtypes(include=['float64', 'int64']).corr(), cmap="coolwarm", annot=True, vmin=-1, vmax=1)
    plt.title("Correlation Heatmap", fontsize=16)
    plt.show()

if __name__ == "__main__":
    clean_data()