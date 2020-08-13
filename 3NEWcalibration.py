
import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
import sys

time.sleep(20)

cred = credentials.Certificate('/home/pi/Desktop/hx711py-final/iot-med-firebase-adminsdk-269bo-7c3624a3c4.json') #Location of credentials file
default_app = firebase_admin.initialize_app(cred)
db = firestore.client()

if sys.version_info[0] != 3:
    raise Exception("Python 3 is required.")

hx = HX711(5, 6, gain=64)
global first
global flag

def cleanAndExit():
    print("Cleaning up...")
    GPIO.cleanup()
    print("Bye!")
    sys.exit()


def setup():
    """
    code run once
    """
    print("Initializing.\n Please ensure that the scale is empty.")
    scale_ready = False
    while not scale_ready:
        if (GPIO.input(hx.DOUT) == 0):
            scale_ready = False
        if (GPIO.input(hx.DOUT) == 1):
            print("Initialization complete!")
            scale_ready = True
            
def calibrate():    
    hx.set_offset(8418541.3125)
    hx.set_scale(-143.42)
    

flag = 0
first = 0

def loop():
    global first
    global flag
    try:
        prompt_handled = False
        while not prompt_handled:
            val = hx.get_grams()
            if flag==0:
                first = val
                
            hx.power_down()
            time.sleep(60)
            hx.power_up()
            print("Item weighs {} grams.\n".format(val))
            diff = first-val
            difference = "%.1f" % round(diff,2)
            #print("the diference", difference)
            d = float(difference)
            percent = (val/first)*100
            r_percent= int(percent)
            #print(r_percent)
            if(r_percent > 0):
                print("Percent left -> ", r_percent)
                med_ref = db.collection(u'devices').document(u'dev_0003').collection(u'readings').document(u'{}'.format(time.time())).set({u'value':r_percent})
                print('Uploaded to database')
            
            flag = flag+1
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

if __name__ == "__main__":

    setup()
    calibrate()
    while True:
        loop()
    
    
    
    
    
    
    
    
    
    
    