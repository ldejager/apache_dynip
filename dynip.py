#!/usr/bin/env python
#
# Apache dynamic Allow from IP
#
# Usage: dynip.py domain config
# Example: dynip.py domain.com /path/to/apache/config/file/to/update
# Requires: .ipdb in the same directory as this script

import socket
import argparse
import subprocess
import os

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
        self._wdpath = os.path.dirname(os.path.realpath(__file__)) + "/.ipdb"

    def __get_old_ip__(self):
        """ Read the old IP from a tmp file """

        global oldip

        try:
            with open(self._wdpath, "r") as f:
                oldip = f.readline()
        except IOError:
            print "Unable to read %s" % self._wdpath
            exit(1)

        return oldip

    def __get_new_ip__(self):
        """ Grab IP address from provided domain name """

        ip = socket.gethostbyname_ex(self._domain)[2]
        for ip in ip:
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
            print "Error reading or writing %s" % self._config

    def __set_old_ip__(self):
        """ Set obtained IP as the old IP in tmp file """

        try:
            with open(self._wdpath, "w") as f:
                f.write(self.__get_new_ip__())
                f.close()
        except IOError:
            print "Error writing current IP to %s" % self._wdpath

    def __restart_apache__(self):
        """ Restart the httpd daemon once changes have been made """

        try:
            command = ['service', 'httpd', 'reload']
            subprocess.call(command, shell=False)
        except OSError, e:
            print "Error reloading httpd:", e


if __name__ == '__main__':

    DynIP = ApacheDynIP(argument.domain, argument.config)

    DynIP.__get_new_ip__()
    DynIP.__get_old_ip__()
    DynIP.__write_config__()
    DynIP.__set_old_ip__()
    DynIP.__restart_apache__()
