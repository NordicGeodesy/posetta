"""Posetta, translating between different position formats

Posetta is a command line and GUI utility for translating between different
file formats used for representing points and possibly velocities.

See README.md and __main__.py for more information.
"""

# Standard library imports
from datetime import date as _date
from collections import namedtuple as _namedtuple


# Version of Posetta
#
# This is automatically set using the bumpversion script
__version__ = "0.0.1"


# Start of development
_birthday = _date(2018, 4, 20)


# Maintainers of Posetta
_Author = _namedtuple("_Author", ["name", "email", "start", "end"])
_AUTHORS = [
    _Author("Geir Arne Hjelle", "geir.arne.hjelle@kartverket.no", _birthday, _date.max),
    _Author("Kristian Evers", "kbevers@sdfe.dk", _birthday, _date.max),
]

__author__ = ", ".join(a.name for a in _AUTHORS if a.start < _date.today() < a.end)
__contact__ = ", ".join(a.email for a in _AUTHORS if a.start < _date.today() < a.end)
__url__ = "https://github.com/NordicGeodesy/posetta"


# Copyleft of the library
__copyright__ = f"{_birthday.year} - {_date.today().year} Nordic Geodetic Commision"
