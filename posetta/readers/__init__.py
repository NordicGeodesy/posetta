"""Readers that can read different coordinate file formats

Description:
------------

To add a new reader, simply create a new .py-file which defines a class
inheriting from `posetta.readers._reader.Reader` or one of its subclasses. The
class must be decorated with the `posetta.lib.plugins.register` decorator as
follows:

    from posetta.readers import _reader
    from posetta.lib import plugins

    @plugins.register
    class MyNewFormat(_reader.Reader):
        ...

To use a reader, call it using one of the read-functions defined below:

    from posetta import readers
    data = readers.read_file("file_with_new_format.new", "my_new_format", ...)

or

    from posetta import readers
    with open("file_with_new_format.new", mode="rb") as input_stream:
        data = readers.read_stream(input_stream, "my_new_format", ...)

Note that the stream should be opened as a binary stream to allow the readers
to handle encodings if necessary.


The name used in `read_file` and `read_stream` to call the reader is the name
of the module (file) containing the reader.

"""

# Standard library imports
import pathlib
from typing import Any, IO, List, Optional, Tuple, Union

# Posetta imports
from posetta.readers._reader import Reader
from posetta.lib import exceptions
from posetta.lib import plugins


def names() -> Tuple[str, ...]:
    """List the names of available readers

    Note that this will import all readers.

    Returns:
        Names of the available readers.
    """
    return plugins.list_all(package_name=__name__)


def exists(reader_name: str) -> bool:
    """Check whether the given reader exists

    Args:
        reader_name:  Name of reader.

    Returns:
        True if reader exists, False otherwise.
    """
    return plugins.exists(package_name=__name__, plugin_name=reader_name)


def short_docs(*readers: str) -> List[Tuple[str, str]]:
    """Get one line documentation for readers

    If no readers are specified, documentation for all available readers are returned.

    Args:
        readers:  Names of readers.

    Returns:
        Names and documentation for readers.
    """
    if not readers:
        readers = names()

    return [(r, plugins.doc(__name__, r, long_doc=False)) for r in readers]


def read_stream(
    input_stream: IO[bytes], reader_name: Optional[str] = None, **reader_args: Any
) -> Reader:
    """Read a bytes stream with a given reader

    If the reader is not specified, an attempt to guess at an appropriate
    reader is made. A NoReaderFound error is raised if no such appropriate
    reader is found.

    Args:
        input_stream:  Stream of bytes that should be read.
        reader_name:   Name of reader that should be used.

    Returns:
        Data in stream.
    """
    if reader_name is None:
        reader_name = identify(input_stream)

    reader = plugins.call(
        package_name=__name__,
        plugin_name=reader_name,
        input_stream=input_stream,
        **reader_args,
    )
    reader.read()
    return reader


def read_file(
    file_path: Union[str, pathlib.Path],
    reader_name: Optional[str] = None,
    **reader_args: Any,
) -> Reader:
    """Read a file with a given reader

    If the reader is not specified, an attempt to guess at an appropriate
    reader is made. A NoReaderFound error is raised if no such appropriate
    reader is found.

    Args:
        file_path:    Path to file that should be read.
        reader_name:  Name of reader that should be used.

    Returns:
        Data in file.
    """
    with open(file_path, mode="rb") as input_stream:
        return read_stream(input_stream, reader_name)


def identify(input_stream: IO[bytes]) -> str:
    """Identify a reader that can read a given file

    A NoReaderFound error is raised if no such appropriate reader is found.

    Args:
        file_path:    Path to file that should be identified.

    Returns:
        Name of reader that can read the given file.
    """
    import IPython

    where_am_i = "readers.__init__.identify"
    IPython.embed()

    raise exceptions.NoReaderFound(
        f"Found no reader that can read {input_stream.name}"
    ) from None
