# -*- coding: utf-8 -*-

""" pourover.exceptions

This module contains exceptions raised by Pourover
"""


class PouroverException(ValueError):
    """ Generic Exception that may have occured doing something CEF related """
    def __init__(self, *args, **kwargs):
        """ Initialize PouroverException """
        self.line = kwargs.pop('line', None)
        super(PouroverException, self).__init__(*args, **kwargs)


class CEFLineError(PouroverException):
    """ A formatting error was found in a line meant to be in CEF format """
