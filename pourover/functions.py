# -*- coding: utf-8 -*-

""" pourover.functions

This module contains parsing functions provided by pourover

:copyright: (c) Zachary Hart
:license: Apache 2.0, see LICENSE for more details.
"""


def parse_line(line):
    """ Parse a CEF formatted log line

    Parse the data and fields from a log line in CEF format and return them in an easy-to-manipulate dict, breaking
    extensions into the key-value pairs presented in the log line.

    :param line: A CEF formatted line, beginning with a CEF header and ending in any present extensions
    :type line: str
    :return: Key-Value pairs of CEF headers and extensions
    :rtype: dict
    """
    pass


def parse_file(filepath):
    """ Parse all messages in a CEF formatted log file

    Parse the data and fields from a file in CEF format and return them in a easy-to-manipulate list, breaking
    extensions into the key-value pairs presented in the log line

    :param filepath: The file to parse log lines from
    :type filepath: str
    :return: A list of key-value pair sets of CEF headers and extensions
    :rtype: list
    """
    pass


def format_dict(version, dev_vendor, dev_product, dev_version, signature_id, name, severity, **kwargs):
    """ Return a CEF formatted log line from header values and any extensions

    Format CEF header values plus any provided key-value pairs of extensions into a CEF formatted log line

    :param version: CEF version number
    :param dev_vendor: Device Vendor
    :param dev_product: Device Product
    :param dev_version: Device Version
    :param signature_id: Signature Id
    :param name: Name
    :param severity: Severity
    :param kwargs: key-value pairs of extensions
    :type version: int
    :type dev_vendor: str
    :type dev_product: str
    :type dev_version: str
    :type signature_id: str
    :type name: str
    :type severity: int
    :return: a CEF formatted log line
    :rtype: str
    """
    pass
