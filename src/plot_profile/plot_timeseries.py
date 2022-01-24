"""Plot variables of various measurement devices over time."""

# Standard library
import datetime
from datetime import datetime as dt

# Third-party
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.units as munits
import numpy as np
import pandas as pd

converter = mdates.ConciseDateConverter()
munits.registry[np.datetime64] = converter
munits.registry[datetime.date] = converter
munits.registry[datetime.datetime] = converter

# Local
from .stations import sdf
from .utils import save_fig
from .variables import vdf
