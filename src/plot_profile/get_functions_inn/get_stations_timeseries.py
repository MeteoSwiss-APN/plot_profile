"""
Functions to read in data from weather stations of ACINN, Innsbruck iBox stations

Author: Tobia Lezuo
Based on: TS_read_stations.py in wrf_crossinn_toni package by Antonia Fritz

Created: 27.10.2022
"""

import numpy as np
import pandas as pd
import datetime
import os.path as path
import glob2

# plot profile imports
from plot_profile.utils.dwh_retrieve import parse_timestamps
from plot_profile.utils.stations import sdf


from ipdb import set_trace

# %% Function to parse_timestamps again, adding minutes
def parse_timestamps_min(t):
    """
    Put timestamps to format str ('yyyy-mm-dd HH:MM:SS')

    E.g. '2021081812' will become '2021-08-18 12:00:00'

    Args:
        t10 (string)

    Returns:
        t17 (string)

    """

    t17=str(t[0:4]) +'-'+ str(t[4:6]) +'-'+ str(t[6:8]) +' '+ str(t[8:10]) +':00:00'
    
    return t17

def getKey(dct,value): # finds 
    '''
    Function to find the dict key = station specific variable name for a secific var = value

    Parameters
    ----------
    dct : dictionary
        "var_s":"var"
    value : str
        value=var
        
    Returns
    -------
    var_stationname : str
        key=var_s
    '''
    var_stationname = str([key for key in dct if (dct[key] == value)])
    var_stationname = var_stationname[2:-2] # cuts the edges of the string
    return var_stationname

# %% Function to read in ACINN data
def read_acinn(station, var, path_ACINN, timestamps,
               correct_direction=False):
    '''
    Function to read in the station data of ACINN

    Parameters
    ----------
    station : str
        Abreviation for the station as indicated in stations.py in sdf
    var : str
        short name of desired variable
    path_ACINN : str
        Path to the ACINN data
    timestamps : list of strings     
        either 1 or 2 timestamps YYYYmmddHH
        then converted to start_time, end_time

    Returns
    -------
    data : pandas Dataframe
        Daraframe containing the ACINN data for:
        - temp:    2m Temperature in K
        - press:  surface pressure in hPa
        - wind_vel:  wind speed in m/s
        - wind_dir: wind direction in degree
        - h_m:   height of the wind sensor in m
        The measurements closest to the WRF output heights (agl) are selected.

    '''
    
    # parse timestamp input to 2 string of format YYYYmmddHH
    t1,t2 = parse_timestamps(timestamps)
    # parse timestamp to match csv row name of format 'yyyy-mm-dd HH:MM:SS'
    start_time = parse_timestamps_min(t1)
    end_time = parse_timestamps_min(t2)

    # As the ACINN data sets aren't labelled consistently, a dict is needed
    # to bring them all to the same names. Only important parameters are kept.
    # Description of parameters can be found at:
    # https://acinn-data.uibk.ac.at/pages/station-list.html
    acinn_v = {'hoch': {
                        'ta_avg': 'temp',   # RAW: Air temperature, ventilation [°C] 
                        # 'tpt100_avg':'temp', # RAW: Air temperature, ventilation [°C] , looks the same as above
                        'p': 'press', # RAW: Air pressure [hPa]
                        'ws_1_avg': 'wind_vel', # RAW: wind vel [ms] at 1,2,3m 
                                                #VERY WEIRD!!
                        # 'ws_2_avg': 'wind_vel',
                        # 'ws_3_avg': 'wind_vel',
                        'w_dir_avg':'wind_dir', # RAW: wind dir [deg] at 1m
                        'cnr4_lw_in_wm2':'lw_down', # RADIAT1
                        'cnr4_lw_out_wm2':'lw_up', # RADIAT1
                        'cnr4_sw_in_wm2':'sw_down', # RADIAT1
                        'cnr4_sw_out_wm2':'sw_up', # RADIAT1
                        'rawdate':'timestamp'},
                'kols': {'taact1_avg': 'temp',  # RAW_TRH_PROF: TAACT1_AVG: 2m temp [°C]
                        # 'rhact1_avg': 'rh', # RAW_TRH_PROF: RHACT1_AVG: 2m rh [%]
                        'pact': 'press', #RAW: PACT: air pessure at station [hPa]
                        'wind_speed_4': 'wind_vel', #SONIC_2: WIND_SPEED4: 12m wind vel [ms]
                        'avg_wdir4': 'wind_dir', #SONIC_2: AVG_WDIR4: 12m wind dir [deg]
                        'rawdate':'timestamp'},
               'egg': {'ta_avg': 'temp',   # RAW: Air temperature, ventilation [°C]
                        'p_avg': 'press',   # RAW: Air pressure, in loggerbox, not aerated [hPa]
                        'wind_dir2':'wind_dir', # FLUXL: wind dir at 5.65m [deg]                        
                        'rawdate':'timestamp'},
               'weer': {'ta_avg': 'temp',   # RAW: Air temperature, ventilation [°C]
                        'p_avg': 'press',   # RAW: Air pressure, in loggerbox, not aerated [hPa]
                        'wind_dir2':'wind_dir', # RAW: wind dir at 5.65m [deg]                        
                        'cnr4_lw_in_wm2':'lw_down', # RADIAT1
                        'cnr4_lw_out_wm2':'lw_up', # RADIAT1
                        'cnr4_sw_in_wm2':'sw_down', # RADIAT1
                        'cnr4_sw_out_wm2':'sw_up', # RADIAT1                       
                        'rawdate':'timestamp'},
               'terf': {'taact_avg': 'temp',  # RAW: Air temperature, ventilation [°C]
                        'pact': 'press', # RAW: Air pressure, in loggerbox, not aerated [hPa]
                        # 'wind_dir1':'wind_dir', # RAW: wind dir at 6.12 m [deg]      
                        'wind_dir2':'wind_dir', # RAW: wind dir at 11.2 m [deg]                              
                        'rawdate':'timestamp'},
               'arb': {
                        # 'taact_2m_avg': 'temp',  # RAW: Air temperature, ventilation [°C] 2m NOT WORKING
                        'taact_1m_avg':'temp',  # RAW: Air temperature, ventilation [°C] 1m
                        # 'taact_3m_avg':'temp',  # RAW: Air temperature, ventilation [°C] 3m
                       'pact': 'press', # RAW: Air pressure, in loggerbox, not aerated [hPa]
                       'ws_young_avg': 'wind_vel', # RAW: Wind speed, 2m, Young Wind Monitor [ms]
                                                        # there are more for ws on1,3m but no wdir
                       'wdir_young_avg': 'wind_dir', # RAW: Wind direction, 2m, Young Wind Monitor [deg]
                        'cnr4_lw_in_wm2':'lw_down', # RADIAT1
                        'cnr4_lw_out_wm2':'lw_up', # RADIAT1
                        'cnr4_sw_in_wm2':'sw_down', # RADIAT1
                        'cnr4_sw_out_wm2':'sw_up', # RADIAT1                          
                       'rawdate':'timestamp'},
}

    # Read in the data
    # When downloading the data from the ACINN website, it is given as one (or
    # sometimes two) files named 'data.csv' inside a folder including the
    
    # station name
    name = sdf[station].long_name
    # fin all files
    file_ACINN = glob2.glob(path.join(path_ACINN, f'*{name}*', 'data.csv'))
    # print number of files
    print(len(file_ACINN))
    # get variable nomenclature in this data/station = get key of dict value var
    var_s = getKey(acinn_v[station],var)

    if len(file_ACINN) == 0:
        raise ValueError(f'No ACINN data found for {station}')
    

    for file in file_ACINN: 
        data1 = pd.read_csv(file, delimiter=';', skiprows=1)
        # save data1 only if variable is inside
        if str(var_s) in data1.columns:
            data=data1
            data.index = pd.to_datetime(data.rawdate)
            # cut to desired time range
            data = data[start_time: end_time]
        
            
    
    for c in data.columns:
        # Delete all columns that do not contain relevant data
        if c not in acinn_v[station].keys():
            del(data[c])
            
        # And rename the relevant ones to be consistent
        else: #if c in acinn_v[station].keys():
            data.rename(columns={c: acinn_v[station][c]}, inplace=True)
            
    # initialize relevant variables list
    relevant_vars = ["timestamp",var]
    # cut df to relevant variables
    data=data[relevant_vars]

    # set_trace()
    return(data)
# %%
