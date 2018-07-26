import pika, json, logging
from device_client.PZLutils import PZLutils



pzl = PZLutils()
#logging.basicConfig(filename='dev_consume.log', level=logging.INFO)
logging.basicConfig(level=logging.INFO)

def populate_data(data):
    hw_info = {}
    url = 'http://127.0.0.1:5000/puzzle/api/v1/hwinfo'
    get_dev_slno = pzl.this_device_slno()
    logging.info("Populating hardware datas from device ===> Sl.No: {}".format(get_dev_slno))
    if get_dev_slno in data["devices"]:
        """for nested follow this snippet
        # hw_info[data["scan_id"]] = {}
        # hw_info[data["scan_id"]][get_dev_slno] = pzl.read_json(pzl.retrieve_hwinfo(url))"""
        # unnested
        hw_info["scanid"] = data["scan_id"]
        hw_info["devslno"] = get_dev_slno
        hw_info.update(pzl.read_json(pzl.retrieve_hwinfo(url)))
    print(json.dumps(hw_info))
    return json.dumps(hw_info)

def callback(ch, method, properties, body):
    pzl = PZLutils()
    data = pzl.read_json(body)
    if data:
        logging.info("Consuming from MES server")
    hw_info = populate_data(data)
    ch.queue_declare(queue='hwinfo_queue', durable=True)
    logging.info("Publishing to device server side")
    ch.basic_publish(exchange='',
                          routing_key='hwinfo_queue',
                          body=hw_info,
                          properties=pika.BasicProperties(delivery_mode=1))

def consumeAndpublish(host='localhost', ex_name="devSNo", ex_type='fanout'):
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
