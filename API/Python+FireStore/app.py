from json import dumps

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from flask import Flask
from flask import jsonify
from flask import request
import google.cloud.exceptions
import base64
import os
from passlib.context import CryptContext
cred = credentials.Certificate('mexibm-47994-firebase-adminsdk-39gkc-ab1f0a7cd4.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
claimIdCounter=0
app = Flask(__name__, static_url_path='')
port = int(os.getenv('PORT', 8000))
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
    if(checkUser(email)):
        output="Already registerd"
    else:
        password = request.values.get('password')
        employee_id = request.values.get('employee_id')
        password_hash = pwd_context.encrypt(password)
        role = request.values.get('role')
        if role == None:
            role = 'User'
        user = db.collection('register').document()
        id = user.set({
            'name': name,
            'email': email,
            'password': password_hash,
            'employee_id': employee_id,
            'role': role
        })
        doc_ref = db.collection('register').document()
        try:
            doc = doc_ref.get()
            output = True
        except google.cloud.exceptions.NotFound:
            #print(u'No such document!')
            output = "No such document"
    return jsonify({'result' : output})
    #?name=kalpit&distance=300
def checkUser(email):
    cities_ref = db.collection('register')
    query = cities_ref.where('email', '==', email).get()
    flag =False
    if(query):
        for doc in query:
            flag=True
    return flag
@app.route('/login/<email>/<password>',methods=['GET'])
def login_user(email,password):
    output="Not Found"
    password=password
    cities_ref = db.collection('register')
    query = cities_ref.where('email', '==', email).get()
    if(query):
        for doc in query:
            doc_dict=doc.to_dict()
            output=doc_dict
            if pwd_context.verify(password, doc_dict['password']):
                output['current_status'] = True
                if type(output['password']) != str:
                    output['password']=output['password'].decode("utf-8")
            else:
                output="Password Does not match"
    else:
        output="Document Not found"
    return jsonify({'result' : output})
@app.route('/claim', methods=['GET'])
def get_all_claim():
    #claim = mongo.db.userclaim
    output=["Not Found"]
    claim = db.collection('claims').get()
    result=[]
    for doc in claim:
        # print(u'{} => {}'.format(doc.id, doc.to_dict()))
        output = doc.to_dict()
        output.pop('image',None)
        result.append(output)
    return jsonify({'result' : result})
    #return make_response(dumps(result))
@app.route('/claim/<name>', methods=['GET'])
def get_one_claim(name):
    output="Not Found"
    claim_ref = db.collection('claims').where(u'name', u'==', name).get()
    # docs = claim_ref.where(u'name', '==','het' ).get()
    result=[]
    for doc in claim_ref:
        # print(u'{} => {}'.format(doc.id, doc.to_dict()))
        output=doc.to_dict()
        output.pop('image')
        result.append(output)
    # print('result',result)
    return jsonify({'result' : result})

@app.route('/claim', methods=['POST'])
def add_claim():
    import datetime as dt
    import dateutil.tz as dz
    local = dz.tzlocal()
    now = dt.datetime.now()
    utc = dz.tzutc()
    now = now.replace(tzinfo=local)
    utc_now = now.astimezone(utc)
    output="Not Found"
    global claimIdCounter
    name=request.values.get('name')
    description=request.values.get('description')
    busniessType=request.values.get('busniesstype')
    image=request.values.get('image')
    email = request.values.get('email')
    claim = db.collection('claims').document()
    claimIdCounter+= 1
    claim_id = claim.set({
        'claim_id':claimIdCounter,
        'name': name,
        'description': description,
        'busniesstype': busniessType,
        'date':utc_now,
        'status':u'progress',
        'status_update_date':utc_now,
        'image':image,
        'email':email
    })
    doc_ref = db.collection('claims').document()
    try:
        output = True
    except google.cloud.exceptions.NotFound:
        output = False
    return jsonify({"result":output})
    #?name=&distance=
@app.route('/claim/<name>/<claim_id>/<status>', methods=['PUT'])
def update_claim(name,status,claim_id):
    import datetime as dt
    import dateutil.tz as dz
    local = dz.tzlocal()
    now = dt.datetime.now()
    utc = dz.tzutc()
    now = now.replace(tzinfo=local)
    utc_now = now.astimezone(utc)
    output=False
    claim_id=int(claim_id)
    claim_ref = db.collection('claims')
    docs = claim_ref.where('name','==',name).where('claim_id', '==', claim_id).get()
    for doc in docs:
        # doc_id = doc.to_dict()
        doc_ref = db.collection('claims').document(doc.id)
        x=doc_ref.update({
            'status': status,
            'status_update_date':utc_now
        })
        output=True
    return jsonify({"result":output})
    #?name=&distance=

@app.route('/forgetpassword/<email>/<password>', methods=['GET'])
def update_password(email,password):
    output="Not Found"
    password=password
    cities_ref = db.collection('register')
    query = cities_ref.where('email', '==', email).get()
    if(query):
        for doc in query:
            password_hash = pwd_context.encrypt(password)
            doc_ref = db.collection('register').document(doc.id)
            x = doc_ref.update({
                'password': password_hash,
            })
            output = True
    return jsonify({'result' : output})
@app.route('/busniesstype/<busniesstype>', methods=['GET'])
def get_filtered_claims(busniesstype):
    claim_ref = db.collection('claims')
    result=[]
    docs = claim_ref.where('busniesstype', '==',busniesstype).get()
    for doc in docs:
        # print(u'{} => {}'.format(doc.id, doc.to_dict()))
        output=doc.to_dict()
        output.pop('image', None)
        result.append(output)
    return jsonify({'result' : result})

@app.route('/claim/<name>/<claim_id>', methods=['GET'])
def get_claim(name,claim_id):
    claim_ref = db.collection('claims')
    claim_id=int(claim_id)
    docs = claim_ref.where('name','==',name).where('claim_id', '==', claim_id).get()
    result=[]
    for doc in docs:
        # print(u'{} => {}'.format(doc.id, doc.to_dict()))
        output=doc.to_dict()
        if type(output['image']) != str:
            output['image'] = output['image'].decode("utf-8")
        result.append((output))

    return jsonify({'result' : result})
@app.route('/delete',methods=['DELETE'])
def clear_collection():
    delete_collection(db.collection('register'), 10)
    delete_collection(db.collection('claims'), 10)
    # claimIdCounter=0
    return jsonify({'result':True})

def delete_collection(coll_ref, batch_size):
    docs = coll_ref.limit(10).get()
    deleted = 0
    global claimIdCounter
    for doc in docs:
        doc.reference.delete()
        deleted = deleted + 1
        claimIdCounter=0

    if deleted >= batch_size:
        return delete_collection(coll_ref, batch_size)
		
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
