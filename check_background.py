import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("data/combined_dataset.csv")
base = [c for c in df.columns if c.endswith("_AVG")]

print("Average current per line, every file:")
print(df.groupby("source_file")[["I1_rms_AVG", "I2_rms_AVG", "I3_rms_AVG"]]
      .mean().round(2).to_string())

# Line-independent features: sort the three currents so the line does not matter
cur = np.sort(df[["I1_rms_AVG", "I2_rms_AVG", "I3_rms_AVG"]].values, axis=1)[:, ::-1]
df["I_max"], df["I_mid"], df["I_min"] = cur.T
df["IH5_sum"] = df[["I1_H5_AVG", "I2_H5_AVG", "I3_H5_AVG"]].sum(axis=1)
df["IH7_sum"] = df[["I1_H7_AVG", "I2_H7_AVG", "I3_H7_AVG"]].sum(axis=1)

def split(d):
    tr, te = [], []
    for label, g in d.groupby("label"):
        files = list(dict.fromkeys(g["source_file"]))
        if len(files) > 1:
            tr.append(g[g["source_file"] != files[-1]])
            te.append(g[g["source_file"] == files[-1]])
        else:
            cut = int(len(g) * 0.8)
            tr.append(g.iloc[:cut]); te.append(g.iloc[cut:])
    return pd.concat(tr), pd.concat(te)

train_df, test_df = split(df)

sets = {
    "All 24 features (before)": base,
    "Without Line 2 columns": [c for c in base if not c.startswith(("U2", "I2"))],
    "Line-independent currents + power + PF + harmonics":
        ["I_max", "I_mid", "I_min", "P_sum_AVG", "PF_sum_AVG", "IH5_sum", "IH7_sum"],
    "Line-independent, without middle current":
        ["I_max", "I_min", "P_sum_AVG", "PF_sum_AVG", "IH5_sum", "IH7_sum"],
}

print("\nAccuracy on unseen sessions:")
for name, cols in sets.items():
    m = RandomForestClassifier(n_estimators=100, random_state=42)
    m.fit(train_df[cols], train_df["label"])
    acc = accuracy_score(test_df["label"], m.predict(test_df[cols]))
    print(f"{acc:.2%}  <- {name}")