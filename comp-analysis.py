#!/usr/bin/env python3

from http import HTTPStatus
import pandas as pd
import requests

resp = requests.get("https://www.levels.fyi/js/salaryData.json")
print("Response code: ", resp.status_code)
if resp.status_code != HTTPStatus.OK:
    raise RuntimeError("Failed to fetch data!")

data = resp.json()
df = pd.DataFrame(data)
df = df[ \
  df["location"].str.contains(", Canada$") & \
  (df["title"] == "Software Engineer") & \
  (pd.to_numeric(df["yearsofexperience"]) >= 7) & \
  (pd.to_numeric(df["yearsofexperience"]) <= 8) \
]

print("Num samples:", df.shape[0])
# All monetary quantities are stored in USD in levels.fyi data.
print("Median:", pd.DataFrame.median(pd.to_numeric(df.totalyearlycompensation)), "k USD")
print("Standard deviation:", pd.DataFrame.std(pd.to_numeric(df.totalyearlycompensation)), "k USD")
p90 = pd.to_numeric(df.totalyearlycompensation).quantile(q = 0.9)
print("90-th percentile:", p90, "k USD")
kUsdToCad = 1.28
print("90-th percentile:", p90 * kUsdToCad, "k CAD")
