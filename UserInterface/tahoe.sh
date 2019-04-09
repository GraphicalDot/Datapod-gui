#!/bin/bash

#<UDF name="nickname" Label="Storage Node Nickname" example="node01" />
#<UDF name="introducer" Label="Introducer FURL" example="pb://wfpe..." />

apt-get update
apt-get -y upgrade
adduser --disabled-password --gecos "" tahoe
apt-get -y install tahoe-lafs
su - -c "tahoe create-node --nickname=$NICKNAME --introducer=$INTRODUCER --port=tcp:1235 --location=tcp:`curl -4 -s icanhazip.com`:1235" tahoe

echo "[Unit]
Description=Tahoe-LAFS autostart node
After=network.target

[Service]
Type=simple
User=tahoe
WorkingDirectory=/home/tahoe
ExecStart=/usr/bin/tahoe run .tahoe --logfile=logs/node.log

[Install]
WantedBy=multi-user.target" >> /etc/systemd/system/tahoe-autostart-node.service

systemctl enable tahoe-autostart-node.service

systemctl start tahoe-autostart-node.service