"""Tests for the writers.proj module
"""
import os
import tempfile

import pytest

from posetta.data.coordset import CoordSet
from posetta.writers.proj import ProjWriter

XYZ_OUTPUT = "687071.44\t6210141.33\t10.0\t#  \n"
XYZT_OUTPUT = "687071.44\t6210141.33\t10.0\t2018.75\t#  \n"
COMMENT_OUTPUT = "687071.44\t6210141.33\t10.0\t2018.75\t#  testing\tTESTING\t\n"


def _write_and_read_file_as_string(cset):
    """
    This is a somewhat hacky way of getting a temporary file name.
    ProjWriter won't open an existing file so we create a temporary
    file that is deleted immediately after we store the path of it.
    We can now pass that path on to ProjWriter, write and read it
    and the manually clean it up again.
    """
    with tempfile.NamedTemporaryFile() as temp:
        tmpfile = temp.name

    proj_writer = ProjWriter(tmpfile, cset)
    proj_writer.write()
    with open(tmpfile, "r") as f:
        string = f.read()
    os.remove(tmpfile)

    return string


def test_proj_writer():
    """
    Test some things
    """
    cset = CoordSet()
    cset.add("positions", (687071.44,), 0, "easting")
    cset.add("positions", (6210141.33,), 1, "northing")
    cset.add("positions", (10,), 2, "elevation")

    xyz_string = _write_and_read_file_as_string(cset)
    assert XYZ_OUTPUT == xyz_string

    cset.add("epochs", (2018.75,), 0, "elevation")
    xyzt_string = _write_and_read_file_as_string(cset)
    assert XYZT_OUTPUT == xyzt_string

    cset.add("values", ("testing",), None, "comment1")
    cset.add("values", ("TESTING",), None, "comment2")
    comment_string = _write_and_read_file_as_string(cset)
    assert COMMENT_OUTPUT == comment_string

    return True
