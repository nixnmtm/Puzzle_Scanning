### To clone single branch:

git clone -b HBv1 --single-branch http://40.74.91.221/puzzle/edge-server-factory-api.git heartbeat

### DScanning Client as Service:
1. Run setupDScanning.sh
2. START  : ```systemctl start DScanning@"10.10.70.89 5672 rmquser 123456"```
3. STATUS : ```systemctl status DScanning@"10.10.70.89 5672 rmquser 123456"```
4. STOP   : ```systemctl status DScanning@"10.10.70.89 5672 rmquser 123456"```

### SSCanning Server as Service:
1. Run setupSScanning.sh
2. START  : ```systemctl status SScanning@"10.10.70.89 5672 rmquser 123456 10.10.70.89 3000 4000"```
3. STATUS : ```systemctl status SScanning@"10.10.70.89 5672 rmquser 123456 10.10.70.89 3000 4000"```
4. STOP   : ```systemctl status SScanning@"10.10.70.89 5672 rmquser 123456 10.10.70.89 3000 4000"```