============
plot_profile
============

*plot_profile* is a Python-based command line tool to retrieve and visualise both observational data as well as variables simulated with ICON

Installation
------------
1. ``git clone git@github.com:MeteoSwiss-APN/plot_profile.git``
2. ``conda activate base``
3. ``conda install pip``
4. ``conda deactivate``
5. ``make venv install`` (or: ``install-dev``)

*I am not sure whether step 2 and 3 are required*

Usage
-----
1. ``conda activate plot_profile``
2. Available entry-points (show available options with ``--help``)

- ``plot_rs``: plot radiousounding
 
  ``plot_rs --date 2021111912 --params temp --params dewp_temp --alt_top 2500``
   
- ``plot_icon_profiles``: plot vertical profiles of variables from ICON simulations
 
  ``plot_icon_profiles --date 21111012 --folder /scratch/swester/output_icon/ICON-1/ --var qv --var temp --var qc --leadtime 12 --leadtime 13 --add_rs 12``
   
- ``plot_icon_heatmap``: plot heatmap (time-height-crosssection) of ICON simulation
 
  ``plot_icon_heatmap --date 21111812 --folder /scratch/swester/output_icon/ICON-1/ --var clc --alt_top 2000 --start_leadtime 12 --end_leadtime 24 --verbose``



Credits
-------

This package was created with `Cookiecutter`_ and the `MeteoSwiss-APN/mch-python-blueprint`_ project template.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`MeteoSwiss-APN/mch-python-blueprint`: https://github.com/MeteoSwiss-APN/mch-python-blueprint

TO DO's
-------
- complete stations.py: add station height and remove umlaute
- if dwh-dataframe is empty, (icon-)plot should still be produced, just without data
- allow for multiple icon_names in variables.py
- plot timeseries of DWH-surface variables
- add timeseries of simulated surface variables for 1 or more configurations
- heatmap of MWR temperature data (started by Steffi but not finished yet)
- labelling of leadtimes and radiosoundings in icon_profiles-plot
- support read-in of ICON files in GRIB2-format
- allow different filename-formats for ICON-files
