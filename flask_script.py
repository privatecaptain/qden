from flask import Flask, request, make_response, redirect, render_template
import sqlite3
import requests
db_connector = sqlite3.connect("qden_data.db",check_same_thread=False)


app = Flask(__name__)



def sendmail(to,link):
    return requests.post(
        "https://api.mailgun.net/v3/sandboxf32357e89d9f49879486f38f1affacc0.mailgun.org/messages",
        auth=("api", "key-49df66c0deb773d5ee957597be27f9e9"),
        data={"from": "Q-DEN Air2O <mailgun@sandboxf32357e89d9f49879486f38f1affacc0.mailgun.org>",
              "to": [to,],
              "subject": "Verification Email",
              "text": "Congratulations on creating your Q-DEN account click on the link below to activate your account.\n" + link})



def adduser(name,email,password):
	try:
		with db_connector:
			cursor = db_connector.cursor()
			t = (name,email,password,0)
			cursor.execute("INSERT INTO USERS(name,email,password,active) VALUES(?,?,?,?);",t)
			return True
	except:
		return False

def activate(email):
	try:
		with db_connector:
			cursor =  db_connector.cursor()
			t = (1,email)
			cursor.execute("UPDATE USERS SET active=? WHERE email=?;",t)
			return True
	except:
		return False



def valid_login(email,password):
	try:
		with db_connector:
			cursor = db_connector.cursor()
			t = (email,)
			cursor.execute("SELECT password FROM USERS WHERE email=?;",t)
			dpass = cursor.fetchone()[0]
			print dpass,password
			if dpass:
				if dpass == password:
					return True	
	except:
		pass
	return False

def log_the_user_in(email):
	try:
		with db_connector:
			cursor = db_connector.cursor()
			t = (email,)
			cursor.execute("SELECT active FROM USERS WHERE email=?;",t)
			act = cursor.fetchone()[0]
			if int(act) == 1:
				return render_template('index.html')
	except:
		pass
	return render_template("verify_email.html")


@app.route('/')
def index():
    return render_template('login.html')



@app.route('/login', methods=['POST'])
def login():
	if request.method == 'POST':
		if valid_login(request.form['email'],
						request.form['password']):
			return log_the_user_in(request.form['email'])
		else:
			return render_template('loginerror.html')
	return render_template('login.html')



@app.route('/signup',methods=['POST'])
def signup():
	if request.method == 'POST':
		email = request.form['email']
		name = request.form['name']
		password = request.form['password']
		if adduser(name,email,password):
			link = 'http://127.0.0.1:5000/activate/' + str(email)
			sendmail(email,link)
			return render_template('success.html')
	return render_template('login.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name = name)


@app.route('/activate/<email>')
def activate_user(email):
	if activate(email):
		return render_template('verified.html')


if __name__ == '__main__':
    app.run(debug = True)
    # app.run()
