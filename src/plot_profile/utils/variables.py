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
        "clcl",
        "clcm",
        "clch",
        "clct",
        "ddt_t_lw",
        "ddt_t_sw",
        "dewp_temp",
        "2m_dewp_temp",
        "grad_temp",
        "hor_vis",
        "press",
        "qc",
        "qc_dia",
        "qi_dia",
        "qv",
        "2m_qv",
        "qv_dia",
        "rel_hum",
        "lw_down",
        "lw_up",
        "lw_net",
        "sw_down",
        "sw_up",
        "sw_net",
        "temp",
        "2m_temp",
        "tke",
        "tqv",
        "tqc",
        "tqc_dia",
        "u",
        "v",
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
        "icon_names",
        "arome_name",
        "min_value",
        "max_value",
        "dwh_id",
        "icon_hfl",
        # line appearance
        "color",
        "marker",
        "linestyle",
        "colormap",
        # value transformations
        "mult",
        "mult_arome",
        "plus",
        "plus_arome",
        "avg",
        "avg_arome",
        "acc",
    ],
)

# set default values for certain attributes
vdf.loc["icon_name"] = None
vdf.loc["icon_names"] = None
vdf.loc["arome_name"] = None
vdf.loc["min_value"][:] = None
vdf.loc["max_value"][:] = None
vdf.loc["dwh_id"][:] = None
vdf.loc["icon_hfl"] = False
vdf.loc["color"] = "blue"
vdf.loc["marker"][:] = "o"
vdf.loc["linestyle"] = "solid"
vdf.loc["colormap"] = sns.color_palette("viridis", as_cmap=True)
vdf.loc["mult"][:] = 1
vdf.loc["mult_arome"][:] = 1
vdf.loc["plus"][:] = 0
vdf.loc["plus_arome"][:] = 0
vdf.loc["avg"][:] = False
vdf.loc["avg_arome"][:] = False
vdf.loc["acc"][:] = False


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

# Cloud covers

# cloud cover: clc
vdf["clc"].short_name = "clc"
vdf["clc"].icon_name = "clc"
vdf["clc"].icon_names = ["clc", "CLC"]
vdf["clc"].arome_name = "fCV"
vdf["clc"].long_name = "Cloud cover"
vdf["clc"].unit = "%"
vdf["clc"].min_value = -0.05
vdf["clc"].max_value = 1.05
vdf["clcl"].mult_arome = 100
vdf["clc"].color = "yellowgreen"
vdf["clc"].colormap = "bone"

# cloud cover LOW: clcl
vdf["clcl"].short_name = "clcl"
vdf["clcl"].icon_name = "clcl"
vdf["clcl"].icon_names = ["clcl", "CLCL"]
vdf["clcl"].arome_name = "LCV"
vdf["clcl"].long_name = "Low cloud cover"
vdf["clcl"].unit = "%"
vdf["clcl"].min_value = -0.05
vdf["clcl"].max_value = 1.05
vdf["clcl"].mult_arome = 0.01
vdf["clcl"].color = "peru"
vdf["clcl"].colormap = "bone"

# cloud cover MEDIUM: clcm
vdf["clcm"].short_name = "clcm"
vdf["clcm"].icon_name = "clcm"
vdf["clcm"].icon_names = ["clcm", "CLCM"]
vdf["clcm"].arome_name = "MCV"
vdf["clcm"].long_name = "Medium cloud cover"
vdf["clcm"].unit = "%"
vdf["clcm"].min_value = -0.05
vdf["clcm"].max_value = 1.05
vdf["clcm"].mult_arome = 0.01
vdf["clcm"].color = "mediumorchid"
vdf["clcm"].colormap = "bone"

# cloud cover HIGH: clch
vdf["clch"].short_name = "clch"
vdf["clch"].icon_name = "clch"
vdf["clch"].icon_names = ["clch", "CLCH"]
vdf["clch"].arome_name = "HCV"
vdf["clch"].long_name = "High cloud cover"
vdf["clch"].unit = "%"
vdf["clch"].min_value = -0.05
vdf["clch"].max_value = 1.05
vdf["clch"].mult_arome = 0.01
vdf["clch"].color = "cornflowerblue"
vdf["clch"].colormap = "bone"

# cloud cover TOTAL: clct
vdf["clct"].short_name = "clct"
vdf["clct"].icon_name = "clct"
vdf["clct"].icon_names = ["clct", "CLCT"]
vdf["clct"].long_name = "Total cloud cover"
vdf["clct"].unit = "%"
vdf["clct"].min_value = -0.05
vdf["clct"].max_value = 1.05
vdf["clct"].mult_arome = 0.01

# temperature tendency due to longwave radiative heating
#  ddt_t_lw
vdf["ddt_t_lw"].short_name = "ddt_t_lw"
# vdf["ddt_t_lw"].icon_name = "THHR_RAD"
# TODO: various names from different configurations
vdf["ddt_t_lw"].icon_name = "ddt_temp_radlw"
vdf["ddt_t_lw"].icon_names = ["ddt_temp_radlw", "THHR_RAD"]
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
vdf["ddt_t_sw"].icon_names = ["ddt_temp_radsw", "SOHR_RAD"]
vdf["ddt_t_sw"].long_name = "T-tend SW radiation"
vdf["ddt_t_sw"].unit = "K/h"
vdf["ddt_t_sw"].mult = 3600
vdf["ddt_t_sw"].min_value = -3.0
vdf["ddt_t_sw"].max_value = 3.0
vdf["ddt_t_sw"].color = "goldenrod"
vdf["ddt_t_sw"].colormap = sns.light_palette("goldenrod", as_cmap=True)

# dewpoint temperature: dewp_temp
vdf["dewp_temp"].short_name = "dewp_temp"
vdf["dewp_temp"].arome_name = "Td"
vdf["dewp_temp"].long_name = "Dew point temperature"
vdf["dewp_temp"].unit = "°C"
vdf["dewp_temp"].plus_arome = -273.15
vdf["dewp_temp"].min_value = -5
vdf["dewp_temp"].max_value = 15
vdf["dewp_temp"].dwh_id = {"rs": "747", "2m": "194"}

# 2m temperature: 2m_dewp_temp
vdf["2m_dewp_temp"].short_name = "2m_dewp_temp"
vdf["2m_dewp_temp"].icon_name = "td_2m"
vdf["2m_dewp_temp"].arome_name = "Td2m"
vdf["2m_dewp_temp"].long_name = "2m dew point temperature"
vdf["2m_dewp_temp"].unit = "°C"
vdf["2m_dewp_temp"].color = "orangered"
vdf["2m_dewp_temp"].marker = "o"
vdf["2m_dewp_temp"].linestyle = "-"
vdf["2m_dewp_temp"].plus = -273
vdf["2m_dewp_temp"].plus_arome = -273

# gradient tempearture vertical
vdf["grad_temp"].short_name = "grad_temp"
vdf["grad_temp"].icon_name = "grad_temp"
vdf["grad_temp"].icon_names = [
    "grad_temp",
]
vdf["grad_temp"].arome_name = "grad_temp"
vdf["grad_temp"].long_name = "Vertical temperature gradient"
vdf["grad_temp"].unit = "°C/m"
vdf["grad_temp"].dwh_id = {"30m_tower": "grad_temp:4957:4949"}

# horizontal visiblity: hor_vis
vdf["hor_vis"].short_name = "hor_vis"
vdf["hor_vis"].long_name = "Horizontal visibility"
vdf["hor_vis"].unit = "m"
vdf["hor_vis"].min_value = 0
vdf["hor_vis"].max_value = 5000
vdf["hor_vis"].dwh_id = {"2m": "1547"}

# pressure: press
vdf["press"].short_name = "press"
vdf["press"].icon_names = ["p", "P"]
vdf["press"].arome_name = "P"
vdf["press"].long_name = "Pressure"
vdf["press"].unit = "hPa"
vdf["press"].mult_arome = 0.01
vdf["press"].dwh_id = {"rs": "744", "2m": "90"}

# cloud water: qc
vdf["qc"].short_name = "qc"
vdf["qc"].icon_name = "QC"
vdf["qc"].icon_names = ["QC", "qc"]
vdf["qc"].arome_name = "LWC"
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
vdf["qc_dia"].icon_names = ["tot_qc_dia"]
vdf["qc_dia"].long_name = "Diagnostic cloud water"
vdf["qc_dia"].unit = "g/kg"
vdf["qc_dia"].min_value = -0.01
vdf["qc_dia"].max_value = 0.07
vdf["qc_dia"].color = "darkblue"
vdf["qc_dia"].mult = 1000


# diagnostic cloud ice: qi_dia
vdf["qi_dia"].short_name = "qi_dia"
vdf["qi_dia"].icon_name = "tot_qi_dia"
vdf["qi_dia"].icon_names = ["tot_qi_dia"]
vdf["qi_dia"].long_name = "Diagnostic cloud ice"
vdf["qi_dia"].unit = "g/kg"
vdf["qi_dia"].min_value = -0.01
vdf["qi_dia"].max_value = 0.07
vdf["qi_dia"].color = "darkblue"
vdf["qi_dia"].mult = 1000

# specific humidity: qv
vdf["qv"].short_name = "qv"
vdf["qv"].icon_name = "QV"
vdf["qv"].icon_names = ["QV", "qv"]
vdf["qv"].arome_name = "qv"
vdf["qv"].long_name = "Specific humidity"
vdf["qv"].unit = "g/kg"
vdf["qv"].min_value = 0
vdf["qv"].max_value = 6
vdf["qv"].color = "skyblue"
vdf["qv"].colormap = "PuBu"
vdf["qv"].mult = 1000
vdf["qv"].mult_arome = 1000
vdf["qv"].dwh_id = {
    "2m": "qv",
    "2m_tower": "qv",
    "10m_tower": "qv",
    "30m_tower": "qv",
    "rs": "qv",
    "ralmo": "4919",
}

# 2m specific humidity: 2m_qv
vdf["2m_qv"].short_name = "2m_qv"
vdf["2m_qv"].icon_name = "qv_2m"
vdf["2m_qv"].arome_name = "2m_qv"
vdf["2m_qv"].long_name = "2m specific humidity"
vdf["2m_qv"].unit = "g/kg"
vdf["2m_qv"].min_value = 0
vdf["2m_qv"].max_value = 6
vdf["2m_qv"].color = "skyblue"
vdf["2m_qv"].colormap = "PuBu"
vdf["2m_qv"].mult = 1000
vdf["2m_qv"].mult_arome = 1000

# diagnostic humidity: qv_dia
vdf["qv_dia"].short_name = "qv_dia"
vdf["qv_dia"].icon_name = "tot_qv_dia"
vdf["qv_dia"].icon_names = [
    "tot_qv_dia",
]
vdf["qv_dia"].long_name = "Diagnostic humidity"
vdf["qv_dia"].unit = "g/kg"
vdf["qv_dia"].min_value = -0.01
vdf["qv_dia"].max_value = 0.07
vdf["qv_dia"].color = "darkblue"
vdf["qv_dia"].mult = 1000

# relative humidity: rel_hum
vdf["rel_hum"].short_name = "rel_hum"
vdf["rel_hum"].long_name = "Relative humidity"
vdf["rel_hum"].icon_name = "rel_hum"
vdf["rel_hum"].icon_names = [
    "rel_hum",
]
vdf["rel_hum"].arome_name = "Hu"
vdf["rel_hum"].unit = "%"
vdf["rel_hum"].min_value = 0
vdf["rel_hum"].max_value = 100
# vdf["rel_hum"].mult = 100
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
vdf["lw_down"].icon_name = "athd_s"
vdf["lw_down"].icon_names = [
    "athd_s",
]
vdf["lw_down"].avg = True
vdf["lw_down"].dwh_id = {"2m": "175", "2m_tower": "3762"}

# radiation: longwave upward
vdf["lw_up"].short_name = "lw_up"
vdf["lw_up"].long_name = "Upward LW rad"
vdf["lw_up"].unit = "W/m2"
vdf["lw_up"].icon_names = [
    "athu_s",
]
vdf["lw_up"].avg = True
vdf["lw_up"].dwh_id = {
    "2m": "1531",
    "2m_tower": "5118",  # no data yet in DWH
    "30m_tower": "5181",  # no data yet in DWH
}

# radiation: longwave net
vdf["lw_net"].short_name = "lw_net"
vdf["lw_net"].long_name = "Net LW rad"
vdf["lw_net"].unit = "W/m2"
vdf["lw_net"].icon_name = "athb_s"
vdf["lw_net"].icon_names = [
    "athb_s",
]
vdf["lw_net"].arome_name = "LW"
vdf["lw_net"].mult_arome = 1 / 3600
vdf["lw_net"].avg = True
vdf["lw_net"].acc = True
vdf["lw_net"].dwh_id = {"2m": "net_calc:175:1531:"}

# radiation: shortwave downward
vdf["sw_down"].short_name = "sw_down"
vdf["sw_down"].long_name = "Downward SW rad"
vdf["sw_down"].unit = "W/m2"
vdf["sw_down"].dwh_id = {"2m": "96", "2m_tower": "3873"}
vdf["sw_down"].icon_name = "asod_s"
vdf["sw_down"].icon_names = ["asod_s", "ASOD_S", "GLOB"]
vdf["sw_down"].avg = True

# radiation: shortwave upward ("reflected")
vdf["sw_up"].short_name = "sw_up"
vdf["sw_up"].long_name = "Upward SW rad"
vdf["sw_up"].unit = "W/m2"
vdf["sw_up"].dwh_id = {"2m": "1871", "2m_tower": "4995"}

# radiation: shortwave net
vdf["sw_net"].short_name = "sw_net"
vdf["sw_net"].long_name = "Net SW rad"
vdf["sw_net"].unit = "W/m2"
vdf["sw_net"].icon_name = "asob_s"
vdf["sw_net"].icon_names = ["asob_s", "ASOD_S"]
vdf["sw_net"].arome_name = "SW"
vdf["sw_net"].mult_arome = 1 / 3600
vdf["sw_net"].avg = True
vdf["sw_net"].acc = True
vdf["sw_net"].dwh_id = {"2m": "net_calc:96:1871:"}

# temperature: temp
vdf["temp"].short_name = "temp"
vdf["temp"].icon_name = "T"
vdf["temp"].icon_names = ["T", "t"]
vdf["temp"].arome_name = "T"
vdf["temp"].long_name = "Temperature"
vdf["temp"].unit = "°C"
vdf["temp"].min_value = -3.0  # 275
vdf["temp"].max_value = 5  # 287
vdf["temp"].color = "orangered"
vdf["temp"].marker = "o"
vdf["temp"].linestyle = "-"
vdf["temp"].mult = 1
vdf["temp"].plus = -273
vdf["temp"].plus_arome = -273
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
vdf["2m_temp"].icon_names = ["T_2M", "t_2m"]
vdf["2m_temp"].arome_name = "T2m"
vdf["2m_temp"].long_name = "2m temperature"
vdf["2m_temp"].unit = "°C"
vdf["2m_temp"].min_value = -3.0  # 275
vdf["2m_temp"].max_value = 5  # 287
vdf["2m_temp"].color = "orangered"
vdf["2m_temp"].marker = "o"
vdf["2m_temp"].linestyle = "-"
vdf["2m_temp"].mult = 1
vdf["2m_temp"].plus = -273
vdf["2m_temp"].plus_arome = -273
vdf["2m_temp"].avg = False

# turblent kinetic energy; tke
vdf["tke"].short_name = "tke"
vdf["tke"].icon_name = "TKE"
vdf["tke"].arome_name = "TKE"
vdf["tke"].long_name = "Turbulent kinetic energy"
vdf["tke"].icon_hfl = True
vdf["tke"].unit = "m2/s2"

# total water vapour: tqv
vdf["tqv"].short_name = "tqv"
vdf["tqv"].icon_name = "TQV"
vdf["tqv"].icon_names = ["TQV", "tqv"]
vdf["tqv"].long_name = "Total water vapour"
vdf["tqv"].unit = "kg/m2"
vdf["tqv"].dwh_id = {"2m": "2537"}

# liquid water path : tqc
vdf["tqc"].short_name = "tqc"
vdf["tqc"].icon_name = "tqc"
vdf["tqc"].icon_names = ["TQC", "tqc"]
vdf["tqc"].long_name = "Liquid water path"
vdf["tqc"].unit = "kg/m2"


# total column integrated diagnostic cloud water: tqc_dia
vdf["tqc_dia"].short_name = "tqc_dia"
vdf["tqc_dia"].icon_name = "tqc_dia"
vdf["tqc_dia"].icon_names = ["tqc_dia"]
vdf["tqc_dia"].long_name = "Diagnostic liquid water path"
vdf["tqc_dia"].unit = "kg/m2"

# x wind
vdf["u"].short_name = "u"
vdf["u"].long_name = "x wind velocity"
vdf["u"].icon_name = "U"
vdf["u"].icon_names = ["U", "u"]
vdf["u"].arome_name = "U"
vdf["u"].unit = "m/s"

# y wind
vdf["v"].short_name = "v"
vdf["v"].long_name = "y wind velocity"
vdf["v"].icon_name = "V"
vdf["v"].icon_names = ["V", "v"]
vdf["v"].arome_name = "V"
vdf["v"].unit = "m/s"

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
vdf["wind_dir"].icon_name = "wind_dir"
vdf["wind_dir"].arome_name = "wind_dir"
vdf["wind_dir"].long_name = "Wind direction"
vdf["wind_dir"].unit = "°"
vdf["wind_dir"].min_value = 0
vdf["wind_dir"].max_value = 360
vdf["wind_dir"].dwh_id = {"rs": "743", "10m_tower": "197", "lidar": "743"}

# wind velocity: wind_vel
vdf["wind_vel"].short_name = "wind_vel"
vdf["wind_vel"].icon_name = "wind_vel"
vdf["wind_vel"].arome_name = "wind_vel"
vdf["wind_vel"].long_name = "Wind velocity"
vdf["wind_vel"].unit = "m/s"
vdf["wind_vel"].min_value = 0
vdf["wind_vel"].max_value = 30
vdf["wind_vel"].dwh_id = {"rs": "748", "10m_tower": "196", "lidar": "748"}

# !!! if adding new variable: don't forget to add at the top and in cli-file!!!

if __name__ == "__main__":
    print(vdf)
