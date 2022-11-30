#Import Flask Library
from datetime import datetime 
from flask import Flask, render_template, request, session, url_for, redirect
import pymysql.cursors
from datetime import datetime

#Initialize the app from Flask
app = Flask(__name__)

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='',
                       db='air_ticket_reservation_system',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)

@app.route('/customerViews/success')
def success():
	username = session['username']
	return render_template('/customerViews/success.html',username=username)

@app.route('/adminViews/successAdmin')
def successAdmin():
	username = session['username']
	return render_template('/adminViews/successAdmin.html',username=username)


#<--------------------------------------------- CUSTOMER ----------------------------------------------------------------------->


@app.route('/checkFlight', methods = ['GET', 'POST'])
def checkFlight(): 

	username = session['username']
	time = str(request.form.get('viewOption'))

	if time == "Future flights":
		time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

		# time = "Displaying Future Flights"
	else:
		time = "Displaying All Flights"
		# time = "hehe"

	cursor = conn.cursor()
	query = "SELECT email FROM customer WHERE username = %s"
	cursor.execute(query, (username))
	tempData = cursor.fetchall()
	email = str(tempData[0]['email'])
	# data = str(email)
	cursor.close()

	cursor = conn.cursor()
	checkExistsquery = "SELECT * FROM ticket WHERE customer_email = %s"
	cursor.execute(checkExistsquery, (email))
	data = cursor.fetchall()
	# data = type(email)
	cursor.close()
	error = "FLIGHT STATUS UPDATE COMPLETE!"

	# if data:
	# 	second_cursor = conn.cursor()
	# 	setStatusquery = "UPDATE flight SET stat=%s WHERE flight_num = %s AND airline_name = %s AND depart_date_time = %s"
	# 	second_cursor.execute(setStatusquery, (new_stat, f_num, airline_name, dep_date_time))
	# 	conn.commit() 
	# 	second_cursor.close()
	# else:
	# 	error = "NO SUCH FLIGHT EXISTS"

	return render_template('/customerViews/customerOperationResult.html', data=data, time = time)

#<--------------------------------------------- CUSTOMER ----------------------------------------------------------------------->


#<--------------------------------------------- ADMIN ----------------------------------------------------------------------->

@app.route('/adminView/createAirplane', methods = ['GET', 'POST'])
def createAirPlane():
	id = request.form['ID']
	airline_name = request.form['Airline_name']
	manufacturer = request.form['Manufacturer']
	seats = request.form['Seats']
	age = request.form['Age']

	cursor = conn.cursor()
	query = "INSERT INTO airplane(id, airline_name, manufacturer, seats, age) VALUES(%s, %s, %s, %s, %s)"
	error = None
	try:
		cursor.execute(query, (id, airline_name, manufacturer, seats, age))
		conn.commit() 
		error = "AIRPLANE CREATION SUCCESS!"
	except:
		error = "FAILED TO CREATE AIRPLANE, Double Check ID/Airline_Name Fields"
	finally:
		cursor.close()

	return render_template('/adminViews/adminOperationResult.html', error=error)

@app.route('/adminView/setFlightStatus', methods = ['GET', 'POST'])
def setFlightStatus(): 
	new_stat = request.form['status']
	f_num = request.form['F#']
	airline_name = request.form['Airline_name']
	dep_date_time = request.form['dep']

	cursor = conn.cursor()
	checkExistsquery = "SELECT * FROM flight WHERE flight_num = %s AND airline_name = %s AND depart_date_time = %s"
	cursor.execute(checkExistsquery, (f_num, airline_name, dep_date_time))
	data = cursor.fetchall()
	cursor.close()
	error = "FLIGHT STATUS UPDATE COMPLETE!"

	if data:
		second_cursor = conn.cursor()
		setStatusquery = "UPDATE flight SET stat=%s WHERE flight_num = %s AND airline_name = %s AND depart_date_time = %s"
		second_cursor.execute(setStatusquery, (new_stat, f_num, airline_name, dep_date_time))
		conn.commit() 
		second_cursor.close()
	else:
		error = "NO SUCH FLIGHT EXISTS"

	return render_template('/adminViews/adminOperationResult.html', error=error)
	
@app.route('/adminViews/createFlight', methods = ['GET', 'POST'])
def createFlight(): 
	f_num = request.form['F#']
	airline_name = request.form['airline_name']
	dep_date_time = request.form['dep']
	dep_airport = request.form['departure_airport']
	arr_airport = request.form['arrival_airport']
	airplane_id = request.form['airplane_id']
	arrive_date_time = request.form['arrive_date_time']
	b_price = request.form['base_price']
	status = request.form['status']

	cursor = conn.cursor()
	query = "INSERT INTO flight VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
	error = None

	try:
		cursor.execute(query, (f_num,airline_name,dep_date_time,dep_airport,arr_airport, airplane_id,arrive_date_time,b_price,status))
		conn.commit() 
		error = "FLIGHT CREATED SUCCESSFULLY!"
	except:
		error = "FAILED TO CREATE FLIGHT, Double Check F Number/ Departure Airport/ Arrival Airport"
	finally:
		cursor.close()

	return render_template('/adminViews/adminOperationResult.html', error=error)

#<--------------------------------------------- ADMIN ----------------------------------------------------------------------->


@app.route('/customerViews/cancelTripScreen')
def cancelTripScreen():
	username = session['username']
	return render_template('/customerViews/cancelTripScreen.html',username=username)

@app.route('/customerViews/purchaseScreen')
def purchaseScreen():
	username = session['username']
	return render_template('/customerViews/purchaseScreen.html',username=username)

@app.route('/customerViews/rateCommentScreen')
def rateCommentScreen():
	username = session['username']
	return render_template('/customerViews/rateCommentScreen.html',username=username)

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
@app.route('/customerViews/customerRegister')
def customerRegister():
	return render_template('/customerViews/customerRegister.html')

#Define route for register
@app.route('/adminViews/adminRegister')
def adminRegister():
	return render_template('/adminViews/adminRegister.html')

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
		session['username'] = username
		session['logged'] = True 
		if dataCustomer:
			#creates a session for the the user
			#session is a built in
			session['admin'] = False
			return redirect(url_for('success'))
			# return redirect(url_for('home'))
		elif dataAdmin:
			session['admin'] = True
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
	session.pop('admin')
	return redirect('/')
		
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)
