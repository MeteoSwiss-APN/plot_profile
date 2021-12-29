"""Purpose: Parse Data.

Author: Michel Zeller

Date: 15/10/2021.
"""

# Local
from .dwh_retrieve import dwh_retrieve
from .utils import slice_top_bottom


def get_rs(date, params, station, print_steps, alt_bot, alt_top):
    """Retrieve and parse the relevant data from the server and return a complete dataframe containing the data.

    Args:
        date:               str         YYYYMMDDHH
        params:             tuple       parameters, that should be included in the plot
        station:            df          station and attributes
        print_steps:        bool        optional parameter to print intermediate steps in terminal
        alt_bot:            int         lower altitude limit
        alt_top:            int         upper altitude limit

    Returns:
        df:                 df          dataframe w/ columns for all specified variables

    """
    df = dwh_retrieve(
        device="rs",
        station=station.short_name,
        vars=list(params),
        timestamps=date,
        verbose=print_steps,
    )

    crit = slice_top_bottom(df["altitude"], alt_top, alt_bot, verbose=True)

    # return sliced dataframe and drop lines with nan-values
    return df[crit].dropna()
