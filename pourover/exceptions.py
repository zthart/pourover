# -*- coding: utf-8 -*-

""" pourover.exceptions

This module contains exceptions raised by Pourover

:copyright: (c) Zachary Hart
:license: Apache 2.0, see LICENSE for more details.
"""


class PouroverException(ValueError):
    """ Generic Exception that may have occured doing something CEF related """
    def __init__(self, *args, **kwargs):
        """ Initialize PouroverException """
        self.line = kwargs.pop('line', None)
        super(PouroverException, self).__init__(*args, **kwargs)


class CEFLineError(PouroverException):
    """ A formatting error was found in a line meant to be in CEF format """


class IncompleteLineError(CEFLineError):
    """ A CEFLine object was blank or contained an incomplete set of data """


class CEFLogError(PouroverException):
    """ A formatting error was found while performing an operation on a CEFLog object"""


class SyslogPrefixError(CEFLogError):
    """ An inconsistency with the presence or absence of syslog prefixes was found """
