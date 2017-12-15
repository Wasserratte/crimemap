import pymysql
import datetime
import dbconfig

class DBHelper:		

    def connect(self, database="crimemap"):
        return pymysql.connect (host='localhost',
                  user=dbconfig.db_user,		
                  passwd=dbconfig.db_password,		
                  db=database)				

    def get_all_crimes(self):
        connection = self.connect()		
        try:				
            query = "SELECT latitude, longitude, date, category, description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)            #Get all data from the database and store it in query.
                                                #cursor execute it an has now all the data.
            named_crimes = []   #Empty dictionary

            for crime in cursor:    #We make a dictionary and store in in the variable named_crime
                named_crime = {
                    'latitude': crime[0],
                    'longitude': crime[1],
                    'date': datetime.datetime.strftime(crime[2], '%Y-%m-%d'), #We have to convert the time in a
                    'category': crime[3],                                     #string.
                    'description': crime[4] # As key we use the MySQL-Database-Names; so it is easier to call them
                }
                named_crimes.append(named_crime)    #Add the dictionary structure to the empty dictionary
            return named_crimes #We give the named_crimes dictionary back to the program
        finally:
            connection.close()
                    
            

    def add_crime(self, category, date, latitude, longitude, description):
        connection = self.connect()
        try:
            query = "INSERT INTO crimes (category, date, latitude, longitude, description) \
                    VALUES (%s, %s, %s, %s, %s)"
            with connection.cursor() as cursor:
                cursor.execute(query, (category, date, latitude, longitude, description))
                connection.commit()
        except Exception as e:
            print (e)
        finally:
            connection.close()


    def clear_all(self):
        connection = self.connect()
        try:
            query = "DELETE FROM crimes;"
            with connection.cursor() as cursor:	
                cursor.execute(query)		
                connection.commit()		
        finally:
            connection.close()
