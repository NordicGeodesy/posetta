"""Tests for the lib.plugins-module

"""

# Standard library imports
import sys

# Third party imports
import pytest

# Posetta imports
from posetta.lib import exceptions
from posetta.lib import plugins
from posetta.readers._reader import Reader


@pytest.fixture
def tmpfile(tmpdir):
    """A temporary file that can be read"""
    file_path = tmpdir.join("test")
    file_path.write("Temporary test file")

    return file_path


#
# Tests
#
def test_package_not_empty():
    """Test that list_all() finds some plugins in posetta.readers-package"""
    readers = plugins.list_all("posetta.readers")
    assert len(readers) > 0


def test_package_empty():
    """Test that list_all() does not find any plugins in posetta.lib-package"""
    lib_plugins = plugins.list_all("posetta.lib")
    assert len(lib_plugins) == 0


def test_package_non_existing():
    """Test that a non-existent package raises an appropriate error"""
    with pytest.raises(exceptions.UnknownPackageError):
        plugins.list_all("posetta.non_existent")


def test_plugin_exists():
    """Test that an existing plugin returns True for exists()"""
    package_name = "posetta.readers"
    plugin_name = plugins.list_all(package_name)[0]
    assert plugins.exists(package_name, plugin_name)


@pytest.mark.parametrize("plugin_name", ["exceptions", "non_existent"])
def test_plugin_exists_not(plugin_name):
    """Test that a non-existing plugin returns False for exists()

    Tests both for an existing module (posetta.lib.exceptions) and a non-existent module
    (posetta.lib.non_existent).
    """
    assert not plugins.exists("posetta.lib", plugin_name)


def test_call_existing_plugin(tmpfile):
    """Test that calling a reader-plugin returns a Reader instance"""
    package_name = "posetta.readers"
    plugin_name = plugins.list_all(package_name)[0]
    with open(tmpfile, mode="rb") as input_stream:
        reader = plugins.call(package_name, plugin_name, input_stream=input_stream)
    assert isinstance(reader, Reader)


def test_call_non_exising_plugin():
    with pytest.raises(exceptions.UnknownPluginError):
        plugins.call("posetta.lib", "non_existent")
