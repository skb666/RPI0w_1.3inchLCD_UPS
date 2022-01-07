#!/usr/bin/bash

HOSTNAME=$(hostname);
ETH0_IP=$(ip addr show eth0 2>/dev/null | grep 'inet ' | awk '{print $2}');
WLAN0_IP=$(ip addr show wlan0 2>/dev/null | grep 'inet ' | awk '{print $2}');
UPTIME=$(uptime -p | cut -d ' ' -f 2-);

echo $HOSTNAME
echo $ETH0_IP
echo $WLAN0_IP
echo $UPTIME

