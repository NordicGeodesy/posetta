# Posetta, the Universal Translator of Geodetic Coordinate File Formats

Posetta is a command line and GUI utility for translating between different
file formats used for representing geodetic coordinates.

**Note:** Posetta is still in pre-alpha status. Its functionality will change,
  and it should not be depended on in any production-like setting.

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)


## Installing Posetta

Posetta is available at [PyPI](https://pypi.org/project/posetta/). You can
install it by simply running

    pip install posetta


## Installing Posetta from source

Posetta depends on other brilliant Python packages, like for instance numpy. We
recommend using the Anaconda distribution to ease the installation of these
dependencies.

### Install Anaconda

Go to [www.anaconda.com/download](https://www.anaconda.com/download), and
download Anaconda for Python 3.


### Download the Posetta source code

If you have not already done so, download the Posetta source code, from
[GitHub](https://github.com/NordicGeodesy/posetta). Then enter the main
`posetta` directory before running the install commands below.

    cd posetta


### Install dependencies

You should now install the necessary dependencies using the
`environment.yml`-file. You can do this either in your current conda
environment, or choose to create a new `posetta`-environment. In general, you
should install `posetta` in its own environment.

To install `posetta` in a new environment named `posetta` and activate it, do

    conda env create -n posetta -f environment.yml
    conda activate posetta

To instead install `posetta` in your current environment, do

    conda env update -f environment.yml


### Install the Posetta package

To do the actual installation of Posetta, use the `flit` packaging tool:

    flit install --dep production

If you want to develop the Posetta package, install it in editable mode using

    flit install -s

On Windows, you can install in editable mode using

    flit install --pth-file


## Using Posetta

Posetta can be used either as a command line application, or a graphical (GUI)
application.


### Posetta at the command line



### Posetta as a graphical (GUI) application



