# -*- coding: utf-8 -*-

""" Pourover's non-exhaustive test suite. """

import pourover
import pytest
from datetime import datetime

SAMPLE_LINE = 'Apr 15 22:11:20 testhost CEF:0|Test Vendor|Test Product|Test Version|100|Test Name|100|src=1.1.1.1 dst=1.1.1.2'
SAMPLE_EXPLODE = {
    'version': 0,
    'dev_vendor': 'Test Vendor',
    'dev_product': 'Test Product',
    'dev_version': 'Test Version',
    'dev_event_class_id': 100,
    'name': 'Test Name',
    'severity': 100,
    }

class TestPourover:

    def test_factory_availability(self):
        pourover.parse_line(SAMPLE_LINE)
        pourover.create_line(**SAMPLE_EXPLODE)
    
    def test_object_availability(self):
        pourover.CEFLog()
        pourover.CEFMessage()

    def test_parse_correctness(self):
        line = pourover.parse_line(SAMPLE_LINE)
        assert line._raw_line is not None
        assert line._raw_header is not None
        assert len(line._extensions) == 2
        assert len(line._headers) == 8
        assert line.prefix is not None
        assert line.version == 0
        assert line.device_vendor == 'Test Vendor'
        assert line.device_product == 'Test Product'
        assert line.device_version == 'Test Version'
        assert line.device_event_class_id == '100'
        assert line.name == 'Test Name'
        assert line.severity == 100
        assert line.extensions is not None
        assert len(line.extensions) == 2
        assert line.headers is not None
        assert len(line.headers) == 8
        assert line.has_extensions
        assert line.timestamp is not None
        assert line.timestamp == datetime.strptime('Apr 15 22:11:20', '%b %d %H:%M:%S').replace(year=2018)

    def test_log_append(self):
        log = pourover.CEFLog()
        message = pourover.parse_line(SAMPLE_LINE)
        log.append(message)
        assert len(log) == 1
        assert log.has_syslog_prefix
        assert not log.is_empty
        assert isinstance(log[0], pourover.CEFMessage)

