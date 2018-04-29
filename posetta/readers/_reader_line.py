"""Basic functionality for reading datafiles line by line using Numpy

Description:
------------

Read file formats that contain data in nicely formatted columns in text files.
"""

# Standard library imports
import pathlib
from typing import Any, Dict, Union

# Third party imports
import numpy as np

# Posetta imports
from posetta.readers._reader import Reader


class LineReader(Reader):
    """An abstract base class that has basic methods for reading a datafile

    This class provides functionality for using numpy to read a file line by line. You should inherit from this one,
    and at least specify the necessary parameters in `setup_reader`.
    """

    def __init__(self, file_path: Union[str, pathlib.Path]) -> None:
        """Set up the basic information needed by the Reader

        Add a self._array property for the raw numpy array data.

        Args:
            file_path):    Path to file that will be read.
        """
        super().__init__(file_path)
        self._array = None

    def setup_reader(self) -> Dict[str, Any]:
        """Set up information needed for the reader

        This should return a dictionary with all parameters needed by np.genfromtxt to do the actual reading.

        Returns:
            Parameters needed by np.genfromtxt to read the input file.
        """
        raise NotImplementedError

    def read_data(self) -> None:
        """Read data from the data file

        Uses the np.genfromtxt-function to read the file. Any necessary parameters should be returned by
        `setup_reader`. See `self.structure_data` if the self.data-dictionary needs to be structured in a particular
        way.
        """
        self.meta["__params__"] = self.setup_reader()
        self._array = np.genfromtxt(self.file_path, **self.meta["__params__"])
        self.structure_data()

    def structure_data(self) -> None:
        """Structure raw array data into the self.data dictionary

        This simple implementation creates a dictionary with one item per column in the array. Override this method for
        more complex use cases.
        """
        for name in self._array.dtype.names:
            self.data[name] = self._array[name]
