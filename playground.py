import pandas as pd
import numpy as np

from helpers.utils import *

# input_file = "EURUSD_M15.csv"
# fix_csv_format(input_file, output_file="./data/EURUSD_M15.csv")

file = pd.read_csv(
    "./data/EURUSD_M15.csv",
    header=None,
    names=["Time", "Open", "High", "Low", "Close", "Volume"],
)

file.to_csv("EURUSD_M15.csv", index=False)
