#!/usr/bin/env python
import pika
import json
from PZLutils import PZLutils

#pzl = PZLutils()
#
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='logs',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='logs',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    pzl = PZLutils()
    json_data = body
    url = 'http://127.0.0.1:5000/puzzle/api/v1/hwinfo'
    print(body)
    print(pzl.retrieve_hwinfo(json_data, url))

channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

channel.start_consuming()