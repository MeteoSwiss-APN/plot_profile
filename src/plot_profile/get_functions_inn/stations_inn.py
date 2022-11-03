"""Purpose: Define stations and their attributes.

Author: Tobia Lezuo
Based on: plot_porfile/src/plot_profile/utils/stations.py from Stephanie Westerhuis; Stations.csv by Antonia Fritz

Date: 28.10.2022
"""

# Third-party
import pandas as pd

sdfi = pd.DataFrame(
    # variables
    columns=[
        "kols",  # Kolsass ibox
        "weer",  # Weerberg ibox
    ],
    # attributes
    index=[
        "short_name",
        "long_name",
        "lat",
        "lon",
        "elevation",  # it's not called "height", neither "altitude"
    ],
)

# Kolsass ibox
sdfi["kols"].short_name = "kols"
sdfi["kols"].long_name = "Kolsass"
sdfi["kols"].lat = 47.305
sdfi["kols"].lon = 11.622
sdfi["kols"].elevation = 547

# Weerberg ibox
sdfi["kols"].short_name = "weer"
sdfi["kols"].long_name = "Weerberg"
sdfi["kols"].lat = 47.299
sdfi["kols"].lon = 11.672
sdfi["kols"].elevation =  930 
