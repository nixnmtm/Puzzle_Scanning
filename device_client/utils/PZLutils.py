#!/usr/bin/env python

"""Utilities fro puzzle device info"""
from __future__ import division
import random
import json
import requests
import logging
import subprocess

class PZLutils(object):

    def execute_cmd(self, cmd):
        """Execute the given command on the local node

        :param cmd: Command to run locally.
        :param timeout: Timeout value
        :type cmd: str
        :type timeout: int
        :return return_code, stdout, stderr
        :rtype: tuple(int, str, str)
        """

        #logging.info(" Local Command: {}".format(cmd))
        out = ''
        err = ''
        prc = subprocess.Popen(cmd, shell=True, bufsize=1,
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        with prc.stdout:
            for line in iter(prc.stdout.readline, b''):
                line = line.decode("utf-8")
                #logging.info("  {}".format(line.strip('\n')))
                out += line

        with prc.stderr:
            for line in iter(prc.stderr.readline, b''):
                line = line.decode("utf-8")
                #logging.warning("  {}".format(line.strip('\n')))
                err += line

        ret = prc.wait()
        return ret, out, err

    # ---------------------------------------------------------------------------

    def this_device_slno(self):

        """Get device name from the device - This is a dummy"""
        """Getting a random name from a list to check"""
        #dev_list = ["{0:03}".format(i) for i in range(10)]
        #dev_list = [i for i in range(1001, 1004)]
        dev_list = ["Q186I15900", "Q186I15901", "Q186I15815"]
        pzl_devname = random.choice(dev_list)
        return pzl_devname

    def retrieve_hwinfo(self, url):

        """Call HWInfo API and retrieve the response"""

        apiResponse = requests.get(url, verify=True)
        if apiResponse.ok:
            hwinfo = apiResponse.text
            return hwinfo
        else:
            return apiResponse.raise_for_status()


    def read_json(self, json_data):

        """Convert bytes or str datatype to dict"""

        if type(json_data) == bytes:
            data = json_data.decode('ascii')
            data = json.loads(data)
            return data
        if type(json_data) == str:
            data = json.loads(json_data)
            return data