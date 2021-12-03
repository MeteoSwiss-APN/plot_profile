"""Purpose: Define variables and their attributes.

Author: Stephanie Westerhuis

Date: 11/29/2021
"""
# Third-party
import pandas as pd

vdf = pd.DataFrame(
    # variables
    columns=["temp", "qc", "qv", "clc", "ddt_t_rad_lw", "ddt_t_rad_sw"],
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
vdf.loc["min_value"][:] = None
vdf.loc["max_value"][:] = None
vdf.loc["dwh_id"][:] = None


# fill variable dataframe with specific values

# temp
vdf["temp"].short_name = "temp"
vdf["temp"].icon_name = "T"
vdf["temp"].long_name = "Temperature"
vdf["temp"].unit = "K"
vdf["temp"].min_value = 275
vdf["temp"].max_value = 287
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
vdf["qv"].mult = 1000

# cloud water
vdf["qc"].short_name = "qc"
vdf["qc"].icon_name = "QC"
vdf["qc"].long_name = "Cloud water"
vdf["qc"].unit = "g/kg"
vdf["qc"].min_value = -0.01
vdf["qc"].max_value = 0.07
vdf["qc"].mult = 1000

# cloud cover
vdf["clc"].short_name = "clc"
vdf["clc"].icon_name = "CLC"
vdf["clc"].long_name = "Cloud cover"
vdf["clc"].unit = ""
vdf["clc"].min_value = -0.05
vdf["clc"].max_value = 1.05

# temperature tendency due to longwave radiative heating
vdf["ddt_t_rad_lw"].short_name = "ddt_t_rad_lw"
vdf["ddt_t_rad_lw"].icon_name = "THHR_RAD"
vdf["ddt_t_rad_lw"].long_name = "T-tend LW radiation"
vdf["ddt_t_rad_lw"].unit = "K/s"

# temperature tendency due to longwave radiative heating
vdf["ddt_t_rad_sw"].short_name = "ddt_t_rad_sw"
vdf["ddt_t_rad_sw"].icon_name = "SOHR_RAD"
vdf["ddt_t_rad_sw"].long_name = "T-tend SW radiation"
vdf["ddt_t_rad_sw"].unit = "K/s"


if __name__ == "__main__":
    print(vdf)
