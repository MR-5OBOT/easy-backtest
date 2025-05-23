# import pandas as pd
# import numpy as np
#
# from helpers.utils import *
#
# # input_file = "EURUSD_M15.csv"
# # fix_csv_format(input_file, output_file="./data/EURUSD_M15.csv")
#
# file = pd.read_csv(
#     "./data/EURUSD_M15.csv",
#     header=None,
#     names=["Time", "Open", "High", "Low", "Close", "Volume"],
# )
#
# file.to_csv("EURUSD_M15.csv", index=False)

import pandas as pd
from datetime import time

df = pd.read_csv("./data/EURUSD_M15-10000.csv")


def analyze_session_highs_lows(
    df, start_time="02:00", end_time="05:00", price_col_high="High", price_col_low="Low"
):
    """
    Analyze OHLC data to find the most frequent hour for highs and lows in a custom session.

    Parameters:
    - df: DataFrame with columns [Time, Open, High, Low, Close, Volume]
    - start_time: Session start time (e.g., "02:00")
    - end_time: Session end time (e.g., "05:00")
    - price_col_high: Column name for high prices (default: "High")
    - price_col_low: Column name for low prices (default: "Low")

    Returns:
    - Most frequent hour for highs and lows
    """
    # Ensure Time is in datetime format
    df = df.copy()  # Avoid modifying original DataFrame
    df["Time"] = pd.to_datetime(df["Time"], errors="coerce")

    # Validate inputs
    if df["Time"].isna().any():
        raise ValueError("Some Time values could not be parsed to datetime.")

    try:
        start = pd.to_datetime(start_time).time()
        end = pd.to_datetime(end_time).time()
    except ValueError:
        raise ValueError(
            "start_time and end_time must be in HH:MM format (e.g., '02:00')."
        )

    # Filter for the custom session
    session_data = df[df["Time"].dt.time.between(start, end)]

    if session_data.empty:
        return "No data found in the specified session time range."

    # Group by date
    daily_sessions = session_data.groupby(session_data["Time"].dt.date)

    # Lists to store hours of highs and lows
    high_hours = []
    low_hours = []

    # Find hour of highest high and lowest low for each day
    for _, group in daily_sessions:
        if not group.empty:
            high_time = group.loc[group[price_col_high].idxmax(), "Time"]
            low_time = group.loc[group[price_col_low].idxmin(), "Time"]
            high_hours.append(high_time.hour)
            low_hours.append(low_time.hour)

    if not high_hours or not low_hours:
        return "No valid highs or lows found in the session data."

    # Find most frequent hour
    high_hour_freq = pd.Series(high_hours).value_counts().idxmax()
    low_hour_freq = pd.Series(low_hours).value_counts().idxmax()

    # Format output
    return {
        "most_frequent_high_hour": f"{high_hour_freq}:00",
        "most_frequent_low_hour": f"{low_hour_freq}:00",
    }


# Analyze London session (02:00–05:00)
result = analyze_session_highs_lows(df, start_time="02:00", end_time="05:00")
print(result)

# Example for another session (e.g., Asian session 00:00–03:00)
result = analyze_session_highs_lows(df, start_time="08:00", end_time="11:00")
print(result)
