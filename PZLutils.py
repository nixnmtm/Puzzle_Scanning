#!/usr/bin/env python

"""Utilities fro puzzle device info"""
from __future__ import division
import random
import json
import requests

class PZLutils(object):

    def _this_device_name(self):

        """Get device name from the device - This is a dummy"""
        """Getting a random name from a list to check"""

        dev_list = ["{0:03}".format(i) for i in range(10)]
        pzl_devname = random.choice(dev_list)
        print("This Device Name: {}".format(pzl_devname))
        return pzl_devname

    def call_HWInfo_api(self, url):

        """Call HWInfo API and extract the response"""

        apiResponse = requests.get(url, verify=True)
        if apiResponse.ok:
            #hwinfo = json.loads(apiResponse.text)
            hwinfo = apiResponse.text
            return hwinfo
        else:
            return apiResponse.raise_for_status()

    def retrieve_hwinfo(self, data, url):

        """If device name in query retrieve hardware information of the device"""

        #data = json.loads(data)  # convert the json into python compatible
        data = json.loads(data)
        for i in data:
            if i == "devices":
                if self._this_device_name() in data[i]:
                    return self.call_HWInfo_api(url)
                else:
                    #return "ERROR"
                    raise ResourceWarning("Device {} is not listed".format(self._this_device_name()))

# pzl = PZLutils()
# #json_data = json.loads(body)
# dat = {}
# dat["devices"] = ["{0:03}".format(i) for i in range(5)]
# json_data = json.dumps(dat)  # data will be in json format
# url = 'http://127.0.0.1:5000/puzzle/api/v1/hwinfo'
#
# print(pzl.retrieve_hwinfo(json_data, url))