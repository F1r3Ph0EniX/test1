#Imports
from flask import *
import sqlite3

#Functions & Procedures

def get_data():
    '''Function to get all records from people table'''
    records = []

    #Query to perform on database
    query = "SELECT FullName, ScreenName FROM People"

    connection = sqlite3.connect("school.db") #Connects to database
    cursor = connection.cursor() #Cursor object to perform operations in database
    cursor.execute(query) #execute command, cursor now points to relevant data
    results = cursor.fetchall() #data pointed to by cursor is fetched
    
    connection.close() #connection to database is terminated

    #formatting data into required form
    for result in results:
        #print(result) #Debugging
        name = result[0]
        screenName = result[1]
        
        if "Staff" in screenName:
            identification = "Staff"
            
        elif "Student" in screenName:
            identification = "Student"
        else:
            identification = "Person"

        record = [name, screenName, identification]
        records.append(record)

    #print(records) #Debugging
    return records

#Main Program

app = Flask(__name__) #creates Flask instance

@app.route("/") #Homepage
def home():
    records = get_data()
    return render_template("index.html", records=records)

if __name__ == "__main__": #Runs app
    
    app.run(host="127.0.0.1", port=8230, debug=True, threaded=True, use_reloader=True)
