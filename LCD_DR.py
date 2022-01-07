import spidev as SPI
import ST7789
from PIL import Image,ImageDraw,ImageFont


class LCD_DR(object):
    def __init__(self, bus=0, device=0):
        # 240x240 display with hardware SPI
        self._disp = ST7789.ST7789(SPI.SpiDev(bus, device))
        # set font
        self._font12 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 12)
        self._font16 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 16)
        self._font24 = ImageFont.truetype('/usr/share/fonts/truetype/wqy/wqy-microhei.ttc', 24)
        # Create blank image for drawing
        self._image = Image.new("RGB", (self._disp.width, self._disp.height), "BLACK")
        self._draw = ImageDraw.Draw(self._image)
        self._image_old = None

    def Init(self):
        # Initialize library.
        self._disp.Init()
        # Clear display.
        self._disp.clear()

    def DrawFrame(self):
        self._draw.line([(15, 15), (225, 15)], fill="BLUE", width=5)
        self._draw.line([(225, 15), (225, 225)], fill="BLUE", width=5)
        self._draw.line([(225, 225), (15, 225)], fill="BLUE", width=5)
        self._draw.line([(15, 225), (15, 15)], fill="BLUE", width=5)

    def DrawLabel(self):
        self._draw.rectangle([(15+15, 15-12), (15+15+12*6, 15-12+24)], fill="BLACK")
        self._draw.text((15+15, 15-12), '  INFO  ', fill="WHITE", font=self._font24)

        self._draw.text((30, 31), 'Hostname', fill="RED", font=self._font16)
        self._draw.text((30, 31+18), 'Battery', fill="RED", font=self._font16)
        self._draw.text((30, 31+18*2), 'Power', fill="RED", font=self._font16)
        self._draw.text((30, 31+18*3), 'IPv4', fill="RED", font=self._font16)
        self._draw.text((30, 31+18*4), 'Uptime', fill="RED", font=self._font16)
        self._draw.line([(24+8*10, 35), (24+8*10, 30+18*5)], fill="GRAY", width=1)

        # white border row
        self._draw.line([(25, 30), (215, 30)], fill="WHITE", width=1)
        self._draw.line([(25, 35+18*5), (215, 35+18*5)], fill="WHITE", width=1)
        self._draw.line([(25, 215), (215, 215)], fill="WHITE", width=1)
         # white border col
        self._draw.line([(25, 30), (25, 215)], fill="WHITE", width=1)
        self._draw.line([(215, 30), (215, 215)], fill="WHITE", width=1)

    def DrawInfo(self, hostname, battery, power, ipv4, uptime):
        # Clear with blank
        self._draw.rectangle([(30+8*10, 33), (210, 33+18*5)], fill="BLACK")
        # drawing with info
        self._draw.text((30+8*10, 33), '{:<}'.format(hostname), fill="#33FF33", font=self._font12)
        self._draw.text((30+8*10, 33+18), '{:<}'.format(battery), fill="#33FF33", font=self._font12)
        self._draw.text((30+8*10, 33+18*2), '{:<}'.format(power), fill="#33FF33", font=self._font12)
        self._draw.text((30+8*10, 33+18*3), '{:<}'.format(ipv4), fill="#33FF33", font=self._font12)
        self._draw.text((30+8*10, 33+18*4), '{:<}'.format(uptime), fill="#33FF33", font=self._font12)

    def DrawKeyStatus(self, key_stat):
        #self._draw.rectangle([(30, 40+18*5), (210, 210)], fill="BLACK")
        x1, y = (30+20, 40+18*5+10)
        x2 = 30+40
        # self._draw.polygon([(20+x, 20+y), (30+x, 2+y), (40+x, 20+y)], outline=255, fill=0xff00)  #Up
        # self._draw.polygon([(0+x, 30+y), (18+x, 21+y), (18+x, 41+y)], outline=255, fill=0xff00)  #left
        # self._draw.polygon([(60+x, 30+y), (42+x, 21+y), (42+x, 41+y)], outline=255, fill=0xff00) #right
        # self._draw.polygon([(30+x, 60+y), (40+x, 42+y), (20+x, 42+y)], outline=255, fill=0xff00) #down
        # self._draw.rectangle((20+x, 22+y, 40+x, 40+y), outline=255, fill=0xff00) #center
        # self._draw.ellipse((70+x, 0+y, 90+x, 20+y), outline=255, fill=0xff00) #k1
        # self._draw.ellipse((100+x, 20+y, 120+x, 40+y), outline=255, fill=0xff00) #k2
        # self._draw.ellipse((70+x, 40+y, 90+x, 60+y), outline=255, fill=0xff00) #k3
        if key_stat['k_up'] == 1:
            #print('KEY_Up pressed')
            self._draw.polygon([(20+x1, 20+y), (30+x1, 2+y), (40+x1, 20+y)], outline=255, fill=0xff00)  #Up
        else:
            self._draw.polygon([(20+x1, 20+y), (30+x1, 2+y), (40+x1, 20+y)], outline=255, fill=0)  #Up

        if key_stat['k_down'] == 1:
            #print('KEY_Down pressed')
            self._draw.polygon([(30+x1, 60+y), (40+x1, 42+y), (20+x1, 42+y)], outline=255, fill=0xff00) #down
        else:
            self._draw.polygon([(30+x1, 60+y), (40+x1, 42+y), (20+x1, 42+y)], outline=255, fill=0) #down

        if key_stat['k_left'] == 1:
            #print('KEY_Left pressed')
            self._draw.polygon([(0+x1, 30+y), (18+x1, 21+y), (18+x1, 41+y)], outline=255, fill=0xff00)  #left
        else:
            self._draw.polygon([(0+x1, 30+y), (18+x1, 21+y), (18+x1, 41+y)], outline=255, fill=0)  #left

        if key_stat['k_right'] == 1:
            #print('KEY_Right pressed')
            self._draw.polygon([(60+x1, 30+y), (42+x1, 21+y), (42+x1, 41+y)], outline=255, fill=0xff00) #right
        else:
            self._draw.polygon([(60+x1, 30+y), (42+x1, 21+y), (42+x1, 41+y)], outline=255, fill=0) #right

        if key_stat['k_press'] == 1:
            #print('KEY_Press pressed')
            self._draw.rectangle((20+x1, 22+y, 40+x1, 40+y), outline=255, fill=0xff00) #center
        else:
            self._draw.rectangle((20+x1, 22+y, 40+x1, 40+y), outline=255, fill=0) #center

        if key_stat['k_1'] == 1:
            #print('KEY_1 pressed')
            self._draw.ellipse((70+x2, 0+y, 90+x2, 20+y), outline=255, fill=0xff00) #k1
        else:
            self._draw.ellipse((70+x2, 0+y, 90+x2, 20+y), outline=255, fill=0) #k1

        if key_stat['k_2'] == 1:
            #print('KEY_2 pressed')
            self._draw.ellipse((100+x2, 20+y, 120+x2, 40+y), outline=255, fill=0xff00) #k2
        else:
            self._draw.ellipse((100+x2, 20+y, 120+x2, 40+y), outline=255, fill=0) #k2

        if key_stat['k_3'] == 1:
            #print('KEY_3 pressed')
            self._draw.ellipse((70+x2, 40+y, 90+x2, 60+y), outline=255, fill=0xff00) #k3
        else:
            self._draw.ellipse((70+x2, 40+y, 90+x2, 60+y), outline=255, fill=0) #k3

    def Show(self):
        if self._image_old is None or self._image_old != self._image:
            self._image_old = self._image.copy()
            self._disp.ShowImage(self._image, 0, 0)


if __name__ == '__main__':
    lcd = LCD_DR()

    lcd.Init()

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
    
    lcd.DrawFrame()
    lcd.DrawLabel()
    lcd.DrawInfo('raspberrypi', '4.18V (40%)', 'Unplug', 'No connection', '1h,45m')
    lcd.DrawKeyStatus(key_stat)
    lcd.Show()

