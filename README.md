# ict-gnu-final-sem-project-2015-ibm-group_07_mex
# Mex
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
	To update status of claim
		127.0.0.1:5000/claim/<user_emailid>/<status_value>
			status_value=approve or diapproved 
	

