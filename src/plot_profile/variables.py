"""Purpose: Define variables and their attributes.

Author: Stephanie Westerhuis

Date: 11/29/2021
"""
# Third-party
import pandas as pd
from numpy.core.fromnumeric import _var_dispatcher

vdf = pd.DataFrame(
    # variables
    columns=[
        "temp",
        "qc",
        "qv",
    ],
    # attributes
    index=[
        "icon_name",
        "long_name",
        "short_name",
        "unit",
        "min_value",
        "max_value",
        "dwh_id",
        # line appearance
        "color",
        "marker",
        "linestyle",
        # value transformations
        "mult",
        "plus",
        "avg",
    ],
)

# set default values for certain attributes
vdf.loc["color"] = "black"
vdf.loc["marker"][:] = "o"
vdf.loc["linestyle"] = "solid"
vdf.loc["mult"][:] = 1
vdf.loc["plus"][:] = 0
vdf.loc["avg"][:] = False


# fill variable dataframe with specific values

# temp
vdf["temp"].short_name = "temp"
vdf["temp"].icon_name = "T"
vdf["temp"].long_name = "Temperature"
vdf["temp"].unit = "K"
vdf["temp"].min_value = 275
vdf["temp"].max_value = 287
vdf["temp"].dwh_id = 999
vdf["temp"].color = "red"
vdf["temp"].marker = "o"
vdf["temp"].linestyle = "-"
vdf["temp"].mult = 1
vdf["temp"].plus = 0
vdf["temp"].avg = False

# specific humidity
vdf["qv"].short_name = "qv"
vdf["qv"].icon_name = "QV"
vdf["qv"].long_name = "Specific humidity"
vdf["qv"].unit = "g/kg"
vdf["qv"].min_value = 0
vdf["qv"].max_value = 6
vdf["qv"].dwh_id = 999
vdf["qv"].mult = 1000

# cloud water
vdf["qc"].short_name = "qc"
vdf["qc"].icon_name = "QC"
vdf["qc"].long_name = "Cloud water"
vdf["qc"].unit = "g/kg"
vdf["qc"].min_value = 0
vdf["qc"].max_value = 0.05
vdf["qc"].dwh_id = 999
vdf["qc"].mult = 1000
