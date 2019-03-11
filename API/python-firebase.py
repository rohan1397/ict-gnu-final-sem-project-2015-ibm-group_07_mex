import firebase_admin
from firebase_admin import db
import flask

app = flask.Flask(__name__)

from firebase import firebase
from firebase_admin import credentials
cred = credentials.Certificate("mexibm-47994-firebase-adminsdk-39gkc-ab1f0a7cd4.json")
firebase_admin.initialize_app(cred)
#firebase = firebase.FirebaseApplication('https://mexibm-47994.firebaseio.com', None)
ref = db.reference('/register',url='https://mexibm-47994.firebaseio.com')
print(ref.get())
snapshot = ref.order_by_child('name').get()
print(snapshot)
for key, val in snapshot.items():
    print('The {0} dinosaur\'s score is {1}'.format(key, val))
#

# #get
#
# result = firebase.get('/register', None)
# print(result)
#
# snapshot = ref.order_by_child('height').get()
# #insert
# #
# # data =  { 'name': 'Rohan',
# #           'password': 11321,
# #           'emailid': 'rohan1997jaion@gmail.com'
# #           }
# # result = firebase.post('register/',data)
# # print(result)
#
# #update
# #
# # firebase.put('/register/-LZxz_q0bZluoAIVKgtC','emailid','12324')
# # print('updated')