# Pourover: Log Parsing for Lizards
[![license](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
![python](https://img.shields.io/badge/python-3.6-blue.svg)

Pourover is the only _chemicaly-altered_ CEF Log Parsing library for Python, ideal for consumption by Lizard People.

![the requests guy does it so maybe it'll work for me](https://user-images.githubusercontent.com/4873335/38774515-0f0b5514-4039-11e8-8437-facadd57a85c.jpg)

Some stuff we can do:
```python
>>> import pourover
>>> line = pourover.parse_line('CEF:0|<DeviceVendor>|<DeviceProduct>|<DeviceVersion>|<DeviceEventClassID>|<Name>|<Severity>|')
>>> line.has_syslog_prefix
False
>>> line.has_extensions
False
>>> str(line)
'CEF:0|<DeviceVendor>|<DeviceProduct>|<DeviceVersion>|<DeviceEventClassID>|<Name>|<Severity>|'
```

## :crocodile: Features :crocodile:

This is a WIP project - check back as more features are added

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

_If you've found a Bug or would like to make a feature requests, please see the **Contributing** section above, thanks!_

If you'd like to reach out, shoot me an email at **[zach@csh.rit.edu](mailto:zach@csh.rit.edu)**
