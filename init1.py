#Import Flask Library
from datetime import datetime 
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

@app.route('/default')
def default():
	return render_template('default.html',)

#Define a route to hello function
@app.route('/', methods=['GET','POST'])
def index():
	print("Hello")
	return render_template('index.html')

@app.route('/searchFlight', methods=['GET', 'POST'])
def searchFlight():
	# necessary flight information 
	departure_city = request.form['departCity']
	departure_airport = request.form['departAiport']
	arrival_city = request.form['arriveCity']
	arrival_airport = request.form['arriveAirport']
	depart_date_time = request.form['departDT']
	arrival_date_time = request.form['ReturnDT']

	#cursor used to send queries
	cursor = conn.cursor()

	# execute query for ONEWAY TRIP into cursor
	if arrival_date_time == "":
		query = ('SELECT * FROM flight WHERE '
		'('
			'(departure_airport = %s OR departure_airport IN (SELECT name FROM airport WHERE city = %s)) AND '
			'(arrival_airport = %s OR arrival_airport IN (SELECT name FROM airport WHERE city = %s)) AND '
			'(depart_date_time = %s)'
		')')
		cursor.execute(query, (departure_airport, departure_city, arrival_airport, arrival_city, depart_date_time))
	# execute query for ROUND TRIP into cursor 
	else:
		query = ('SELECT * FROM flight WHERE '
		'('
			'(departure_airport = %s OR departure_airport IN (SELECT name FROM airport WHERE city = %s)) AND '
			'(arrival_airport = %s OR arrival_airport IN (SELECT name FROM airport WHERE city = %s)) AND '
			'(arrive_date_time = %s AND depart_date_time = %s AND arrival_airport = departure_airport)'
		')')
		cursor.execute(query, (departure_airport, departure_city, arrival_airport, arrival_city, arrival_date_time, depart_date_time))

	# catch data
	data = cursor.fetchall()
	error = None 	
	cursor.close()

	# TODO: render template with queried data 
	return render_template('flightdata.html', data= data)

@app.route('/searchFlightStatus', methods=['GET', 'POST'])
def searchFlightStatus():
	# necessary flight information 

	airline_name = request.form['airline']
	flight_number = request.form['flight']
	date = request.form['depArr']

	cursor = conn.cursor()
	query = "SELECT stat FROM flight WHERE airline_name = %s AND flight_num = %s AND ((DATE(depart_date_time) = %s) OR (DATE(arrive_date_time) = %s))"
	cursor.execute(query, (airline_name, flight_number, date, date))

	data = cursor.fetchall()
	error = None 
	cursor.close()

	return render_template('flightdata.html', data= data)


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
	query = 'SELECT * FROM airline_staff WHERE username = %s and passwd = %s'
	cursor.execute(query, (username, password))
	#stores the results in a variable
	data = cursor.fetchone()
	#use fetchall() if you are expecting more than 1 data row
	cursor.close()
	error = None
	if(data):
		#creates a session for the the user
		#session is a built in
		session['username'] = username
		return redirect(url_for('success'))
		# return redirect(url_for('home'))
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
		return render_template('register.html', error = error)
	else:
		ins = 'INSERT INTO airline_staff (username,passwd) VALUES(%s, %s)'
		cursor.execute(ins, (username, password))
		conn.commit()
		cursor.close()
		return render_template('index.html')
		
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
