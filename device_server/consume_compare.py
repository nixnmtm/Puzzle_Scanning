#!/usr/bin/env python

import pika, json, logging, requests
import more_itertools as mit

logging.basicConfig(level=logging.INFO)
all_dev = []
test = {}
deviinfo_url = "http://10.10.70.89:3000/puzzle/api/v1/deviceinfo/getById"

def get_mesdevinfo(url, devid):
    if devid is str:
        pass
    else:
        devid = str(devid)
        params = {"serialno": devid}
    try:
        mesdevinfo = requests.get(url, params=params)
        mesdevinfo = json.loads(mesdevinfo.text)
        if not mesdevinfo["info"]:
            logging.error("No valid device(serialno: {}) information from MES server".format(devid))
        if mesdevinfo["info"][0]["serialno"] == devid:
            return mesdevinfo["info"][0]["macInfo"]
    except Exception as e:
        logging.error("Damn, error in accessing the MES device info url")

def add2list(data):
    all_dev.append(json.dumps(data))
    print(all_dev)

def read_json(json_data):
    """Convert bytes datatype to str"""

    if type(json_data) == bytes:
        data = json_data.decode('ascii')
        data = json.loads(data)
        return data
    if type(json_data) == str:
        data = json.loads(json_data)
        return data

def callback(ch, method, properties, body):
    data = read_json(json_data=body)
    local_devid = data["serialno"]
    mesmacinfo = get_mesdevinfo(url=deviinfo_url, devid=local_devid)
    #mesmacinfo = get_mesdevinfo(url=deviinfo_url, devid="1007") # error test
    for k, v in data["macinfo"].items():
        for i in mesmacinfo:
            if k == i.get("interface"):
            #if k == "enp3s0":
                if v.get("macaddr") == i.get("macaddr"):
                    data["macinfo"][k]["scanstatus"] = "PASS"
                else:
                    data["macinfo"][k]["scanstatus"] = "FAIL"
            else:
                data["macinfo"][k]["scanstatus"] = "FAIL"
    test.update(data)
    all_dev.append(data)
    ch.basic_ack(delivery_tag = method.delivery_tag)

def start_connection(host='localhost', queue_name='hwinfo_queue'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    logging.info('[*] Waiting for client device information. To exit press CTRL+C')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue=queue_name)
    channel.start_consuming()

def main():
    start_connection()
if __name__ == '__main__':
    main()


# def dummy():
#     print(all)

# def get_numofdev(data):
#     totdev = data["ndev"]
#     return totdev


