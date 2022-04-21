"""Purpose: define command line inputs.

Author: Michel Zeller

Date: 09/03/2022.
"""

# Standard library
from pprint import pprint

# Third-party
import click

# First-party
from plot_profile.plot_profiles.get_profiles import get_data
from plot_profile.plot_profiles.get_profiles import parse_inputs
from plot_profile.plot_profiles.plot_profiles import create_plot


@click.command()
# MANDATORY: date, loc
@click.option(
    "--date",
    default=click.DateTime("21111812"),
    type=click.DateTime(formats=["%y%m%d%H"]),
    help="MANDATORY: Init date of icon simulation: YYMMDDHH.",
)
@click.option(
    "--loc", default="pay", type=str, help="MANDATORY: Name of location. Def: pay"
)
# ADD MODELS AND OBSERVATIONS TO PLOT W/: add_model, model_src, add_obs
@click.option(
    "--add_model",
    type=(str, str, str),
    multiple=True,
    help="Specify which model/variable/model_id should be added to plot.",
)
@click.option(
    "--model_src",
    type=(str, click.Path(exists=True), click.DateTime(formats=["%y%m%d%H"])),
    multiple=True,
    help="Specify for each model ID, one source flag. I.e. <model_id> <folder> <init>",
)
@click.option(
    "--add_obs",
    type=(str, str),
    multiple=True,
    help="Specify which device/variable should be added to plot.",
)
@click.option(
    "--grid_file",
    type=str,
    default="/store/s83/swester/grids/HEIGHT_ICON-1E.nc",
    help="Icon file containing HEIGHT field. Def: ICON-1E operational 2021",
)
# AXES LIMITS (optional): ymin, ymax, xmin, xmax
@click.option(
    "--ymin",
    type=float,
    multiple=False,
    help="Minimum value of y-axis/axes. Def: Fits values.",
)
@click.option(
    "--ymax",
    default=5000,
    type=float,
    multiple=False,
    help="Maximum value of y-axis/axes. Def: Fits values.",
)
@click.option(
    "--xmin",
    type=float,
    multiple=True,
    help="Minimum value of x-axis/axes. Def: Fits values.",
)
@click.option(
    "--xmax",
    type=float,
    multiple=True,
    help="Maximum value of x-axis/axes. Def: Fits values.",
)
# OTHERS: appendix, datatypes, grid, outpath,
@click.option(
    "--appendix", type=str, help="String to append to output filename. Def: None"
)
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
    is_flag=True,
    default=False,
    help="Add grid to plot.",
)
@click.option(
    "--show_marker",
    is_flag=True,
    default=False,
    help="Add marker to model plots. Default: d (diamond)",
)
@click.option(
    "--outpath",
    type=str,
    help="Path to folder where the plots should be saved. Def: /scratch/USER/tmp",
)
@click.option(
    "--verbose",
    is_flag=True,
    default=False,
    help="Output details on what is happening.",
)
@click.option("--colours", multiple=True, help="Overwrite default colours.")
def main(
    *,
    # Mandatory
    date: click.DateTime,
    loc: str,
    # Models, Devices and Variables
    add_model: tuple,
    model_src: tuple,
    add_obs: tuple,
    grid_file: str,
    # Axes Limits
    ymin: float,
    ymax: float,
    xmin: tuple,
    xmax: tuple,
    # Various
    colours: tuple,
    appendix: str,
    grid: bool,
    show_marker: bool,
    datatypes: tuple,
    outpath: str,
    verbose: bool,
):
    """Plot vertical profiles.

    Example:
        plot_profiles --loc pay --date 21111900 --add_obs rs temp --add_model icon temp ref --add_model icon temp exp --model_src ref /scratch/swester/output_icon/ICON-1/ 21111812 --model_src exp /scratch/swester/output_icon/exp1/ 21111812

    """
    elements, multi_axes = parse_inputs(loc, add_model, add_obs, model_src, verbose)

    if verbose and multi_axes:
        print("Employing two different axes: Bottom and Top.")

    data_dict, lt_dict = get_data(
        date=date,
        loc=loc,
        grid=grid_file,
        ylims=(ymin, ymax),
        elements=elements,
        verbose=verbose,
    )

    create_plot(
        data_dict=data_dict,
        lt_dict=lt_dict,
        date=date,
        location=loc,
        xlims=(xmin, xmax),
        ylims=(ymin, ymax),
        colours=colours,
        show_marker=show_marker,
        grid=grid,
        appendix=appendix,
        datatypes=datatypes,
        outpath=outpath,
        multi_axes=multi_axes,
        verbose=verbose,
    )

    return
