#!/usr/bin/env python3

from http import HTTPStatus
import pandas as pd
import requests

resp = requests.get("https://www.levels.fyi/js/salaryData.json")
print(f"Response: {resp.status_code}")
if resp.status_code != HTTPStatus.OK:
    # AFAIK this endpoint only responds with HTTP 200 and not any other 2xx
    # status for successful queries
    raise RuntimeError(f"Possible failure in fetching salaryData.json: {resp.status_code}")

data = resp.json()
df = pd.DataFrame(data)
df = df[ \
  df["location"].str.contains(", Canada$") & \
  (df["title"] == "Software Engineer") & \
  (pd.to_numeric(df["yearsofexperience"]) >= 7) & \
  (pd.to_numeric(df["yearsofexperience"]) <= 8) \
]

print(f"Num samples: {df.shape[0]}")
# All monetary quantities are stored in USD in levels.fyi data.
print(f"Median: {pd.DataFrame.median(pd.to_numeric(df.totalyearlycompensation))} k USD")
print(f"Standard deviation: {pd.DataFrame.std(pd.to_numeric(df.totalyearlycompensation))} k USD")

kUsdToCad = 1.28

p90 = pd.to_numeric(df.totalyearlycompensation).quantile(q = 0.9)
print(f"90-th percentile: {p90} k USD")
print(f"90-th percentile: {p90 * kUsdToCad} k CAD")

p75 = pd.to_numeric(df.totalyearlycompensation).quantile(q = 0.75)
print(f"75-th percentile: {p75 * kUsdToCad} k CAD")
