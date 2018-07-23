#!/usr/bin/env python
import pika
import json



connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='devSNo',
                         exchange_type='fanout')
data = {}
data['devices'] = ["{0:03}".format(i) for i in range(5)]
json_data = json.dumps(data)
channel.basic_publish(exchange='devSNo',
                      routing_key='',
                      body=json_data)

print(" [x] Sent {}".format(json_data))

connection.close()


