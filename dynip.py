#!/usr/bin/env python
#
# Apache dynamic Allow from IP
#
# Usage: dynip.py domain config
# Example: dynip.py domain.com /path/to/apache/config/file/to/update
# Requires: /tmp/oldip

import socket
import argparse

args_parse = argparse.ArgumentParser(prog='dynip.py', usage='%(prog)s [domain] [config]')
args_parse.add_argument("domain", help="Provide domain which we should resolve and update the apache configuration with")
args_parse.add_argument("config", help="Provide configuration file that we should update with the provided IP")
argument = args_parse.parse_args()

oldip = ""

class ApacheDynIP(object):
    """ Apache Dynamic IP Class """

    def __init__(self, domain, config):
        """ Initializing """

        self._domain = domain
        self._config = config

    @staticmethod
    def __get_old_ip__(self):
        """ Read the old IP from a tmp file """

        try:
            with open("/tmp/oldip", "r") as f:
                oldip = f.readline()
        except IOError:
            print "Unable to read tmp file"

        return oldip

    def __get_new_ip__(self):
        """ Grab IP address from provided domain name """

        ip = socket.gethostbyname_ex(self._domain)[2]
        for ip in ip:
            """ print ip """
            """ print self.__get_old_ip__() """
            return ip

    def __write_config__(self):
        """ Write apache configuration to disk """

        try:
            with open(self._config, "r") as f:
                newlines = []
                for line in f.readlines():
                    newlines.append(line.replace(self.__get_old_ip__(), self.__get_new_ip__()))
            with open(self._config, "w") as f:
                for line in newlines:
                    f.write(line)
        except IOError:
            print "Error reading or writing configuration file"


if __name__ == '__main__':

    DynIP = ApacheDynIP(argument.domain, argument.config)

    DynIP.__get_new_ip__()
    DynIP.__get_old_ip__()
    DynIP.__write_config__()
