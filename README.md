# Retrieve hardware info based on device id

1. Consume device id from main server (as of now rabbitmq_server_dummy.py)
2. Check whether the local device is in the list (device_client.py, PZLUtils.py)
3. Run retrieve HWInfo API (device_client.py, PZLUtils.py)
4. Route it to queue, server side
5. Compare Mongo DB data and HWInfo data 
6. Insert if SUCCESS
7. send log if FAIL 


### **Dependencies:**

* Python 3.5
* flask 1.0.2
* pika 0.11.0
* requests 2.19.1

#### RabbitMQ Version: 3.7.7(Erlang 21.0)

# Json Hardware details Format
```
{
  "CPUinfo": {
    "Architecture": "x86_64",
    "CPU(s)": "12",
    "Core(s) per socket": "6",
    "Thread(s) per core": "2"
  },
  "MEMinfo": {
    "MemAvailable": "12.71 GB",
    "MemFree": "10.92 GB",
    "MemTotal": "23.47 GB"
  },
  "PCIinfo": {
    "0000:02:00.0": {
      "Description": "Ethernet Controller X710 for 10GbE SFP+",
      "Driver": "i40e",
      "Interface": "enp2s0f0",
      "MACaddr": "00:18:7d:a4:cc:a3"
    },
    "0000:08:00.0": {
      "Description": "I211 Gigabit Network Connection",
      "Driver": "igb",
      "Interface": "enp8s0",
      "MACaddr": "e0:18:7d:2e:cb:44"
    },
    "0000:09:00.0": {
      "Description": "I211 Gigabit Network Connection",
      "Driver": "igb",
      "Interface": "enp9s0",
      "MACaddr": "e0:18:7d:2e:cb:45"
    },
    "0000:0a:00.0": {
      "Description": "I211 Gigabit Network Connection",
      "Driver": "igb",
      "Interface": "enp10s0",
      "MACaddr": "e0:18:7d:2e:cb:45"
    }
  }
}
```