"""Basic functionality for reading datafiles, extended by individual readers

Description:
------------

This module contains an abstract base class that can be extended for reading data files
in Posetta.
"""

# Standard library imports
import codecs
from typing import Any, Dict, IO, List, Union

# Third party imports
import pandas as pd

# Posetta imports
from posetta import data


class Reader:
    """An abstract base class with basic methods for reading a datafile

    This class provides functionality for reading a file. You should
    inherit from one of the specific readers like for instance
    ChainReader, LineReader, SinexReader etc

    Attributes:
        input_stream: IO[str]    - Stream that input is read from.
        reader_name: str         - Name of the reader (module).
        data: Dict[str, Any]     - The coordinate data read from file.
        meta: Dict[str, Any]     - Metainformation read from file.
        file_path: str           - Name of datafile being read.
        encoding: str            - Encoding used when reading.

    """

    def __init__(self, input_stream: IO[bytes], encoding: str = "utf-8") -> None:
        """Set up the basic information needed by the reader

        Args:
            input_stream:  Byte stream that will be read.
            encoding:      Encoding of input stream.
        """
        self.input_stream = codecs.getreader(encoding)(input_stream)
        self.encoding = encoding
        self.reader_name = self.__module__.split(".")[-1]

        try:
            self.file_path = input_stream.name
        except AttributeError:
            self.file_path = "<unknown>"

        # Initialize the data
        self.meta: Dict[str, Any] = dict(
            __reader_name__=self.reader_name,
            __source_path__=self.file_path,
            __source_encoding__=encoding,
        )
        self.data: Dict[str, Any] = dict()

    def setup_reader(self) -> None:
        """Set up a reader so that it can read data from a file.

        This method may be overwritten if a reader needs to do some
        preparatory work.
        """
        pass

    def read(self) -> None:
        """Read data

        This is a basic implementation that carries out the whole
        pipeline of reading datafiles.

        Subclasses should typically implement (at least) the
        `read_data`-method.
        """
        self.setup_reader()
        self.read_data()

    def read_data(self) -> None:
        """Read data from the data file

        Data should be read from `self.input_stream` and stored in the
        dictionary `self.data`. A description of the data may be placed
        in the dictionary `self.meta`.
        """
        raise NotImplementedError(f"{self.reader_name} must implement read_data()")

    def as_dict(self, include_meta: bool = False) -> Dict[str, Any]:
        """Return the data as a dictionary

        Args:
            include_meta:   Include meta-data in the returned dict?

        Returns:
            The data that has been read as a dictionary.
        """
        return dict(self.data, __meta__=self.meta) if include_meta else self.data.copy()

    def as_dataframe(self, index: Union[None, str, List[str]] = None) -> pd.DataFrame:
        """Return the data as a Pandas DataFrame

        This is a basic implementation, assuming the `self.data`
        dictionary has a simple structure. More advanced readers may
        need to reimplement this method.

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

        Returns:
            The data that has been read as a coordinate dataset.
        """
        raise NotImplementedError(f"{self.reader_name} must implement as_coordset()")

    def __repr__(self) -> str:
        """A simple string representation of the reader
        """
        return f"{self.__class__.__name__}('{self.file_path}')"
