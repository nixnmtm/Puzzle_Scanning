#!/usr/bin/env python

import pika
import json
import logging
from device_client.PZLutils import PZLutils

logging.basicConfig(level=logging.INFO)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hwinfo_queue', durable=True)
print(' [*] Waiting for hardware info of devices. To exit press CTRL+C')

#all_dev = {}
def callback(ch, method, properties, body):
    #callback.counter += 1
    pzl = PZLutils()
    #str(callback.counter)] = pzl.read_json(body)
    print(json.dumps(pzl.read_json(body), sort_keys=True, indent=4, separators=(',', ': ')))
    ch.basic_ack(delivery_tag = method.delivery_tag)
    #print(json.dumps(all_dev))
callback.counter = 0
channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='hwinfo_queue')
channel.start_consuming()


