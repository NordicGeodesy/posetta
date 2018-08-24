"""Tests for the writers.proj module
"""
# Standard library imports
import sys

# Third party imports
import pytest

# Posetta imports
from posetta.data import CoordSet
from posetta import writers


#
# Test data sets
#
@pytest.fixture
def xyz():
    cset = CoordSet()
    cset.add("positions", (687071.44,), 0, "easting")
    cset.add("positions", (6210141.33,), 1, "northing")
    cset.add("positions", (10,), 2, "elevation")

    expected = "687071.44\t6210141.33\t10.0\t#  \n"

    return cset, expected


@pytest.fixture
def xyzt():
    cset, _ = xyz()
    cset.add("epochs", (2018.75,), 0, "epoch")

    expected = "687071.44\t6210141.33\t10.0\t2018.75\t#  \n"

    return cset, expected


def xyzt_comment():
    cset, _ = xyzt()
    cset.add("values", ("testing",), None, "comment1")
    cset.add("values", ("TESTING",), None, "comment2")

    expected = "687071.44\t6210141.33\t10.0\t2018.75\t#  testing\tTESTING\t\n"

    return cset, expected


#
# Tests
#
@pytest.mark.parametrize("data", [xyz(), xyzt(), xyzt_comment()])
def test_proj_write_to_file(write_and_read, data):
    """Test writing to file
    """
    cset, expected = data
    assert write_and_read("proj", cset) == expected


@pytest.mark.parametrize("data", [xyz(), xyzt(), xyzt_comment()])
def test_proj_write_to_stdout(capsys, data):
    cset, expected = data
    writers.write_stream(sys.stdout.buffer, "proj", cset)
    stdout, stderr = capsys.readouterr()

    assert stdout == expected
    assert stderr == ""
