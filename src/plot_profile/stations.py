"""Purpose: Define stations and their attributes.

Author: Stephanie Westerhuis

Date: 12/24/2021
"""
# Third-party
import pandas as pd

sdf = pd.DataFrame(
    # variables
    columns=[
        "pay",
    ],
    # attributes
    index=[
        "short_name",
        "long_name",
        "dwh_id",
        "lat",
        "lon",
        "elevation",  # it's not called "height", neither "altitude"
    ],
)

# payerne
sdf["pay"].short_name = "pay"
sdf["pay"].long_name = "Payerne"
sdf["pay"].dwh_id = "06610"
sdf["pay"].dwh_name = "PAY"
sdf["pay"].lat = 46.81291
sdf["pay"].lon = 6.94418
sdf["pay"].elevation = 490.0
