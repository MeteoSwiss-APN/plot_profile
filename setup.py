"""Set up the project."""
# Standard library
from typing import List
from typing import Sequence

# Third-party
from pkg_resources import parse_requirements
from setuptools import find_packages
from setuptools import setup


def read_present_files(paths: Sequence[str]) -> str:
    """Read the content of those files that are present."""
    contents: List[str] = []
    for path in paths:
        try:
            with open(path, "r") as f:
                contents += ["\n".join(map(str.strip, f.readlines()))]
        except FileNotFoundError:
            continue
    return "\n\n".join(contents)


description_files = [
    "README",
    "README.rst",
    "README.md",
    "HISTORY",
    "HISTORY.rst",
    "HISTORY.md",
]

metadata = {
    "name": "plot_profile",
    "version": "0.1.1",
    "description": "Plot radiosounding profiles [to be continued]",
    "long_description": read_present_files(description_files),
    "author": "Michel Zeller",
    "author_email": "michel.zeller@meteoswiss.ch",
    "url": "https://github.com/mizeller/plot_profile",
    "keywords": "plot_profile",
    "classifiers": [
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
}

python = ">= 3.7"

# Runtime dependencies (unpinned: only critical version restrictions)
with open("requirements/requirements.in") as f:
    requirements = list(map(str, parse_requirements(f.readlines())))

scripts = [
    "plot_profile=plot_profile.cli:main",  # main, no plotting routines attached
    "plot_rs=plot_profile.plot_rs.cli_rs:main",
    "plot_icon_profiles=plot_profile.plot_icon.cli_icon_profiles:main",
    "plot_icon_heatmap=plot_profile.plot_icon.cli_icon_heatmap:main",
    "plot_mwr_heatmap=plot_profile.plot_mwr.cli_mwr_heatmap:main",
    "plot_timeseries=plot_profile.plot_timeseries.cli_timeseries:main",
    "plot_profiles=plot_profile.plot_profiles.cli_profiles:main",
]

setup(
    python_requires=python,
    install_requires=requirements,
    entry_points={"console_scripts": scripts},
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_save=False,
    **metadata,
)
