"""Basic functionality for reading datafiles, extended by individual readers

Description:
------------

This module contains an abstract base class that can be extended for reading data files
in Posetta.
"""

# Standard library imports
import pathlib
from typing import Any, Dict, List, Union

# Third party imports
import pandas as pd

# Posetta imports
from posetta import data


class Reader:
    """An abstract base class that has basic methods for reading a datafile

    This class provides functionality for reading a file. You should inherit from one of
    the specific readers like for instance ChainReader, LineReader, SinexReader etc

    Attributes:
        file_path: Union[str, pathlib.Path] - Path to the datafile that will be read.
        reader_name: str                    - Name of the reader (module).
        data: Dict[str, Any]                - The coordinate data read from file.
        meta: Dict[str, Any]                - Metainformation read from file.
    """

    def __init__(self, file_path: Union[str, pathlib.Path]) -> None:
        """Set up the basic information needed by the reader

        Args:
            file_path:    Path to file that will be read.
        """
        self.file_path = pathlib.Path(file_path)
        self.reader_name = self.__module__.split(".")[-1]

        # Initialize the data
        self.meta: Dict[str, Any] = dict(
            __reader_name__=self.reader_name, __data_path__=self.file_path
        )
        self.data: Dict[str, Any] = dict()

    def setup_reader(self) -> None:
        """Set up a reader so that it can read data from a file.
        """
        pass

    def read(self) -> "Reader":
        """Read data

        This is a basic implementation that carries out the whole pipeline of reading
        datafiles.

        Subclasses should typically implement (at least) the `read_data`-method.
        """
        self.setup_reader()
        self.read_data()
        return self

    def read_data(self) -> None:
        """Read data from the data file

        Data should be read from `self.file_path` and stored in the dictionary
        `self.data`. A description of the data may be placed in the dictionary
        `self.meta`. If the file is not found, a FileNotFoundError should be raised.
        """
        raise NotImplementedError

    def as_dict(self, include_meta: bool = False) -> Dict[str, Any]:
        """Return the data as a dictionary

        Args:
            include_meta:   Include meta-data in the returned dict?

        Returns:
            The data that has been read as a dictionary.
        """
        return dict(self.data, __meta__=self.meta) if include_meta else self.data.copy()

    def as_dataframe(self, index: Union[str, List[str]] = None) -> pd.DataFrame:
        """Return the data as a Pandas DataFrame

        This is a basic implementation, assuming the `self.data`-dictionary has a simple
        structure. More advanced readers may need to reimplement this method.

        Args:
            index:      Name of field to use as index. May also be a list of strings.

        Returns:
            The data that has been read as a DataFrame.
        """
        df = pd.DataFrame.from_dict(self.data)
        if index is not None:
            df.set_index(index, drop=True, inplace=True)

        return df

    def as_coordset(self) -> data.CoordSet:
        """Return the data as a coordinate dataset

        This is a basic implementation, assuming the `self.data`-dictionary has a simple
        structure. More advanced readers may need to reimplement this method.

        Returns:
            The data that has been read as a coordinate dataset.
        """
        return data.CoordSet(1, 2, 3)
