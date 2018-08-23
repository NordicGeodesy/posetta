"""Common functions for all writers tests

"""

# System library imports
import pathlib
import sys

# Third party imports
import pytest

# Posetta imports
from posetta import writers


@pytest.fixture
def write_and_read(tmpdir):
    """Factory for write and read functions

    Creates a function that can write a CoordSet to a temporary file
    using the given writer, and then reads back the file as a string.
    """

    def _write_and_read(writer, cset, encoding="utf-8"):
        file_path = tmpdir.join(f"test_{writer}")
        writers.write_file(file_path, writer, cset)
        return file_path.read_text(encoding=encoding)

    return _write_and_read


@pytest.fixture
def write_to_stdout():
    """Factory for functions that write to stdout

    This is needed as a workaround because Pytest mocks out standard out
    """

    def _write_to_stdout(writer, cset, encoding="utf-8"):
        writers.write_stream(sys.stdout.buffer, writer, cset)

    return _write_to_stdout
