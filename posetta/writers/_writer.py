"""Basic functionality for writing datafiles, extended by individual writers

Description:
------------

This module contains an abstract base class that can be extended for writing data files
in Posetta.
"""

# Standard library imports
import codecs
from typing import IO

# Third party imports

# Posetta imports
from posetta import data
from posetta.lib import exceptions


class Writer:
    """An abstract base class that has basic methods for writing a datafile

    This class provides functionality for writing a file. You should inherit from one of
    the specific writers like for instance ChainWriter, LineWriter, SinexWriter etc

    Attributes:
        output_stream: IO[str]    - Stream that output is written to.
        data: data.CoordSet       - The coordinate data to be written.
        writer_name: str          - Name of the writer (module).
        file_path: str            - Name of the datafile that will be written.
        encoding: str             - Encoding of output file.
    """

    def __init__(
        self, output_stream: IO[bytes], cset: data.CoordSet, encoding: str = "utf-8"
    ) -> None:
        """Set up the basic information needed by the writer

        Args:
            output_stream:  Byte stream to write to.
            cset:           Data that will be written.
            encoding:       Encoding used when writing data.
        """
        self.output_stream = codecs.getwriter(encoding)(output_stream)
        self.data = cset
        self.encoding = encoding
        self.writer_name = self.__module__.split(".")[-1]

        try:
            self.file_path = output_stream.name
        except AttributeError:
            self.file_path = "<unknown>"

    def setup_writer(self) -> None:
        """Set up a writer so that it can write data to a file.

        This method may be overwritten if a writer needs to do some preparatory work.
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
