# Scan BurnIn devices

1. Start scanning when command received in all client devices. (as of now rabbitmq_server_dummy.py)

    ``` Fanout mechanism    - exchange = 'devicescan'
                            - exchange_type = fanout
                            - queue --> exlcusive = True
             should be maintained in both Producer and Consumer ```
            
2. Locally, retrieve all device informations using HWInfo API.(http://40.74.91.221/Nixon/VNet_APIs/blob/master/HWInfo.py)
3. Publish it back to edge server using the same connection through unique route key.(device_scan.py, server_scan.py, PZLUtils.py)

       ``` Work Queue mechanism - queue_name = 'hwinfo_queue'
                                - durable = True ```
                            
5. GET MES data from device_info API and compare with HWInfo data.
6. POST notifications to notifications API.
7. POST compared response/log to deviceScan API.
8. Check if all macs passed the scan, then result is "Pass" and send to Pair API.

### **Dependencies:**

* Python 3.5
* flask 1.0.2
* pika 0.11.0
* requests 2.19.1
* more_itertools 4.2.0

#### RabbitMQ Version: 3.7.7(Erlang 21.0)

### Hardware information Json format
1. "scanstatus" : (0:Fail, 1: Pass)
2. "result": (0:Fail, 1: Pass) # if all macs passed the scan, then result is "Pass" and send to Pair API

### DScanning Client as Service:
1. Run setupDScanning.sh
2. START  : ```systemctl start DScanning@"10.10.70.89 5672 rmquser 123456"```
3. STATUS : ```systemctl status DScanning@"10.10.70.89 5672 rmquser 123456"```
4. STOP   : ```systemctl status DScanning@"10.10.70.89 5672 rmquser 123456"```


Example:

```
{
    "operationid": 1,
    "scaninfo": [
        {
            "macinfo": [
                {
                    "interface": "enp4s0",
                    "macaddr": "e0:18:7d:2e:ca:68",
                    "scanstatus": "1"
                },
                {
                    "interface": "enp6s0",
                    "macaddr": "e0:18:7d:2e:ca:6a",
                    "scanstatus": "0"
                },
                {
                    "interface": "enp5s0",
                    "macaddr": "e0:18:7d:2e:ca:69",
                    "scanstatus": "0"
                }
            ],
            "sn": 1001,
            "result": "0"
        },
        {
            "macinfo": [
                {
                    "interface": "enp5s0",
                    "macaddr": "e0:18:7d:2e:ca:69",
                    "scanstatus": "1"
                },
                {
                    "interface": "enp2s0f3",
                    "macaddr": "00:18:7d:a4:cc:a6",
                    "scanstatus": "1"
                },
                {
                    "interface": "enp8s0",
                    "macaddr": "e0:18:7d:2e:cb:44",
                    "scanstatus": "1"
                }
            ],
            "sn": 1003,
            "result": "1"
        }
    ]
}

```