import RPi.GPIO as GPIO


class KEY(object):
    def __init__(self, key):
        self._stat = 'KEY_CHECK'
        self._flag = 0
        self._key = key

    def Init(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._key, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # Input with pull-up

    def Scan(self, release=0):
        if self._stat == 'KEY_CHECK':
            if not GPIO.input(self._key):
                self._stat = 'KEY_COMFIRM'
        elif self._stat == 'KEY_COMFIRM':
            if not GPIO.input(self._key):
                self._stat = 'KEY_RELEASE'
                self._flag = 1
            else:
                self._stat = 'KEY_CHECK'
        elif self._stat == 'KEY_RELEASE':
            if GPIO.input(self._key):
                self._stat = 'KEY_CHECK'
                if release:
                    self._flag = 2
                else:
                    self._flag = 0

    def getKeyStatus(self):
        return self._flag

    def reset(self):
        self._flag = 0


class KEY_BD(object):
    def __init__(self, up=6, down=19, left=5, right=26, press=13, k1=21, k2=20, k3=16):
        #init GPIO
        # for P4:
        # sudo vi /boot/config.txt
        # gpio=6,19,5,26,13,21,20,16=pu
        self._keys = {
            'k_up': KEY(up), 
            'k_down': KEY(down),
            'k_left': KEY(left), 
            'k_right': KEY(right), 
            'k_press': KEY(press), 
            'k_1': KEY(k1),
            'k_2': KEY(k2),
            'k_3': KEY(k3)
        }
        self._key_stat = dict()

    def Init(self):
        for key in self._keys.values():
            key.Init()

    def Scan(self, release=0):
        for key in self._keys.values():
            key.Scan(release)

    def getKeyStatus(self):
        self._key_stat.clear()
        for tag, key in self._keys.items():
            self._key_stat[tag] = key.getKeyStatus()
        return self._key_stat

    def reset(self, tag='*'):
        def reset_all(self):
            for key in self._keys.values():
                key.reset()
        if tag == '*':
            reset_all(self)
        else:
            key = self._keys.get(tag, None)
            if not key:
                reset_all(self)
            else:
                key.reset()


if __name__ == '__main__':
    import time
    from threading import Thread

    kbd = KEY_BD()
    kbd.Init()

    def keyScan():
        global kbd
        while True:
            kbd.Scan(1)
            time.sleep(0.01)

    task = Thread(target=keyScan)
    task.start()

    while True:
        key_stat = kbd.getKeyStatus()

        if key_stat['k_up'] == 1:
            print('KEY_Up pressed')
        elif key_stat['k_up'] == 2:
            print('KEY_Up released')

        if key_stat['k_down'] == 1:
            print('KEY_Down pressed')
        elif key_stat['k_down'] == 2:
            print('KEY_Down released')

        if key_stat['k_left'] == 1:
            print('KEY_Left pressed')
        elif key_stat['k_left'] == 2:
            print('KEY_Left released')

        if key_stat['k_right'] == 1:
            print('KEY_Right pressed')
        elif key_stat['k_right'] == 2:
            print('KEY_Right released')

        if key_stat['k_press'] == 1:
            print('KEY_Press pressed')
        elif key_stat['k_press'] == 2:
            print('KEY_Press released')

        if key_stat['k_1'] == 1:
            print('KEY_1 pressed')
        elif key_stat['k_1'] == 2:
            print('KEY_1 released')

        if key_stat['k_2'] == 1:
            print('KEY_2 pressed')
        elif key_stat['k_2'] == 2:
            print('KEY_2 released')

        if key_stat['k_3'] == 1:
            print('KEY_3 pressed')
        elif key_stat['k_3'] == 2:
            print('KEY_3 released')

        for tag, flag in key_stat.items():
            if flag:
                kbd.reset(tag)