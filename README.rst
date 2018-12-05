Pourover: Log Parsing for Lizards
=================================

.. image:: https://img.shields.io/badge/license-Apache%202.0-blue.svg
    :target: LICENSE

.. image:: https://img.shields.io/badge/python-3.6,%203.7-blue.svg
    :target: https://pypi.org/project/pourover/

.. image:: https://img.shields.io/badge/pypi-v0.1--beta8-green.svg
    :target: https://pypi.org/project/pourover/

.. image:: https://circleci.com/gh/zthart/pourover/tree/develop.svg?style=svg
    :target: https://circleci.com/gh/zthart/pourover/tree/develop

Pourover is the only *chemicaly-altered* CEF Log Parsing library for
Python, ideal for consumption by Lizard People.

.. figure:: https://user-images.githubusercontent.com/4873335/38774515-0f0b5514-4039-11e8-8437-facadd57a85c.jpg
   :alt: the requests guy does it so maybe it'll work for me

Some stuff we can do:

.. code-block:: python

    from datetime import datetime
    import pourover


    # Create log objects from a file
    log = pourover.parse_file('test.log')

    # check the length pythonically - expose useful properties
    if len(log) > 10:
        if log.has_syslog_prefix and log.start_time > datetime(year=2018, month=4, day=20):
            # perform some operations
            pass
        else:
            # perform some operations on a logfile that doesn't have syslog prefixes
            pass
    else:
        # perform some operations on a really small log
        pass

    # Find messages with a certain value in the header
    search_results = log.search_headers('Specific Vendor')

    for message in log:
        # iterate through each message in the log like you'd expect to be able to
        pass

    # Logs can be indexed/sliced in the way you'd expect
    first_message = log[0]
    last_message = log[-1]

    # Create message objects from a string
    message = pourover.parse_line('Apr 15 22:11:20 testhost CEF:0|Test Vendor|Test Product|Test Version|100|Test Name|100|src=1.1.1.1 dst=1.1.1.2')

    if message.has_syslog_prefix:
        if message.timestamp > datetime(year=2018, month=4, day=20):
            # perform an operation on logs from later than April 20th, 2018
            pass

    if 'src' in message.extensions:
        # do something if it's got an extension called 'src'
        pass
        
    if message.device_vendor == 'Some Vendor':
        # do something if the vendor is Some Vendor
        pass

    # stick this message right onto that log (it'll even order the messages by timestamp - wow!)
    log.append(message)

Installing :computer:
---------------------

To install Pourover, simply run

.. code-block:: bash

    $ pip install pourover
    ✨🐊✨

Features :crocodile:
--------------------

| - :dragon_face: Create CEF-formatted log lines from parameters with support for extensions and a syslog prefix
| - :dragon_face: Create useful line objects from a string, or an entire log object from a file
| - :dragon_face: Iterable log objects to manipulate collections of logs at once
| - :dragon_face: Parse lines with or without syslog prefixes *or* extensions with ease
| - :dragon_face: Search logs for messages with specific headers or extensions
| - :dragon_face: **And more to come...**

Contributing :dragon:
---------------------

| :bug: **Bugs:**
| Please create any issues you think I should check out! If there's a
  bug you spot or a function you think is acting up, please let me know.
  This project will have tests eventually, but until then I'm sure there
  will be issues sprouting up from time to time!

| :sparkles: **New Features/PRs:**
| The project is still in it's infancy, so PRs might have a rough time
  getting merged in while the codebase is in a constant state of flux,
  but I'd me more than happy to have a discussion with you about a new
  feature you'd like to see!

Get in Touch :snake:
--------------------

If you've found a Bug or would like to make a feature request, please
see the **Contributing** section above, thanks!

If you'd like to reach out, shoot me an email at `zach@csh.rit.edu <mailto:zach@csh.rit.edu>`_.
