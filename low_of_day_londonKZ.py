import pandas as pd
from datetime import time
import numpy as np

from helpers.utils import *
from helpers.formulas import *
from helpers.data_cleaning import *
from helpers.data_preprocessing import *


# Read the CSV
df = pd.read_csv(
    "./data/EURUSD_H1.csv",
    # header=None,
    # names=["Time", "Open", "High", "Low", "Close"],
)
# print(df.head())

# Check for required columns
df_check(df, required_columns=["timestamp", "Open", "High", "Low", "Close"])

# df.rename(columns={"Time": "timestamp"}, inplace=True)
df["timestamp"] = pd.to_datetime(
    df["timestamp"],
    errors="coerce",
    # format="%Y-%m-%d %H:%M:%S",  # manual format
    # format="%Y-%m-%d %H:%M",  # manual format
)

# If it's already timezone-aware from a different source, you might skip tz_localize
# or convert directly if it's another timezone.
# If your timestamps are NAVIE and already represent New York time,
# you would localize to 'America/New_York' directly.
try:
    df["timestamp"] = df["timestamp"].dt.tz_localize("GMT")
except (
    TypeError
):  # If already timezone-aware (e.g., from a previous tz_localize or tz_convert)
    pass  # It's already localized, or you might want to convert if it's not UTC

# 2. Convert to New York Time
df["timestamp_ny"] = df["timestamp"].dt.tz_convert("America/New_York")

# 3. Extract New York Date and Time (for easier daily grouping and time window checks)
df["date_ny"] = df["timestamp_ny"].dt.date
df["time_ny"] = df["timestamp_ny"].dt.time

# df = df.drop("Volume", axis=1)
# df.to_csv("./data/EURUSD_H1_clean.csv", index=False)
print(df.head())
# print(df.info())
