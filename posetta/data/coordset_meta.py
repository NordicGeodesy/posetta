"""Coordinate dataset meta-information

Description:
------------

"""

# Standard library imports
from typing import Dict, Tuple

# Third party imports

# Posetta imports


class CoordSetMeta:
    """Coordinate Dataset Metainformation


    Attributes:
        fields:   Fields in CoordSet
    """

    def __init__(self) -> None:
        """Set up fields for the CoordSetMeta
        """
        pass

    def __repr__(self) -> str:
        """A simple string representation of the reader
        """
        return f"{self.__class__.__name__}()"
