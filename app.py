from flask import Flask, render_template, url_for, request, session, redirect
from flask_session import Session
import MySQLdb
import json
import os
from flask import jsonify
from datetime import datetime,timedelta
app = Flask(__name__)
sess = Session()

cursor = None
db = None
def connect_database():
	global cursor,db
	# Open database connection
	db = MySQLdb.connect(os.environ["CAB_SHARING_MYSQL_IP"], os.environ["CAB_SHARING_MYSQL_USER"], os.environ["CAB_SHARING_MYSQL_PASSWORD"], os.environ["CAB_SHARING_MYSQL_DATABASENAME"])
	# prepare a cursor object using cursor() method
	cursor = db.cursor()

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/post-cab", methods=["POST"])
def postCab():
	if cursor == None or db == None :
		connect_database()
	# else :
		# return render_template("index.html") #return with error ******
	form_dict = request.form.to_dict()
	date = form_dict["date"]
	time = form_dict["time"]
	dateTime = date + time 
	threshold = form_dict["threshold"]
	print ("{} - {}".format(type(date),date))
	print ("{} - {}".format(type(time),time))
	# dateTime = datetime.strptime(form_dict["datetime"], '%Y-%m-%dT%H:%M:%S.%fZ')
	query = "INSERT INTO cabdetails (name,emailid,number,availSeats,source,dest,date,time,threshold) values ('%s','%s','%s','%s','%s','%s', '%s','%s','%s')" % (form_dict["name"],form_dict["emailid"],form_dict["number"],form_dict["availSeats"],form_dict["source"],form_dict["dest"],date,time,threshold)
	try :
		cursor.execute(query)
		db.commit()
		return jsonify(success=True)
	except Exception as e :
		print e
		return jsonify(success=False)
		#Reder teml with error
	# for key in form_dict.keys() :
	# 	print ("{} - {}\n".format(key,form_dict[key]))
	# flag = True
	# msg = "Your ride data has been successfully submitted"
	# msgcode = "RidePost"
	# return jsonify(success=True)
	# return render_template('index.html' , flag=flag, msg=msg,msgcode=msgcode)


@app.route("/search-cab",methods=["POST"])
def searchCab() :
	if cursor == None or db == None :
		connect_database()
	# else :
		# return render_template("index.html") #return with error ******
	query = "SELECT * FROM cabdetails"
	form_dict = request.form.to_dict()
	print form_dict
	dest = form_dict["dest"]
	date = form_dict["date"]
	time = form_dict["time"]
	print dest 
	print ("{} - {}".format(type(date) , date))
	print ("{} - {}".format(type(time) , time))
	userDatetime = convertDateTime(date,time)
	print userDatetime
	try :
		cursor.execute(query)
		cabsList = list()
		for row in cursor.fetchall():
			if (dest == row[5]) :
				x = row[6].strftime("%Y-%m-%d")
				y= str(row[7])
				cabDateTime = convertDateTime(x,y[:-3])
				print cabDateTime
				if ((cabDateTime <= userDatetime + timedelta(hours=row[8])) and (cabDateTime >= userDatetime - timedelta(hours=row[8])) ) :
					cabsList.append(dict(name= row[0],
								email=row[1],
								number=row[2],
								availSeats=row[3],
								dest=row[5],
								# date=str(row[6]),
								# time=str(row[7]),
								threshold = row[8]
								))
		return jsonify(success=True, data=json.loads(json.dumps(cabsList)))
	except Exception as e :
		print e 
		return jsonify(success=False)
		#Reder teml with errordef

@app.route("/get-all-cabs")
def allCabs():
	if cursor == None or db == None :
		connect_database()
	query = "SELECT * FROM cabdetails"
	try :
		cursor.execute(query)
		cabsList = list()
		for row in cursor.fetchall():
			# if (dest == row[5]) :
			# print row[6]
			# x = row[6].strftime("%Y-%m-%d")
			# y= str(row[7])
			# cabDateTime = convertDateTime(x,y[:-3])
			# print cabDateTime
			# if ((cabDateTime <= userDatetime + timedelta(hours=row[8])) and (cabDateTime >= userDatetime - timedelta(hours=row[8])) ) :
			cabsList.append(dict(name= row[0],
						email=row[1],
						number=row[2],
						availSeats=row[3],
						dest=row[5],
						date=str(row[6]),
						time=str(row[7]),
						threshold = row[8]
						))
		# response = app.response_class(
  #       response=json.dumps(cabsList),
  #       status=200,
  #       mimetype='application/json')
		# # return response	
		print cabsList
		return jsonify(success=True, data=json.loads(json.dumps(cabsList)))

	except Exception as e :
		return jsonify(success=False)
		print e
		pass
def convertDateTime(date , time):
	if len(time) == 8 :
		time = time[:5]
		print time
	return datetime.strptime(date+"T"+time,'%Y-%m-%dT%H:%M')
	 
app.secret_key = 'kwoc'
app.config['SESSION_TYPE'] = 'filesystem'

sess.init_app(app)
app.debug = True

if __name__ == "__main__" :
	app.run(debug=True)