#!/usr/bin/env python
import pika
import json

data = {}


def send_dev_SlNo():
    #send_dev_SlNo.counter += 1
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange='devSNo',
                             exchange_type='fanout')
    #data["scan_id"] = str(send_dev_SlNo.counter)
    data["scan_id"] = 1
    print(["{0:03}".format(i) for i in range(8)])
    data['devices'] = ["{0:03}".format(i) for i in range(8)]
    json_data = json.dumps(data)
    channel.basic_publish(exchange='devSNo',
                          routing_key='',
                          body=json_data)

    print(" [x] Sent from dummy server{}".format(json_data))
    connection.close()

send_dev_SlNo.counter = 0


for i in range(5):
    send_dev_SlNo()
