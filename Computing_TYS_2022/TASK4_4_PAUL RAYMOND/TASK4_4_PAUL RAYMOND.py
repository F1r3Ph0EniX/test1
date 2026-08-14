#Imports
from flask import *
import sqlite3

#Functions & Procedures

def outstandingLoans():
    '''Function that returns records of books that have yet to be returned, and member data'''

    query = '''SELECT Member.FamilyName, Member.GivenName, Book.Title FROM Member
    JOIN Loan ON Loan.MemberNumber = Member.MemberNumber
    JOIN Book ON Loan.BookID = Book.BookID
    WHERE Loan.Returned = "FALSE"'''

    connection = sqlite3.connect("LIBRARY.db") #Connects python program to library database
    cursor = connection.cursor() #Cursor object used to perform operations on database

    cursor.execute(query) #Cursor points to relevant data
    results = cursor.fetchall() #Obtains data pointed to by cursor

    connection.close() #Terminates connection

    records = []
    for result in results:
        record = [result[0], result[1], result[2]]
        records.append(record)

    return records
    
    
#Main Program

app = Flask(__name__)

@app.route("/")
def home():
    loans = outstandingLoans()
    

    return render_template('index.html', loans=loans)


if __name__ == "__main__":
    app.run("127.0.0.1", 8600)

#Testing
#print(outstandingLoans())
