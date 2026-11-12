import pandas as pd
import numpy as np

# Load your updated combined dataset (23 classes, all 3 lines)
df = pd.read_csv("data/combined_dataset.csv")

feature_cols = [
    "U1_rms_AVG", "I1_rms_AVG",
    "U2_rms_AVG", "I2_rms_AVG",
    "U3_rms_AVG", "I3_rms_AVG",
    "Freq_AVG", "P_sum_AVG", "PF_sum_AVG",
    "U1_thd-f_AVG", "U2_thd-f_AVG", "U3_thd-f_AVG",
    "U1_H5_AVG", "U1_H7_AVG",
    "U2_H5_AVG", "U2_H7_AVG",
    "U3_H5_AVG", "U3_H7_AVG",
    "I1_H5_AVG", "I1_H7_AVG",
    "I2_H5_AVG", "I2_H7_AVG",
    "I3_H5_AVG", "I3_H7_AVG",
]

# Step 1: Calculate baseline mean/std for each device
baseline_stats = df.groupby("label")[feature_cols].agg(["mean", "std"])
print(baseline_stats)
baseline_stats.to_csv("data/baseline_stats.csv")
print("\nSaved baseline stats to data/baseline_stats.csv")


# Step 2: Deviation-checking function (same logic as before)
def check_deviation(new_reading, device_label, baseline_stats, feature_cols, threshold=3):
    alerts = []
    for feature in feature_cols:
        mean = baseline_stats.loc[device_label, (feature, "mean")]
        std = baseline_stats.loc[device_label, (feature, "std")]
        value = new_reading[feature]
        if std == 0 or pd.isna(std):
            continue
        z_score = (value - mean) / std
        if abs(z_score) > threshold:
            alerts.append({
                "feature": feature,
                "value": round(value, 3),
                "expected_mean": round(mean, 3),
                "z_score": round(z_score, 2)
            })
    return alerts


# Step 3: Validate on real healthy data (skip startup rows)
baseline_stats_reload = pd.read_csv("data/baseline_stats.csv", header=[0, 1], index_col=0)

test_row = df[df["label"] == "1PhaseMotor"].iloc[10]  # steady-state row
alerts = check_deviation(test_row, "1PhaseMotor", baseline_stats_reload, feature_cols)

print("\n--- Healthy Data Test (1PhaseMotor) ---")
if len(alerts) >= 2:
    print("⚠️ Deviations detected:")
    for a in alerts:
        print(f"  - {a['feature']}: value={a['value']}, expected~{a['expected_mean']}, z-score={a['z_score']}")
else:
    print("✅ Reading looks normal (no significant deviation)")


# Step 4: Validate with simulated fault
print("\n--- Simulated Fault Test (1PhaseMotor) ---")
simulated_fault = df[df["label"] == "1PhaseMotor"].iloc[10].copy()
simulated_fault["I1_rms_AVG"] = simulated_fault["I1_rms_AVG"] * 1.4
simulated_fault["PF_sum_AVG"] = simulated_fault["PF_sum_AVG"] * 0.3

alerts = check_deviation(simulated_fault, "1PhaseMotor", baseline_stats_reload, feature_cols)

if len(alerts) >= 2:
    print("⚠️ Deviations detected (simulated fault correctly caught):")
    for a in alerts:
        print(f"  - {a['feature']}: value={a['value']}, expected~{a['expected_mean']}, z-score={a['z_score']}")
else:
    print("❌ No deviation detected — simulated fault was missed!")

# ---- Debug: check actual z-scores regardless of threshold ----
print("\n--- Debug: raw z-scores for simulated changes ---")
for feature in ["I1_rms_AVG", "PF_sum_AVG"]:
    mean = baseline_stats_reload.loc["1PhaseMotor", (feature, "mean")]
    std = baseline_stats_reload.loc["1PhaseMotor", (feature, "std")]
    value = simulated_fault[feature]
    z = (value - mean) / std if std > 0 else 0
    print(f"{feature}: value={value:.4f}, mean={mean:.4f}, std={std:.4f}, z-score={z:.2f}")