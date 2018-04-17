# Pourover: Log Parsing for Lizards
[![license](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
![python](https://img.shields.io/badge/python-3.6-blue.svg)

Pourover is the only _chemicaly-altered_ CEF Log Parsing library for Python, ideal for consumption by Lizard People.

![the requests guy does it so maybe it'll work for me](https://user-images.githubusercontent.com/4873335/38774515-0f0b5514-4039-11e8-8437-facadd57a85c.jpg)

Some stuff we can do:
```python
from datetime import datetime
import pourover


# Create log objects from a file
log = pourover.parse_file('test.log')

# useful properties like linecount and start_time
if log.linecount > 10:
    if log.has_syslog_prefix and log.start_time > datetime(year=2018, month=4, day=20):
        # perform some operations
        pass
    else:
        # perform some operations on a logfile that doesn't have syslog prefixes
        pass
else:
    # perform some operations on a really small log
    pass

for message in log:
    # iterate through each message in the log like you'd expect to be able to
    pass

# Create message objects from a string
message = pourover.parse_line('Apr 15 22:11:20 testhost CEF:0|Test Vendor|Test Product|Test Version|100|Test Name|100|src=1.1.1.1 dst=1.1.1.2')

if message.has_syslog_prefix:
    if message.timestamp > datetime(year=2018, month=4, day=20):
        # perform an operation on logs from later than April 20th, 2018
        pass

if 'src' in message.extensions:
    # do something if it's got an extension called 'src'
    pass
    
if message.headers['DeviceVendor'] == 'Some Vendor':
    # do something if the vendor is Some Vendor
    pass

# stick this message right onto that log (it'll even order the messages by timestamp - wow!)
log.append(message)
```

## :crocodile: Features :crocodile:

* :dragon_face: Create CEF-formatted log lines from parameters with support for extensions and a syslog prefix
* :dragon_face: Create useful line objects from a string, or an entire log object from a file
* :dragon_face: Iterable log objects to manipulate collections of logs at once
* :dragon_face: Parse lines with or without syslog prefixes _or_ extensions with ease
* :dragon_face: **And more to come...**

## :dragon: Contributing :dragon:

:bug: **Bugs:**  
Please create any issues you think I should check out! If there's a bug you spot or a function you think is acting up, 
please let me know. This project will have tests eventually, but until then I'm sure there will be issues sprouting up 
from time to time! 

:sparkles: **New Features/PRs:**  
The project is still in it's infancy, so PRs might have a rough 
time getting merged in while the codebase is in a constant state of flux, but I'd me more than happy to have a 
discussion with you about a new feature you'd like to see!

## :snake: Get in Touch :snake:

_If you've found a Bug or would like to make a feature request, please see the **Contributing** section above, thanks!_

If you'd like to reach out, shoot me an email at **[zach@csh.rit.edu](mailto:zach@csh.rit.edu)**
