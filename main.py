import pandas as pd
from datetime import time
import numpy as np

from helpers.utils import *
from helpers.formulas import *
from helpers.data_cleaning import *
from helpers.data_preprocessing import *


# Read the CSV
df = pd.read_csv("./data/EURUSD_M15-10000.csv")

# Check for required columns
df_check(df, required_columns=["Time", "Open", "High", "Low", "Close"])

# Convert the 'Time' column to datetime and rename it to 'timestamp'
df.rename(columns={"Time": "timestamp"}, inplace=True)
df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

# Extract the time part into a separate column
df["Time"] = df["timestamp"].dt.time

# Define range for the session (start and end time)
start_time = time(2, 0, 0)
end_time = time(5, 0, 0)
filtered = df[df["Time"].between(start_time, end_time)]

# Get the most frequent value in the filtered "Time" column
most_frequent_value = filtered["Time"].mode()[0]  # mode() returns the most common value
print("Most frequent time:", most_frequent_value)
