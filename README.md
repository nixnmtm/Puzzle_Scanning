# Retrieve hardware info based on device serial number

1. Start scanning when command received in all client devices. (as of now rabbitmq_server_dummy.py)

    ``` Fanout mechanism    - exchange = 'devicescan'
                            - exchange_type = fanout
                            - queue --> exlcusive = True
             should be maintained in both Producer and Consumer ```
            
2. Locally, retrieve all device informations using HWInfo API.(http://40.74.91.221/Nixon/VNet_APIs/blob/master/HWInfo.py)
3. Publish it back to main server using the same connection through unique route key.(device_scan.py, server_scan.py, PZLUtils.py)

       ``` Work Queue mechanism - queue_name = 'hwinfo_queue'
                                - durable = True ```
                            
5. GET MES data from device_info API and compare with HWInfo data.
6. POST notifications to notifications API.
7. POST compared response/log to deviceScan API.

### **Dependencies:**

* Python 3.5
* flask 1.0.2
* pika 0.11.0
* requests 2.19.1
* more_itertools 4.2.0

#### RabbitMQ Version: 3.7.7(Erlang 21.0)

### Hardware information Json format

Accumulating each device dictionary in a list

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
            "sn": 1001
        },
        {
            "macinfo": [
                {
                    "interface": "enp5s0",
                    "macaddr": "e0:18:7d:2e:ca:69",
                    "scanstatus": "0"
                },
                {
                    "interface": "enp2s0f3",
                    "macaddr": "00:18:7d:a4:cc:a6",
                    "scanstatus": "0"
                },
                {
                    "interface": "enp8s0",
                    "macaddr": "e0:18:7d:2e:cb:44",
                    "scanstatus": "0"
                }
            ],
            "sn": 1003
        }
    ]
}

```