#!/bin/sh

serviceName="DScanning"
servicePath="/home/test/"$serviceName"Client"
rm -rf $servicePath
mkdir $servicePath
cp -R device_client $servicePath
chmod 777 -R $servicePath
cp ./${serviceName}.service /etc/systemd/system/
chmod 777 /etc/systemd/system/${serviceName}.service

# install the dependencies for DScanning to run
#pip3 install -r requirements.txt

systemctl daemon-reload
