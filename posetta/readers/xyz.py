"""Gridded data in three columns of numbers, header possible

Description:
------------


Example:
--------

East     North   Value
-25.0000 63.0000 0.0188
-23.0000 63.0000 0.01884
-21.0000 63.0000 0.01798
-19.0000 63.0000 0.01706
-17.0000 63.0000 0.01708
-15.0000 63.0000 0.01795
-13.0000 63.0000 0.01854
-25.0000 65.0000 0.01927
-23.0000 65.0000 0.02014
-21.0000 65.0000 0.02156
-19.0000 65.0000 0.02489
-17.0000 65.0000 0.03102
-15.0000 65.0000 0.01805
-13.0000 65.0000 0.01812


Specification:
--------------

http://www.gdal.org/frmt_xyz.html

"""

# Posetta imports
from posetta import data
from posetta.lib import plugins
from posetta.readers._reader_line import LineReader


@plugins.register
class XyzReader(LineReader):
    """A reader for xyz-files
    """
    _headers = dict(
        x=("positions", 0),
        y=("positions", 1),
        z=("positions", 2),
        east=("positions", 0),
        north=("positions", 1),
        up=("positions", 2),
        lon=("positions", 0),
        lat=("positions", 1),
        height=("positions", 2),
    )

    def setup_reader(self) -> None:
        self.meta["__params__"] = dict(names=True)

    def as_coordset(self) -> data.CoordSet:
        """Return the data as a coordinate dataset

        Returns:
            The data that has been read as a coordinate dataset.
        """
        cset = data.CoordSet()
        for column, value in self.data.items():
            table, idx = self._headers.get(column.lower(), ("values", None))
            cset.add(table, val=value, idx=idx, column_name=column)
        return cset
