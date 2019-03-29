
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import base64
# import matplotlib.pyplot as plt
from passlib.context import CryptContext

app = Flask(__name__)
#bcrypt = Bcrypt(app)
app.config['MONGO_DBNAME'] = 'API'
app.config['MONGO_URI'] = "mongodb://rohan_1308:Rj1997Rj@cluster0-shard-00-00-dik6a.mongodb.net:27017,cluster0-shard-00-01-dik6a.mongodb.net:27017,cluster0-shard-00-02-dik6a.mongodb.net:27017/API?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true"

# client = pymongo.MongoClient("mongodb://rohan_1308:<password>@cluster0-shard-00-00-dik6a.mongodb.net:27017,cluster0-shard-00-01-dik6a.mongodb.net:27017,cluster0-shard-00-02-dik6a.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true")
# db = client.test

pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)
claimIdCounter=0
mongo = PyMongo(app)
@app.route('/resgiter',methods=['POST'])
def resgiter_user():
  output = "Not Found"
  user = mongo.db.register
  print(user)
  name=request.values.get('name')
  email=request.values.get('email')
  if (checkUser(email)):
    output = "Already registerd"
  else:
    password = request.values.get('password')
    password_hash = pwd_context.encrypt(password)
    role = request.values.get('role')
    print(type(role))
    if role == None:
      role='User'
    print(name,password,email)
    user.insert({'name': name,'email':email,'password':password_hash,'role':role})
    output = True
  return jsonify(output)

def checkUser(email):
  # cities_ref = db.collection('register')
  user=mongo.db.register
  flag = False
  s = user.find_one({'email': email}, {'password': 1, '_id': 0})
  if (s):
    for doc in s:
      print(doc)
      flag = True
  return flag

@app.route('/login/<email>/<password>',methods=['GET'])
def login_user(email,password):
  output="Not Found"
  print(email,password)
  user=mongo.db.register
  password=password
  s=user.find_one({'email':email},{'password':1,'_id':0})
  if s:
    print('in if')
    print(type(s['password']))
    if pwd_context.verify(password, s['password']):
      output=True
    else:
      output ="Password does not match"
  else:
    output ="No such User"
  return jsonify({'result':output})
@app.route('/claim', methods=['GET'])
def get_all_claim():
  output=["Not Found"]
  print("HEllo")
  claim = mongo.db.userclaim
  result=[]
  for s in claim.find({},{"_id":0}):
    s.pop('image')
    result.append(s)
    # output['image'] =output['image'].decode("utf-8")
  return jsonify({'result' : result})

@app.route('/claim/<name>', methods=['GET'])
def get_one_claim(name):
  claim = mongo.db.userclaim
  s=claim.find({'name': name}, {"_id": 0})
  output=[]
  for i in s:
    print(type(i))
    i.pop('image')
    output.append(i)
  if output == []:
    output="Not Found"
  return jsonify({'result' : output})
@app.route('/claim', methods=['POST'])
def add_claim():
  import datetime as dt
  import dateutil.tz as dz
  global claimIdCounter
  claimIdCounter += 1
  local = dz.tzlocal()
  now = dt.datetime.now()
  utc = dz.tzutc()
  now = now.replace(tzinfo=local)
  utc_now = now.astimezone(utc)
  claim = mongo.db.userclaim
  name=request.values.get('name')
  description=request.values.get('description')
  busniessType=request.values.get('busniesstype')
  email=request.values('email')
  image=request.values.get('image')
  date=utc_now
  claim_id = claim.insert({'claim_id':claimIdCounter,'name': name, 'description': description,'busniessType':busniessType,'date':date,'status': 'disapprove','status_update_date': utc_now,'image': image,'email':email})
  new_claim = claim.find_one({'_id': claim_id },{"_id":0})
  output = new_claim
  return jsonify(output)
  #?name=&distance=
@app.route('/claim/<name>/<claim_id>/<status>', methods=['PUT'])
def update_claim(name,claim_id,status):
  import datetime as dt
  import dateutil.tz as dz
  global claimIdCounter
  claimIdCounter += 1
  local = dz.tzlocal()
  now = dt.datetime.now()
  utc = dz.tzutc()
  now = now.replace(tzinfo=local)
  utc_now = now.astimezone(utc)
  print('in up[date function')
  claim = mongo.db.userclaim
  output=False
  claim.update({'name':name,'claim_id':claim_id},{"$set": { "status": status,"status_update_date": utc_now } })
  output=[]
  for i in claim.find({'name': name,'claim_id':claim_id,'status':status}, {"_id": 0}):
    output=True
  return jsonify({'result':output})

@app.route('/forgetpassword/<email>/<password>', methods=['GET'])
def update_password(email,password):
    output="Not Found"
    password=password
    user = mongo.db.register
    s=user.find_one({'email':email},{'password':1,'_id':0})
    if(s):
        for doc in s:
            password_hash = pwd_context.encrypt(password)
            user.update({'email':email},{"$set":{'password':password_hash}})
            output = True
    return jsonify({'result' : output})
@app.route('/busniesstype/<busniesstype>', methods=['GET'])
def get_filtered_claims(busniesstype):
    claim = mongo.db.userclaim
    result=[]
    docs = claim.find({'busniesstype', '==',busniesstype},{"_id":0})
    for doc in docs:
        output=doc.to_dict()
        output.pop('image', None)
        result.append(output)
    return jsonify({'result' : result})

@app.route('/claim/<name>/<claim_id>', methods=['GET'])
def get_claim(name,claim_id):
    claim=mongo.db.userclaim
    claim_id=int(claim_id)
    docs = claim.find({'name':name,'claim_id':claim_id},{"_id":0})
    result=[]
    for doc in docs:
        output=doc.to_dict()
        if type(output['image']) != str:
            output['image'] = output['image'].decode("utf-8")
        result.append((output))

    return jsonify({'result' : result})

if __name__ == '__main__':
    app.run(debug=True)
