============
plot_profile
============

*plot_profile* is a Python-based command line tool to retrieve and visualise both observational data as well as variables simulated with ICON

------------
Installation
------------
1. ``git clone https://github.com/MeteoSwiss-APN/plot_profile.git``
2. ``conda activate base``
3. ``conda install pip``
4. ``conda deactivate``
5. ``make venv install`` (or: ``install-dev``)

*I am not sure whether step 2 and 3 are required*

-----
Usage
-----
First run ``conda activate plot_profile``.

The available entrypoints can be displayed with: ``plot_profile -h``.

Below you find example commands for each entrypoint.

plot_rs
=======
Plot radiosoundings

``plot_rs --date 2021111912 --params temp --params dewp_temp --alt_top 2500`` 
  
``plot_rs --date 2022011112 --params temp --clouds --relhum_thresh 95 --grid``
  
``plot_rs --date 2022041912 --params temp --params dewp_temp --params wind_vel --params wind_dir``

plot_profiles
=============
Compare vertical profiles of e.g. radiosounding
  
``plot_profiles``: compare vertical profiles of radiosounding and models for 1 specific valid time

  ``plot_profiles --loc pay --date 21111900 --add_obs rs temp --add_model icon temp ref --add_model icon temp exp --model_src ref /scratch/swester/output_icon/ICON-1/ 21111812 --model_src exp /scratch/swester/output_icon/exp1/ 21111812``
  
  ! "exp" and "ref" serve as identifiers to connect an add_model-statement to the model_src
  
- ``plot_timeseries``: timeseries of observed and modelled variables

  ``plot_timeseries --loc pay --start 21111900 --end 21111912 --add_obs 2m ver_vis --add_obs 2m cbh``
  
  ``plot_timeseries --loc pay --start 21111900 --end 21111906 --add_model icon temp 1 ref --add_model icon temp 1 exp --add_obs 10m_tower temp --model_src ref /scratch/swester/output_icon/ICON-1/ 21111812 --model_src exp /scratch/swester/output_icon/exp1/ 21111812``

- ``plot_icon_profiles``: plot vertical profiles of variables from ICON simulations at *multiple* leadtimes

  ``plot_icon_profiles --date 21111812 --folder /scratch/swester/output_icon/ICON-1/ --var qc --var qc_dia --leadtime 18  --loc pay``

  ``plot_icon_profiles --date 21111012 --folder /scratch/swester/output_icon/ICON-1/ --var qv --var temp --var qc --leadtime 12 --leadtime 13``
  
  ! if more than 2 variables are specified, 3 separate plots are created

- ``plot_icon_heatmap``: plot heatmap (time-height-crosssection) of ICON simulation

  ``plot_icon_heatmap --date 21111812 --folder /scratch/swester/output_icon/ICON-1/ --var temp --alt_top 2000 --start_leadtime 0 --end_leadtime 12 --verbose``

  ``plot_icon_heatmap --date 21111812 --folder /scratch/swester/output_icon/ICON-1/ --var clc --alt_top 2000 --start_leadtime 0 --end_leadtime 24 --add_cbh``
  
  ! for some reason currently not understood the start_leadtime is not correctly used on the x-axis, always use *--start_leadtime 0*



Credits
-------

This package was created with `Cookiecutter`_ and the `MeteoSwiss-APN/mch-python-blueprint`_ project template.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`MeteoSwiss-APN/mch-python-blueprint`: https://github.com/MeteoSwiss-APN/mch-python-blueprint

TO DO's
-------
- allow for multiple icon_names in variables.py
- allow different filename-formats for ICON-files
- output filename of plot_timeseries is funky
- heatmap x-axis tick labeling ignores --start_leadtime
- if dwh-dataframe is empty, (icon-)plot should still be produced, just without data
