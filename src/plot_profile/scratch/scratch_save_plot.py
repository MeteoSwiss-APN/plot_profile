"""Script to retrieve username and save plots in /scratch/user/tmp."""
# Standard library
import getpass
from pathlib import Path

# Third-party
import matplotlib.pyplot as plt


def save_fig(filename, datatypes, outpath, fig=None):
    """Save current figure at outpath. Create outpath if it doesn't exist or default to /scratch/<user>/tmp/.

    Args:
        filename:       str     Name of File.
        datatypes:      tuple   Tuple containig the desired output file types
        outpath:        str     Path to output directory
        fig:            Figure  Figure which should be saved. If None, get current figure.

    """
    fig = fig or plt.gcf()

    if not outpath:
        for datatype in datatypes:
            username = getpass.getuser()
            filepath = Path(f"/scratch/{username}/tmp/{filename}.{datatype}")
            Path(filepath).parents[0].mkdir(parents=True, exist_ok=True)
            plt.savefig(filepath)

        return
    else:
        for datatype in datatypes:
            filepath = Path(f"{outpath}/{filename}.{datatype}")
            Path(filepath).parents[0].mkdir(parents=True, exist_ok=True)
            plt.savefig(filepath)
            print(f"Path to file:\t{filepath}")
        return
