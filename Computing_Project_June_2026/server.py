#Imports
import os
import sqlite3
from flask import *

#Functions & Procedures

def initialise_study_planner(): #Procedure to create and initialise the study planner database


    connection = sqlite3.connect("study_planner.db") #Creates a connection to study_planner.db, creates study_planner.db if not exists
    cursor = connection.cursor() #Instantiates a cursor object which will be used to perform operations in the database

    #Deletes existing tables
    cursor.execute("DROP TABLE IF EXISTS TASK_STATUS")
    cursor.execute("DROP TABLE IF EXISTS TASK_CATEGORIES")
    cursor.execute("DROP TABLE IF EXISTS TASKS")
    cursor.execute("DROP TABLE IF EXISTS SESSIONS")
    cursor.execute("DROP TABLE IF EXISTS SUBJECTS")
    cursor.execute("DROP TABLE IF EXISTS USERS")

    #Creates tables
    cursor.execute("""CREATE TABLE "USERS" (
	"userID"	INTEGER NOT NULL,
	"email"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("userID" AUTOINCREMENT)
        );""")
    cursor.execute("""CREATE TABLE "SUBJECTS" (
	"subjectID"	INTEGER NOT NULL,
	"subjectName"	TEXT NOT NULL,
	"userID"	INTEGER NOT NULL,
	PRIMARY KEY("subjectID" AUTOINCREMENT),
	FOREIGN KEY("userID") REFERENCES "USERS"("userID")
        );""")
    #TASK_STATUS is a table which assists TASKS by providing key-value pairs for progress status
    cursor.execute("""CREATE TABLE "TASK_STATUS" (
	"statusID"	INTEGER NOT NULL,
	"statusName"	TEXT NOT NULL,
	PRIMARY KEY("statusID")
        );""")
    #TASK_CATEGORIES is a table which assists TASKS by providing categorisation
    cursor.execute("""CREATE TABLE "TASK_CATEGORIES" (
	"categoryID"	INTEGER NOT NULL,
	"categoryName"	TEXT NOT NULL,
	PRIMARY KEY("categoryID")
        );""")
    cursor.execute("""CREATE TABLE "TASKS" (
	"taskID"	INTEGER NOT NULL,
	"title"		TEXT NOT NULL,
	"description"	TEXT,
	"dueDate"	TEXT NOT NULL,
	"priority"	TEXT NOT NULL,
	"userID"	INTEGER NOT NULL,
	"subjectID"	INTEGER NOT NULL,
	"statusID"	INTEGER NOT NULL,
	"categoryID"	INTEGER NOT NULL,
	PRIMARY KEY("taskID" AUTOINCREMENT),
	FOREIGN KEY("categoryID") REFERENCES "TASK_CATEGORIES"("categoryID"),
	FOREIGN KEY("statusID") REFERENCES "TASK_STATUS"("statusID"),
	FOREIGN KEY("subjectID") REFERENCES "SUBJECTS"("subjectID"),
	FOREIGN KEY("userID") REFERENCES "USERS"("userID")
        );""")
    cursor.execute("""CREATE TABLE "SESSIONS" (
	"sessionID"	INTEGER NOT NULL,
	"date"	TEXT NOT NULL,
	"startTime"	TEXT NOT NULL,
	"endTime"	TEXT NOT NULL,
	"remarks"	TEXT,
	"userID"	INTEGER NOT NULL,
	"subjectID"	INTEGER NOT NULL,
	PRIMARY KEY("sessionID" AUTOINCREMENT),
	FOREIGN KEY("subjectID") REFERENCES "SUBJECTS"("subjectID"),
	FOREIGN KEY("userID") REFERENCES "USERS"("userID")
        );""")

    #Inserts key values into relevant tables
    cursor.execute("INSERT INTO TASK_STATUS(statusID, statusName) VALUES (1,'Not Started'), (2, 'In Progress'), (3, 'Completed')")
    cursor.execute("""INSERT INTO TASK_CATEGORIES (categoryID, categoryName) VALUES
        (1, 'Homework'), (2, 'Revision'), (3, 'Project'), (4, 'Consultation'), (5, 'Test Prep')""")

    connection.commit() #Saves changes
    connection.close() #Terminates connection to database

def getEmails(): #Used to retrieve emails for error checking and preventing potential collisions

    connection = sqlite3.connect("study_planner.db") #Connects to database
    cursor = connection.cursor() #Used to perform operations in database

    cursor.execute("SELECT email FROM USERS")
    results = cursor.fetchall()

    connection.close() #Terminates connection

    return results

def checkEmail(email):

    existing_emails = getEmails()

    print("Existing emails: ", existing_emails)

    for record in existing_emails:
        Email = record[0]

        if email == Email:
            return False
        
    return True

def tasks_display(userID):

    tasks_query = """SELECT 
    TASKS.taskID,
    TASKS.title, 
    TASKS.description, 
    TASKS.dueDate, 
    TASKS.priority,
    SUBJECTS.subjectName,
    TASK_STATUS.statusName,
    TASK_CATEGORIES.categoryName
    FROM TASKS INNER JOIN SUBJECTS ON TASKS.subjectID = SUBJECTS.subjectID INNER JOIN TASK_STATUS ON TASKS.statusID = TASK_STATUS.statusID INNER JOIN TASK_CATEGORIES ON TASKS.categoryID = TASK_CATEGORIES.categoryID
     WHERE TASKS.userID = ?"""

    connection = sqlite3.connect("study_planner.db") #Connects python script to student_planner.db
    cursor = connection.cursor() #Used to perform operations in database

    cursor.execute(tasks_query, (int(userID),))
    results = cursor.fetchall() #Assigns all value pointed at by cursor to results

    connection.close() #Terminates connection

    return results


def insert_task(title, description, dueDate, priority, subject_id, user_id, category_id):

    #Default settings
    status_id = 1

    #Packaging record
    record = [title, description, dueDate, priority, user_id, subject_id, status_id, category_id]
    connection = sqlite3.connect("study_planner.db") #Connects to database
    cursor = connection.cursor() #Used to perform operations in database

    #inserting record
    cursor.execute("INSERT INTO TASKS(title, description, dueDate, priority, userID, subjectID, statusID, categoryID) VALUES (?,?,?,?,?,?,?,?)", record)

    connection.commit() #Saves changes
    connection.close() #Terminates connection

def amend_task(taskID, title, description, dueDate, priority, subject_id, user_id, status_id, category_id): #Helper function to edit a task


    #Packaging record
    record = [title, description, dueDate, priority, subject_id, status_id, category_id, taskID, user_id] #Includes taskID to find task
    connection = sqlite3.connect("study_planner.db") #Connects to database
    cursor = connection.cursor() #Used to perform operations in database

    #Updating record
    cursor.execute("UPDATE TASKS SET title=?, description=?, dueDate=?, priority=?, subjectID=?, statusID=?, categoryID=? WHERE taskID=? AND userID=?", record)

    connection.commit() #Saves changes
    connection.close() #Terminates connection

def update_task_status(taskID, userID, statusID):

    #Packaging record
    record = [statusID, taskID, userID]

    connection = sqlite3.connect("study_planner.db") #Connects to database
    cursor = connection.cursor() #Used to perform operations in database

    #Updating specified task's status
    cursor.execute("UPDATE TASKS SET statusID=? WHERE taskID=? AND userID=?", record)

    connection.commit() #Saves changes
    connection.close() #Terminates connection

def delete_task(taskID, user_id):

    record = [taskID, user_id]

    connection = sqlite3.connect("study_planner.db") #Connects to database
    cursor = connection.cursor() #Used to perform operations in database

    #Deleting record
    cursor.execute("DELETE FROM TASKS WHERE taskID=? AND userID=?", record)

    connection.commit() #Saves changes
    connection.close() #Terminates connection

def sessions_display(userID):

    query = """SELECT
    SESSIONS.sessionID,
    SESSIONS.date,
    SESSIONS.startTime,
    SESSIONS.endTime,
    SESSIONS.remarks,
    SUBJECTS.subjectName
    FROM SESSIONS INNER JOIN SUBJECTS ON SESSIONS.subjectID = SUBJECTS.subjectID WHERE SESSIONS.userID = ?"""

    connection = sqlite3.connect("study_planner.db") #Connects to database
    cursor = connection.cursor() #Used to perform operations in database

    cursor.execute(query, (int(userID),))
    results = cursor.fetchall()

    connection.close() #Terminates connection

    return results

def insert_session(date, startTime, endTime, subjectID, remarks, userID):

    record = [date, startTime, endTime, remarks, userID, subjectID]

    connection = sqlite3.connect("study_planner.db") #Connects to database
    cursor = connection.cursor() #Used to perform operations in database

    cursor.execute("INSERT INTO SESSIONS(date, startTime, Endtime, remarks, userID, subjectID) VALUES (?,?,?,?,?,?)", record)

    connection.commit() #Saves changes
    connection.close() #Terminates connection

def delete_session(sessionID, userID):

    record = [sessionID, userID]

    connection = sqlite3.connect("study_planner.db") #Connects to database
    cursor = connection.cursor() #Used to perform operations in database

    #Deleting record
    cursor.execute("DELETE FROM SESSIONS WHERE sessionID=? AND userID=?", record)

    connection.commit() #Saves changes
    connection.close() #Terminates connection

def find_subject(user_id, subject):

    #Finding subjectID for subject
    connection = sqlite3.connect("study_planner.db") #connects to database
    cursor = connection.cursor() #Used to perform operations in database

    #Resolving subject
    cursor.execute("SELECT subjectID FROM SUBJECTS WHERE subjectName=? AND userID=?", (subject, user_id))
    result = cursor.fetchone()

    #Validation
    if result:
        subjectID = result[0]
    else:
        cursor.execute("INSERT INTO SUBJECTS (subjectName, userID) VALUES (?,?)", (subject, user_id))
        subjectID = cursor.lastrowid
    
    connection.commit() #Saves changes
    connection.close() #Terminates connection

    return subjectID

#Main Program

app = Flask(__name__)
app.secret_key = "91102062026Yoga"



#Default web page
@app.route("/")
def home():
    return render_template("index.html")



#Used when user login/signup fails
@app.route("/err")
def errhome():
    return render_template("error_home.html")



#Page for user to enter login information
@app.route("/login")
def loginpage():
    return render_template("login.html")



#Page for user to enter sign up information
@app.route("/signup")
def signuppage():
    return render_template("signup.html")



#Dashboard which contains most recent tasks of user etc.
@app.route("/dashboard")
def dashboard():
    if "userID" not in session:
        return redirect(url_for('loginpage'))
    
    user_id = session["userID"]
    tasks = tasks_display(user_id)
    sessions = sessions_display(user_id)
    return render_template("dashboard.html", user_tasks=tasks, user_sessions=sessions)



@app.route("/add_task")
def submit_task():
    return render_template("task_submission.html")



@app.route("/edit_task")
def amend_task_page():

    if "userID" not in session:
        return redirect(url_for('loginpage'))
    user_id = session["userID"]

    tasks = tasks_display(user_id)
    return render_template("task_amend.html", user_tasks=tasks)



@app.route("/update_task", methods=["GET", "POST"])
def amended_task():
    if "userID" not in session:
        return redirect(url_for('loginpage'))
    user_id = session['userID']

    taskID = int(request.form['taskID'])
    statusID = int(request.form['status'])

    #Validation
    #Connects to db to verify if taskID belongs to user, if not returns error
    connection = sqlite3.connect("study_planner.db") #Connects to database
    cursor = connection.cursor() #Used to perform operations in database

    # Ask SQL if BOTH the taskID and userID match in a single query
    cursor.execute("SELECT 1 FROM TASKS WHERE taskID=? AND userID=?", (taskID, user_id))
    task_exists = cursor.fetchone()

    connection.close() #Terminates connection

    if task_exists:
        update_task_status(taskID, user_id, statusID)
        return redirect(url_for('dashboard'))
    else:
        print("TaskID does not exists for User!")
        tasks = tasks_display(user_id)
        return render_template("task_amend_err.html", user_tasks=tasks)






@app.route("/submit_task", methods=["POST"])
def task_submission():
    if "userID" not in session:
        return redirect(url_for('loginpage'))
    user_id = session['userID']
    
    #Obtaining data from html form
    title = request.form['title']
    description = request.form['description']
    dueDate = request.form['dueDate']
    priority = request.form['priority']
    subject = request.form['subject'].strip().upper()
    categoryID = int(request.form['category'])

    #Finding subjectID for subject
    connection = sqlite3.connect("study_planner.db") #connects to database
    cursor = connection.cursor() #Used to perform operations in database

    #Resolving subject
    cursor.execute("SELECT subjectID FROM SUBJECTS WHERE subjectName=? AND userID=?", (subject, user_id))
    result = cursor.fetchone()

    #Validation
    if result:
        subjectID = result[0]
    else:
        cursor.execute("INSERT INTO SUBJECTS (subjectName, userID) VALUES (?,?)", (subject, user_id))
        subjectID = cursor.lastrowid
    
    connection.commit() #Saves changes
    connection.close() #Terminates connection

    #Inserts new task into database
    insert_task(title, description, dueDate, priority, subjectID, user_id, categoryID)
    return redirect(url_for("dashboard"))

    



@app.route("/delete_task")
def delete_task_page():

    if "userID" not in session:
        return redirect(url_for('loginpage'))
    user_id = session['userID']

    tasks = tasks_display(user_id)
    return render_template("task_delete.html", user_tasks=tasks)





@app.route("/deleted_task", methods=["POST"])
def deleted_task():

    if "userID" not in session:
        return redirect(url_for('loginpage'))
    user_id = session['userID']

    taskID = int(request.form['taskID'])

    delete_task(taskID, user_id)
    return redirect(url_for('dashboard'))
    



    
@app.route("/session_submission")
def session_submission_page():
    if "userID" not in session:
        return redirect(url_for('loginpage'))
    user_id = session['userID']

    sessions = sessions_display(user_id)
    return render_template("session_submission.html", user_sessions=sessions)





@app.route("/submit_session", methods=["POST"])
def session_submission():

    #To prevent user overide
    if "userID" not in session:
        return redirect(url_for('loginpage'))
    user_id = session['userID']

    date = request.form["date"]
    startTime = request.form["startTime"]
    endTime = request.form["endTime"]
    subject = request.form["subject"].strip().upper()
    remarks = request.form["remarks"]

    subject_id = find_subject(user_id, subject)

    #Insert new session into database
    insert_session(date, startTime, endTime, subject_id, remarks, user_id)

    #Returns user to dashboard
    return redirect(url_for('dashboard'))





@app.route("/session_deletion_page")
def session_deletion_page():

    if "userID" not in session:
        return redirect(url_for('loginpage'))
    user_id = session['userID']

    sessions = sessions_display(user_id)
    return render_template("session_deletion.html", user_sessions=sessions)





@app.route("/session_deletion", methods=["POST"])
def session_deletion():

    if "userID" not in session:
        return redirect(url_for('loginpage'))
    user_id = session['userID']

    sessionID = int(request.form['sessionID'])

    delete_session(sessionID, user_id)
    return redirect(url_for('dashboard'))


    


#Used to check validity of login details with USERS table in database
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    print(email, email.strip(), password, password.strip()) #Debugging

    if not email.strip() == "" or password.strip() == "": #Modify to do error checking

        connection = sqlite3.connect("study_planner.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM USERS WHERE email = ? AND password = ?", (email, password))
        recordsSearch = cursor.fetchone()
        connection.close()

        if recordsSearch:
            print("Record found, redirecting to dashboard")
            session["userID"] = recordsSearch[0]
            return redirect(url_for('dashboard'))
        else:
            print("Record not found, redirecting to error_home")
            return redirect(url_for('errhome'))
    else:
        print("Authentication failed!")
        return render_template("error_home.html")





#Used to insert sign up details into USERS table in database
@app.route("/signup", methods=["POST"])
def signup():
    email = request.form.get("email")
    password = request.form.get("password")

    

    if checkEmail(email): #modify to check format and char length!

        package = [email, password]
        
        connection = sqlite3.connect("study_planner.db")
        cursor = connection.cursor()
        try:
            cursor.execute("INSERT INTO USERS(email, password) VALUES (?,?)", package)
        except sqlite3.IntegrityError:
            print("ID Error")
            return redirect(url_for('signuppage'))
        #cursor.execute("INSERT INTO Authentication VALUES (?,?)")
        
        connection.commit()
        connection.close()
        print("Signup Successful, redirecting to home")
        return redirect(url_for('home'))
    else:
        print("Signup Not Successful, redirecting to error_home")
        return redirect(url_for('errhome'))





if __name__ == "__main__":
    if not os.path.isfile("study_planner.db"): #Checks if the study planner database already exists
        initialise_study_planner()
    app.run(host="127.0.0.1", port=5050,debug=True) #Launches the web application


#Excess code dump


#title = request.form['title']
    #description = request.form['description']
    #dueDate = request.form['dueDate']
    #priority = request.form['priority']
    #subject = request.form['subject'].strip().upper()
    #categoryID = int(request.form['category'])
#Finding subjectID for subject
    #connection = sqlite3.connect("study_planner.db") #connects to database
    #cursor = connection.cursor() #Used to perform operations in database

    ##Resolving subject
    #cursor.execute("SELECT subjectID FROM SUBJECTS WHERE subjectName=? AND userID=?", (subject, user_id))
    #result = cursor.fetchone()

    ##Validation
    #if result:
    #    subjectID = result[0]
    #else:
    #    cursor.execute("INSERT INTO SUBJECTS (subjectName, userID) VALUES (?,?)", (subject, user_id))
    #    subjectID = cursor.lastrowid
    #
    #connection.commit() #Saves changes
    #connection.close() #Terminates connection