import numpy as np
import pandas as pd

df = pd.read_csv("students_performance.csv")
print(df.head())

subjects = ["math score", "reading score", "writing score"]

mean_val = {}
median_val = {}
mode_val = {}

for sub in subjects:
    mean_val[sub] = round(df[sub].mean(), 2)
    median_val[sub] = round(df[sub].median(), 2)
    mode_val[sub] = round(df[sub].mode()[0], 2)

variance_val = {}
std_val = {}
range_val = {}

for sub in subjects: 
    variance_val[sub] = round(df[sub].var(ddof = 0), 2)
    std_val[sub] = round(df[sub].std(ddof = 0), 2)
    range_val[sub] = round(df[sub].max() - df[sub].min(), 2)

df["total score"] = df[["math score", "reading score", "writing score"]].mean(axis=1)


Q1 = df["total score"].quantile(0.25)
Q3 = df["total score"].quantile(0.75)
IQR = Q3 - Q1


less_than_Q1 = (df["total score"] < Q1).mean() * 100
between_Q1_Q3 = ((df["total score"] >= Q1) & (df["total score"] <= Q3)).mean() * 100
more_than_Q3 = (df["total score"] > Q3).mean() * 100

import zipfile
import joblib
import json

def convert_numpy_types(data):
    if isinstance(data, dict):
        return {k: convert_numpy_types(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_numpy_types(v) for v in data]
    elif isinstance(data, np.generic):
        return data.item()
    else:
        return data

descriptive_stats = ['mean_val', 'median_val', 'mode_val', 'variance_val', 'std_val', 'range_val']
for stat in descriptive_stats:
    with open(stat + '.json', 'w') as f:
        json.dump(convert_numpy_types(eval(stat)), f, ensure_ascii=False, indent=4)

df['total score'].to_csv('total score.csv', index=False)

joblib.dump(Q1, "Q1")
joblib.dump(Q3, "Q3")
joblib.dump(IQR, "IQR")
joblib.dump(less_than_Q1, "less_than_Q1")
joblib.dump(between_Q1_Q3, "between_Q1_Q3")
joblib.dump(more_than_Q3, "more_than_Q3")

notebook_path = 'uncovering_the_secrets.ipynb'

def compress(file_names):
    print("File Paths:")
    print(file_names)
    # Select the compression mode ZIP_DEFLATED for compression
    # or zipfile.ZIP_STORED to just store the file
    compression = zipfile.ZIP_DEFLATED
    # create the zip file first parameter path/name, second mode
    with zipfile.ZipFile("result.zip", mode="w") as zf:
        for file_name in file_names:
            # Add file to the zip file
            # first parameter file to zip, second filename in zip
            zf.write('./' + file_name, file_name, compress_type=compression)

file_names = ['mean_val.json', 'median_val.json', 'mode_val.json',
             'variance_val.json', 'std_val.json', 'range_val.json', 
             'less_than_Q1', 'between_Q1_Q3', 'more_than_Q3',
             'total score.csv', 'Q1', 'Q3', 'IQR', notebook_path]
compress(file_names)