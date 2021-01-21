#######################################################

import hashlib, uuid, mysql.connector, os

SQLpassword = os.environ.get('databasePassword')                     #### Go to Environment Variables on Desktop to change ####

con = mysql.connector.connect(                                       #### Connecting to MySQL ####
  host="127.0.0.1",
  user="root",
  password=f"{SQLpassword}",                                         #### Using the f string allows to pass variables directly through ###
  database='testPython'
)

cur = con.cursor()                                                   #### Creates a Cursor For User - Instead of Arrows ####
cursor.execute("SHOW DATABASES")
db = cur.fetchall()                                                  #### Fetches All The Rows Of A Query Result ####
print(db)                                                            #### It returns all the rows as a list of tuples ####

dropDB = """DROP DATABASE IF EXISTS `testPython`"""                  #### Check To See if Database Exists ####
cur.execute(dropDB)
createDb = """CREATE DATABASE `testPython`"""                        #### To Create Database in mySQL #### 
cur.execute(createDb)
con.commit()                                                         ### Sends a COMMIT statement to the MySQL server, committing the current transaction ####

except:
    print('Sorry, error')
else:
    print('Database created! :) ')
                                                                         #### Creating a Table in the SQL database ####
createTable = """CREATE TABLE IF NOT EXISTS `users` (          
    `username` VARCHAR(50) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `email` VARCHAR(50) NOT NULL,
    PRIMARY KEY (`username`)
);"""

cur.execute(createTable)
con.commit()

except:
    print('Sorry, error')

######## FUNCTIONS FOR USER INPUT ########

def getUserInfo():
    valid = False
    while not valid:
        username = input("Hi! Welcome to the New Database! \n\nEnter a Username: ")
        password = input("Now, please enter a Password: ")
        email = input("Please enter your email address: ")
        if username and password and email:
            valid = True
            return username, password, email 

def getLoginInfo():
        valid = False
        while not valid:
            username = input("Hi! Welcome to the New Database! \n\nEnter a Username: ")
            password = input("Now, please enter a Password: ")
            if username and password:
                valid = True
                print('It worked! Thank you! \n')
                return username, password

def addToDb(username, HashedPassword, email):
    try:
        sql = f"""INSERT INTO `users` VALUES ('{username}', '{HashedPassword}','{email}')"""
        cur.execute(sql)
        con.commit()
    except:
        print('Nothing here, please try again! ')
    else:
        print('Completed, thank you! ')
    

############## FUNCTIONS FOR HASHING PASSWORD ###############

def hashPassword(password):                                         #### Salt is a randomly generated value, that uses UUID4 method ####
    salt = uuid.uuid4().hex                                         #### .hex is used to convert the output of UUID4 into a hexidecimal value ####
    hashedPassword = hashlib.sha256(salt.encode()+password.encode()).hexdigest()+":"+salt
    return hashedPassword

def verifyhash(userpass, storedpass):                                #### Verifies the hash ####
    try:
        password,salt=storedpass.split(":")                          #### Prevents crash in instance of invalid stored hash ####
    except:
        pass
    else:
        found = False
        dbPassword = password
        userGuessPassword = hashlib.sha256(salt.encode()+userpass.encode()).hexdigest()
        if dbPassword == userGuessPassword:
            found = True
            return found

 ################ MAIN FUNCTION FOR PROGRAM ######################           
            
def main():
    x = 0
    while not x:
        try:
            entry = int(input('Hi. Welcome to the database. Choose one of the following: \n1.Register \n2.Login 3.Exit '))
        except:
            print("Please choose either 1, 2 or 3 to begin ")
        else:
            if entry == 1:
                username, password, email = getUserInfo()
                hashedUserpass = hashPassword(password)
                addToDb(username, hashedUserpass, email)
            elif entry == 2:
                loggedIn = False
                username, password = getLoginInfo()
                while not loggedIn:
                        sql = f"""SELECT password FROM users WHERE username='{username}'"""
                        cur.execute(sql)
                        items = cur.fetchone()
                        print(items)
                        if items:
                            dbPassword = items[0]
                            match = verifyhash(password, dbPassword)
                            if match:
                                loggedIn = True
                                print('Success! You are now logged in! ')
                            else:
                                print('Sorry, the password is not recognised ')
                        else:
                            print('Sorry, I could not find you ')

            elif entry == 3:
                print('Ok. Goodbye!')
                x = 1
            else:
                print("Please choose either 1, 2 or 3 to begin ")
    while(1):
        main()


cur.execute(sql)
items = cur.fetchone()
print(items)

hashedUserpass = hashPassword(password)
otherHash = hashPassword('password')                                #### Already stored in database on sign up ####
print(verifyhash('password', otherHash))