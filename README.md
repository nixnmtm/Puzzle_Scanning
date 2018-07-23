# Retrieve hardware info based on device id

1. Consume device id from main server (as of now rabbitmq_server_dummy.py)
2. Check whether the local device is in the list (device_client.py, PZLUtils.py)
3. Run retrive HWInfo API (device_client.py, PZLUtils.py)
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
