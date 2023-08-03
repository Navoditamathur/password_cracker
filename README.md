# password_cracker
Flask to crack and validate passwords of registered users

Objective:

The goal of this programming project is to implement a password authentication mechanism and a password cracker to study the vulnerabilities of choosing weak passwords. 

Description:	

	The project has a mechanism that registers and adds a new user into the system and 	stores the user’s password information in a file. The password can contain only lower-	case letters and a maximum of 2 numbers and 2 special characters ('@', '#', '$', '%', '&'). 	Security is ensured by storing not the password strings but message digests (hash) of the 	passwords to prevent attacks. It also 	allows registered users to login using a module 	which asks for the username and password from the user and verifies it based on the 	information stored in the password 	file. It computes the MD5 message digest of the 	entered password and checks if it matches the MD5 digest of the corresponding user 	password stored in the password file. The program accepts the user only if the message 	digests match.
	The project also offers mechanisms to crack the password of any existing user 	with a 	known username based on a dictionary of commonly used words. Users logged in 	can also validate their passwords and know the time taken to crack their password and 	how strong it is.

Instructions:

•	Make sure to have python 3.10 installed.
•	Open terminal at the folder and install flask
	Pip install flask 
	Pip install flask_session
•	Run by entering the command flask run
•	Open 127.0.0.1
Note:
•	In case flask doesn’t work please open terminal and run ISP_2150.py. It gives options to do the same via terminal.
•	In config.py, replace dictionary.txt with short_dictionary.txt
![image](https://github.com/Navoditamathur/password_cracker/assets/37864618/d6bb5303-71fb-413e-873d-194ed0e9f1b6)

