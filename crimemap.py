
from flask import Flask			#Import libraries
from flask import render_template
from flask import request
import dbconfig
if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper


app = Flask(__name__)		#Initializing our application
DB = DBHelper()			#DB is the instance(object) of the DBHelper
				#class, which contains the neccessaary methods
@app.route("/")
def home():
    try:
        data = DB.get_all_inputs()
    except Exception as e:
        print e					#When the mainpage is called, all datas in the
        data = None				#database will be grabed and displayed
    return render_template("home.html", data=data)

@app.route("/submitcrime", methods=["POST"])		#Function is called, when mainpage /submitcrime
def submitcrime():					#This function receives the input of the user
    category = request.form.get("category")             #from the html page and pass it to the 
    date = request.form.get("date")                     #DBHelper() class to use the add_crime method.
    latitude = float(request.form.get("latitude"))
    longitude = float(request.form.get("longitude"))
    description = request.form.get("description")
    DB.add_crime(category, date, latitude, longitude, description)  #Calls the home() function to show the result
    return home()

@app.route("/clear")	#Function is called, when mainpage /clear
def clear():
    try:			#DB-Clear_all() methode is used
        DB.clear_all()
    except Exception as e:
        print e
    return home()	#Return to home() function, so the new database content will be displayed


if __name__ == '__main__':
    app.run(port=5000, debug=True)
