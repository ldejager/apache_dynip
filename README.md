Apache DynIP
============

Allows updating of the Apache "Allow from x.x.x.x " configuration with a dynamic IP periodically.

Usage:      dynip.py domain config
Example:    dynip.py home.dyndns.org /etc/httpd/conf.d/vhost.conf

Known Issues
============

There needs to be a space between the IP address being replaced and the closing Location tag. I'm currently looking into this particular bug.

        <Location "/">
                Order deny,allow
                Deny from all
                Allow from 5.66.90.210

        </Location>

