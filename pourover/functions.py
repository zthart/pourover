# -*- coding: utf-8 -*-

""" pourover.functions

This module contains parsing functions provided by pourover

:copyright: (c) Zachary Hart
:license: Apache 2.0, see LICENSE for more details.
"""

HEADER_SEP = r'(.*(?<!\\)\|){,7}(.*)'
HEADER_SPLIT = r'(?<!\\)\|'


def parse_line(line):
    """ Parse a CEF formatted log line

    Parse the data and fields from a log line in CEF format and return them in an easy-to-manipulate dict, breaking
    extensions into the key-value pairs presented in the log line.

    :param line: A CEF formatted line, beginning with a CEF header and ending in any present extensions
    :type line: str
    :return: The parsed line object
    :rtype: :class:`CEFLine <CEFLine>`
    """
    pass


def parse_file(filepath):
    """ Parse all messages in a CEF formatted log file

    Parse the data and fields from a file in CEF format and return them in a easy-to-manipulate list, breaking
    extensions into the key-value pairs presented in the log line

    :param filepath: The file to parse log lines from
    :type filepath: str
    :return: The parsed log object
    :rtype: :class:`CEFLog <CEFLog>`
    """
    pass


def format_dict(version, dev_vendor, dev_product, dev_version, signature_id, name, severity, set_syslog_prefix=False, **kwargs):
    """ Return a CEF formatted log line from header values and any extensions

    Format CEF header values plus any provided key-value pairs of extensions into a CEF formatted log line

    :param version: CEF version number
    :param dev_vendor: Device Vendor
    :param dev_product: Device Product
    :param dev_version: Device Version
    :param signature_id: Signature Id
    :param name: Name
    :param severity: Severity
    :param set_syslog_prefix: Optionally include the syslog timestamp and host
    :param kwargs: key-value pairs of extensions
    :type version: int
    :type dev_vendor: str
    :type dev_product: str
    :type dev_version: str
    :type signature_id: str
    :type name: str
    :type severity: int
    :type set_syslog_prefix: bool
    :return: a CEF formatted log line
    :rtype: str
    """
    pass
