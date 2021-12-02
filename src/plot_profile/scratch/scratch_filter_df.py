"""Script to filter a dataframe w/ conditions applied on index column."""
# Standard library
import pickle

# import pandas as pd
# import numpy as np
f1 = open("/scratch/swester/tmp/test_dataframe.pckl", "rb")
df = pickle.load(f1)
lower_threshold, upper_threshold = 1000, 1500
df = df[df.index <= upper_threshold]
df = df[df.index >= lower_threshold]
print(df)
# CAUTION: df = df[(df.index >= lower_threshold) and (df.index <= upper_threshold)] gives an error!
f1.close()
