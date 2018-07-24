#!/usr/bin/env python
import pika
from device_client.PZLutils import PZLutils

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='devSNo',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='devSNo',
                   queue=queue_name)

print('[*] Waiting for Device serial numbers. To exit press CTRL+C')

def callback(ch, method, properties, body):

    pzl = PZLutils()
    data = pzl.read_json(body)
    url = 'http://127.0.0.1:5000/puzzle/api/v1/hwinfo'
    #print(pzl.retrieve_hwinfo(data=data, url=url))
    channel.basic_publish(exchange='',
                          routing_key='hwinfo_queue',
                          body=pzl.retrieve_hwinfo(data, url))

channel.basic_consume(callback, queue=queue_name, no_ack=True)
channel.start_consuming()

