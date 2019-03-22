import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask
from flask import jsonify
from flask import request
import google.cloud.exceptions
import base64
from passlib.context import CryptContext
cred = credentials.Certificate('mexibm-47994-firebase-adminsdk-39gkc-ab1f0a7cd4.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
#bcrypt = Bcrypt(app)
# app.config['MONGO_DBNAME'] = 'compose'
# app.config['MONGO_URI'] = "mongodb://admin:JOISQFGXCPOQYKPW@portal-ssl79-37.bmix-eu-gb-yp-e5902193-7191-433e-af74-9ce860475330.1409146671.composedb.com:17584,portal-ssl82-23.bmix-eu-gb-yp-e5902193-7191-433e-af74-9ce860475330.1409146671.composedb.com:17584/compose?authSource=admin&ssl=true"
pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)
# mongo = PyMongo(app)

@app.route('/register', methods=['POST'])
def resgiter_user():
  output="Not Found"
  name = request.values.get('name')
  email = request.values.get('email')
  password = request.values.get('password')
  employee_id = request.values.get('employee_id')
  password_hash = pwd_context.encrypt(password)
  user = db.collection('register').document()
  id = user.set({
    'name': name,
    'email': email,
    'password': password_hash,
    'employee_id': employee_id
  })
  doc_ref = db.collection('register').document()
  try:
    doc = doc_ref.get()
    output = True
  except google.cloud.exceptions.NotFound:
    print(u'No such document!')
    output = False
  return jsonify(output)

@app.route('/login/<email>/<password>',methods=['GET'])
def login_user(email,password):
  output="Not Found"
  password=password
  cities_ref = db.collection('register')
  query = cities_ref.where('email', '==', email).get()
  if(query):
    for doc in query:
      doc_dict=doc.to_dict()
      print(u'{} => {}'.format(doc.id,doc_dict['password']))
      if pwd_context.verify(password, doc_dict['password']):
        output=True
      else:
        output="Password Does not match"
  else:
    output="Document Not found"
  return jsonify(output)

@app.route('/claim', methods=['GET'])
def get_all_claim():
  #claim = mongo.db.userclaim
  output="Not Found"
  claim = db.collection('claims').get()
  for doc in claim:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))
    output = doc.to_dict()
    doc_id = doc.to_dict()
    print(doc_id['status'])
    output['image'] =output['image'].decode("utf-8")
    print('output',type(output))
  return jsonify({'result' : output})

@app.route('/claim/<name>', methods=['GET'])
def get_one_claim(name):
  output="Not Found"
  claim_ref = db.collection('claims')
  docs = claim_ref.where('name', '==',name ).get()
  for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))
    output=doc.to_dict()
  return jsonify({'result' : output})

@app.route('/claim', methods=['POST'])
def add_claim():
  import datetime as dt
  output="Not Found"
  name=request.values.get('name')
  description=request.values.get('description')
  busniessType=request.values.get('busniesstype')
  image=request.values.get('image')
  claim = db.collection('claims').document()
  claim_id = claim.set({
    'name': name,
    'description': description,
    'busniessType': busniessType,
    'date':dt.datetime.now(),
    'status':'disapprove',
    'status_update_date':dt.datetime.now(),
    'image':image
  })
  doc_ref = db.collection('claims').document()
  try:
    output = True
  except google.cloud.exceptions.NotFound:
    output = False
  return jsonify(output)
        
@app.route('/claim/<name>/<status>', methods=['PUT'])
def update_claim(name,status):
  import datetime as dt
  output=False
  claim_ref = db.collection('claims')
  docs = claim_ref.where('name', '==', name).get()
  for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))
    # doc_id = doc.to_dict()
    doc_ref = db.collection('claims').document(doc.id)
    x=doc_ref.update( {
      'status': status,
      'status_update_date':dt.datetime.now()
    })
    output=True
  return jsonify(output)

@app.route('/claim/<busniesstype>', methods=['GET'])
def get_filtered_claims(busniesstype):
  output="Not Found"
  claim_ref = db.collection('claims')
  docs = claim_ref.where('busniesstype', '==',busniesstype).get()
  for doc in docs:
    print(u'{} => {}'.format(doc.id, doc.to_dict()))
    output=doc.to_dict()
  return jsonify({'result' : output})

if __name__ == '__main__':
    app.run(debug=True)
