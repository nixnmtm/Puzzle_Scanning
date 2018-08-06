#!/usr/bin/env python

import pika, json, logging, requests
import more_itertools as mit

logging.basicConfig(level=logging.INFO)
all_dev = []
devfound = []
devsucess = []
deviinfo_url = "http://10.10.70.89:3000/puzzle/api/v1/deviceinfo/getById"
post_api = 0  # if (0: dont POST, 1: POST)

def read_json(json_data):
    """Convert bytes datatype to str"""

    if type(json_data) == bytes:
        data = json_data.decode('ascii')
        data = json.loads(data)
        return data
    if type(json_data) == str:
        data = json.loads(json_data)
        return data


def get_mesdevinfo(url, devid):
    """Get MES device info from deviceinfo API"""
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
        logging.error("Damn, error in accessing the url")

    try:
        mesdevinfo = json.loads(mesdevinfo.text)
        if not mesdevinfo["info"]:
            logging.error("No valid device(serialno: {}) information from MES server".format(devid))
        if mesdevinfo["info"][0]["serialno"] == devid:
            return mesdevinfo["info"][0]["macInfo"]
    except Exception as e:
        logging.error("No device info found")

def compareMES(locdata, mesdata):

    """Compare, double check and report scanstatus,
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

def accumulate_all(all_dev):
    alldevresponse = {}
    operationid = []
    scaninfo = []
    for num, devs in enumerate(all_dev):
        info = {}
        for k, v in devs.items():
            macdetails = []
            for n, (i, j) in enumerate(devs["macinfo"].items()):
                temp = {}
                temp["interface"] = i
                temp["scanstatus"] = j["scanstatus"]
                temp["macaddr"] = j["macaddr"]
                macdetails.insert(n, temp)
            if k == "sn":
                info["sn"] = devs[k]
                info["macinfo"] = macdetails
        scaninfo.insert(num, info)

    alldevresponse["operationid"] = all_dev[0]["operationid"]
    alldevresponse["scaninfo"] = scaninfo
    return(alldevresponse)

def notify(dev):

    """Notify to notification API"""
    if post_api == 1:
        try:
            notifyurl = "http://10.10.70.89:4000/notifications/devicescan"
            headers = {'Content-Type': "application/json"}
            note = {}
            #send["status"] = logging.warning("Error_found_in_device_serial_no:_{}".format(dev))
            note["sn"] = dev
            note["status"] = "Errors found"
            senddata = json.dumps(note)
            logging.info("Sending notification of {}".format(dev))
            requests.post(url=notifyurl, headers=headers, data=senddata)

        except Exception as e:
            logging.error("Damn, error in posting")

def postlog_deviceinfo(info):

    """Post compared data with status to device info API"""
    if post_api == 1:
        try:
            url = "http://10.10.70.89:3000/puzzle/api/v1/log/deviceScan"
            headers = {'Content-Type': "application/json"}
            senddata = json.dumps(info)
            print(senddata)
            # print("Final Data:\n{}".format(json.dumps(finaldict, sort_keys=True, indent=4, separators=(',', ': '))))
            logging.info("Posting device info")
            requests.post(url=url, headers=headers, data=senddata)

        except Exception as e:
            logging.error("Damn, error in posting device info")

def post2pair(devs, operationid):

    """Post the devices that has scanned successfull to Pair API"""

    pairdevs = {}
    pairdevs["operationId"] = operationid
    pairdevs["snArray"] = devs

    try:
        url = "http://40.74.91.221/puzzle/edge-server-factory-api/wikis/Run-Pair-API"
        headers = {'Content-Type': "application/json"}
        senddata = json.dumps(pairdevs)
        print(senddata)
        logging.info("Posting successful devices to pair")
        requests.post(url=url, headers=headers, data=senddata)

    except Exception as e:
        logging.error("Damn, error in posting devices to pair")

def checkNupdate(devfound, updatedict):
    """Check status and update result for each device """
    if updatedict["scaninfo"]:
        res = updatedict["scaninfo"].copy()
        for i in devfound:
            index = list(mit.locate(res, pred=lambda d: d["sn"] == i))
            devdict = res[index[0]]["macinfo"]
            if not any(a["scanstatus"] == '0' for a in devdict):  # if value in the list of dict
                updatedict["scaninfo"][index[0]]["result"] = '1'  # if not any fail add result success
                devsucess.append(i)
            else:
                updatedict["scaninfo"][index[0]]["result"] = '0'
                notify(i)
    return updatedict

def scanningReal():

    """ ** Accumulate all device info with compared data
        ** Check mac status and update device scan result
        ** Notify
    """
    global all_dev
    global devfound
    if len(accumulate_all(all_dev)["scaninfo"]) == len(devfound):
        logging.info("Number of devices received and collected match")
    else:
        logging.warn("Number of devices received and collected mismatch")
    alldevinfo = accumulate_all(all_dev)
    finaldict = checkNupdate(devfound, alldevinfo)
    postlog_deviceinfo(finaldict)
    post2pair(devsucess, finaldict["operationid"])
    logging.info("Devices found:\n{}".format(devfound))
    logging.info("Devices passed scanning and sent to pairing:\n{}".format(devsucess))
    logging.info("Resume consuming")
    all_dev = []
    devfound = []

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
    scanned = compareMES(data, mesmacinfo)
    timer_id = ch.connection.add_timeout(10, scanningReal)  # timeout, send received details and resume consuming
    all_dev.append(scanned)
    ch.basic_ack(delivery_tag = method.delivery_tag)


def run(host, queue_name, username, password, port):
    """Establish connection and run"""
    credentials = pika.PlainCredentials(username=username, password=password)
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port, credentials=credentials))
    except Exception as e:
        logging.error("Connection to server not established")

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




