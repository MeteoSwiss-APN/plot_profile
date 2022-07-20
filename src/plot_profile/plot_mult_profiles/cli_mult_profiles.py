"""Purpose: define command line inputs for plot_mult_profiles.

Author: Arthur Dandoy

Date: 03/05/2022.
"""

# Standard library

# Third-party
import click

# First-party
from plot_profile.plot_mult_profiles.get_mult_profiles import get_mult_data
from plot_profile.plot_mult_profiles.get_mult_profiles import parse_inputs
from plot_profile.plot_mult_profiles.plot_mult_profiles import create_mult_plot

# from ipdb import set_trace


@click.command()
# options without default value (mandatory to specify by user)
@click.option(
    "--init",
    type=click.DateTime(formats=["%y%m%d%H"]),
    help="MANDATORY: Init date of model. Reference date from which leadtimes are determined. I.e. <%y%m%d%H> ex: 21111812",
)
@click.option(
    "--variable",
    type=str,
    help="MANDATORY: Specify variable name.",
)
# add model output to plot ! ex: arome, icon
@click.option(
    "--add_model",
    required=False,
    type=str,
    help="Model name (ex: arome, icon)",
)
@click.option(
    "--model_src",
    required=False,
    type=click.Path(exists=True),
    help="Specify for each model ID, one source flag. I.e. <folder>",
)
# add observation to plot ! ex: rs, mwr, lidar...
@click.option(
    "--add_obs",
    type=str,
    multiple=True,
    help="Specify which device should be added to plot.",
)
@click.option(
    "--leadtime",
    type=int,
    multiple=True,
    default=(0,),
    help="Leadtime(s) to be shown in one plot. Def: 0.",
)
# options with default value
@click.option(
    "--grid_file",
    type=str,
    default="/store/s83/swester/grids/HEIGHT_ICON-1E.nc",
    help="Icon file containing HEIGHT field. Def: ICON-1E operational 2021",
)
@click.option("--ymin", type=int, help="Altitude bottom. Def: surface.")
@click.option("--ymax", default=2000, type=int, help="Altitude top. Def: 2000")
@click.option(
    "--datatypes",
    type=click.Choice(
        [
            "eps",
            "jpeg",
            "jpg",
            "pdf",
            "pgf",
            "png",
            "ps",
            "raw",
            "rgba",
            "svg",
            "svgz",
            "tif",
            "tiff",
        ],
        case_sensitive=True,
    ),
    multiple=True,
    default=[
        "png",
    ],
    help="Choose data type(s) of final result. Def: png",
)
@click.option(
    "--grid",
    type=str,
    default="/store/s83/swester/grids/HEIGHT_ICON-1E.nc",
    help="Icon file containing HEIGHT field. Def: ICON-1E operational 2021",
)
# @click.option("--lat", type=float, help="Latitude of location.")
# @click.option("--lon", type=float, help="Longitude of location.")
@click.option("--loc", type=str, help="Name of location.")
@click.option(
    "--outpath",
    type=str,
    help="Path to folder where the plots should be saved. Def: /scratch/USER/tmp",
)
@click.option(
    "--grid",
    is_flag=True,
    help="Show grid on plot. Flag, def: False",
)
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Output details on what is happening.",
)
@click.option(
    "--xmin",
    type=float,
    multiple=True,
    help="Minimum value of xaxis. Def: Fits values.",
)
@click.option(
    "--xmax",
    type=float,
    multiple=True,
    help="Maximum value of xaxis. Def: Fits values.",
)
def main(
    init: click.DateTime,
    variable: str,
    add_model: str,
    model_src: str,
    leadtime: tuple,
    add_obs: tuple,
    grid_file: str,
    ymin: int,
    ymax: int,
    datatypes: tuple,
    # ind: int,
    # lat: float,
    # lon: float,
    loc: str,
    outpath: str,
    grid: bool,
    verbose: bool,
    xmin: tuple,
    xmax: tuple,
):
    """Plot vertical profiles of variables from icon, arome simulations or observations.

    Example command:
    plot_mult_profiles --init 21111812 --loc pay --variable temp --add_model icon --model_src
    /scratch/swester/output_icon/ICON-1/ --leadtime 12 --leadtime 14 --leadtime 16 --grid

    Model output is expected to be in netcdf-format in a sub-folder named after the given date.

    """
    # check inputs
    parse_inputs(variable, add_model, model_src, add_obs, loc, verbose)

    data_dict = get_mult_data(
        init=init,
        variable=variable,
        model=add_model,
        model_src=model_src,
        add_obs=add_obs,
        leadtimes=leadtime,
        loc=loc,
        grid=grid_file,
        ylims=(ymin, ymax),
        verbose=verbose,
    )

    # pprint(data_dict)

    create_mult_plot(
        data_dict=data_dict,
        variable=variable,
        leadtimes=leadtime,
        date_ref=init,
        location=loc,
        xlims=(xmin, xmax),
        ylims=(ymin, ymax),
        grid=grid,
        datatypes=datatypes,
        outpath=outpath,
        verbose=verbose,
    )

    print("--- done")
