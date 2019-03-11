from pymongo import MongoClient
#client = MongoClient('sl-eu-gb-p05.dblayer.com',port=17584,username='admin',password='JOISQFGXCPOQYKPW',authSource='admin',authMechanism='SCRAM-SHA-1')
#uri = "mongodb://admin:JOISQFGXCPOQYKPW@sl-eu-gb-p05.dblayer.com:17584/?authSource=admin&authMechanism=SCRAM-SHA-1"
uri="mongodb://admin:JOISQFGXCPOQYKPW@portal-ssl79-37.bmix-eu-gb-yp-e5902193-7191-433e-af74-9ce860475330.1409146671.composedb.com:17584,portal-ssl82-23.bmix-eu-gb-yp-e5902193-7191-433e-af74-9ce860475330.1409146671.composedb.com:17584/compose?authSource=admin&ssl=true"
client=MongoClient(uri)

print(client)
print(client.list_database_names())
dblist = client.list_database_names()
if "mydatabase" in dblist:
  print("The database exists.")

# clinet=MongoClient('sl-eu-gb-gb-p05.dblayer.com',port=17584,username='admin','passwo')