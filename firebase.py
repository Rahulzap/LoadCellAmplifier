import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time


cred = credentials.Certificate('/home/pi/Desktop/hx711py/iot-med-firebase-adminsdk-269bo-7c3624a3c4.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

'''users_ref = db.collection(u'devices')
docs = users_ref.get()

for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))'''

med_ref = db.collection(u'devices').document(u'dev_0001').collection(u'readings').document(u'{}'.format(time.time())).set({u'value':u'3'})


