# Search AprilTags
#

import sensor, image, time, lcd, pyb
from pyb import UART

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.VGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False)
sensor.set_auto_whitebal(False)
lcd.init()
clock = time.clock()


uart = UART(3, 9600, timeout_char=1000)
uart.init(9600, bits=8, parity=None, stop=1, timeout_char=1000)
uartget=False

tag_families = 0
tag_families |= image.TAG16H5 # comment out to disable this family
tag_families |= image.TAG25H7 # comment out to disable this family
tag_families |= image.TAG25H9 # comment out to disable this family
tag_families |= image.TAG36H10 # comment out to disable this family
tag_families |= image.TAG36H11 # comment out to disable this family (default family)
tag_families |= image.ARTOOLKIT # comment out to disable this family

start = pyb.millis()
while(True):
    #clock.tick()
    img = sensor.snapshot()
    if pyb.elapsed_millis(start) >= 200:
        arrobj=img.find_apriltags(families=tag_families)
        #print(len(arrobj))
        #if len(img.find_apriltags(families=tag_families))>0:
        if len(arrobj)>0 :
           strsend="#"+str(len(arrobj))+";"
           #for tag in img.find_apriltags(families=tag_families): # defaults to TAG36H11 without "families".
           for tag in arrobj: # defaults to TAG36H11 without "families".
              img.draw_rectangle(tag.rect(), color = (255, 0, 0))
              img.draw_cross(tag.cx(), tag.cy(), color = (0, 255, 0))
              strsend=strsend+str(tag.id())+";"+str(tag.cx())+";"+str(tag.cy())+";"+str(tag.h())+";"+str(tag.w())+";"
           strsend=strsend+"$"
        else :
           strsend="#0;0;0;0;0;0;$"
        print(strsend)
        uart.write(strsend)
        start = pyb.millis()
        pyb.delay(200)
    # get uart data
    if (uart.any()>0):
        s=uart.read()
        str2=str2+s
        if s=='$':
           uartget=True
    if uartget == True:
       #
       print("get data from uart = %s",str2)
       uartget=False
       str2=""
    #
    lcd.display(img.scale(0.25,0.25))
    #print(clock.fps())
