============
plot_profile
============

'plot_profile' is a Python-based command line tool to retrieve and visualise observational data from radiousounding measurements.

Usage
--------
To get a list of all availabe commands, just type:
``plot_profile --help``.
General usage: ``plot_profile [options]``

+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
| options                   | type | description                                                     | default                                          |
+===========================+======+=================================================================+==================================================+
| --station-id              | str  | station ID [XXXXX]                                              | 06610 (Payerne)                                  |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
| --date                    | str  | date of interest [YYYYMMDDHH]                                   | 2021083100                                       |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
| --alt_bot                 | int  | lower boundary for altitude                                     | elevation of radiosounding station               |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
| --alt_top                 | int  | upper boundary for altitude                                     | 10% over max altitude of radiosounding retrieval |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|| --params                 || str || physical quantities of interest                                || all of them; hint: add multiple params like:    |
||                          ||     || possible values: 743/winddir, 745/temp, 747/dewp, 748/windvel) || --params 743 --params temp   --params windvel   |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|| --outpath                || str || path to folder where plots should be saved                     || plots/                                          |
||                          ||     || (directory is created, if it doesn't exist already)            ||                                                 |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|  --grid                   | bool | add grid                                                        | if_flag = True                                   |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|  --clouds                 | bool | add clouds                                                      | if_flag = True                                   |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|  --relhum_thresh          | int  | relative humidity threshold to show clouds                      | 80%                                              |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|  --print_steps            | bool | print intermediate steps (i.e. for debugging)                   | if_flag = True                                   |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|| --standard_settings      || bool|| use pre-defined standard settings                              || temp_range: -100-30 [°C], windvel_range:        |
||                          ||     || (i.e. to compare days more easily)                             ||  0-50 [km/h]. if_flag = True                    |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|  --personal_settings      | bool | define personal axis limits                                     | if_flag = True                                   |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|  --temp_min               | float| mininum temperature                                             | none                                             |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|  --temp_max               | float| maximum temperature                                             | none                                             |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|  --windvel_min            | float| minimum wind velocity                                           | none                                             |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+
|  --windvel_max            | float| maximum wind velocity                                           | none                                             |
+---------------------------+------+-----------------------------------------------------------------+--------------------------------------------------+


Credits
-------

This package was created with `Cookiecutter`_ and the `MeteoSwiss-APN/mch-python-blueprint`_ project template.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`MeteoSwiss-APN/mch-python-blueprint`: https://github.com/MeteoSwiss-APN/mch-python-blueprint
