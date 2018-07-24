#!/usr/bin/env python

import pika, json
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hwinfo_queue', durable=True)
print(' [*] Waiting for hardware info of devices. To exit press CTRL+C')

def callback(ch, method, properties, body):

    print(" [x] Received from local device: \n{}".format(body))
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='hwinfo_queue')
channel.start_consuming()

