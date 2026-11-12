import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

df = pd.read_csv("data/combined_dataset.csv")
base = [c for c in df.columns if c.endswith("_AVG")]

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
    "All 24 features": base,
    "Device-only (no voltage, no frequency)": [c for c in base if not c.startswith("U") and c != "Freq_AVG"],
    "Current + power + PF only": ["I1_rms_AVG", "I2_rms_AVG", "I3_rms_AVG", "P_sum_AVG", "PF_sum_AVG"],
}

results = {}
for name, cols in sets.items():
    m = RandomForestClassifier(n_estimators=100, random_state=42)
    m.fit(train_df[cols], train_df["label"])
    t = test_df.assign(pred=m.predict(test_df[cols]))
    rows = []
    for f, g in t.groupby("source_file"):
        top = g["pred"].mode()[0]
        rows.append((f, g["label"].iloc[0], top, (g["pred"] == top).mean()))
    pf = pd.DataFrame(rows, columns=["file", "true", "predicted", "share"])
    row_acc = accuracy_score(t["label"], t["pred"])
    file_acc = (pf["true"] == pf["predicted"]).mean()
    results[name] = (row_acc, pf)
    print(f"{row_acc:.2%} of rows | {file_acc:.0%} of test files right  <- {name}")

best = max(results, key=lambda k: results[k][0])
print("\nPer-file result for:", best)
print(results[best][1].round(2).to_string(index=False))