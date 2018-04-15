# -*- coding: utf-8 -*-

""" pourover.exceptions

This module contains exceptions raised by Pourover
"""


class PouroverException(ValueError):
    """ Generic Exception that may have occured doing something CEF related """
    def __init__(self, *args, **kwargs):
        """ Initialize PouroverException """
        pass
