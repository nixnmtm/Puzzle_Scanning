#!/usr/bin/env python

import sys
import pika
import json
import logging
import requests
#from device_client.utils import pzlutils, hwinfo
from utils import pzlutils, hwinfo

pzl = pzlutils.PZLutils()
#logging.basicConfig(filename='dev_consume.log', level=logging.INFO, filemode='w')
logging.basicConfig(level=logging.INFO)

def populate_data(data):
    hw_info = {}
    get_dev_slno = pzl.this_device_slno()
    logging.info("Populating hardware datas from device ===> Sl.No: {}".format(get_dev_slno))
    hw_info["operationId"] = data["operationId"]
    hw_info["sn"] = get_dev_slno
    temp = hwinfo.pci_info()
    hw_info["macinfo"] = {}
    for k in temp["pciinfo"].keys():
        hw_info["macinfo"][temp["pciinfo"][k]["interface"]] = {}
        hw_info["macinfo"][temp["pciinfo"][k]["interface"]]["macaddr"] = temp["pciinfo"][k]["macaddr"]
    print(hw_info)
    return hw_info

def callback(ch, method, properties, body):
    data = pzl.read_json(body)
    print(data)
    try:
        if data["action"] == 1: # configured with assumption that only start action is available
            logging.info("{}Scanning Initiated{}".format("-"*10, "-"*10))
            hw_info = populate_data(data)
            ch.queue_declare(queue='hwinfo_queue', durable=True)
            if not hw_info: # if dictionary is empty
                pass
            else: # publishing to server from client only if the device is present

                logging.info("Publishing to device server side")
                ch.basic_publish(exchange='',
                                  routing_key='hwinfo_queue',
                                  body=json.dumps(hw_info),
                                  properties=pika.BasicProperties(delivery_mode=1))
    except Exception as e:
        logging.error("**Scanning not initiated." + str(e))

def run(host, ex_name, ex_type, username, password, port):
    credentials = pika.PlainCredentials(username=username, password=password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, credentials=credentials))
    channel = connection.channel()
    channel.exchange_declare(exchange=ex_name,
                             exchange_type=ex_type)
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=ex_name, queue=queue_name)
    logging.info('[*] Waiting to start scan. To exit press CTRL+C')
    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    channel.start_consuming()


if __name__ == '__main__':

    def callapi(data):
        url = 'http://{}:{}/deviceInfo'.format("localhost", 8882)
        headers = {'Content-type': 'application/json'}
        r = requests.post(url, data, headers=headers)
        print('Response Code: ', r.status_code)
        retData = {}
        if r.status_code == 200:
            retData["result"] = 1
            retData["data"] = json.loads(r.text)
        else:
            retData["result"] = 2
        return retData


    def myInput():
        retData = {}
        inputdata = {
            "config": {
                "name": [1]
            },
            "device": {
                "name": [0]
            }
        }
        tmp = json.dumps(inputdata)
        tmpapi = callapi(tmp)
        if tmpapi["result"] == 1: # PASS:
            rabbitMQ = {}
            sn = None
            flag = 0
            apidata = tmpapi["data"]
            tmp = apidata["config"]
            for loop in tmp:
                data = loop["data"]
                if loop["name"] == 1:
                    if isinstance(data, dict):
                        flag = flag + 1
                        rabbitMQ["username"] = data["user"]
                        rabbitMQ["password"] = data["password"]
                        rabbitMQ["host"] = data["ip"]
                        rabbitMQ["port"] = data["port"]
            tmp = apidata["device"]
            for loop in tmp:
                data = loop["data"]
                if loop["name"] == 0:
                    if len(data) > 0:
                        flag = flag + 1
                        sn = data
            if flag == 2:
                retData["result"] = 1 # PASS
                retData["rabbitMQ"] = rabbitMQ
                retData["sn"] = sn
            else:
                retData["result"] = 2
            print("myInput retData {}".format(data))
        else:
            retData["result"] = 2
        return retData


    myInputData = myInput()
    if myInputData["result"] == 1:
        mqdata = myInputData["rabbitMQ"]
        sn = myInputData["sn"]
        print(mqdata)
        print(sn)

    # mqhost = str(sys.argv[1])
    # mqport = int(sys.argv[2])
    # mqusername = str(sys.argv[3])
    # mqpassword = str(sys.argv[4])
    ex_name = "devicescan"
    ex_type = 'fanout'

    mqhost = mqdata['host']
    mqport = int(mqdata['port'])
    mqusername = mqdata["username"]
    mqpassword = mqdata["password"]

    run(mqhost, ex_name, ex_type, mqusername, mqpassword, mqport)
