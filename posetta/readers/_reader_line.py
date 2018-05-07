"""Basic functionality for reading datafiles line by line using Numpy

Description:
------------

Read file formats that contain data in nicely formatted columns in text files.
"""

# Standard library imports
import pathlib
from typing import Union

# Third party imports
import numpy as np

# Posetta imports
from posetta.lib import exceptions
from posetta.readers._reader import Reader


class LineReader(Reader):
    """An abstract base class that has basic methods for reading a datafile

    This class provides functionality for using numpy to read a file line by line. You
    should inherit from this one, and at least specify the necessary parameters in
    `setup_reader`.
    """

    def __init__(self, file_path: Union[str, pathlib.Path]) -> None:
        """Set up the basic information needed by the Reader

        Add a self._array property for the raw numpy array data.

        Args:
            file_path):    Path to file that will be read.
        """
        super().__init__(file_path)
        self._array = None

    def setup_reader(self) -> None:
        """Set up information needed for the reader

        This method must create a dictionary at `self.meta["__params__"]` containing all
        parameters needed by np.genfromtxt to do the actual reading.
        """
        raise NotImplementedError(f"{self.reader_name} must implement setup_reader()")

    def read_data(self) -> None:
        """Read data from the data file

        Uses the np.genfromtxt-function to read the file. Any necessary parameters
        should be returned by `setup_reader`. See `self.structure_data` if the
        self.data-dictionary needs to be structured in a particular way.
        """
        if "__params__" not in self.meta:
            raise exceptions.ReaderError(
                f"{self.__class__.__name__} is not properly set up."
            )

        self._array = np.genfromtxt(self.file_path, **self.meta["__params__"])
        self.structure_data()

    def structure_data(self) -> None:
        """Structure raw array data into the self.data dictionary

        This simple implementation creates a dictionary with one item per column in the
        array. Override this method for more complex use cases.
        """
        if self._array is None:
            raise exceptions.ReaderError(
                f"No data found in {type(self)}. Have you called read_data() yet?"
            )

        for name in self._array.dtype.names:
            self.data[name] = self._array[name]
