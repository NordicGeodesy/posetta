"""Definition of Posetta-specific exceptions

Description:
------------

Custom exceptions used by Posetta for more specific error messages and
handling.
"""


class PosettaException(Exception):
    pass


class NoReaderFound(PosettaException):
    pass


class UnknownPackageError(PosettaException):
    pass


class UnknownPluginError(PosettaException):
    pass
