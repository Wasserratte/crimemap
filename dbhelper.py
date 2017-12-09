import pymysql
import dbconfig

class DBHelper:		#Defines the new class with the methods for our MySQL database.

    def connect(self, database="crimemap"):
        return pymysql.connect (host='localhost',
                  user=dbconfig.db_user,		#Makes the connection to our database.
                  passwd=dbconfig.db_password,		#Returns the function to the program, so
                  db=database)				#it is available for the other functions.

    def get_all_inputs(self):
        connection = self.connect()		#Calls the connect-method to get a connection to our 
        try:				#database.
            query = "SELECT description FROM crimes;"
            with connection.cursor() as cursor:
                cursor.execute(query)	#Wich SELECT we grab the content in our crime table.
            return cursor.fetchall()	#In this example only the description column.
        finally:			#fetchall() transforms data into a list, so we can
            connection.close()		#display it.

    def add_input(self, data):
        connection = self.connect()
        try:
            query = "INSERT INTO crimes (description) VALUES (%s);"
            with connection.cursor() as cursor:
                cursor.execute(query, data) #With the MySQL-Command INSERT we add data to our
                connection.commit()	#database; here in the description column with the
        finally:			#value from the user input.
            connection.close()		#To save our changes in our database we have to commit it.


    def clear_all(self):
        connection = self.connect()
        try:
            query = "DELETE FROM crimes;"
            with connection.cursor() as cursor:	#With the MySQL-Command DELETE we can delete
                cursor.execute(query)		#data from our database. Here the whole content
                connection.commit()		#of our table crimes.
        finally:
            connection.close()
