import picamera
from datetime import datetime
from time import sleep

camera = picamera.PiCamera()
camera.awb_mode = 'cloudy'

while True :
    now = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    camera.capture("~/fotos/"+now+".jpg")
    sleep(3)