#!/usr/bin/env python

import pika, json, logging, requests
import more_itertools as mit

logging.basicConfig(level=logging.INFO)
all_dev = []
devfound = []
deviinfo_url = "http://10.10.70.89:3000/puzzle/api/v1/deviceinfo/getById"

def get_mesdevinfo(url, devid):
    if devid is str:
        pass
    else:
        devid = str(devid)
    try:
        querystring = {"serialno": devid}
        headers = {
            'Cache-Control': "no-cache",
            'Postman-Token': "4e74f131-a27f-4aa1-82da-54fa4d646344"
        }
        mesdevinfo = requests.request("GET", url, params=querystring, headers=headers)

    except Exception as e:
        logging.error("Damn, error in accessing the MES device info url")

    try:
        mesdevinfo = json.loads(mesdevinfo.text)
        if not mesdevinfo["info"]:
            logging.error("No valid device(serialno: {}) information from MES server".format(devid))
        if mesdevinfo["info"][0]["serialno"] == devid:
            return mesdevinfo["info"][0]["macInfo"]
    except Exception as e:
        logging.error("No device info found")

def read_json(json_data):
    """Convert bytes datatype to str"""

    if type(json_data) == bytes:
        data = json_data.decode('ascii')
        data = json.loads(data)
        return data
    if type(json_data) == str:
        data = json.loads(json_data)
        return data

def notify():
    global all_dev
    global devfound
    logging.info("Sending notification to the user")
    print(all_dev)
    print(devfound)
    logging.info("Resume consuming")
    all_dev = []
    devfound = []

def double_check(locdata, mesdata):

    """double check and report scanstatus,
    whether device and mac address are same as in MES data"""

    for k, v in locdata["macinfo"].items():
        for i in mesdata:
            if k == i.get("interface"):
            #if k == "enp3s0":
                if v.get("macaddr") == i.get("macaddr"):
                    locdata["macinfo"][k]["scanstatus"] = "1"
                else:
                    locdata["macinfo"][k]["scanstatus"] = "0"
            else:
                locdata["macinfo"][k]["scanstatus"] = "0"
    return locdata

timer_id=None
def callback(ch, method, properties, body):

    """Receive local_device info and
    do compare adn send number of devices found"""

    # Timer for stop receiving
    global timer_id
    if timer_id is not None:
        ch.connection.remove_timeout(timer_id)
    data = read_json(json_data=body)
    print("Received in server:\n{}".format(data))
    local_devid = data["sn"]
    devfound.append(local_devid) # collect the devices replied
    # mesinfo comparision
    mesmacinfo = get_mesdevinfo(url=deviinfo_url, devid=local_devid)
    scanned = double_check(data, mesmacinfo)
    timer_id = ch.connection.add_timeout(10, notify)  # timeout, send received details and resume consuming
    all_dev.append(scanned)
    ch.basic_ack(delivery_tag = method.delivery_tag)


def run(host, queue_name, username, password, port):
    credentials = pika.PlainCredentials(username=username, password=password)
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, credentials=credentials))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    logging.info('[*] Waiting for client device information. To exit press CTRL+C')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(callback, queue=queue_name)
    channel.start_consuming()

if __name__ == '__main__':
    host = '10.10.70.89'
    queue_name = 'hwinfo_queue'
    username = "rmquser"
    password = "123456"
    port = 5672
    run(host, queue_name, username, password, port)




