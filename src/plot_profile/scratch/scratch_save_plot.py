"""Script to retrieve username and save plots in /scratch/user/tmp."""
# Standard library
import getpass
from pathlib import Path

# Third-party
import matplotlib.pyplot as plt


def save_fig(filename, filetype, fig=None):
    print(f"In save_fig function.")
    fig = fig or plt.gcf()
    username = getpass.getuser()
    filepath = f"/scratch/{username}/tmp/{filename}.{filetype}"
    plt.savefig(filepath)
    print(f"saved plot @ {filepath}")
    return


if __name__ == "__main__":
    print(Path.cwd())
