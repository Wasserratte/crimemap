
import datetime
import dateparser
from flask import Flask     #Import libraries
import json
from flask import render_template
from flask import request
import string
import dbconfig
if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper


app = Flask(__name__)
DB = DBHelper()
categories = ['mugging', 'break-in'] #global variable for the drop-down list html and Python-Validation-Check

def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")	#Convert the userinput into a correct date
    except TypeError:
        return None

def sanitize_string(userinput):
    whitelist = string.letters + string.digits + " !?$.,;:-'()&"
    return filter(lambda x: x in whitelist, userinput) #Checks the whitelist with the filter and lambda function

@app.route("/")
def home(error_message=None):
    crimes = DB.get_all_crimes()
    crimes = json.dumps(crimes) #Convert the dictionary in a string
    return render_template("home.html", crimes=crimes, categories=categories, error_message=error_message)


@app.route("/submitcrime", methods=["POST"])		#Function is called, when mainpage /submitcrime
def submitcrime():					#This function receives the input of the user
    category = request.form.get("category")
    if category not in categories: #Validation-Check
        return home()             				      #from the html page and pass it to the 
    date = format_date(request.form.get("date")) #Call function       #DBHelper() class to use the add_crime method.
    if not date:
        return home("Invalid date. Please use yyyy-mm-dd format")
    try:
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except ValueError:	#The Validation-Check
        return home()
    description = sanitize_string(request.form.get("description"))
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
