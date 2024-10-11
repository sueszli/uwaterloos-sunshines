from pathlib import Path
import csv
import numpy as np
import pandas as pd

datapath = Path("__file__").parent / 'data' / 'sunshines-final.csv'
df = pd.read_csv(datapath)
print(df.head())


# use data wrangler to find the interesting bits
