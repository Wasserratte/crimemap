
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

@app.route("/add", methods=["POST"])		#Function is called, when mainpage /add
def add():					#This function receives the input of the user
    try:					#and put it into the DB-Method to insert
        data = request.form.get("userinput")	#this input into our database
        DB.add_input(data)
    except Exception as e:
        print e
    return home()	#Give  the information to the home() function so the new content
			#of our database will be displayed

@app.route("/clear")	#Function is called, when mainpage /clear
def clear():
    try:			#DB-Clear_all() methode is used
        DB.clear_all()
    except Exception as e:
        print e
    return home()	#Return to home() function, so the new database content will be displayed


if __name__ == '__main__':
    app.run(port=5000, debug=True)
