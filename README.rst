============
plot_profile
============

*plot_profile* is a Python-based command line tool to retrieve and visualise observational data from radiousounding measurements.

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

  a) ``plot_rs``: plot radiousounding
  b) ``plot_icon``: plot vertical profiles of variables from ICON simulations


Example command:
``plot_icon --date 21111012 --folder /scratch/swester/output_icon/ICON-1/ --var qv --var temp --var qc --leadtime 12 --leadtime 13``

Credits
-------

This package was created with `Cookiecutter`_ and the `MeteoSwiss-APN/mch-python-blueprint`_ project template.

.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`MeteoSwiss-APN/mch-python-blueprint`: https://github.com/MeteoSwiss-APN/mch-python-blueprint
