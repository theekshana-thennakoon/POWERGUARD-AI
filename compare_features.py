import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("data/combined_dataset.csv")

# Part 1: average current on each line, per file, for labels with 2+ sessions
multi = [l for l, g in df.groupby("label") if g["source_file"].nunique() > 1]
print("Average current per line (check if the active line changes between sessions):")
print(df[df["label"].isin(multi)]
      .groupby(["label", "source_file"])[["I1_rms_AVG", "I2_rms_AVG", "I3_rms_AVG"]]
      .mean().round(3).to_string())

# Part 2: compare feature sets using the same "last session = test" rule
def split(df):
    tr, te = [], []
    for label, g in df.groupby("label"):
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
    "All 24 features": [c for c in df.columns if c.endswith("_AVG")],
    "Device-only (current, power, PF, current harmonics)": [
        "I1_rms_AVG", "I2_rms_AVG", "I3_rms_AVG", "P_sum_AVG", "PF_sum_AVG",
        "I1_H5_AVG", "I1_H7_AVG", "I2_H5_AVG", "I2_H7_AVG", "I3_H5_AVG", "I3_H7_AVG"],
    "Current + power + PF only": [
        "I1_rms_AVG", "I2_rms_AVG", "I3_rms_AVG", "P_sum_AVG", "PF_sum_AVG"],
}

print("\nAccuracy on unseen sessions:")
for name, cols in sets.items():
    m = RandomForestClassifier(n_estimators=100, random_state=42)
    m.fit(train_df[cols], train_df["label"])
    acc = accuracy_score(test_df["label"], m.predict(test_df[cols]))
    print(f"{acc:.2%}  <- {name}")