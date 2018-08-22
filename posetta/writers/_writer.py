"""Basic functionality for writing datafiles, extended by individual writers

Description:
------------

This module contains an abstract base class that can be extended for writing data files
in Posetta.
"""

# Standard library imports
import pathlib
from typing import Union

# Third party imports

# Posetta imports
from posetta import data
from posetta.lib import exceptions


class Writer:
    """An abstract base class that has basic methods for writing a datafile

    This class provides functionality for writing a file. You should inherit from one of
    the specific writers like for instance ChainWriter, LineWriter, SinexWriter etc

    Attributes:
        file_path: Union[str, pathlib.Path] - Path to the datafile that will be written.
        writer_name: str                    - Name of the writer (module).
    """

    def __init__(
        self, file_path: Union[str, pathlib.Path], cset: data.CoordSet
    ) -> None:
        """Set up the basic information needed by the writer

        Args:
            file_path:    Path to file that will be written.
            cset:         Data that will be written
        """
        self.file_path = pathlib.Path(file_path)
        self.data = cset
        self.writer_name = self.__module__.split(".")[-1]

    def setup_writer(self) -> None:
        """Set up a writer so that it can write data to a file.
        """
        pass

    def write(self) -> None:
        """Write data

        This is a basic implementation that carries out the whole pipeline of writing
        datafiles.

        Subclasses should typically implement (at least) the `write_data`-method.
        """
        self.setup_writer()
        if self.data.num_obs:
            self.write_data()
        else:
            raise exceptions.WriterError("Input dataset is empty")

    def write_data(self) -> None:
        """Write data to the data file

        Data should be write to `self.file_path` and stored in the dictionary
        `self.data`. A description of the data may be placed in the dictionary
        `self.meta`. If the file is not found, a FileNotFoundError should be raised.
        """
        raise NotImplementedError(f"{self.writer_name} must implement write_data()")

    def __repr__(self) -> str:
        """A simple string representation of the writer
        """
        return f"{self.__class__.__name__}('{self.file_path}')"
