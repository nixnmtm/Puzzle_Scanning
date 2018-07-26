# Retrieve hardware info based on device serial number

1. Consume device serial number from MES server (as of now rabbitmq_server_dummy.py)

    ``` Fanout mechanism    - exchange = 'devSNo'
                            - exchange_type = fanout
                            - queue --> exlcusive = True
             should be maintained in both Producer and Consumer ```
            
2. Locally, check whether the current device Sl.No in the list (consume_retreive_produce.py, PZLUtils.py)
3. Run retrieve HWInfo API (consume_retreive_produce.py, PZLUtils.py).
4. Publish it back to main server using the same connection through unique route key.(consume_retreive_produce.py, consume_compare.py, PZLUtils.py)

       ``` Work Queue mechanism - queue_name = 'hwinfo_queue'
                                - durable = True ```
                            
5. Compare Mongo DB data and HWInfo data and POST the report and notification message.

### **Dependencies:**

* Python 3.5
* flask 1.0.2
* pika 0.11.0
* requests 2.19.1

#### RabbitMQ Version: 3.7.7(Erlang 21.0)

### Hardware information Json format

Accumulating each device dictionary in a list

```
{ "scanid": "1",
  "devslno": "007",
  "cpuinfo": {
    "architecture": "x86_64",
    "corepersocket": "6",
    "cpu": "12",
    "threadpercore": "2"
  },
  "meminfo": {
    "memavailable": "11.37 GB",
    "memfree": "9.15 GB",
    "memtotal": "23.47 GB"
  },
  "pciinfo": {
    "0000:02:00.1": {
      "description": "Ethernet Controller X710 for 10GbE SFP+",
      "driver": "i40e",
      "interface": "enp2s0f1",
      "macaddr": "00:18:7d:a4:cc:a4"
    },
    "0000:02:00.2": {
      "description": "Ethernet Controller X710 for 10GbE SFP+",
      "driver": "i40e",
      "interface": "enp2s0f2",
      "macaddr": "00:18:7d:a4:cc:a5"
    },
    "0000:03:00.0": {
      "description": "I211 Gigabit Network Connection",
      "driver": "igb",
      "interface": "enp3s0",
      "macaddr": "e0:18:7d:2e:ca:67"
    },
    "0000:04:00.0": {
      "description": "I211 Gigabit Network Connection",
      "driver": "igb",
      "interface": "enp4s0",
      "macaddr": "e0:18:7d:2e:ca:68"
    },
    "0000:05:00.0": {
      "description": "I211 Gigabit Network Connection",
      "driver": "igb",
      "interface": "enp5s0",
      "macaddr": "e0:18:7d:2e:ca:69"
    }
  }
}

```