import pandas as pd
df = pd.read_csv("data/combined_dataset.csv")
cols = ["I1_rms_AVG","I2_rms_AVG","I3_rms_AVG","P_sum_AVG","PF_sum_AVG"]
labels = ["LED+Oscilloscope","LED","Oscilloscope"]
d = df[df["label"].isin(labels)]
print(d.groupby(["label","source_file"])[cols].mean().round(2).to_string())