import sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()


#create teacher table
teacherTblCMD = """CREATE TABLE IF NOT EXISTS
tblTeacher(teacherID INTEGER PRIMARY KEY, firstName TEXT, lastName TEXT, username TEXT, password TEXT)"""

#create class table
classTblCMD = """CREATE TABLE IF NOT EXISTS
tblClass(classID TEXT PRIMARY KEY, teacherID INTEGER, FOREIGN KEY(teacherID) REFERENCES tblTeacher(teacherID))"""

#create student table
studentTblCMD = """CREATE TABLE IF NOT EXISTS
tblStudent(studentID INTEGER PRIMARY KEY, classID TEXT, firstName TEXT, lastName TEXT, username TEXT, password TEXT, totalScore INTEGER, FOREIGN KEY(classID) REFERENCES tblClass(classID))"""






cursor.execute(teacherTblCMD)
print("Created teacher table")

cursor.execute(classTblCMD)
print("Create class table")

cursor.execute(studentTblCMD)
print("Created student table")

#insert into teacher table
cursor.execute("INSERT INTO tblTeacher VALUES(0,'Kazan','Villanueva','villanuevak','password')")
print("inserted test teacher info")

cursor.execute("INSERT INTO tblTeacher VALUES(1,'Maths','Teacher','teacherm','password')")
print("inserted test teacher info")

#insert into class table
cursor.execute("INSERT INTO tblClass VALUES('12C',0)")
print("inserted class info")

cursor.execute("INSERT INTO tblClass VALUES('12D',0)")
print("inserted class info")

#insert into student table
cursor.execute("INSERT INTO tblStudent VALUES(0,'12C','John','Doe','14doej','password',0)") 
print("inserted test student info")

cursor.execute("INSERT INTO tblStudent VALUES(1,'12C','Doe','Jane','14doeja','password',5)") 
print("inserted test student info")

cursor.execute("INSERT INTO tblStudent VALUES(2,'12D','Doe','John','14johnd','password',3)") 
print("inserted test student info")




cursor.close()
connection.commit()
connection.close()


