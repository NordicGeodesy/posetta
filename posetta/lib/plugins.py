"""Set up a simple plug-in architecture for Posetta

Description:
------------

In order to be able to add readers and writers etc without needing to hardcode
names, but rather pick them from the command line or similar, we use a simple
plug-in architecture. The plug-in mechanism is based on the different plug-ins
registering themselves using the :func:`register` decorator::

    from posetta.lib import plugins

    @plugins.register
    def simple_reader(file_path, num_points):
        ...

Plug-ins are registered based on the name of the module (file) they are defined
in, as well as the package (directory) which contains them. Typically all
plug-ins of a given type are collected in a package, e.g. readers, writers,
etc. To list all plug-ins in a package use :func:`list_all`::

    > from posetta.lib import plugins
    > plugins.list_all('posetta.readers')
    ['reader_one', 'reader_three', 'reader_two']

Note that the plug-ins are sorted alphabetically.

A plug-in may be called using :func:`call`::

    > from posetta.lib import plugins
    > plugins.call('posetta.readers', plugin_name='reader_one',
    ...            arg_to_plugin='hello')
    <result from reader_one>

Arguments to the plug-ins should be passed as named arguments to :func:`call`.
"""

# Standard library imports
from collections import namedtuple
import importlib
import pathlib
import re
import sys
from typing import Any, Callable, Dict, Tuple

# Posetta imports
from posetta.lib import exceptions


# Simple structure containing information about a plug-in
Plugin = namedtuple("Plugin", ["name", "function", "doc"])
Plugin.__doc__ = """Information about a plug-in

    Args:
        name: str        - Name of the plug-in.
        function:        - The plug-in.
        doc: str         - Doc string of the plug-in (module)
    """


# The _PLUGINS-dict is populated by the :func:`register` decorator in each
# module.
_PLUGINS: Dict[str, Dict[str, Plugin]] = dict()


#
# REGISTER PLUG-INS
#
def register(func: Callable) -> Callable:
    """Register a plug-in

    Plug-ins are registered based on the name of the module (file) they are
    defined in, as well as the package (directory) which contains
    them. Typically all plug-ins of a given type are collected in a package,
    e.g. readers, writers, etc.

    Args:
        func:  The function that is being registered.

    Returns:
        The function that is being registered (untouched).
    """
    # Get information from the function being registered
    package_name, _, plugin_name = func.__module__.rpartition(".")
    doc = sys.modules[func.__module__].__doc__
    plugin = Plugin(plugin_name, func, doc or "")

    # Store Plugin-object in _PLUGINS dictionary
    _PLUGINS.setdefault(package_name, dict())[plugin_name] = plugin

    return func


#
# CALL PLUG-INS
#
def call(package_name: str, plugin_name: str, **plugin_args: Any) -> Any:
    """Call a plug-in

    If the plug-in is not part of the package an UnknownPluginError is raised.

    Args:
        package_name:  Name of package containing plug-ins.
        plugin_name:   Name of the plug-in (module).
        plugin_args:   Named arguments passed on to the plug-in.

    Returns:
        Return value of the plug-in.
    """
    # Get Plugin-object
    plugin = load(package_name, plugin_name)

    # Call plug-in
    return plugin.function(**plugin_args)


#
# GET DOCUMENTATION FOR PLUG-INS
#
def doc(
    package_name: str,
    plugin_name: str,
    long_doc: bool = True,
    include_details: bool = False,
) -> str:
    """Document one plug-in

    Documentation is taken from the module doc-string. If the plug-in is not part of the
    package an UnknownPluginError is raised.

    Args:
        package_name:     Name of package containing plug-ins.
        plugin_name:      Name of the plug-in (module).
        long_doc:         Use long doc-string or short one-line string.
        include_details:  Include development details like parameters and return values?

    Returns:
        Documentation of the plug-in.
    """
    # Get Plugin-object and pick out doc-string
    doc = load(package_name, plugin_name).doc

    if long_doc:
        # Strip short description and indentation
        lines = [d.strip() for d in "\n\n".join(doc.split("\n\n")[1:]).split("\n")]

        # Stop before Args:, Returns: etc if details should not be included
        idx_args = len(lines)
        if not include_details:
            re_args = re.compile("(Args:|Returns:|Details:|Attributes:)$")
            try:
                idx_args = [re_args.match(l) is not None for l in lines].index(True)
            except ValueError:
                pass
        return "\n".join(lines[:idx_args]).strip()

    else:
        # Return short description
        return doc.split("\n\n")[0].replace("\n", " ").strip()


#
# LIST AVAILABLE PLUG-INS
#
def list_all(package_name: str) -> Tuple[str, ...]:
    """List all plug-ins in a package

    Lists all available plug-ins in the package.  Do note, however, that this
    will import all python files in the package.

    Args:
        package_name:  Name of package containing plug-ins.

    Returns:
        Sorted list of strings with names of plug-ins.
    """
    # Import all plug-ins
    _import_all(package_name)

    # Figure out names of plug-ins
    plugin_names = _PLUGINS.get(package_name, dict()).keys()

    return tuple(sorted(plugin_names))


def exists(package_name: str, plugin_name: str) -> bool:
    """Check whether or not a plug-in exists in a package

    Tries to import the given plug-in.

    Args:
        package_name:  Name of package containing plug-ins.
        plugin_name:   Name of the plug-in (module).

    Returns:
        True if plug-in exists, False otherwise.
    """
    if plugin_name not in _PLUGINS.get(package_name, dict()):
        try:
            _import_one(package_name, plugin_name)
        except exceptions.UnknownPluginError:
            return False

    return plugin_name in _PLUGINS.get(package_name, dict())


#
# LOAD PLUG-INS
#
def load(package_name: str, plugin_name: str) -> Plugin:
    """Load one plug-in from a package

    Tries to load the plugin with the given name.

    Args:
        package_name:  Name of package containing plug-ins.
        plugin_name:   Name of the plug-in (module).

    Returns:
        Name of plug-in.
    """
    if plugin_name not in _PLUGINS.get(package_name, dict()):
        _import_one(package_name, plugin_name)

    try:
        return _PLUGINS[package_name][plugin_name]
    except KeyError:
        msg = "Module '{}.{}' does not contain a plugin".format(
            package_name, plugin_name
        )
        raise exceptions.UnknownPluginError(msg) from None


def _import_one(package_name: str, plugin_name: str) -> None:
    """Import a plugin from a package

    This is essentially just a regular python import. As the module is
    imported, the _PLUGINS-dict will be populated by @register decorated
    function in the file.

    Args:
        package_name:  Name of package containing plug-ins.
        plugin_name:   Name of the plug-in (module).
    """
    try:
        importlib.import_module(package_name + "." + plugin_name)
    except ImportError:
        msg = "Plugin '{}' not found in '{}'".format(plugin_name, package_name)
        raise exceptions.UnknownPluginError(msg) from None


def _import_all(package_name: str) -> None:
    """Import all .py-files in the given package directory

    As each file is imported, the _PLUGINS-dict will be populated by @register
    decorated functions in each file.

    Files with names starting with an underscore are not imported.

    Args:
        package_name:  Name of package containing plug-ins.
    """
    # Figure out the directory of the package by importing it. The package must contain
    # __init__.py for this to work, as otherwise __file__ is not set.
    try:
        package = importlib.import_module(package_name)
    except ImportError:
        msg = f"Plug-in package '{package_name}' not found"
        raise exceptions.UnknownPackageError(msg) from None

    try:
        directory = pathlib.Path(package.__file__).parent
    except AttributeError:
        msg = f"Plug-in package '{package_name}' must include '__init__.py'"
        raise exceptions.UnknownPluginError(msg) from None

    # Import all .py files in the given directory
    for file_path in directory.glob("*.py"):
        plugin_name = file_path.stem
        if not plugin_name.startswith("_"):
            _import_one(package_name, plugin_name)
