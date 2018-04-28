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
import pathlib
from typing import List, Union

from posetta.lib import plugins
from posetta.data import CoordSet


def names() -> List[str]:
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


def write(
    file_path: Union[str, pathlib.Path], writer_name: str, cset: CoordSet
) -> None:
    """Write data to a file with a given writer

    Args:
        file_path:    Path to file that should be written.
        writer_name:  Name of writer that should be used.
        cset:         Data that should be written as a coordinate dataset.
    """
    return plugins.call(
        package_name=__name__, plugin_name=writer_name, file_path=file_path, cset=cset
    )
