"""Purpose: Define variables and their attributes.

Author: Stephanie Westerhuis

Date: 11/29/2021
"""
# Third-party
import pandas as pd
import seaborn as sns

vdf = pd.DataFrame(
    # variables
    columns=[
        "temp",
        "qc",
        "qv",
        "clc",
        "ddt_t_rad_lw",
        "ddt_t_rad_sw",
        "qc_dia",
        "qv_dia",
        "qi_dia",
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
        "colormap",
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
vdf.loc["colormap"] = sns.color_palette("viridis", as_cmap=True)
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
vdf["temp"].unit = "°C"
vdf["temp"].min_value = -3.0  # 275
vdf["temp"].max_value = 5  # 287
vdf["temp"].color = "orangered"
vdf["temp"].marker = "o"
vdf["temp"].linestyle = "-"
vdf["temp"].mult = 1
vdf["temp"].plus = -273
vdf["temp"].avg = False
vdf["temp"].dwh_id = {"rs": 745}

# specific humidity
vdf["qv"].short_name = "qv"
vdf["qv"].icon_name = "QV"
vdf["qv"].long_name = "Specific humidity"
vdf["qv"].unit = "g/kg"
vdf["qv"].min_value = 0
vdf["qv"].max_value = 6
vdf["qv"].color = "skyblue"
vdf["qv"].mult = 1000

# cloud water
vdf["qc"].short_name = "qc"
vdf["qc"].icon_name = "QC"
vdf["qc"].long_name = "Cloud water"
vdf["qc"].unit = "g/kg"
vdf["qc"].min_value = -0.01
vdf["qc"].max_value = 0.07
vdf["qc"].color = "darkblue"
vdf["qc"].mult = 1000

# cloud cover
vdf["clc"].short_name = "clc"
vdf["clc"].icon_name = "clc"
vdf["clc"].long_name = "Cloud cover"
vdf["clc"].unit = ""
vdf["clc"].min_value = -0.05
vdf["clc"].max_value = 1.05
vdf["clc"].color = "yellowgreen"

# temperature tendency due to longwave radiative heating
vdf["ddt_t_rad_lw"].short_name = "ddt_t_rad_lw"
# vdf["ddt_t_rad_lw"].icon_name = "THHR_RAD"
vdf["ddt_t_rad_lw"].icon_name = "ddt_temp_radlw"
vdf["ddt_t_rad_lw"].long_name = "T-tend LW radiation"
vdf["ddt_t_rad_lw"].unit = "K/h"
vdf["ddt_t_rad_lw"].mult = 3600
vdf["ddt_t_rad_lw"].min_value = -3.0
vdf["ddt_t_rad_lw"].max_value = 3.0
vdf["ddt_t_rad_lw"].color = "seagreen"
vdf["ddt_t_rad_lw"].colormap = sns.color_palette("vlag", as_cmap=True)

# temperature tendency due to longwave radiative heating
vdf["ddt_t_rad_sw"].short_name = "ddt_t_rad_sw"
# vdf["ddt_t_rad_sw"].icon_name = "SOHR_RAD"
vdf["ddt_t_rad_sw"].icon_name = "ddt_temp_radsw"
vdf["ddt_t_rad_sw"].long_name = "T-tend SW radiation"
vdf["ddt_t_rad_sw"].unit = "K/h"
vdf["ddt_t_rad_sw"].mult = 3600
vdf["ddt_t_rad_sw"].min_value = -3.0
vdf["ddt_t_rad_sw"].max_value = 3.0
vdf["ddt_t_rad_sw"].color = "goldenrod"
vdf["ddt_t_rad_sw"].colormap = sns.light_palette("goldenrod", as_cmap=True)

# tot_qc_dia
vdf["qc_dia"].short_name = "qc_dia"
vdf["qc_dia"].icon_name = "tot_qc_dia"
vdf["qc_dia"].long_name = "Diagnostic cloud water"
vdf["qc_dia"].unit = "g/kg"
vdf["qc_dia"].min_value = -0.01
vdf["qc_dia"].max_value = 0.07
vdf["qc_dia"].color = "darkblue"
vdf["qc_dia"].mult = 1000

# tot_qv_dia
vdf["qv_dia"].short_name = "qv_dia"
vdf["qv_dia"].icon_name = "tot_qv_dia"
vdf["qv_dia"].long_name = "Diagnostic humidity"
vdf["qv_dia"].unit = "g/kg"
vdf["qv_dia"].min_value = -0.01
vdf["qv_dia"].max_value = 0.07
vdf["qv_dia"].color = "darkblue"
vdf["qv_dia"].mult = 1000

# tot_qi_dia
vdf["qi_dia"].short_name = "qi_dia"
vdf["qi_dia"].icon_name = "tot_qi_dia"
vdf["qi_dia"].long_name = "Diagnostic cloud ice"
vdf["qi_dia"].unit = "g/kg"
vdf["qi_dia"].min_value = -0.01
vdf["qi_dia"].max_value = 0.07
vdf["qi_dia"].color = "darkblue"
vdf["qi_dia"].mult = 1000

# if adding new variable: don't forget to add at the top and in cli-file!!!

if __name__ == "__main__":
    print(vdf)
