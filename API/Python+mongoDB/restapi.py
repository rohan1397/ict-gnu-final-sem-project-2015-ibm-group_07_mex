
from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import base64
# import matplotlib.pyplot as plt
from passlib.context import CryptContext

app = Flask(__name__)
#bcrypt = Bcrypt(app)
app.config['MONGO_DBNAME'] = 'compose'
app.config['MONGO_URI'] = "mongodb://admin:JOISQFGXCPOQYKPW@portal-ssl79-37.bmix-eu-gb-yp-e5902193-7191-433e-af74-9ce860475330.1409146671.composedb.com:17584,portal-ssl82-23.bmix-eu-gb-yp-e5902193-7191-433e-af74-9ce860475330.1409146671.composedb.com:17584/compose?authSource=admin&ssl=true"
pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)
mongo = PyMongo(app)
@app.route('/register',methods=['POST'])
def resgiter_user():
  print(mongo)
  #return jsonify("mongo")

  user = mongo.db.register
  name=request.values.get('name')
  password=request.values.get('password')
  password_hash=pwd_context.encrypt(password)
  print(type(password_hash))
  email=request.values.get('email')
  print(name)
  user_id = user.insert({'name': name,'email':email,'password':password_hash})
  new_user = user.find_one({'_id': user_id },{"_id":0})
  output = new_user
  return jsonify(output)
  #?name=kalpit&distance=300
@app.route('/login/<email>/<password>',methods=['GET'])
def login_user(name,password):
  print(name,password)
  user=mongo.db.register
  password=password
  s=user.find_one({'email':email},{'password':1,'_id':0,'name':1})
  if s:
    #output=s
    print('in if')
    print(type(s['password']))
    if pwd_context.verify(password, s['password']):
      output=s
    else:
      output ="Password does not match"
  else:
    output ="No such User"
    return False
  return jsonify({'result':output})
@app.route('/claim', methods=['GET'])
def get_all_claim():
  claim = mongo.db.userclaim
  output = []
  for s in claim.find({},{"_id":0}):
    #output.append({'name' : s['name'], 
    output=s #'distance' : s['distance']})
    filename=s['name']+'.jpeg'
    image_64_decode=base64.decodestring(output['image'])
    image_result = open(filename, 'wb') # create a writable image and write the decoding result 
    image_result.write(image_64_decode)  
    #output.append(s)
  return jsonify({'result' : output})

@app.route('/claim/<name>', methods=['GET'])
def get_one_claim(name):
  claim = mongo.db.userclaim
  filename='public/image/'+name+'.jpeg'
  print(filename)
  s = claim.find_one({'name' : name},{"_id":0})
  if s:
    output = s
    image_64_decode=base64.decodestring(output['image'])
    image_result = open(filename, 'wb') # create a writable image and write the decoding result 
    image_result.write(image_64_decode)  
  else:
    output = "No such name"
  return jsonify({'result' : output})
@app.route('/claim', methods=['POST'])
def add_claim():
  import datetime as dt
  claim = mongo.db.userclaim
  name=request.values.get('name')
  description=request.values.get('description')
  busniessType=request.values.get('busniessType')
  with open("public/image/try.jpeg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
  date=dt.datetime.now()
  print(name,description)
  claim_id = claim.insert({'name': name, 'description': description,'busniessType':busniessType,'date':date,'image':encoded_string})
  new_claim = claim.find_one({'_id': claim_id },{"_id":0})
  output = new_claim
  return jsonify(output)
  #?name=&distance=

if __name__ == '__main__':
    app.run(debug=True)
