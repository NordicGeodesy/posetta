"""XYZ: Three columns of numbers, no header

Description:
------------


Example:
--------


Specification:
--------------

<URL>
"""

# Posetta imports
from posetta.readers._reader_line import LineReader
from posetta.lib import plugins


@plugins.register
class XyzReader(LineReader):
    """A reader for xyz-files
    """

    def setup_reader(self):
        return dict(names=['epochs', 'postions', 'velocities'])
