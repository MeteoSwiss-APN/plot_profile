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
        "altitude",
        "cbh",
        "clc",
        "clct",
        "clcl",
        "ddt_t_lw",
        "ddt_t_sw",
        "dewp_temp",
        "hor_vis",
        "press",
        "qc",
        "qc_dia",
        "qi_dia",
        "qv",
        "qv_dia",
        "rel_hum",
        "lw_down",
        "lw_up",
        "sw_down",
        "sw_up",
        "temp",
        "2m_temp",
        "tqv",
        "ver_vis",
        "wind_dir",
        "wind_vel",
    ],
    # attributes
    index=[
        # mandatory entries
        "long_name",
        "short_name",
        "unit",
        # general
        "icon_name",
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
vdf.loc["icon_name"] = None
vdf.loc["min_value"][:] = None
vdf.loc["max_value"][:] = None
vdf.loc["dwh_id"][:] = None
vdf.loc["color"] = "black"
vdf.loc["marker"][:] = "o"
vdf.loc["linestyle"] = "solid"
vdf.loc["colormap"] = sns.color_palette("viridis", as_cmap=True)
vdf.loc["mult"][:] = 1
vdf.loc["plus"][:] = 0
vdf.loc["avg"][:] = False


# fill variable dataframe with specific values
##############################################

# altitude
vdf["altitude"].short_name = "altitude"
vdf["altitude"].long_name = "Altitude"
vdf["altitude"].unit = "m asl"
vdf["altitude"].min_value = 0
vdf["altitude"].max_value = 5000
vdf["altitude"].dwh_id = {"rs": "742"}

# cloud base height: cbh
vdf["cbh"].short_name = "cbh"
vdf["cbh"].long_name = "Cloud base height"
vdf["cbh"].unit = "m"
vdf["cbh"].min_value = 0
vdf["cbh"].max_value = 2000
vdf["cbh"].mult = 0.3048
vdf["cbh"].dwh_id = {"2m": "1541"}

# cloud cover: clc
vdf["clc"].short_name = "clc"
vdf["clc"].icon_name = "clc"
vdf["clc"].long_name = "Cloud cover"
vdf["clc"].unit = ""
vdf["clc"].min_value = -0.05
vdf["clc"].max_value = 1.05
vdf["clc"].color = "yellowgreen"
vdf["clc"].colormap = "bone"

# cloud cover: clcl
vdf["clcl"].short_name = "clcl"
vdf["clcl"].icon_name = "CLCL"
vdf["clcl"].long_name = "Low cloud cover"
vdf["clcl"].unit = "%"
vdf["clcl"].min_value = -0.05
vdf["clcl"].max_value = 1.05

# cloud cover: clct
vdf["clct"].short_name = "clct"
vdf["clct"].icon_name = "CLCT"  # "clct"
vdf["clct"].long_name = "Total cloud cover"
vdf["clct"].unit = ""
vdf["clct"].min_value = -0.05
vdf["clct"].max_value = 1.05

# temperature tendency due to longwave radiative heating
#  ddt_t_lw
vdf["ddt_t_lw"].short_name = "ddt_t_lw"
# vdf["ddt_t_lw"].icon_name = "THHR_RAD"
# TODO: various names from different configurations
vdf["ddt_t_lw"].icon_name = "ddt_temp_radlw"
vdf["ddt_t_lw"].long_name = "T-tend LW radiation"
vdf["ddt_t_lw"].unit = "K/h"
vdf["ddt_t_lw"].mult = 3600
vdf["ddt_t_lw"].min_value = -3.0
vdf["ddt_t_lw"].max_value = 3.0
vdf["ddt_t_lw"].color = "seagreen"
vdf["ddt_t_lw"].colormap = sns.color_palette("vlag", as_cmap=True)

# temperature tendency due to shortwave radiative heating:
#  ddt_t_sw
vdf["ddt_t_sw"].short_name = "ddt_t_sw"
# vdf["ddt_t_sw"].icon_name = "SOHR_RAD"
# TODO: various names from different configurations
vdf["ddt_t_sw"].icon_name = "ddt_temp_radsw"
vdf["ddt_t_sw"].long_name = "T-tend SW radiation"
vdf["ddt_t_sw"].unit = "K/h"
vdf["ddt_t_sw"].mult = 3600
vdf["ddt_t_sw"].min_value = -3.0
vdf["ddt_t_sw"].max_value = 3.0
vdf["ddt_t_sw"].color = "goldenrod"
vdf["ddt_t_sw"].colormap = sns.light_palette("goldenrod", as_cmap=True)

# dewpoint temperature: dewp_temp
vdf["dewp_temp"].short_name = "dewp_temp"
vdf["dewp_temp"].long_name = "Dew point temperature"
vdf["dewp_temp"].unit = "°C"
vdf["dewp_temp"].min_value = -5
vdf["dewp_temp"].max_value = 15
vdf["dewp_temp"].dwh_id = {"rs": "747", "2m": "194"}

# horizontal visiblity: hor_vis
vdf["hor_vis"].short_name = "hor_vis"
vdf["hor_vis"].long_name = "Horizontal visibility"
vdf["hor_vis"].unit = "m"
vdf["hor_vis"].min_value = 0
vdf["hor_vis"].max_value = 5000
vdf["hor_vis"].dwh_id = {"2m": "1547"}

# pressure: press
vdf["press"].short_name = "press"
vdf["press"].long_name = "Pressure"
vdf["press"].unit = "hPa"
vdf["press"].short_name = "press"
vdf["press"].dwh_id = {"rs": "744"}


# cloud water: qc
vdf["qc"].short_name = "qc"
vdf["qc"].icon_name = "QC"
vdf["qc"].long_name = "Cloud water"
vdf["qc"].unit = "g/kg"
vdf["qc"].min_value = -0.01
vdf["qc"].max_value = 0.07
vdf["qc"].color = "darkblue"
vdf["qc"].colormap = "YlGn"
vdf["qc"].mult = 1000

# diagnostic cloud water: qc_dia
vdf["qc_dia"].short_name = "qc_dia"
vdf["qc_dia"].icon_name = "tot_qc_dia"
vdf["qc_dia"].long_name = "Diagnostic cloud water"
vdf["qc_dia"].unit = "g/kg"
vdf["qc_dia"].min_value = -0.01
vdf["qc_dia"].max_value = 0.07
vdf["qc_dia"].color = "darkblue"
vdf["qc_dia"].mult = 1000

# diagnostic cloud ice: qi_dia
vdf["qi_dia"].short_name = "qi_dia"
vdf["qi_dia"].icon_name = "tot_qi_dia"
vdf["qi_dia"].long_name = "Diagnostic cloud ice"
vdf["qi_dia"].unit = "g/kg"
vdf["qi_dia"].min_value = -0.01
vdf["qi_dia"].max_value = 0.07
vdf["qi_dia"].color = "darkblue"
vdf["qi_dia"].mult = 1000

# specific humidity: qv
vdf["qv"].short_name = "qv"
vdf["qv"].icon_name = "QV"
vdf["qv"].long_name = "Specific humidity"
vdf["qv"].unit = "g/kg"
vdf["qv"].min_value = 0
vdf["qv"].max_value = 6
vdf["qv"].color = "skyblue"
vdf["qv"].colormap = "PuBu"
vdf["qv"].mult = 1000

# diagnostic humidity: qv_dia
vdf["qv_dia"].short_name = "qv_dia"
vdf["qv_dia"].icon_name = "tot_qv_dia"
vdf["qv_dia"].long_name = "Diagnostic humidity"
vdf["qv_dia"].unit = "g/kg"
vdf["qv_dia"].min_value = -0.01
vdf["qv_dia"].max_value = 0.07
vdf["qv_dia"].color = "darkblue"
vdf["qv_dia"].mult = 1000

# relative humidity: rel_hum
vdf["rel_hum"].short_name = "rel_hum"
vdf["rel_hum"].long_name = "Relative humidity"
vdf["rel_hum"].unit = "%"
vdf["rel_hum"].min_value = 0
vdf["rel_hum"].max_value = 100
vdf["rel_hum"].dwh_id = {
    "rs": "746",
    "2m_tower": "3698",
    "10m_tower": "4953",
    "30m_tower": "4961",
}

# radiation: longwave downward
vdf["lw_down"].short_name = "lw_down"
vdf["lw_down"].long_name = "Downward LW rad"
vdf["lw_down"].unit = "W/m2"
vdf["lw_down"].icon_name = "ATHD_S"
vdf["lw_down"].avg = True
vdf["lw_down"].dwh_id = {"2m": "175", "2m_tower": "3762"}

# radiation: longwave upward
vdf["lw_up"].short_name = "lw_up"
vdf["lw_up"].long_name = "Upward LW rad"
vdf["lw_up"].unit = "W/m2"
vdf["lw_up"].dwh_id = {
    "2m": "1531",
    "2m_tower": "5118",  # no data yet in DWH
    "30m_tower": "5181",  # no data yet in DWH
}

# radiation: shortwave downward
vdf["sw_down"].short_name = "sw_down"
vdf["sw_down"].long_name = "Downward SW rad"
vdf["sw_down"].unit = "W/m2"
vdf["sw_down"].dwh_id = {"2m": "96", "2m_tower": "3873"}
vdf["sw_down"].icon_name = "asod_s"  # "GLOB"
vdf["sw_down"].avg = True


# radiation: shortwave upward ("reflected")
vdf["sw_up"].short_name = "sw_up"
vdf["sw_up"].long_name = "Upward SW rad"
vdf["sw_up"].unit = "W/m2"
vdf["sw_up"].dwh_id = {"2m": "1871", "2m_tower": "4995"}

# temperature: temp
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
vdf["temp"].dwh_id = {
    "rs": "745",
    "2m": "91",
    "mwr": "3147",
    "5cm": "92",
    "2m_tower": "3702",
    "10m_tower": "4949",
    "30m_tower": "4957",
}

# 2m temperature: 2m_temp
vdf["2m_temp"].short_name = "2m_temp"
vdf["2m_temp"].icon_name = "T_2M"
vdf["2m_temp"].long_name = "2m Temperature"
vdf["2m_temp"].unit = "°C"
vdf["2m_temp"].min_value = -3.0  # 275
vdf["2m_temp"].max_value = 5  # 287
vdf["2m_temp"].color = "orangered"
vdf["2m_temp"].marker = "o"
vdf["2m_temp"].linestyle = "-"
vdf["2m_temp"].mult = 1
vdf["2m_temp"].plus = -273
vdf["2m_temp"].avg = False

# total water vapour: tqv
vdf["tqv"].short_name = "tqv"
vdf["tqv"].icon_name = "TQV"
vdf["tqv"].long_name = "Total water vapour"
vdf["tqv"].unit = "kg/m2"
vdf["tqv"].dwh_id = {"2m": "2537"}

# vertical visibility: ver_vis
vdf["ver_vis"].short_name = "ver_vis"
vdf["ver_vis"].long_name = "Vertical visibility"
vdf["ver_vis"].unit = "m"
vdf["ver_vis"].min_value = 0
vdf["ver_vis"].max_value = 1000
vdf["ver_vis"].mult = 0.3048
vdf["ver_vis"].dwh_id = {"2m": "6199"}

# wind direction: wind_dir
vdf["wind_dir"].short_name = "wind_dir"
vdf["wind_dir"].long_name = "Wind direction"
vdf["wind_dir"].unit = "°"
vdf["wind_dir"].min_value = 0
vdf["wind_dir"].max_value = 360
vdf["wind_dir"].dwh_id = {"rs": "743"}

# wind velocity: wind_vel
vdf["wind_vel"].short_name = "wind_vel"
vdf["wind_vel"].long_name = "Wind velocity"
vdf["wind_vel"].unit = "m/s"
vdf["wind_vel"].min_value = 0
vdf["wind_vel"].max_value = 30
vdf["wind_vel"].dwh_id = {"rs": "748"}

# !!! if adding new variable: don't forget to add at the top and in cli-file!!!

if __name__ == "__main__":
    print(vdf)
