import pika, json, logging
from device_client.PZLutils import PZLutils


pzl = PZLutils()
#logging.basicConfig(filename='dev_consume.log', level=logging.INFO, filemode='w')
logging.basicConfig(level=logging.INFO)

def populate_data(data):
    hw_info = {}
    url = 'http://127.0.0.1:5000/puzzle/api/v1/hwinfo'
    get_dev_slno = pzl.this_device_slno()
    if get_dev_slno in data["devices"]:
        logging.info("Populating hardware datas from device ===> Sl.No: {}".format(get_dev_slno))
        #for nested follow this snippet
        # hw_info[data["scan_id"]] = {}
        # hw_info[data["scan_id"]][get_dev_slno] = pzl.read_json(pzl.retrieve_hwinfo(url))
        # unnested
        #hw_info["ndev"] = len(data["devices"])
        hw_info["scanid"] = data["scan_id"]
        hw_info["serialno"] = get_dev_slno
        temp = pzl.read_json(pzl.retrieve_hwinfo(url))
        if "cpuinfo" in temp.keys():
            temp.pop("cpuinfo")
        if "meminfo" in temp.keys():
            temp.pop("meminfo")
        hw_info["macinfo"] = {}
        for k in temp["pciinfo"].keys():
            hw_info["macinfo"][temp["pciinfo"][k]["interface"]] = {}
            hw_info["macinfo"][temp["pciinfo"][k]["interface"]]["macaddr"] = temp["pciinfo"][k]["macaddr"]
    else:
        logging.info("{} is not in the scan list".format(get_dev_slno))
    return hw_info

def callback(ch, method, properties, body):
    pzl = PZLutils()
    data = pzl.read_json(body)
    try:
        if data:
            logging.info("{}Scanning Started{}".format("-"*10, "-"*10))

        hw_info = populate_data(data)
        print(hw_info)
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
        logging.error("**Scanning Failed. " + str(e))


def consumeAndpublish(host='localhost', ex_name="devicescan", ex_type='fanout'):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
    channel = connection.channel()
    channel.exchange_declare(exchange=ex_name,
                             exchange_type=ex_type)
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=ex_name, queue=queue_name)
    logging.info('[*] Waiting for Device serial numbers. To exit press CTRL+C')
    channel.basic_consume(callback, queue=queue_name, no_ack=True)
    channel.start_consuming()

def main():
    consumeAndpublish()
if __name__ == '__main__':
    main()
