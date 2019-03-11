# Use CouchDB to create a CouchDB client
# from cloudant.client import CouchDB
# client = CouchDB(USERNAME, PASSWORD, url='http://127.0.0.1:5984', connect=True)

# Use Cloudant to create a Cloudant client using account
from cloudant.client import Cloudant
import cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey
USERNAME="8d047230-2a9a-4ea5-8635-385a10e22857-bluemix"
PASSWORD="eb19e769be27224647840d37cfa9f7d5bacfef887d2ba0a3ec8cb771d09736dd"
URL="https://8d047230-2a9a-4ea5-8635-385a10e22857-bluemix.cloudant.com"
#client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME, connect=True)
# or using url
#
client = Cloudant(USERNAME,PASSWORD,url=URL)
client.connect()
# or with a 429 replay adapter that includes configured retries and initial backoff
# client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME,
#                   adapter=Replay429Adapter(retries=10, initialBackoff=0.01))

# or with a connect and read timeout of 5 minutes
# client = Cloudant(USERNAME, PASSWORD, account=ACCOUNT_NAME,
#                   timeout=300)

# Perform client tasks...
session = client.session()
print('Username: {0}'.format(session['userCtx']['name']))
print('Databases: {0}'.format(client.all_dbs()))
databaseName = "mex"
# myDatabaseDemo # = client.create_database(databaseName)
# if myDatabaseDemo.exists():
# 	print ("'{0}' successfully created.\n".format(databaseName))
#createDatabase()
# Disconnect from the server
# print(myDatabaseDemo)
cloudant.database.CloudantDatabase(client, 'mex')
print(cloudant.database_url())
s=['rohanjain','1234','rohan@gmail.com']
for document in s:
	# Retrieve the fields in each row.
	#number = document[0]
	name = document[0]
	password = document[1]
	email = document[2]

	# Create a JSON document that represents
	# all the data in the row.
	jsonDocument = {
		"name": name,
		"email": email,
		"password": password,
	}

	# Create a document using the Database API.
	newDocument = myDatabaseDemo.create_document(jsonDocument)

	# Check that the document exists in the database.
	if newDocument.exists():
		print("Document '{0}' successfully created.".format(name))