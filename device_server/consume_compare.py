#!/usr/bin/env python

import pika
import json
import logging
from device_client.PZLutils import PZLutils
from collections import OrderedDict

logging.basicConfig(level=logging.INFO)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hwinfo_queue', durable=True)
print(' [*] Waiting for hardware info of devices. To exit press CTRL+C')

# def pzlorderDict(d):
#     orders = ("scanid", "devslno", "cpuinfo", "meminfo", "pciinfo")
#     for key in orders:
#         v = d[key]
#         del d[key]
#         d[key] = v
#     return d

all_dev = []
def callback(ch, method, properties, body):
    #callback.counter += 1
    pzl = PZLutils()
    #str(callback.counter)] = pzl.read_json(body)
    data = OrderedDict(pzl.read_json(body))
    all_dev.append(json.dumps(data, sort_keys=True, indent=2, separators=(',', ': ')))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    print(json.dumps(all_dev))
callback.counter = 0
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='hwinfo_queue')
channel.start_consuming()


