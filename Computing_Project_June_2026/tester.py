import sqlite3

def getEmails(): #Used to retrieve emails for error checking and preventing potential collisions

    connection = sqlite3.connect("study_planner.db") #Connects to database
    cursor = connection.cursor() #Used to perform operations in database

    cursor.execute("SELECT email FROM USERS")
    results = cursor.fetchall()

    connection.close() #Terminates connection

    print(results)

    return results

def checkEmail(email):

    existing_emails = getEmails()

    print("Existing emails: ", existing_emails)

    for record in existing_emails:
        Email = record[0]
        print(name)
        if email == Email:
            return False
    return True

print(checkEmail("paul@gmail.com"))
