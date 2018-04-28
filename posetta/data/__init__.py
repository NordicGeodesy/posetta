"""Coordinate dataset

The CoordSet is a data structure that is used internally when translating
between different coordinate data formats.

"""

from collections import namedtuple


# Temporary definition of CoordSet
CoordSet = namedtuple("CoordSet", ["epochs", "positions", "velocities"])
