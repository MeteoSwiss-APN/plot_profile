from sys import path_hooks
import glob2
import os.path as path
import pandas as pd
from plot_profile.utils.stations import sdf


path_ACINN = '/users/tlezuo/data/stations/ACINNiBox/raw'
# name="Weerberg"
name = sdf['weer'].long_name
print(name)
file_ACINN = glob2.glob(path.join(path_ACINN, f'*{name}*', 'data.csv'))
print(file_ACINN)

if len(file_ACINN) == 0:
    raise ValueError(f'No ACINN data found for {station}')

data = pd.read_csv(file_ACINN[0], delimiter=';', skiprows=1)
print(data)