#!/bin/sh

serviceName="DScanning"
servicePath="/home/test/"$serviceName"Client"
rm -r $servicePath
cp -R src $servicePath
chmod 777 -R $servicePath
cp ./$serviceName@.service /etc/systemd/system/
chmod 777 /etc/systemd/system/$serviceName@.service
systemctl daemon-reload