"""Common functions for all tests

"""

# System library imports
import pathlib

# Third party imports
import pytest


@pytest.fixture
def path_examples():
    """Path to the examples directory"""
    return pathlib.Path(__file__).parent.parent / "example_files"
