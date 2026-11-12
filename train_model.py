import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

df = pd.read_csv("data/combined_dataset.csv")
feature_cols = ["I1_rms_AVG", "I2_rms_AVG", "I3_rms_AVG", "P_sum_AVG", "PF_sum_AVG"]

# Last session of each label is the test set, earlier sessions train.
train_parts, test_parts = [], []
for label, g in df.groupby("label"):
    files = list(dict.fromkeys(g["source_file"]))
    if len(files) > 1:
        train_parts.append(g[g["source_file"] != files[-1]])
        test_parts.append(g[g["source_file"] == files[-1]])
    else:
        cut = int(len(g) * 0.8)
        train_parts.append(g.iloc[:cut])
        test_parts.append(g.iloc[cut:])

train_df, test_df = pd.concat(train_parts), pd.concat(test_parts)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(train_df[feature_cols], train_df["label"])
t = test_df.assign(pred=model.predict(test_df[feature_cols]))

print("Training rows:", len(train_df), " Testing rows:", len(test_df))
print(f"Accuracy on unseen sessions (rows): {accuracy_score(t['label'], t['pred']):.2%}")

rows = []
for f, g in t.groupby("source_file"):
    top = g["pred"].mode()[0]
    rows.append((f, g["label"].iloc[0], top, (g["pred"] == top).mean()))
pf = pd.DataFrame(rows, columns=["file", "true", "predicted", "share"])
print(f"Test files identified correctly: {(pf['true'] == pf['predicted']).mean():.0%}")
print(pf.round(2).to_string(index=False))
print(classification_report(t["label"], t["pred"], zero_division=0))

# Final model uses ALL clean data, for the dashboard
final = RandomForestClassifier(n_estimators=100, random_state=42)
final.fit(df[feature_cols], df["label"])
joblib.dump(final, "device_model.pkl")
print("Saved device_model.pkl (trained on all clean data)")