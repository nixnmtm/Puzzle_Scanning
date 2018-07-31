#!/usr/bin/env python
import pika
import json

data = {}


def send_dev_SlNo():
    #send_dev_SlNo.counter += 1
    credentials = pika.PlainCredentials(username="rmquser", password="123456")
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="10.10.70.89", port=5672, credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange='devicescan',exchange_type='fanout')
    data["scan_id"] = 1
    #data['devices'] = ["{0:03}".format(i) for i in range(8)]
    data['devices'] = [i for i in range(1001, 1010)]
    json_data = json.dumps(data)
    channel.basic_publish(exchange='devicescan',
                          routing_key='',
                          body=json_data)
    print(" [x] Sent from dummy server{}".format(json_data))
    connection.close()

for i in range(3):
    send_dev_SlNo()
