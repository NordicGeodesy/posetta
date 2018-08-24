#!/usr/bin/env python3
"""Posetta, The Universal Translator of Geodetic Coordinate File Formats

Posetta can convert input in one format to output with a different
format. Input and output can be either files, or stdin and stdout streams.

\b
Examples:
---------

Convert file_1.txt in XYZ-format to file_2.gri in GRI-format:

  $ posetta -f file_1.txt -F xyz -t file_2.gri -T gri

\b
Input Formats:
--------------

\b
{readers}

\b
Output formats:
---------------

\b
{writers}

\b
About Posetta:
--------------

Posetta, v{version}, MIT License {copyright}

Currently maintained by:

\b
{maintainers}

Contributions are welcome at {url}.

"""

# Standard library imports
import pathlib
import sys
from typing import Any, Dict, Optional, Union

# Third party imports
import click

# Posetta imports
import posetta
from posetta import readers
from posetta import writers


def help_str() -> str:
    """Add information to the module doc-string for a complete help message
    """
    maintainers = [
        f"  + {name} <{email}>"
        for name, email in zip(
            posetta.__author__.split(", "), posetta.__contact__.split(", ")
        )
    ]
    return __doc__.format(
        readers="\n".join(f"  + {name} - {doc}" for name, doc in readers.short_docs()),
        writers="\n".join(f"  + {name} - {doc}" for name, doc in writers.short_docs()),
        maintainers="\n".join(maintainers),
        url=posetta.__url__,
        copyright=posetta.__copyright__,
        version=posetta.__version__,
    )


#
# Starting Point of Command Line Tool
#
@click.command(help=help_str())
@click.option("-f", "--file_from", help="Path of input file. Default is stdin.")
@click.option("-t", "--file_to", help="Path of output file. Default is stdout.")
@click.option(
    "-F", "--fmt_from", help="Input file format (supported formats listed above)."
)
@click.option(
    "-T", "--fmt_to", help="Output file format (supported formats listed above)."
)
@click.option(
    "-O", "--overwrite", is_flag=True, help="Overwrite if output file already exists."
)
@click.option("-V", "--verbose", is_flag=True, help="Say what is happening.")
@click.version_option(None, "-v", "--version")
@click.help_option("-h", "--help")
def cli(
    file_from: str, file_to: str, fmt_from: str, fmt_to: str, **options: Dict[str, Any]
) -> None:
    """The command line interface for Posetta

    Implemented using click: http://click.pocoo.org
    """
    translate(file_from, file_to, fmt_from, fmt_to, options)


#
# Starting Point for the Graphical (GUI) Tool
#
def gui() -> None:
    from posetta.gui import PosettaGui  # Local import to avoid slowing down command line tool

    root = PosettaGui(translate)
    root.mainloop()


#
# Both CLI and GUI end up here :)
#
def translate(
    file_from: Union[str, pathlib.Path],
    file_to: Union[str, pathlib.Path],
    fmt_from: str,
    fmt_to: str,
    options: Optional[Dict[str, Any]] = None,
) -> None:
    """The main workflow of Posetta

    Read file_from with format fmt_from, translate it to format fmt_to and write
    it to file_to.

    Args:
        file_from:  Name of input file.
        file_to:    Name of output file.
        fmt_from:   Format of input file.
        fmt_to:     Format of output file.
        options:    Additional options.
    """
    options = options or dict()
    verbose = _verbose_on if options.get("verbose") else _verbose_off
    path_from = None if file_from is None else pathlib.Path(file_from)
    path_to = None if file_to is None else pathlib.Path(file_to)

    # Check input parameters
    if path_from is not None and not path_from.exists():
        raise click.BadParameter(f"Input file '{path_from}' does not exist")

    if path_to is not None and path_to.exists() and not options.get("overwrite"):
        raise click.BadParameter(
            f"Output file '{path_to}' already exists. Use --overwrite to overwrite it."
        )

    if fmt_from is not None and not readers.exists(fmt_from):
        fmts = ", ".join(readers.names())
        raise click.BadParameter(
            f"Input format '{fmt_from}' is not supported. Use one of {fmts}"
        )

    if fmt_to is None or not writers.exists(fmt_to):
        fmts = ", ".join(writers.names())
        raise click.BadParameter(
            f"Output format '{fmt_to}' is not supported. Use one of {fmts}"
        )

    # Read input as CoordSet
    if path_from is None:
        verbose("Reading from standard input")
        cset = readers.read_stream(sys.stdin.buffer, fmt_from).as_coordset()
    else:
        verbose(f"Reading from '{path_from}'")
        cset = readers.read_file(path_from, fmt_from).as_coordset()

    # Write CoordSet to new format
    if path_to is None:
        verbose("Writing to standard output")
        writers.write_stream(sys.stdout.buffer, fmt_to, cset)
    else:
        verbose(f"Writing to '{path_to}'")
        writers.write_file(path_to, fmt_to, cset)


#
# Convenience functions
#
def _verbose_on(text: str) -> None:
    """Print text to stdout

    Args:
        text:  Text that should be printed.
    """
    print(text)


def _verbose_off(text: str) -> None:
    """Do nothing

    Args:
        text:  Text that will not be printed.
    """
    pass


if __name__ == "__main__":
    cli()
