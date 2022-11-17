#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='air_ticket_reservation_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/success')
def success():
	username = session['username']
	return render_template('success.html',username=username)

@app.route('/successAdmin')
def successAdmin():
	username = session['username']
	return render_template('successAdmin.html',username=username)

@app.route('/default')
def default():
	return render_template('default.html',)

#Define a route to hello function
@app.route('/')
def hello():
	return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
	return render_template('login.html')

#Define route for register
@app.route('/customerRegister')
def customerRegister():
	return render_template('customerRegister.html')

#Define route for register
@app.route('/adminRegister')
def adminRegister():
	return render_template('adminRegister.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
	#grabs information from the forms
	username = request.form['username']
	password = request.form['password']

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	# query = 'SELECT * FROM user WHERE username = %s and password = %s'
	queryAdmin = 'SELECT * FROM airline_staff WHERE username = %s and passwd = %s'
	cursor.execute(queryAdmin, (username, password))

	#stores the results in a variable
	dataAdmin = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()

	cursor = conn.cursor()

	queryCustomer = 'SELECT * FROM customer WHERE username = %s and pass = %s'
	cursor.execute(queryCustomer, (username, password))

		#stores the results in a variable
	dataCustomer = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()

	error = None
	if(dataAdmin or dataCustomer):
		if dataCustomer:
			#creates a session for the the user
			#session is a built in
			session['username'] = username
			return redirect(url_for('success'))
			# return redirect(url_for('home'))
		else:
			session['username'] = username
			return redirect(url_for('successAdmin'))
	else:
		#returns an error message to the html page
		error = 'Invalid login or username'
		return render_template('index.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
	#grabs information from the forms

	username = request.form['username']
	password = request.form['password']
	curr_path = request.url_rule

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('adminRegister.html', error = error)
	else:
		dob = request.form['dob']
		airline_name = request.form['airline_name']
		first_name = request.form['first_name']
		last_name = request.form['last_name']

		ins = 'INSERT INTO airline_staff (date_of_birth,username,airline_name,passwd,first_name,last_name) VALUES(%s,%s,%s,%s,%s,%s)'
		# ins = 'INSERT INTO airline_staff (username,passwd) VALUES(%s, %s)'
		# cursor.execute(ins, (username, airline_name, password, first_name, last_name))
		cursor.execute(ins, (dob, username, airline_name, password, first_name, last_name))
		conn.commit()
		cursor.close()
		return render_template('index.html')
		
#Authenticates the customer register
@app.route('/registerCustomerAuth', methods=['GET', 'POST'])
def registerCustomerAuth():
	#grabs information from the forms

	username = request.form['username']
	password = request.form['password']
	# curr_path = request.url_rule

	#cursor used to send queries
	cursor = conn.cursor()
	#executes query
	query = 'SELECT * FROM airline_staff WHERE username = %s'
	cursor.execute(query, (username))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	error = None
	if(data):
		#If the previous query returns data, then user exists
		error = "This user already exists"
		return render_template('customerRegister.html', error = error)
	else:

		building_num = request.form['building_number']
		city = request.form['city']
		dob = request.form['dob']
		email = request.form['email']
		name = request.form['name']
		password = request.form['password']
		passport_country = request.form['passport_country']
		passport_exp = request.form['passport_expiration']
		passport_num = request.form['passport_number']
		phone = request.form['phone_number']
		state = request.form['state']
		street = request.form['street']																																		
		ins = 'INSERT INTO customer (building_num,city,dob,email,name,pass,passport_country,passport_exp,passport_num,phone_number,state,street,username) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)'
		# ins = 'INSERT INTO airline_staff (username,passwd) VALUES(%s, %s)'
		# cursor.execute(ins, (username, airline_name, password, first_name, last_name))
		cursor.execute(ins, (building_num,city,dob, email, name, password, passport_country, passport_exp, passport_num, phone, state, street, username))
		conn.commit()
		cursor.close()
		return render_template('index.html',erorr=error)

@app.route('/home')
def home():
    
    username = session['username']
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, (username))
    data1 = cursor.fetchall() 
    for each in data1:
        print(each['blog_post'])
    cursor.close()
    return render_template('home.html', username=username, posts=data1)

		
@app.route('/post', methods=['GET', 'POST'])
def post():
	username = session['username']
	cursor = conn.cursor();
	blog = request.form['blog']
	query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
	cursor.execute(query, (blog, username))
	conn.commit()
	cursor.close()
	return redirect(url_for('home'))

@app.route('/logout')
def logout():
	session.pop('username')
	return redirect('/')
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
