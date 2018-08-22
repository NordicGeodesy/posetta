"""Tests for the readers.kms module

"""
import pathlib

# Third party imports
import pytest

# Posetta imports
from posetta.readers.kms import KmsReader

DIR = pathlib.Path.cwd() / "example_files" / "kms"


def test_file_koordinater():
    """
    KmsReader: koordinater
    """
    reader = KmsReader(DIR / "koordinater")
    reader.read()
    assert reader.data["station"][0] == "G.M.182/183"
    assert reader.data["northing"][0] == 6193448.053
    assert reader.data["easting"][0] == 470321.583

    assert reader.data["station"][-1] == "134-10-09039"
    assert reader.data["northing"][-1] == 6182559.836
    assert reader.data["easting"][-1] == 453615.626


def test_file_koter():
    """
    KmsReader: koter
    """
    reader = KmsReader(DIR / "koter")
    reader.read()
    assert reader.data["station"][0] == "G.M.182/183"
    assert reader.data["elevation"][0] == 12.35840

    assert reader.data["station"][-1] == "134-10-09039"
    assert reader.data["elevation"][-1] == 2.32457
