============
plot_profile
============

'plot_profile' is a Python-based command line tool to retrieve and visualise observational data from radiousounding measurements.

Usage
--------
To get a list of all availabe commands, just type:
``plot_profile --help``.

Features
--------

* TODO hello hello

+--------------+------+-----------------------------------------------------------------+--------------------------------------------------+
| flag         | type | description                                                     | default                                          |
+==============+======+=================================================================+==================================================+
| --station-id | str  | station ID [XXXXX]                                              | 06610 (Payerne)                                  |
+--------------+------+-----------------------------------------------------------------+--------------------------------------------------+
| --date       | str  | date of interest [YYYYMMDDHH]                                   | 2021083100                                       |
+--------------+------+-----------------------------------------------------------------+--------------------------------------------------+
| --alt_bot    | int  | lower boundary for altitude                                     | elevation of radiosounding station               |
+--------------+------+-----------------------------------------------------------------+--------------------------------------------------+
| --alt_top    | int  | upper boundary for altitude                                     | 10% over max altitude of radiosounding retrieval |
+--------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|| --params    || str || physical quantities of interest                                || all of them; hint: add multiple params like:    |
||             ||     || possible values: 743/winddir, 745/temp, 747/dewp, 748/windvel) || --params 743 --params temp                      |
+--------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|              |      |                                                                 |                                                  |
+--------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|              |      |                                                                 |                                                  |
+--------------+------+-----------------------------------------------------------------+--------------------------------------------------+





..
    Usage: plot_profile [OPTIONS]

    Options:
    --station_id TEXT               station ID: XXXXX - def: 06610
    --date TEXT                     start date: YYYYMMDDHH - def: 2021083100
    --alt_bot INTEGER               altitude bottom value: int - def: elevation
                                    of radiosounding station
    --alt_top INTEGER               altitude top value: int - def: 10% over max
                                    altitude of radiosounding retrieval
    --params [743|winddir|745|temp|747|dewp|748|windvel]
                                    Default: all
    --outpath TEXT                  path to folder where the plots should be
                                    saved - def: plots/
    --grid                          Show grid on plot - def: False
    --clouds                        Show clouds on plot - def: True
    --relhum_thresh FLOAT           Define the relative humidity threshold for
                                    clouds - def: 80
    --print_steps                   Add this flag to display intermediate steps.
    --standard_settings             temp_range: -100-30 [°C], windvel_range:
                                    0-50 [km/h]
    --personal_settings             If this flag is added, personal 'standard'
                                    settings can be defined using the
                                    temp_min/max and windvel_min/max flags
    --temp_min FLOAT                Define the minimum temperature. Disclaimer:
                                    Add --personal_settings flag!
    --temp_max FLOAT                Define the maximum temperature. Disclaimer:
                                    Add --personal_settings flag!
    --windvel_min FLOAT             Define the minimum windvelocity. Disclaimer:
                                    Add --personal_settings flag!
    --windvel_max FLOAT             Define the maximum windvelocity. Disclaimer:
                                    Add --personal_settings flag!
    --help                          Show this message and exit.

Credits
-------

This package was created with `Cookiecutter`_ and the `MeteoSwiss-APN/mch-python-blueprint`_ project template.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`MeteoSwiss-APN/mch-python-blueprint`: https://github.com/MeteoSwiss-APN/mch-python-blueprint
