"""Simple format readable by PROJ

Description:
------------

PROJ reads files on a line by line basis. Each line contains a coordinate
and possibly a comment. A coordinate is made up of two to four numbers,
usually ordered as x, y, z, t, but this isn't a requirement. Anything
after a # is considered a comment by PROJ. We use that fact to add
extraneous data such as velocities and other generic values.

Example files:
--------------

    example.proj
"""
# Standard library imports

# Third party imports
import numpy as np

# Posetta imports
from posetta import data
from posetta.lib import plugins
from posetta.readers._reader_line import Reader


@plugins.register
class ProjReader(Reader):
    """A reader for files readble by PROJ
    """

    def setup_reader(self) -> None:
        self.meta["__params__"] = dict(names=True)

    def read_data(self) -> None:
        """
        Read PROJ coordinates
        """
        col_names = ("pos_x", "pos_y", "pos_z", "epoch")

        for line in self.input_stream:
            coords, _, comments = line.strip().partition("#")
            for name, coord in zip(col_names, coords.split()):
                self.data.setdefault(name, list()).append(float(coord))
            self.data.setdefault("comments", list()).append([float(c) for c in comments.split()])

    def as_coordset(self) -> data.CoordSet:
        """Return the data as a coordinate dataset

        Returns:
            The data that has been read as a coordinate dataset.
        """
        cset = data.CoordSet()

        if "pos_x" in self.data:
            cset.add("positions", self.data["pos_x"], 0, "x")
        if "pos_y" in self.data:
            cset.add("positions", self.data["pos_y"], 1, "y")
        if "pos_z" in self.data:
            cset.add("positions", self.data["pos_z"], 2, "z")
        if "epoch" in self.data:
            cset.add("epochs", self.data["epoch"], 0, "t")

        # add whatever metadata is available
        for comment in np.array(self.data["comments"]).T:
            cset.add("values", comment, None, "comment")

        return cset
