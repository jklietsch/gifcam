import picamera
from time import sleep
import time
import RPi.GPIO as GPIO
from os import system, path
import os
import string

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
button = 19 #Button GPIO Pin

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
led_1 = 12 #Status LED GPIO Pin
GPIO.setup(led_1, GPIO.OUT)
led_2 = 21 #ON/OFF LED Pin
GPIO.setup(led_2, GPIO.OUT)

########################
### Variables Config ###
########################
num_pics = 8 #Number of pictures to take in Gif
gif_delay = 15 #How much delay in between those pictures (in milliseconds)    

camera = picamera.PiCamera()
camera.resolution = (800, 800)
camera.rotation = 0
###############
### Effects ###
###############
#camera.sharpness = 0
camera.contrast = 50
camera.brightness = 80
#camera.saturation = 0
camera.ISO = 800
#camera.video_stabilization = False
#camera.exposure_compensation = 0
#camera.exposure_mode = 'auto'
#camera.meter_mode = 'average'
#camera.awb_mode = 'auto'
camera.image_effect = 'film'
#camera.color_effects = (128,128)
#camera.hflip = False
#camera.vflip = False
#camera.crop = (0.0, 0.0, 1.0, 1.0)

GPIO.output(led_2, 1)
print('System Ready')

def getCurrentNumber():
    filename = '/home/pi/gifcam/n'
    n = 0;
    if os.path.exists(filename):
        fileObj = open(filename, 'r')
        nStr = fileObj.read()
        n = int(nStr)
        fileObj.close()
    n += 1
    fileObj = open(filename, 'w')
    fileObj.write(str(n))
    fileObj.close()
    return n

while True:
    input_state = GPIO.input(button) # Sense the button
    if input_state == False:
        GPIO.output(led_1, 1)
        print('Gif Started')
        for i in range(num_pics):
    		camera.capture('image{0:04d}.jpg'.format(i))
        filename = '/home/pi/gifcam/gifs/' + str(getCurrentNumber())
        GPIO.output(led_1, 0)
    	print('Processing')
        graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + "*.jpg " + filename + ".gif" 
        os.system(graphicsmagick)
        print('Done')
        print('System Ready')
    else :
        # Switch on LED
        GPIO.output(led_1, 1)
        time.sleep(0.35)
        GPIO.output(led_1, 0)
        time.sleep(0.35)
