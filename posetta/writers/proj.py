"""Write files that are readable by PROJ

Description:
------------
PROJ reads files on a line by line basis. Each line contains a coordinate
and possibly a comment. A coordinate is made up of two to four numbers,
usually ordered as x, y, z, t, but this isn't a requirement. Anything
after a # is considered a comment by PROJ. We use that fact to add
extraneous data such as velocities and other generic values.
"""

# Posetta imports
from posetta.lib import plugins
from posetta.writers._writer import Writer

@plugins.register
class ProjWriter(Writer):
    """A writer of files that PROJ will understand
    """

    def write_data(self) -> None:
        """Write data to a text file in 'x y z t # comment' format.
        """

        # check that dataset has the required columns
        required_columns = {"easting": False, "northing": False}
        for column in self.data.columns:
            # print(column.table, column.idx)
            if column in ("easting", "northing"):
                required_columns[column] = True

        if not (all(value == True for value in required_columns.values())):
            raise WriterError(
                "Input dataset should at least contain eating and northing columns"
            )

        with open(self.file_path, "w") as proj_file:
            for idx in range(self.data.num_obs):
                # assume that position data is ordered as easting, northing, elevation
                # (otherwise a PROJ axisswap operation can fix that).
                for col_idx in range(self.data.tables["positions"].num_cols):
                    proj_file.write(
                        "{val}\t".format(
                            val=self.data.tables["positions"].values[idx][col_idx]
                        )
                    )

                # write epochs if they are present
                if self.data.tables["epochs"].values is not None:
                    proj_file.write(
                        "{val}\t".format(val=self.data.tables["epochs"].values[idx][0])
                    )

                # everything from here is considered a comment by PROJ
                proj_file.write("#  ")

                # write velocities if they are present
                if self.data.tables["velocities"].values is not None:
                    for col_idx in range(self.data.tables["velocities"].num_cols):
                        proj_file.write(
                            "{val}\t".format(
                                val=self.data.tables["velocities"].values[idx][col_idx]
                            )
                        )

                # write additional values if they are present
                if self.data.tables["values"].num_cols is not None:
                    for col_idx in range(self.data.tables["values"].num_cols):
                        proj_file.write(
                            "{val}\t".format(
                                val=self.data.tables["values"].values[idx][col_idx]
                            )
                        )

                proj_file.write("\n")
