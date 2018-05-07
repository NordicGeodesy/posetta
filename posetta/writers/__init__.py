"""Writers that can write different coordinate file formats

Description:
------------

To add a new writer, simply create a new .py-file which defines a class inheriting
from `posetta.writers._writer.Writer`. The class must be decorated with the
`posetta.lib.plugins.register` decorator as follows:

    from posetta.writers import _writer
    from posetta.lib import plugins

    @plugins.register
    class MyNewFormat(_writer.Writer):
        ...

To use a writer, call it using the `write`-function defined below:

    from posetta import writers
    data = writers.write('file_with_new_format.new', 'my_new_format', cset, ...)

The name used in `write` to call the writer is the name of the module (file)
containing the writer.
"""

# Standard library imports
import pathlib
from typing import List, Sequence, Tuple, Union

# Posetta imports
from posetta.data import CoordSet
from posetta.lib import plugins


def names() -> Tuple[str, ...]:
    """List the names of available writers

    Note that this will import all writers.

    Returns:
        Names of the available writers.
    """
    return plugins.list_all(package_name=__name__)


def exists(writer_name: str) -> bool:
    """Check whether the given writer exists

    Args:
        writer_name:  Name of writer.

    Returns:
        True if writer exists, False otherwise.
    """
    return plugins.exists(package_name=__name__, plugin_name=writer_name)


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


def write(
    file_path: Union[str, pathlib.Path], writer_name: str, cset: CoordSet
) -> None:
    """Write data to a file with a given writer

    Args:
        file_path:    Path to file that should be written.
        writer_name:  Name of writer that should be used.
        cset:         Data that should be written as a coordinate dataset.
    """
    writer = plugins.call(
        package_name=__name__, plugin_name=writer_name, file_path=file_path, cset=cset
    )
    writer.write()
