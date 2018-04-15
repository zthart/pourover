# -*- coding: utf-8 -*-

""" pourover.ceflog

This module contains the CEFLog object and related functions

:copyright: (c) Zachary Hart
:license: Apache 2.0, see LICENSE for more details.
"""

from .exceptions import IncompleteLineError, SyslogPrefixError
from . import functions


class CEFLog(object):
    """ The :class:`CEFLog <CEFLog>` object

    This object contains a list of :class:`CEFLine <CEFLine>` objects and exposes them in convenient ways, along with
    some file-wide metadata
    """

    def __init__(self):
        self._line_count = 0
        self._earliest_time = None
        self._latest_time = None
        self.timerange = None

        self.lines = []

        pass

    @property
    def has_syslog_prefix(self):
        """ Returns True if the entries in the log have a syslog prefix

        This attribute determines whether or not the log was created with lines that contain a syslog prefix. If the
        log object is empty (has no lines), this property will return ``None``.
        """
        if len(self.lines) > 0:
            return self.lines[0].has_syslog_prefix
        else:
            return None

    @property
    def is_empty(self):
        """ True if this log has no lines present. """
        return len(self.lines) == 0

    def __repr__(self):
        return '<CEFLog [%s line%s]>' % (self._line_count, 's' if self._line_count != 1 else '')

    def __iter__(self):
        """ Allows you to use the log object as an iterator to interact with the lines. """
        return self.lines.__iter__()

    def append(self, line):
        """ Add a line to the log

        Add a :class:`CEFLine <CEFLine>` object or correctly formatted CEF string to

        :param line:
        :return:
        """
        if not isinstance(line, (CEFLine, str)):
            raise TypeError('Attempting to append %s to a CEFLog object' % type(line))

        if isinstance(line, str):
            line = functions.parse_line(line)

        if line.has_syslog_prefix and not self.has_syslog_prefix:
            raise SyslogPrefixError('A line with a syslog prefix may not be appended to a log whose existing lines '
                                    'have no prefix', line=line)
        elif not line.has_syslog_prefix and self.has_syslog_prefix:
            raise SyslogPrefixError('A line with no syslog prefix may not be appended to a log whose existing lines '
                                    'contain a prefix', line = line)
        else:
            self.lines.append(line)
            self._update_metadata()

    def _update_metadata(self):
        """ Update the metadata attributes of this function

        Updates the :attr:`_line_count`, :attr:`_earliest_time`, :attr:`_latest_time`, and :attr:`timerange` attributes
        of the log object. This function is called with every successful call to :meth:`CEFLog.append`.
        """
        self._line_count = len(self.lines)
        # TODO: Update time-related metadata on log objects with syslog prefixes


class CEFLine(object):
    """ The :class:`CEFLine <CEFLine>` object

    This object contains the header and extension data of a CEF line, and exposes some of the data within in convenient
    ways
    """

    __attrs__ = [
        '_extension_count', '_raw_line', '_raw_header'
    ]

    def __init__(self):
        self._extension_count = 0
        self._raw_line = None
        self._raw_header = None
        self.extensions = {}
        self.headers = {}

    def __repr__(self):
        return '<CEFLine [%s]>' % self._raw_header

    def __str__(self):
        return self._raw_line

    @property
    def has_syslog_prefix(self):
        """ Returns True if a syslog prefix is found before the CEF header

        This attribute checks if a syslog timestamp and host was found before the version of the CEF header, and
        will return True if one is found. Lines with syslog prefixes cannot be added to CEFLog objects that contain
        any line that **does not** have a syslog prefix. Lines without syslog prefixes cannot be added to CEFLog objects
        that contain any line that **does** have a syslog prefix.
        """
        if 'Prefix' in self.headers:
            return True
        elif len(self.headers) == 0:
            raise IncompleteLineError('Could not check for syslog prefix in empty or incomplete line',
                                      line=self)
        else:
            return False

    @property
    def has_extensions(self):
        """ Returns True if the length of the dict of extensions is greater than zero. """
        return len(self.extensions) > 0
