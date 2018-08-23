"""Tests for the readers.kms module

"""

# Posetta imports
from posetta import readers


def test_file_koordinater(path_examples):
    """
    KmsReader: koordinater
    """
    reader = readers.read_file(path_examples / "kms" / "koordinater", "kms")
    cset = reader.as_coordset()

    assert (
        cset.values.values[0, 0] == "G.M.182/183"
    )  # TODO: Add column name indexing on tables
    assert cset.positions.values[0, 1] == 6193448.053
    assert cset.positions.values[0, 0] == 470321.583

    assert cset.values.values[-1, 0] == "134-10-09039"
    assert cset.positions.values[-1, 1] == 6182559.836
    assert cset.positions.values[-1, 0] == 453615.626

    # assert reader.data["station"][0] == "G.M.182/183"
    # assert reader.data["northing"][0] == 6193448.053
    # assert reader.data["easting"][0] == 470321.583

    # assert reader.data["station"][-1] == "134-10-09039"
    # assert reader.data["northing"][-1] == 6182559.836
    # assert reader.data["easting"][-1] == 453615.626


def test_file_koter(path_examples):
    """
    KmsReader: koter
    """
    reader = readers.read_file(path_examples / "kms" / "koter", "kms")
    cset = reader.as_coordset()

    assert cset.values.values[0, 0] == "G.M.182/183"
    assert cset.positions.values[0, 2] == 12.35840

    assert cset.values.values[-1, 0] == "134-10-09039"
    assert cset.positions.values[-1, 2] == 2.32457

    # assert reader.data["station"][0] == "G.M.182/183"
    # assert reader.data["elevation"][0] == 12.35840

    # assert reader.data["station"][-1] == "134-10-09039"
    # assert reader.data["elevation"][-1] == 2.32457
