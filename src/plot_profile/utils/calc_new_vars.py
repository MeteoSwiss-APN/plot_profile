"""Calculate vars that are not in models/observations output files.

Author: Arthur Dandoy
"""

# Standard library
import sys

# Third-party
import numpy as np
import pandas as pd

# First-party
from plot_profile.utils.variables import vdf

# from ipdb import set_trace


def calculate_grad(var_bot, var_top, alt_bot, alt_top, verbose=False):
    """Calculate vertical gradient.

    Args:
        var_bot, var top (pd series):   bot and top variables time series
        alt_bot, alt_top (floats):      altitudes of bot and top (in meters)

    Returns:
        _pandas series : vertical gradient between level top and bot (in var_unit/m)

    """
    if verbose:
        print("Calculating vertical gradient.")

    grad = (var_top - var_bot) / (alt_top - alt_bot)

    return grad


def calculate_tdew_from_rh(rh, T, temperature_metric="celsius", verbose=False):
    """Calculate dew point temperature from relative humidity and temperature.

    Args:
        rh (pd series):    air relative humidity in %
        T (pd series):     air temperature in °C
        temperature_metric (str, optional): Input temperature unit. Defaults to "celsius".

    Returns:
        pandas series: dew point temperature timeseries (in °C or K)

    """
    if verbose:
        print(
            "Calculating dew point temperature (dewp_temp) from relative humidity and temp."
        )

    if temperature_metric != "celsius":
        if verbose:
            print("Assuming input temperature unit is Kelvin for rh calculation.")
        T = T - 273  # K to °C

    # inspired from humidity.to.dewpoint in:
    # https://github.com/geanders/weathermetrics/blob/master/R/moisture_conversions.R
    Tdew = (rh / 100) ** (1 / 8) * (112 + (0.9 * T)) - 112 + (0.1 * T)  # in °C

    if temperature_metric != "celsius":
        Tdew = Tdew + 273  # °C to K

    return Tdew


def calculate_rh_from_qv(T, qv, Press=1013.5, verbose=False):
    """Convert specific humidity into relative humidity.

    Args:
        Press (pd series):   air pressure in hPa
        T (pd series):       air temperature in °C
        qv (pd series):      specific humidity in kg/kg

    Returns:
        pandas series: relative humidity series in %

    """
    if verbose:
        print(
            "Calculating relative humidity (rh) from specific humidity, press and temp."
        )

    # inspired from "qair2rh" function in:
    # https://github.com/PecanProject/pecan/blob/master/modules/data.atmosphere/R/metutils.R
    es = 6.112 * np.exp((17.67 * T) / (T + 243.5))
    e = qv * 1e-3 * Press / (0.378 * qv * 1e-3 + 0.622)

    rh = e / es

    # assign 0 and 1 to values outside [0, 1]
    rh = rh.clip(lower=0, upper=1)

    # convert to %
    rh = 100 * rh

    return rh


def calculate_qv_from_tdew(Press, Tdew, verbose=False):
    """Calculate specific humidity from pressure and dew point temperature.

    Args:
        Press (pd series):   air pressure in hPa
        Tdew (pd series):    dew point temperature in °C

    Returns:
        pandas series: specific humidity series in kg/kg

    """
    if verbose:
        print("Calculating specific humidity (qv) from press and dewp_temp.")

    # after eq. 4.24 in Practical Meteorology from Stull
    # P in hPa, Td in °C and qv in kg/kg
    e = 6.112 * np.exp((17.67 * Tdew) / (Tdew + 243.5))
    qv = (0.622 * e) / (Press - (0.378 * e))

    return qv


def calculate_qv_from_rh(Press, rh, T, verbose=False):
    """Calculate specific humidity from pressure, relative humidity and temperature.

    Args:
        Press (pd series):   air pressure series in hPa
        rh    (pd series):   air relative humidity in %
        T     (pd series):   air temperature in K

    Returns:
        pandas series: specific humidity series in kg/kg

    """
    if verbose:
        print("Calculating specific humidity (qv) from press and relative humidity.")

    Tdew = calculate_tdew_from_rh(rh, T)

    qv = calculate_qv_from_tdew(Press, Tdew)

    return qv


def calculate_wind_vel_from_uv(u, v, verbose=False):
    """Calculate wind velocity from U, V components.

    Args:
        u (pd series) u wind component in m/s
        v (pd series) v wind component in m/s

    Returns:
        pd series: wind velocity in m/s

    """
    if verbose:
        print(
            "Calculating wind velocity (wind_vel) from meridian and zonal wind velocity."
        )

    wind_vel = np.sqrt(u**2 + v**2)

    return wind_vel


def calculate_wind_dir_from_uv(u, v, verbose=False):
    """Calculate wind direction from U, V components.

    Args:
        u (pd series) u wind component in m/s
        v (pd series) v wind component in m/s

    Returns:
        pd series: wind direction in °

    """
    if verbose:
        print(
            "Calculating wind direction (wind_dir) from meridian and zonal wind velocity."
        )

    # convert to wind direction coordinate, different from trig unit circle coords
    # if the wind directin is 360 then returns zero (by %360)
    # inspired from wind_uv_to_dir function in:
    # https://github.com/blaylockbk/Ute_WRF/blob/master/functions/wind_calcs.py

    wind_dir = (270 - np.rad2deg(np.arctan2(v, u))) % 360

    return wind_dir


# TODO: a tester !!! je ne sais pas si ca marche
def calc_rho_arome(p, t, qc, qv, verbose=False):
    """Calculate air density.

    Args:
        p (pd series):   air pressure (Pa)
        t (pd series):   air temperature (K)
        qc (pd series): liquid water content (kg/kg)
        qv (pd series): specific humidity (kg/kg)

    Returns:
        pd series :      air density (kg/m**3)

    """
    if verbose:
        print("Calculating air density (RHO) from press, temp, qc and qv")

    # series must have the same shapes
    if not p.shape == t.shape == qc.shape == qv.shape:
        print(f"--- ! shapes of press, temp, qc and qv don't match !")
        sys.exit(1)

    # constants
    r_d = 287.05  # gas constant for dry air
    r_v = 461.51  # gas constant for moist air
    rvd_m_o = r_v / r_d - 1

    # density, after calrho in meteo_utilities from COSMO-code
    # rho = press/(r_d * temp * ( 1 + rvd_m_o * qv - qc))
    rho = p / (r_d * t * (1 + rvd_m_o * qv - qc))

    return rho


def calc_new_var_profiles(df, new_var, verbose=False):
    """Calculate vert. profile of requested variable from model output variables.

    Args:
        df (DataFrame):            model output variables
        new_var (str):             name of the variable to be calculated
        verbose (bool, optional):  print details. Defaults to False.

    Returns:
        DataFrame: same format as the input but with newly calculated variable

    """
    if verbose:
        print(f"{new_var} needs to be calculated.")

    # parameters to calculate (alphabetical order):

    ## Relative humidity
    if new_var == "rel_hum":
        values = calculate_rh_from_qv(
            T=df["temp"],
            qv=df["qv"],
            verbose=verbose,
        )
        # delete remaining columns
        del df["temp"], df["qv"]

    ## Specific humidity
    elif new_var == "qv":
        values = calculate_qv_from_tdew(
            Press=df["press"],
            Tdew=df["dewp_temp"],
            verbose=verbose,
        )
        # delete remaining columns
        del df["press"], df["dewp_temp"]

    ## Wind velocity
    elif new_var == "wind_vel":
        values = calculate_wind_vel_from_uv(u=df["u"], v=df["v"], verbose=verbose)
        # delete remaining columns
        del df["u"], df["v"]

    ## Wind direction
    elif new_var == "wind_dir":
        values = calculate_wind_dir_from_uv(u=df["u"], v=df["v"], verbose=verbose)
        # delete remaining columns
        del df["u"], df["v"]

    else:
        print(f"{new_var} not available for calculation yet.")

    # convert values to pandas series
    values = pd.Series(values, name=new_var)

    # TODO si jamais icon detecter et appliquer les convertisseurs d'icon
    # do some unity conversions
    values = values * vdf.loc["mult_arome"][new_var] + vdf.loc["plus_arome"][new_var]

    # add values column to the dataframe
    df = pd.concat([df, values], axis=1)

    return df


def calc_new_var_timeseries(df, new_var, levels, verbose=False):
    """Calculate timeseries of requested variable from model output variables.

    Args:
        df (DataFrame):            model output variables
        new_var (str):             name of the variable to be calculated
        levels (list of int):      level of the variables output
        verbose (bool, optional):  defaults to False.

    Returns:
        DataFrame: same format as the input but with newly calculated variable

    """
    if verbose:
        print(f"{new_var} needs to be calculated.")

    # determine variables columns sufix
    sufix_levels = []

    # if level is integer make it a one element list
    if isinstance(levels, int):
        levels = [
            levels,
        ]

    for level in levels:
        if level == 0:
            sufix_levels.append("")
        else:
            sufix_levels.append(f"~{level}")

    # parameters to calculate (alphabetical order):

    ## Gradient vertical de température
    if new_var == "grad_temp":
        values = calculate_grad(
            var_bot=df[f"temp{sufix_levels[0]}"],
            var_top=df[f"temp{sufix_levels[1]}"],
            alt_bot=levels[0],
            alt_top=levels[1],
            verbose=verbose,
        )

        # delete remaining columns
        del df[f"temp{sufix_levels[0]}"], df[f"temp{sufix_levels[1]}"]
        sufix_levels = [""]

    ## Relative humidity
    elif new_var == "rel_hum":
        values = calculate_rh_from_qv(
            T=df[f"temp{sufix_levels[0]}"],
            qv=df[f"qv{sufix_levels[0]}"],
            verbose=verbose,
        )

        # delete remaining columns
        del df[f"temp{sufix_levels[0]}"], df[f"qv{sufix_levels[0]}"]

    ## Specific humidity
    elif new_var == "qv" or "2m_qv":
        if new_var == "2m_qv":
            prefix = "2m_"
        else:
            prefix = ""

        values = calculate_qv_from_tdew(
            Press=df[f"press{sufix_levels[0]}"],
            Tdew=df[f"{prefix}dewp_temp{sufix_levels[0]}"],
            verbose=verbose,
        )

        # delete remaining columns
        del df[f"press{sufix_levels[0]}"], df[f"{prefix}dewp_temp{sufix_levels[0]}"]

    ## Wind velocity
    elif new_var == "wind_vel":
        values = calculate_wind_vel_from_uv(
            u=df[f"u{sufix_levels[0]}"], v=df[f"v{sufix_levels[0]}"], verbose=verbose
        )

        # delete remaining columns
        del df[f"u{sufix_levels[0]}"], df[f"v{sufix_levels[0]}"]

    ## Wind direction
    elif new_var == "wind_dir":
        values = calculate_wind_dir_from_uv(
            u=df[f"u{sufix_levels[0]}"], v=df[f"v{sufix_levels[0]}"], verbose=verbose
        )

        # delete remaining columns
        del df[f"u{sufix_levels[0]}"], df[f"v{sufix_levels[0]}"]

    else:
        print(f"--- ! Variable {new_var} calculation not available yet.")
        sys.exit(1)

    # convert values to pandas series
    values = pd.Series(values, name=f"{new_var}{sufix_levels[0]}")

    # TODO si jamais icon detecter et appliquer les convertisseurs d'icon
    # do some unity conversions
    values = values * vdf.loc["mult_arome"][new_var] + vdf.loc["plus_arome"][new_var]

    # add values column to the dataframe
    df = pd.concat([df, values], axis=1)

    return df
