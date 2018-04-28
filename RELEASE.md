# Make a New Release of Posetta

The following explains the steps of releasing Posetta to GitHub and PyPI. All
official versions of Posetta should be released to GitHub and PyPI.


# Prerequisites

You need to have set up GitHub as explained below. This is only necessary to do
once.

## Set up a GitHub fork of Posetta

You should develop in your personal fork of Posetta, and send Pull Requests to
the main Posetta repository at https://github.com/NordicGeodesy/posetta. To
create a fork, you need to be logged into your GitHub-account. Then go to
https://github.com/NordicGeodesy/posetta and click the `Fork` button in the
upper right hand corner.


## Clone Posetta to Your Computer

Next create a clone of your fork of Posetta on your computer. Go to your
personal fork of Posetta on GitHub. It should be at
https://github.com/your_username/posetta. Then click the green `Clone or
download` button and copy the URL.

On your computer, open a (git) terminal and write

    git clone <URL>

This will clone your fork of Posetta to your computer. See README.md for how to
install Posetta.


# Make a Release


## Bump the Version of Posetta

Versioning should be done according to the principles of Semantic Versioning,
http://semver.org/ See also PEP 440, https://www.python.org/dev/peps/pep-0440/ -
Version Identification and Dependency Specification.

Use the `bumpversion` script to move Posetta to a new version. `bumpversion`
takes one argument, `part` which should be one of `major`, `minor` and `patch`:

    bumpversion --verbose major      # Incompatible API changes
    bumpversion --verbose minor      # New functionality, backwards-compatible
    bumpversion --verbose patch      # Backwards-compatible bug fixes

In the examples below, we use 7.8.9 as the new version number. Replace 7.8.9
with the actual new version number.


## Push Updated Code to GitHub and Create a Pull Request

Bumpversion updates a few files with the latest version number. Make sure you
commit these changes before releasing.

    git checkout -b release_7.8.9
    git add .
    git commit -m "Release v7.8.9"
    git push origin release_7.8.9

Create a Pull Request.

## Create a Tag on GitHub

On Posettas GitHub-page,
[github.com/kartverket/posetta](https://github.com/kartverket/posetta/), click
`Release` in the header line. Then choose `Draft a new release`. Add version
number (`v7.8.9`) and a description of the release. Finally click the `Publish
release`-button.


## Publish to PyPI

From the Posetta-Git folder, do

    flit publish

You can check that Posetta has been released at the PyPI-page for the project,
https://pypi.org/project/posetta/


# Updating Code to use the Latest Version


## GitHub

Check out the latest tag from GitHub: (TODO)



## PyPI

Update your version of Posetta using `pip`:

    pip install --upgrade posetta
