# Mex
# Start Mongodb Service locally(For Windows) 
	assume that you have installed MongoDB to C:\Program Files\MongoDB\Server\3.2\.
	run is this command from command Prompt "C:\Program Files\MongoDB\Server\3.2\bin\mongod.exe"
# Start Mongodb Service locally(For Linux) 
	sudo service mongod start
# Install Requirements.txt
	pip install -r requirements.txt
# Import MongoDb Database
	mongoimport --db <database name> --file <file-path>
# Rest API
	To Get all the claim's
		127.0.0.1:5000/claim (get method)
	To Get Specific Claim according to name 
		127.0.0.1:5000/claim/<name of user> (get method)
	To Insert into database
		127.0.0.1:5000/claim?name="value"&description="value"&busniessType="value"&date="value"&image="value" (post method)
	To Register into system
		127.0.0.1:5000/resgiter?name="value"&password="value"&email="value"
	To login into system 
		127.0.0.1:5000/resgiter/<email_id>/<password>
		
	
