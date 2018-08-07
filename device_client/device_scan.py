#!/usr/bin/env python

import sys
import pika, json, logging
from device_client.PZLutils import PZLutils
sys.path.append("../")

pzl = PZLutils()
#logging.basicConfig(filename='dev_consume.log', level=logging.INFO, filemode='w')
logging.basicConfig(level=logging.INFO)

def populate_data(data):
    hw_info = {}
    get_dev_slno = pzl.this_device_slno()
    logging.info("Populating hardware datas from device ===> Sl.No: {}".format(get_dev_slno))
    hw_info["operationId"] = data["operationId"]
    hw_info["sn"] = get_dev_slno
    temp = pzl.read_json(pzl.retrieve_hwinfo(url))
    if "cpuinfo" in temp.keys():
        temp.pop("cpuinfo")
    if "meminfo" in temp.keys():
        temp.pop("meminfo")
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
    # mqhost = str(sys.argv[1])
    # mqport = int(sys.argv[2])
    # mqusername = str(sys.argv[3])
    # mqpassword = str(sys.argv[4])
    # apihost = str(sys.argv[5])
    # apiport = int(sys.argv[6])
    mqhost = "10.10.70.89"
    mqport = 5672
    mqusername = "rmquser"
    mqpassword = "123456"
    apihost = '127.0.0.1'
    apiport = 5000
    ex_name = "devicescan"
    ex_type = 'fanout'


    url = 'http://'+ apihost +':'+ str(apiport) +'/puzzle/api/v1/hwinfo'
    run(mqhost, ex_name, ex_type, mqusername, mqpassword, mqport)
