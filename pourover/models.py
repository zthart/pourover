# -*- coding: utf-8 -*-

""" pourover.models

This module contains the underlying objects that make this package work

:copyright: (c) Zachary Hart
:license: Apache 2.0, see LICENSE for more details.
"""

from datetime import datetime

from .exceptions import IncompleteLineError, SyslogPrefixError
from . import functions


class CEFLog(object):
    """ The :class:`CEFLog <CEFLog>` object

    This object contains a list of :class:`CEFLine <CEFLine>` objects and exposes them in convenient ways, along with
    some file-wide metadata
    """

    __attrs__ = [
        '_line_count', '_earliest_time', '_latest_time'
    ]

    def __init__(self):
        self._line_count = 0
        self._earliest_time = None
        self._latest_time = None
        self.timerange = None

        self.lines = []

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
        if self.has_syslog_prefix:
            self.lines.sort(key=lambda l: l.timestamp)
        # TODO: Update time-related metadata on log objects with syslog prefixes

    def search_header(self, query, start_time=None, end_time=None):
        """ Rudimentary search of the headers of the lines contained within this log

        Search through the headers of all lines present in this log for the value provided, optionally with a start and
        end timestamp. Timestamps will be ignored for logs whose entries do not have syslog prefixes.

        :param query: The value for which to search
        :param start_time: (optional) a start time to search from - defaults to time of first message in log if
            not provided
        :param end_time: (optional) an end time to search to - defaults to time of last message in log if not provided
        :type query: str
        :type start_time: datetime
        :type end_time: datetime
        :return: a list of log messages that contain the provided query
        :rtype: list of :class:`CEFLine <CEFLine>`
        """
        pass

    def search_extensions(self, query, start_time=None, end_time=None):
        """ Rudimentary search of the extensions of the lines contained within this log

        Search through the extensions of all lines present in this log for the value provided, optionally with a start
        and end timestamp. Timestamps will be ignored for logs whose entries do not have syslog prefixes.

        :param query: The value for which to search
        :param start_time: (optional) A start time to search from - default to time of first message in log if not
            provided
        :param end_time: (optional) An end time to search to - defaults to time of last message in log if not provided
        :type query: str
        :type start_time: datetime
        :type end_time: datetime
        :return: a list of log messages that contain the provided query
        :rtype: list of :class:`CEFLine <CEFLine>`
        """
        pass


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
        else:
            return False

    @property
    def has_extensions(self):
        """ Returns True if the length of the dict of extensions is greater than zero. """
        return len(self.extensions) > 0

    @property
    def timestamp(self):
        """ Returns the datetime value found in the syslog prefix, if present

        This function checks if the log line has a syslog prefix, and if so, will attempt to parse out the timestamp
        present in the prefix. If the the object is in the future (ahead of ``utcnow()``, if we assume it came from the
        current calendar year), the year will be set to the previous year rather than assuming that the log is from the
        future.
        """
        if not self.has_syslog_prefix:
            return None
        else:
            # Pull only the timestamp from the prefix, ignore the hostname
            timestamp = ' '.join(self.headers['Prefix'].split(' ')[:-1])
            # Parse the timestamp from the string, assume current year
            timestamp = datetime.strptime(timestamp, '%b %d %H:%M:%S')

            # assume that our logs are not from the future
            if timestamp.replace(year=datetime.utcnow().year) > datetime.utcnow():
                timestamp = timestamp.replace(year=datetime.utcnow().year - 1)
            else:
                timestamp = timestamp.replace(year=datetime.utcnow().year)
            return timestamp
