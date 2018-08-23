"""Comma-separated values, data in columns

Description:
------------


Example:
--------

East,North,Value
-25.0000,63.0000,0.0188
-23.0000,63.0000,0.01884
-21.0000,63.0000,0.01798
-19.0000,63.0000,0.01706
-17.0000,63.0000,0.01708
-15.0000,63.0000,0.01795
-13.0000,63.0000,0.01854
-25.0000,65.0000,0.01927
-23.0000,65.0000,0.02014
-21.0000,65.0000,0.02156
-19.0000,65.0000,0.02489
-17.0000,65.0000,0.03102
-15.0000,65.0000,0.01805
-13.0000,65.0000,0.01812


Specification:
--------------

TODO

"""

# Standard library imports
import codecs

# Posetta imports
from posetta.lib import plugins
from posetta.writers._writer import Writer


@plugins.register
class CsvWriter(Writer):
    """A writer for csv-files
    """

    def write_data(self) -> None:
        """Write data to a CSV file

        Use pandas to do the work
        """
        self.data.as_dataframe().to_csv(self.output_stream)
