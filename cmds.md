#### To clone single branch:

git clone -b HBv1 --single-branch http://40.74.91.221/puzzle/edge-server-factory-api.git Heartbeat

git clone -b PuzzleScanDev --single-branch http://40.74.91.221/puzzle/device-intel-factory.git Puzzle_Scanning

#### DScanning Client as Service:

1. Run setup_dScanning.sh
2. START  : ```systemctl start dScanning.service"```
3. STATUS : ```systemctl status dScanning.service"```
4. STOP   : ```systemctl status dScanning.service"```

#### SSCanning Server as Service:

1. Run setup_sScanning.sh
2. START  : ```systemctl status SScanning@"10.10.70.89 5672 rmquser 123456 10.10.70.89 3000 4000"```
3. STATUS : ```systemctl status SScanning@"10.10.70.89 5672 rmquser 123456 10.10.70.89 3000 4000"```
4. STOP   : ```systemctl status SScanning@"10.10.70.89 5672 rmquser 123456 10.10.70.89 3000 4000"```


#### Executable project:

create setup.py manually and then
python setup.py sdist
