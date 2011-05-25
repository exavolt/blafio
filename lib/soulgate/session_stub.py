#!/usr/bin/env python

class Error(Exception):
    pass

class InvalidError(Error):
    pass

class NotFoundError(Error):
    pass

class NotStartedError(Error):
    pass

class DataError(Error):
    pass
class DataNotFoundError(DataError):
    pass


