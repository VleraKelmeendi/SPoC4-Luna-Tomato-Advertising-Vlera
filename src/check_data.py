import csv
from pathlib import Path

# Get the main project folder
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"

# Database files
files = {
    "DRO": "db_dro.txt",
    "Lyapunov": "db_lyap.txt",
    "Axial": "db_axial.txt"
}

# Read and check each database
for orbit_name, filename in files.items():
    file_path = DATA_DIR / filename

    with open(file_path, "r") as file:
        reader = csv.reader(file)
        header = next(reader)
        rows = list(reader)

    print(f"\n{orbit_name}")
    print("Number of orbits:", len(rows))
    print("Number of columns:", len(rows[0]))
    print("Columns:", header)




import numpy as np

print("\n--- Orbit Frequency Analysis ---")

for orbit_name, filename in files.items():
    file_path = DATA_DIR / filename
    data = np.loadtxt(file_path, delimiter=",", skiprows=1)

    if orbit_name == "DRO":
        frequencies = data[:, 7]
    else:
        frequencies = np.concatenate([data[:, 7], data[:, 8]])

    print(f"\n{orbit_name}")
    print("Minimum frequency:", np.min(frequencies))
    print("Maximum frequency:", np.max(frequencies))
    print("Average frequency:", np.mean(frequencies))
