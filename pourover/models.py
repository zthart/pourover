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

    def __init__(self):
        self.timerange = None

        self.lines = []

    @property
    def linecount(self):
        """ Returns the number of lines in the log object.

        Uses the ``len()`` builtin to determine the number of log lines currently held by the log

        :return: the number of :class:`CEFLine <CEFLine>` objects currently in the log
        :rtype: int
        """
        return len(self.lines)

    @property
    def start_time(self):
        """ Returns the timestamp of the first line in this log.

        If the log is not empty (the length of the array holding lines is > 0), this property will hold the timestamp
        of the earliest message in the log

        :return: the timestamp of the first :class:`CEFLine <CEFLine>` in the log
        :rtype: datetime
        """
        if not self.is_empty:
            return self.lines[0].timestamp
        else:
            return None

    @property
    def end_time(self):
        """ Returns the timestamp of the last line in this log.

        If the log is not empty (the length of the arry holding lines is > 0), this property will hold the timestamp
        of the last message in the log

        :return: the timestamp of the last :class:`CEFLine <CEFLine>` in the log
        :rtype: datetime
        """
        if not self.is_empty:
            return self.lines[-1].timestamp
        else:
            return None

    @property
    def has_syslog_prefix(self):
        """ Returns True if the entries in the log have a syslog prefix.

        This attribute determines whether or not the log was created with lines that contain a syslog prefix. If the
        log object is empty (has no lines), this property will default to ``False``

        :return: ``True`` the first line added to this log contains a syslog prefix, ``False`` otherwise, or if the log
            has no lines
        :rtype: bool
        """
        if len(self.lines) > 0:
            return self.lines[0].has_syslog_prefix
        else:
            return False

    @property
    def is_empty(self):
        """ True if this log has no lines present. """
        return len(self.lines) == 0

    def __repr__(self):
        return '<CEFLog [%s line%s]>' % (self.linecount, 's' if self.linecount != 1 else '')

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

        if line.has_syslog_prefix ^ self.has_syslog_prefix and not self.is_empty:
            raise SyslogPrefixError('Cannot append lines with headers inconsistent with lines already present',
                                    line=line)
        else:
            self.lines.append(line)
            if self.has_syslog_prefix:
                self.lines.sort(key=lambda l: l.timestamp)

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
