#!/usr/bin/env python

"""Utilities fro puzzle device info"""
from __future__ import division
import random
import json
import requests

class PZLutils(object):

    def this_device_slno(self):

        """Get device name from the device - This is a dummy"""
        """Getting a random name from a list to check"""

        dev_list = ["{0:03}".format(i) for i in range(10)]
        pzl_devname = random.choice(dev_list)
        #print("Device Sl.No: {}".format(pzl_devname))
        return pzl_devname

    def retrieve_hwinfo(self, url):

        """Call HWInfo API and retrieve the response"""

        apiResponse = requests.get(url, verify=True)
        if apiResponse.ok:
            #hwinfo = json.loads(apiResponse.text)
            hwinfo = apiResponse.text
            return hwinfo
        else:
            return apiResponse.raise_for_status()

    def read_json(self, json_data):
        if type(json_data) == bytes:
            data = json_data.decode('ascii')
            data = json.loads(data)
            return data
        if type(json_data) == str:
            data = json.loads(json_data)
            return data
