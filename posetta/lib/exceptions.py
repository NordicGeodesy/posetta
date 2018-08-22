"""Definition of Posetta-specific exceptions

Description:
------------

Custom exceptions used by Posetta for more specific error messages and
handling.
"""


class PosettaException(Exception):
    pass


class CoordSetError(PosettaException):
    pass


class NoReaderFound(PosettaException):
    pass


class ReaderError(PosettaException):
    pass


class WriterError(PosettaException):
    pass


class UnknownPackageError(PosettaException):
    pass


class UnknownPluginError(PosettaException):
    pass
