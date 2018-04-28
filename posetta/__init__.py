"""Posetta, translating between different position formats

Posetta is a command line and GUI utility for translating between different
file formats used for representing points and possibly velocities.

"""
# Standard library imports
from datetime import date as _date
from collections import namedtuple as _namedtuple


# Version of Posetta.
#
# This is automatically set using the posetta_release-script
__version__ = "0.0.1"


# Authors of Posetta.
_Author = _namedtuple("_Author", ["name", "email", "start", "end"])
_Author.__new__.__defaults__ = ("", "", _date(2018, 4, 1), _date.max)

_AUTHORS = sorted(
    [_Author("Geir Arne Hjelle", "geir.arne.hjelle@kartverket.no")],
    key=lambda a: a.name.split()[-1],
)  # Sort on last name

__author__ = ", ".join(a.name for a in _AUTHORS if a.start < _date.today() < a.end)
__contact__ = ", ".join(a.email for a in _AUTHORS if a.start < _date.today() < a.end)


# Copyright of the library
__copyright__ = "2018 - {} NKG".format(_date.today().year)
