import RPi.GPIO as GPIO
import time
import sys
from hx711 import HX711
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate('/home/pi/Desktop/hx711py/iot-med-firebase-adminsdk-269bo-7c3624a3c4.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


    
hx = HX711(5, 6)



def cleanAndExit():
    print ("Cleaning...")
    GPIO.cleanup()
    print ("Bye!")
    sys.exit()



def setup():
    """
    code run once
    """
    
    offset=hx.set_offset(9013025)
    #print(offset)
    hx.set_scale(1)
    hx.tare()
    pass

def 

def loop():
    """
    code run continuosly
    """

    try:
        val = hx.read()
        #print ('reading is')
        #print ('{0: 4.4f}'.format(val))
        actual = (val)/8450000
        #print ('{0: 1.2f}'.format(actual))
        #print (actual)
        percentage = actual*50
        #print (percentage)
        before= percentage-39.5
        caliberated = before*2.4
        #print('calibrated',(caliberated))
        print ('calibrated readings =',('{0: 2.1f}'.format(caliberated)))
        #print ('dont is',('{0: 2.1f}'.format(dont)))
        #print ('The percentage is',('{0: 2.1f}'.format(percentage)))
        med_ref = db.collection(u'devices').document(u'dev_0001').collection(u'readings').document(u'{0: .0f}'.format(time.time())).set({u'value':u'{0: 2.1f}'.format(caliberated)})

        
        '''if percentage <= 56:
            print('too low')
        if percentage >= 57 :
            print('ok')
        if percentage >= 67 :
            print('good')'''
        
        print ('##################')
        '''average = hx.read_average()
        print ('average reading=')
        conv = average/8400000
        print (conv)
        print ('##################')
        '''
        hx.power_down()
        time.sleep(20)
        hx.power_up()

        time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()


##################################

if __name__ == "__main__":

    setup()
    while True:
        loop()
