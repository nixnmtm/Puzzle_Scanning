#!/usr/bin/env python

"""Utilities fro puzzle device info"""
from __future__ import division
import random
import json
import requests

class PZLutils(object):

    def _this_device_slno(self):

        """Get device name from the device - This is a dummy"""
        """Getting a random name from a list to check"""

        dev_list = ["{0:03}".format(i) for i in range(10)]
        pzl_devname = random.choice(dev_list)
        print("Device Sl.No: {}".format(pzl_devname))
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

        """If device serial number in query retrieve hardware information of the device"""

        #data = json.loads(data)  # convert the json into python compatible
        data = json.loads(data)
        for i in data:
            if i == "devices":
                if self._this_device_slno() in data[i]:
                    print("Device Sl.No Matched. \nHardware details retrieved and sent to main server.")
                    return self.call_HWInfo_api(url)
                else:
                    return "Device Sl.No not matched"
                    #return "ERROR"
                    #raise ResourceWarning("Me ({}) not listed.".format(self._this_device_slno()))

    def read_json(self, json_data):
        if type(json_data) == bytes:
            data = json_data.decode('utf8').replace("'", '"')
            data = json.loads(json.dumps(data))
            return data
        if type(json_data) == str:
            data = json.loads(json_data)
            return data
