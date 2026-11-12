import pandas as pd
import os, re, glob

data_folder = "data"

# File prefix -> label
LABELS = {
    "D1": "LED", "D2": "Heater", "D3": "Iron", "D4": "Laptop", "D5": "UPS",
    "D6": "Oscilloscope", "D7": "AirCompressor", "D8": "3PhaseMotor",
    "D9": "1PhaseMotor", "D10": "Transformer", "D11": "AC",
    "P01": "LED+UPS", "P02": "LED+AirCompressor", "P03": "LED+Laptop",
    "P04": "UPS+Laptop", "P05": "UPS+Oscilloscope", "P06": "Laptop+Oscilloscope",
    "P07": "3PhaseMotor+LED", "P08": "1PhaseMotor+LED", "P09": "AC+LED",
    "P10": "Transformer+LED", "P11": "Transformer+AC", "P12": "1PhaseMotor+AC",
    "P13": "UPS+AC", "P14": "LED+Oscilloscope", "P15": "Laptop+AC",
}

# First recordings made with the lab AC running in the background (skipped)
EXCLUDE = {
    "D1_Light_solo.csv", "D2_Heater_solo.csv", "D3_Iron_solo.csv",
    "D4_laptop_solo.csv", "D5_UPS_solo.csv", "D6_Osil_solo.csv",
    "D7_Air_solo.csv", "P01_LED_UPS.csv", "P02_LED_Air.csv",
    "P03_LED_Laptop.csv", "P04_UPS_Laptop.csv", "P05_UPS_Osil.csv",
    "P06_Laptop_Osil.csv",
}

keep_cols = [
    "Date", "Time",
    "U1_rms_AVG", "I1_rms_AVG", "U2_rms_AVG", "I2_rms_AVG", "U3_rms_AVG", "I3_rms_AVG",
    "Freq_AVG", "P_sum_AVG", "PF_sum_AVG",
    "U1_thd-f_AVG", "U2_thd-f_AVG", "U3_thd-f_AVG",
    "U1_H5_AVG", "U1_H7_AVG", "U2_H5_AVG", "U2_H7_AVG", "U3_H5_AVG", "U3_H7_AVG",
    "I1_H5_AVG", "I1_H7_AVG", "I2_H5_AVG", "I2_H7_AVG", "I3_H5_AVG", "I3_H7_AVG",
]

files = []
for path in glob.glob(os.path.join(data_folder, "*.csv")):
    name = os.path.basename(path)
    m = re.match(r"^(D\d+|P\d+)_.*?(?:_s(\d+))?\.csv$", name)
    if not m or m.group(1) not in LABELS:
        continue                      # ignores combined_dataset, baseline_stats, history, background files
    session = int(m.group(2)) if m.group(2) else 1
    files.append((LABELS[m.group(1)], session, name))
files.sort()

all_data = []
for label, session, name in files:
    if name.lower() in {x.lower() for x in EXCLUDE}:
        print(f"Excluded (AC background): {name}")
        continue
    df = pd.read_csv(os.path.join(data_folder, name))
    d = df[keep_cols].copy()
    d["label"] = label
    d["source_file"] = name
    all_data.append(d)

    i2 = d["I2_rms_AVG"].mean()
    parts = label.split("+")
    warn = ""
    if i2 > 1.0 and "AC" not in parts and "3PhaseMotor" not in parts:
        warn = "   <-- CHECK: Line 2 current high, AC may have been on"
    print(f"Loaded {name:28s} {len(d):4d} rows  {label:20s} I2={i2:.2f} A{warn}")

combined = pd.concat(all_data, ignore_index=True)
print("\nCombined shape:", combined.shape)
print("\nRows per label:")
print(combined["label"].value_counts().to_string())
print("\nSessions per label:")
print(combined.groupby("label")["source_file"].nunique().sort_values().to_string())

combined.to_csv("data/combined_dataset.csv", index=False)
print("\nSaved data/combined_dataset.csv")