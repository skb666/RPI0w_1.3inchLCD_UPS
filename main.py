#!/usr/bin/python
import subprocess
import time
from threading import Thread
from UPS_PW import UPS_PW
from LCD_DR import LCD_DR
from KEY_BD import KEY_BD


def shell_run(cmd):
    res = subprocess.Popen(cmd, shell=True,
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
    return res.communicate()

def get_info():
    stdout, stderr = shell_run("bash ./get_info.sh")
    if stdout:
        return stdout.decode('utf-8').split('\n')[:4]
    else:
        return None

def get_ups(ups):
    battery = "%.2fV (%i%%)" % (ups.readVoltage(), ups.readCapacity())
    power = "Plug In" if ups.getPowerStatus() else "Unplug"
    return battery, power


if __name__ == '__main__':
    ups = UPS_PW()
    lcd = LCD_DR()
    kbd = KEY_BD()

    ups.Init()
    lcd.Init()
    kbd.Init()

    key_stat = {
        'k_up': 0, 
        'k_down': 0,
        'k_left': 0, 
        'k_right': 0, 
        'k_press': 0, 
        'k_1': 0,
        'k_2': 0,
        'k_3': 0
    }

    key_stat_old = None

    lcd.DrawFrame()
    lcd.DrawLabel()
    lcd.DrawKeyStatus(key_stat)

    def keyScan():
        global kbd, lcd, key_stat, key_stat_old
        while True:
            kbd.Scan()
            key_stat = kbd.getKeyStatus()
            if key_stat_old is None or key_stat_old != key_stat:
                lcd.DrawKeyStatus(key_stat)
                lcd.Show()
                #print(key_stat)
                key_stat_old = key_stat.copy()
            time.sleep(0.01)

    task = Thread(target=keyScan)
    task.start()

    while True:
        battery, power = get_ups(ups)
        try:
            hostname, eth0_ip, wlan0_ip, uptime = get_info()
            if eth0_ip:
                ipv4 = eth0_ip
            elif wlan0_ip:
                ipv4 = wlan0_ip
            else:
                ipv4 = 'No connection'
            uptime = uptime.replace(' ', '')
            uptime = uptime.replace('weeks', 'week').replace('days', 'day').replace('hours', 'hour').replace('minutes', 'minute')
            uptime = uptime.replace('week', 'w').replace('day', 'd').replace('hour', 'h').replace('minute', 'm')
        except:
            hostname, ipv4, uptime = ("raspberrypi", "No connection", "None")
        
        lcd.DrawInfo(hostname, battery, power, ipv4, uptime)
        lcd.Show()

        time.sleep(15)


