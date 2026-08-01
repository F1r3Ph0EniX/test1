#Task 4.2

#imports
import datetime
import sqlite3

#classes

class Person:

    #Initialising
    def __init__(self, full_name, date_of_birth):
        self.name = full_name
        self.birth_date = date_of_birth

    #Get & Set methods
    def get_name(self):
        return self.name

    def set_name(self, newname):
        self.name = newname

    def get_birth_date(self):
        return self.birth_date

    def set_birth_date(self, newdate):
        self.birth_date = newdate

    def is_adult(self):

        #Obtaining today's year
        today = datetime.date.today()
        today_year = int(str(today)[0:4])
        #print(today_year) #Debugging

        #Obtaining person's birth year
        birth_year = int(str(self.get_birth_date())[0:4])
        #print(birth_year) #Debugging
        
        age = today_year - birth_year

        if age > 18:
            return True
        return False

    def screen_name(self):

        name = self.get_name()
        name = name.strip().replace(" ","")
        
        monthday = self.get_birth_date()[5:].split("-")
        monthday = str(monthday[0] + monthday[1])

        screenName = name + monthday
        #print(screenName) #Debugging

        return screenName

class Staff(Person):

    def __init__(self, full_name, date_of_birth):

        #Call superclass init method
        super().__init__(full_name, date_of_birth)

    def screen_name(self):
        partialScreenName = super().screen_name()
        screenName = partialScreenName + "Staff"

        return screenName

    def is_adult(self):
        #comparator = super().is_adult()

        #if comparator == False:
            #return True
        #return comparator
        return True

class Student(Person):

    def __init__(self, full_name, date_of_birth):
        super().__init__(full_name, date_of_birth)

    def screen_name(self):
        partialScreenName = super().screen_name()
        screenName = partialScreenName + "Student"

        return screenName

    def is_adult(self):
        return False

#Functions & Procedures
def insert_people():

    #Preparing list for database insertion
    people_list = []
    instance_list = []

    with open("people.txt", "r") as file:
        records = file.readlines()
    #file automatically closed

    for record in records:
        
        record = record.strip().split(",")
        fullName = record[0]
        birthDate = record[1]
        identification = record[2]
        #print(identification) #Debugging
        
        if identification == "Person":
            instance = Person(fullName, birthDate)
        elif identification == "Student":
            instance = Student(fullName, birthDate)
        else:
            instance = Staff(fullName, birthDate)

        screenName = instance.screen_name()
        adult = instance.is_adult()
        if adult == True:
            isAdult = 1
        else:
            isAdult = 0
        print(screenName, isAdult)

        people_list.append([fullName, birthDate, screenName, isAdult])
        #instance_list.append(instance)

    print(people_list)
    #print(instance_list)

    #Inserting into database
    connection = sqlite3.connect("school.db") #Initiates connection to database
    cursor = connection.cursor()

    cursor.executemany("INSERT INTO People(FullName,DateOfBirth,ScreenName,IsAdult) VALUES (?,?,?,?)",people_list)

    connection.commit() #Saves changes
    connection.close() #Closes connection
            

#Main Program

#Testing
#man = Person("Jigbon", "2000-06-01")
#woman = Person("Geneva", "2010-09-16")
#print(man.is_adult())
#print(woman.is_adult())
#man.screen_name()

insert_people()
        
