from tkinter import *
from functions import *
import sqlite3
from random import *
from math import *
import datetime



connection = sqlite3.connect("database.db")
cursor = connection.cursor()

#clear the text file for the question data
def resetGameSession(): 
    with open("CurrentGameSession.txt","w") as file:
        pass

#used for clearing the Tk window to switch screen
def clear():
    for widget in main.winfo_children():
        widget.destroy()

#display login screen
def loginScreen():
    resetGameSession()
    clear()
    WTitle = Label(text="Welcome",font=("Arial",20))
    WTitle.pack(anchor=CENTER)

    loginFrame = Frame(main)
    loginFrame.pack(pady=50)

    tCol = Frame(loginFrame)
    tCol.pack(side=LEFT)

    entCol = Frame(loginFrame)
    entCol.pack(side=RIGHT)

    uEntTitle = Label(tCol,text="Username")
    uEntTitle.pack()

    global userEntry

    userEntry = Entry(entCol)
    userEntry.pack()

    pEntTitle = Label(tCol,text="Password")
    pEntTitle.pack()

    global passEntry

    passEntry = Entry(entCol,show="*")
    passEntry.pack()
    

    subDets = Button(main,text="Sign In",width=20,command=submitDetails)
    subDets.pack()

    main.bind('<Return>',lambda event:submitDetails())

    global errorLabel 
    errorLabel = Label(main,text=" ",fg="red")
    errorLabel.pack()

#function for logging in
def submitDetails():
    userQuery = userEntry.get()
    passQuery = passEntry.get()

    #student username format is year joined + username
    if checkNum(userQuery[0]) == True:
        print("Searching for student")
        cursor.execute("SELECT username FROM tblStudent WHERE username='"+str(userQuery)+"'")
        print("test " + str(cursor.fetchone()))

        cursor.execute("SELECT username FROM tblStudent WHERE username='"+str(userQuery)+"'")
        if cursor.fetchone() != None:
            cursor.execute("SELECT username FROM tblStudent WHERE username='"+str(userQuery)+"'")

            sUser = str(cursor.fetchone()[0])

            cursor.execute("SELECT password FROM tblStudent WHERE username='"+str(sUser)+"'")
            sPass = str(cursor.fetchone()[0])
            
            print("Username: " + sUser)
            print("Password: " + sPass)
            
            with open("CurrentUserData.txt","w") as file:
                file.write("student\n" + sUser)
                file.close()


            

            if userQuery == sUser and passQuery == sPass:
                login = True
                print("Login now True")
                studentMenu()

                
            else:
                print("Password does not match")
                errorLabel["text"] = "Password does not match"

        else:
            print("Username does not exist")
            errorLabel["text"] = "Username does not exist"

    #teacher format is surname + first initial
    elif checkNum(userQuery[0]) == False:
        print("Searching for teacher")
        cursor.execute("SELECT username FROM tblTeacher WHERE username='"+str(userQuery)+"'")
        print("test " + str(cursor.fetchone()))

        cursor.execute("SELECT username FROM tblTeacher WHERE username='"+str(userQuery)+"'")
        if cursor.fetchone() != None:
            cursor.execute("SELECT username FROM tblTeacher WHERE username='"+str(userQuery)+"'")
            tUser = str(cursor.fetchone()[0])
            print(tUser)

            cursor.execute("SELECT password FROM tblTeacher WHERE username='"+tUser+"'")
            tPass = str(cursor.fetchone()[0])
            
            print("Username: " + tUser)
            print("Password: " + tPass)

            with open("CurrentUserData.txt","w") as file:
                file.write("teacher\n" + tUser)
                file.close()


            

            

            if userQuery == tUser and passQuery == tPass:
                login = True
                print("Login now True")
                teacherMenu()
                

                
            else:
                print("Password does not match")
                errorLabel["text"] = "Password does not match"

        else:
            print("Username does not exist")
            errorLabel["text"] = "Username does not exist"


#display teacher menu
def teacherMenu():
    clear()
    topBar = Frame(main,bg="gray")
    topBar.pack(fill="x")
    
    title = Label(topBar,fg="white",bg="gray", text="Teacher Menu",font=("Arial",20))
    title.pack(pady=5)

    menuButtons = Frame(main,bg="gray")
    menuButtons.pack(anchor=CENTER,pady=40)

    viewClassButton = Button(menuButtons,height=2,width=20,text="View Classes",command=viewClassesPage)
    viewClassButton.pack(pady=5)

    leaderButton = Button(menuButtons,height=2,width=20,text="Leaderboard",command=leaderBoardPage)
    leaderButton.pack(pady=5)

    exitButton = Button(menuButtons,height=2,width=20,text="Exit",command=main.destroy)
    exitButton.pack(pady=5)

    
#display student menu
def studentMenu():
    clear()
    topBar = Frame(main,bg="gray")
    topBar.pack(fill="x")
    
    title = Label(topBar,fg="white",bg="gray", text="Student Menu",font=("Arial",20))
    title.pack(pady=5)

    menuButtons = Frame(main,bg="gray")
    menuButtons.pack(anchor=CENTER,pady=40)

    startButton = Button(menuButtons,height=2,width=20,text="Start",command=selectGameDiff)
    startButton.pack(pady=5)

    leaderButton = Button(menuButtons,height=2,width=20,text="Leaderboard",command=leaderBoardPage)
    leaderButton.pack(pady=5)

    exitButton = Button(menuButtons,height=2,width=20,text="Exit",command=closeAndSave)
    exitButton.pack(pady=5)

#saves all changes made to the data base and closes the program
def closeAndSave(): 
    cursor.close()
    connection.commit()
    connection.close()
    main.destroy()

#display teacher classes page
def viewClassesPage():
    clear()
    topBar = Frame(main,bg="gray")
    topBar.pack(fill=X)

    returnMenu = Button(topBar,text="Return to menu",command=returnToMenu,height=2,width=15)
    returnMenu.pack(side=LEFT,padx=5)

    title = Label(topBar,bg="grey", text="Classes",font=("Arial",20))
    title.pack(side=LEFT,padx=190,pady=10)

    menuFrame = Frame(main,bg="gray")
    menuFrame.pack(pady=10)

    boxFrame = Frame(menuFrame,bg="gray")
    boxFrame.pack(pady=20)

    global classBox
    classBox = Listbox(boxFrame,highlightbackground="black",highlightthickness=1)
    classBox.pack(side=LEFT)

    classBox.bind('<<ListboxSelect>>',showSelectedClass)
    
    global classContainer
    classContainer = Frame(boxFrame,width=80,bg="blue",height=40,highlightbackground="black",highlightthickness=1)
    classContainer.pack_propagate(0)
    classContainer.pack(side=LEFT,padx=5)

    Label(classContainer,text="").pack(fill=X,side=TOP)
    Label(classContainer,text="").pack(fill=X,side=BOTTOM)

    Button(menuFrame,text="Manage Class",command=manageClassCMD).pack(fill=X,pady=5)
    

    global manageErrorLbl
    manageErrorLbl = Label(menuFrame,text="")
    manageErrorLbl.pack()

    


    info = []
    with open("CurrentUserData.txt","r") as file:
        data = file.read()
        print(data)
        info.append(data.strip().split())
        info = info[0]

    tUsername = info[1]

    print(tUsername)

    


    cursor.execute("SELECT teacherID FROM tblTeacher WHERE username='"+str(tUsername)+"'")
    tID = cursor.fetchone()[0]
    print(tID)

    cursor.execute("SELECT classID FROM tblClass WHERE teacherID="+str(tID))
    classesTemp = cursor.fetchall()
    print("Class list: "+str(classesTemp))

    classes = []
    for i in range(len(classesTemp)):
        classes.append(classesTemp[i][0])

    print(classes)

    for i in range(len(classes)):
        classBox.insert(END,classes[i])


    pass

#works with listBox in function above to display number of students in selected class
def showSelectedClass(event):
    
    classID = str(classBox.get(ANCHOR))
    print(classID)

    for child in classContainer.winfo_children():
        child.destroy()

    cursor.execute("SELECT username FROM tblStudent WHERE classID='"+str(classBox.get(ANCHOR))+"'")
    studentsTemp = cursor.fetchall()
    print(studentsTemp)

    
    students = []
    for i in range(len(studentsTemp)):
        students.append(studentsTemp[i][0])

    print(students)


    Label(classContainer,text=classID).pack(fill=X,side=TOP)

    Label(classContainer,text="Students: " +str(len(students))).pack(fill=X,side=BOTTOM)

# work with function above and function below to save the currently selected class into current user data and 
# display the manage class page to show the students in the class
def manageClassCMD():
    classID = str(classBox.get(ANCHOR))
    print(classID)
    

    if classID == '':
        manageErrorLbl["text"] = "Select class"
        manageErrorLbl["fg"] = "red"
    else:
        with open("CurrentGameSession.txt","w") as file:
            file.write(classID)


        manageClassPage()

#display class of students page
def manageClassPage():
    clear()

    with open("CurrentGameSession.txt","r") as file:
        setTitle = file.read()
    
    print("Class: "+str(setTitle))


    topBar = Frame(main,bg="gray")
    topBar.pack(fill=X)

    returnMenu = Button(topBar,text="Manage Class",command=viewClassesPage,height=2,width=15)
    returnMenu.pack(side=LEFT,padx=5)

    title = Label(topBar,bg="grey", text="Classes",font=("Arial",20))
    title.pack(side=LEFT,padx=190,pady=10)

    classContainer = Frame(main,bg="blue")
    classContainer.pack(fill=BOTH,padx=10,pady=10,expand=TRUE)

    Label(classContainer,text=str(setTitle),width=20).pack(anchor="nw",padx=5,pady=5)

    setBoxContainer  = Frame(classContainer)
    setBoxContainer.pack(side=LEFT)

    global setBox
    setBox = Listbox(setBoxContainer,highlightbackground="black",highlightthickness=1)
    setBox.pack(side=LEFT,padx=10)

    setBox.bind('<<ListboxSelect>>', studentInfoDisplay)

    sb = Scrollbar(setBoxContainer,orient=VERTICAL)
    sb.pack(side=LEFT,fill=Y)

    setBox.configure(yscrollcommand=sb.set)
    sb.config(command=setBox.yview)



    cursor.execute("SELECT username FROM tblStudent WHERE classID ='"+str(setTitle)+"'")
    classSetTemp = cursor.fetchall()
    print(classSetTemp)
    
    
    #classSet = []
    for i in range(len(classSetTemp)):
        #classSet.append(classSetTemp[i][0])
        setBox.insert(END,classSetTemp[i][0])

    #print(classSet)
    global profileContainer
    profileContainer = Frame(classContainer,bg="white",width=160)
    profileContainer.pack(fill=Y,ipady=20,pady=10,padx=10,side=RIGHT,expand=False)

    #Label(profileContainer,text="Name",font=("Arial",20),width=20).pack(fill=X)

    Button(setBoxContainer,text="Add new user",command=enrollStudent).pack()


# creates a new row in the database and appends to the listBox  
def enrollStudent():

    with open("CurrentGameSession.txt","r") as file:
        setTitle = file.read()
    
    print("Class: "+str(setTitle))

    cursor.execute("SELECT studentID FROM tblStudent")
    sIDlist = cursor.fetchall()

    print(sIDlist)

    sIDlist = sorted(sIDlist,reverse=False, key=lambda x:x[0])
    print(sIDlist)

    lrgID = sIDlist[-1][0] +1
    print(lrgID)

    now = str(datetime.datetime.now().year)
    yr = str(now[2])+str(now[3])
    print(yr)

    newUsername = str(yr) + "surnamef" + str(lrgID)
    print(newUsername)

    cursor.execute("INSERT INTO tblStudent VALUES('"+str(lrgID)+"','"+str(setTitle)+"','FirstName','Surname','"+newUsername+"','password',0)") 
    print("inserted test student info")

    setBox.insert(END,newUsername)

    connection.commit()
    pass






#update the student info container to display information of the selected student
def studentInfoDisplay(event):
    for widget in profileContainer.winfo_children():
        widget.destroy()

    studentSelect = str(setBox.get(ANCHOR))
    print(studentSelect)
    

    cursor.execute("SELECT firstName, lastName FROM tblStudent WHERE username='"+str(studentSelect+"'"))
    fullName = cursor.fetchall()
    fullName = str(fullName[0][0])+ " " + str(fullName[0][1])

    print(fullName)

    profileData = """
    StudentID: 
    """

    Label(profileContainer,text=fullName,font=("Arial",15),width=20).pack(fill=X)

    global infoFrame
    infoFrame = Frame(profileContainer,bg="gray")
    infoFrame.pack()

    profileInfoSet = ["studentID","classID","firstName","lastName","username","password","totalScore"]
    
    studentData = []

    for i in range(len(profileInfoSet)):
        cursor.execute("SELECT "+profileInfoSet[i]+" FROM tblStudent WHERE username='"+studentSelect+"'")
        studentData.append(cursor.fetchone()[0])

    print(studentData)

    for i in range(len(studentData)):
        if profileInfoSet[i] != "studentID":
            entryText = StringVar()
            Label(infoFrame,text=profileInfoSet[i],width=15,highlightthickness=2,highlightbackground="black").grid(row=i,column=0)
            Entry(infoFrame,text=entryText,width=15,highlightthickness=2,highlightbackground="black").grid(row=i,column=1)
            entryText.set(studentData[i])

        else:
            Label(infoFrame,text=profileInfoSet[i],width=15,highlightthickness=2,highlightbackground="black").grid(row=i,column=0)
            Label(infoFrame,text=studentData[i],width=15,highlightthickness=2,highlightbackground="black").grid(row=i,column=1)

            global selectSID

            selectSID = studentData[i]
            print("studentID: "+str(selectSID))

    buttonHolder = Frame(profileContainer)
    buttonHolder.pack(side=BOTTOM)

    Button(buttonHolder,text="Remove student",command=removeStudent).pack(side=LEFT,expand=TRUE)
    Button(buttonHolder,text="Confirm changes",command=confirmChanges).pack(side=RIGHT,expand=TRUE)


    pass

#remove currently selected student from database and listBox
def removeStudent():
    studentSelect = str(setBox.get(ANCHOR))
    print(studentSelect)

    cursor.execute("DELETE FROM tblStudent WHERE username='"+studentSelect+"'")

    connection.commit()

    setBox.delete(ANCHOR)

    for item in profileContainer.winfo_children():
        item.destroy()


#confirm updated change made to student info
def confirmChanges():
    studentData = []

    profileInfoSet = ["classID","firstName","lastName","username","password","totalScore"]


    for widget in infoFrame.winfo_children():
        print(widget.winfo_class())
        
        if widget.winfo_class() == "Entry":
            studentData.append(widget.get())

    print(studentData)

    for i in range(len(studentData)):
        print(profileInfoSet[i])
        print(studentData[i])

        if profileInfoSet[i] != "username":
            cursor.execute("UPDATE tblStudent SET "+str(profileInfoSet[i])+" = '" + str(studentData[i])+"' WHERE studentID="+str(selectSID))
            print("updated "+ str(profileInfoSet[i]) + " with " + str(studentData[i]))

        else:
            if checkNum(str(studentData[i])[0]) == True:
                cursor.execute("UPDATE tblStudent SET "+str(profileInfoSet[i])+" = '" + str(studentData[i])+"' WHERE studentID="+str(selectSID))
                print("updated "+ str(profileInfoSet[i]) + " with " + str(studentData[i]))
            else:
                #create suitable student username
                #default student username format: (YEAR JOINED) + SURNAME + ID
                print("unsuitable username for student, recreating new username ")
                now = str(datetime.datetime.now().year)
                yr = str(now[2])+str(now[3])
                print(yr)

                newUsername = str(yr) + str(studentData[i])
                cursor.execute("UPDATE tblStudent SET "+str(profileInfoSet[i])+" = '" + str(newUsername)+"' WHERE studentID="+str(selectSID))
                print("updated "+ str(profileInfoSet[i]) + " with " + str(newUsername))

    
    connection.commit()


            
#display leaderboard page
def leaderBoardPage():
    clear()

    topBar = Frame(main,bg="gray")
    topBar.pack(fill=X)

    returnMenu = Button(topBar,text="Return to menu",command=returnToMenu,height=2,width=15)
    returnMenu.pack(side=LEFT,padx=5)

    title = Label(topBar,bg="grey", text="Leaderboard",font=("Arial",20))
    title.pack(side=LEFT,padx=190,pady=10)

    cursor.execute("SELECT username, totalScore FROM tblStudent")
    listOfUserScore = cursor.fetchall()

    print(listOfUserScore)

    listOfUserScore = sorted(listOfUserScore,reverse=True, key=lambda x:x[1])
    print(listOfUserScore)

    sbFrame = Frame(main,bg="gray")
    sbFrame.pack(pady=10)

    if len(listOfUserScore) < 5:
        for i in range(len(listOfUserScore)):
            Label(sbFrame,text=str(listOfUserScore[i][0])+" Score: "+str(listOfUserScore[i][1]),font=("Arial",12),borderwidth=2,relief="solid",width=20,height=2).grid(pady=3,row=i,column=0)
    elif len(listOfUserScore) >= 5:
        for i in range(5):
            Label(sbFrame,text=str(listOfUserScore[i][0])+" Score: "+str(listOfUserScore[i][1]),font=("Arial",12),borderwidth=2,relief="solid",width=20,height=2).grid(pady=3,row=i,column=0)

#opens CurrentUserData to check if current user is student or teacher and return to respected menu
def returnToMenu():
    info = []
    with open("CurrentUserData.txt","r") as file:
        data = file.read()
        print(data)
        info.append(data.strip().split())

        info = info[0]

        print(info)

    if info[0] == "student":
        studentMenu()
    elif info[0] == "teacher":
        teacherMenu()

#display select difficulty screen
def selectGameDiff():
    clear()
    topBar = Frame(main,bg="gray")
    topBar.pack(fill=X)

    returnMenu = Button(topBar,text="Return to menu",command=returnToMenu,height=2,width=15)
    returnMenu.pack(side=LEFT,padx=5)

    title = Label(topBar,bg="grey", text="Select Difficulty",font=("Arial",20))
    title.pack(side=LEFT,padx=120,pady=5)

    diffButtons = Frame(main)
    diffButtons.pack(anchor=CENTER,pady=50)

    Button(diffButtons,text="Easy",height=2,width=20,command=lambda diff=0:selectDiffAlg(diff)).pack()
    Button(diffButtons,text="Normal",height=2,width=20,command=lambda diff=1:selectDiffAlg(diff)).pack()
    Button(diffButtons,text="Hard",height=2,width=20,command=lambda diff=2:selectDiffAlg(diff)).pack()

#create base screen for game screens and nextQ functions
def createGameScreen():
    open("CurrentGameSession.txt", "w").close()
    topBar = Frame(main,bg="gray")
    topBar.pack(fill=X)

    returnMenu = Button(topBar,text="Return to menu",command=returnToMenu,height=2,width=15)
    returnMenu.pack(side=LEFT,padx=5)

    global nextQButton

    nextQButton = Button(topBar,text="Next Question",command=nextQ) 
    nextQButton.pack(side=RIGHT,padx=5)

    global Qcontainer
    
    Qcontainer = Frame(main,bg="white")
    Qcontainer.pack(side="top",fill="both",expand=True)

    global score
    score = 0

    global scoreLbl
    scoreLbl = Label(topBar,text="Your score: "+str(score))
    scoreLbl.pack(anchor=CENTER)

    
#used for making next question screen and incrementing question number
def nextQ():
    global questionCounter
    if difficulty == "easy":
        if questionCounter < 10:
            questionCounter = questionCounter + 1
            if questionCounter == 10:
                nextQButton["text"] = "Finish"
            clearGameScreen()
            easyScreen()
        elif questionCounter == 10:
            endScreen()
    elif difficulty == "normal":
        if questionCounter < 10:
            questionCounter = questionCounter + 1
            if questionCounter == 10:
                nextQButton["text"] = "Finish"
            clearGameScreen()
            normalScreen()
        elif questionCounter == 10:
            endScreen()

    elif difficulty == "hard":
        if questionCounter < 10:
            questionCounter = questionCounter + 1
            if questionCounter == 10:
                nextQButton["text"] = "Finish"
            clearGameScreen()
            hardScreen()
        elif questionCounter == 10:
            endScreen()
    
#used to reset all counters to original and display respected difficulty game screen
def selectDiffAlg(diff):
    global difficulty 
    global questionCounter
    global prevQ
    if diff == 0:
        print("Easy")
        difficulty = "easy"
        questionCounter = 1
        prevQ = 0
        clear()
        createGameScreen()
        easyScreen()

        

    elif diff == 1:
        print("Normal")
        difficulty = "normal"
        questionCounter = 1
        prevQ = 0
        clear()
        createGameScreen()
        normalScreen()

    elif diff == 2:
        print("Hard")
        difficulty = "hard"
        questionCounter = 1
        prevQ = 0
        clear()
        createGameScreen()
        hardScreen()

#clear question container frame
def clearGameScreen():
    for widget in Qcontainer.winfo_children():
        widget.destroy()



#compare user answer with question answer shown in text file
def questionCheck():
    global prevQ
    global score

    if difficulty == "easy":
        ans = answerEnt.get()


        data = []
        with open("CurrentGameSession.txt","r") as file:
            for line in file:
                data.append(line.strip().split())



        print(data)

        if data[questionCounter-1][-1] == ans:
            print("correct")
            correctLbl["text"] = "Correct"
            correctLbl["fg"] = "green"

            
            print(score)
            

            if prevQ != questionCounter:
                prevQ = questionCounter

                score += 1
                scoreLbl["text"] = "Your score: "+str(score)
            

        else:
            print("incorrect")
            correctLbl["text"] = "Incorrect"
            correctLbl["fg"] = "red"

    elif difficulty == "normal":
        if fromRest == False:
            ans = answerEnt.get()
            data = []
            with open("CurrentGameSession.txt","r") as file:
                for line in file:
                    data.append(line.strip().split())

            print(data)

            if data[questionCounter-1][-1] == ans:
                print("correct")
                correctLbl["text"] = "Correct"
                correctLbl["fg"] = "green"

                

                print(score)
                

                if prevQ != questionCounter:
                    prevQ = questionCounter

                    score += 1
                    scoreLbl["text"] = "Your score: "+str(score)
            
            else:
                print("incorrect")
                correctLbl["text"] = "Incorrect"
                correctLbl["fg"] = "red"
        
        else:
            ans = answerEnt.get()
            data = []
            with open("CurrentGameSession.txt","r") as file:
                for line in file:
                    data.append(line.strip().split())

            print(data)

            if data[questionCounter-1][-1] == ans:
                print("correct")
                correctLbl["text"] = "Correct"
                correctLbl["fg"] = "green"

                

                print(score)
                

                if prevQ != questionCounter:
                    prevQ = questionCounter

                    score += 1
                    scoreLbl["text"] = "Your score: "+str(score)
            
            else:
                print("incorrect")
                correctLbl["text"] = "Incorrect"
                correctLbl["fg"] = "red"

    elif difficulty == "hard":
        ans = answerEnt.get()
        data = []
        with open("CurrentGameSession.txt","r") as file:
            for line in file:
                data.append(line.strip().split())

        print(data)

        if data[questionCounter-1][-1] == ans:
            print("correct")
            correctLbl["text"] = "Correct"
            correctLbl["fg"] = "green"

            

            print(score)
            

            if prevQ != questionCounter:
                prevQ = questionCounter

                score += 1
                scoreLbl["text"] = "Your score: "+str(score)
        
        else:
            print("incorrect")
            correctLbl["text"] = "Incorrect"
            correctLbl["fg"] = "red"
            
    
    pass

#create easy game screen question + graph
def easyScreen():
    print(questionCounter)
    #create question

    questionSide = Frame(Qcontainer,bg="grey")
    questionSide.pack(side="left",padx=30)


    questionTxt = Label(questionSide,text=" ",justify="left")
    questionTxt.pack()

    entryHolder = Frame(questionSide)
    entryHolder.pack(side="bottom",padx=30)

    global answerEnt
    answerEnt = Entry(entryHolder)
    answerEnt.pack()

    Button(entryHolder,text="Submit Answer",command=questionCheck).pack(side="bottom")

    global correctLbl
    correctLbl = Label(entryHolder,text=" ")
    correctLbl.pack(side="bottom")


    pad = 30
    size = 300
    rad=2


    graphCanvas = Canvas(Qcontainer,width=300,height=300,bg="gray")
    graphCanvas.pack(side="right",padx=30)

    graphCanvas.create_line(pad,pad,pad,size-pad)
    graphCanvas.create_line(pad,size-pad,size-pad,size-pad)

    acceler = choice([True,False])
    obj = choice(["car","particle"])

    if acceler == True:

        fromRest = choice([True,False])
        
        if fromRest == True:
            u = 0
        else:
            u = round(uniform(0.5,35),1)
            
        print("U: " + str(u))

        v = round(uniform(35,70),1)
        print("V: " + str(v))

        t = randint(3,15)
        print("T: " + str(t))


        if fromRest == True:
            questionSent = str(questionCounter)+". A " + obj + " accelerates from rest to " + str(v) + "m/s² in " + str(t) + " seconds.\nCalculate the acceleration."
            questionTxt["text"] = questionSent
            print("updated label")
        else:
            questionSent = str(questionCounter)+". A " + obj + " accelerates from " + str(u) + "m/s² to " + str(v) + "m/s² in " + str(t) + " seconds.\nCalculate the acceleration."
            questionTxt["text"] = questionSent
            print("updated label")

    
    else:
        u = round(uniform(35,70),1) 
        print("U: " + str(u))

        v = round(uniform(0,35),1)
        print("V: " + str(v))

        t = randint(3,15)
        print("T: " + str(t))
        
        questionSent = str(questionCounter)+". A " + obj + " deccelerates from " + str(u) + "m/s² to " + str(v) + "m/s² in " + str(t) + " seconds.\nCalculate the acceleration."
        questionTxt["text"] = questionSent
        print("updated label")

    a = findA(u,v,t)

    print("A: " + str(a))

    with open("CurrentGameSession.txt","a") as file:
        data = str(questionCounter) + str(u)+", "+str(v)+", "+str(t)+", "+str(a)+"\n"
        file.write(data)

    



    val = [u,v]

    uVel = val[0]
    vVel = val[1]


    #plot u
    getYU = ((uVel/70)*(size-pad-pad))
    print(str(getYU)+ " pixels")
    
    Ux1 = pad-rad
    Uy1 = size-pad-getYU-rad

    Ux2 = pad+rad
    Uy2 = size-pad-getYU+rad

    graphCanvas.create_oval(Ux1,Uy1,Ux2,Uy2,fill="black")
    print("plotted at: "+ str(Ux1)+", "+str(Uy1)+" and " +str(Ux2)+", "+str(Uy2))

    #plot v

    getYV = ((vVel/70)*(size-pad-pad))

    Vx1 = size-pad-rad
    Vy1 = size-pad-getYV-rad

    Vx2 = size-pad+rad
    Vy2 = size-pad-getYV+rad

    graphCanvas.create_oval(Vx1,Vy1,Vx2,Vy2,fill="black")
    print("plotted at: "+ str(Vx1)+", "+str(Vy1)+" and " +str(Vx2)+", "+str(Vy2))

    #create line

    Ux = pad
    Uy = size-pad-getYU

    Vx = size-pad
    Vy = size-pad-getYV

    graphCanvas.create_line(Ux,Uy,Vx,Vy,width=1)

    graphCanvas.create_polygon(size-pad,size-pad,pad,size-pad,Ux,Uy,Vx,Vy,fill="#348ceb",outline="black")

    #create labels

    Label(graphCanvas,text=uVel,bg="gray").place(x=(pad/15),y=Uy)
    Label(graphCanvas,text=vVel,bg="gray").place(x=(pad/15),y=Vy)
    Label(graphCanvas,text=t,bg="gray").place(x=(size-pad),y=(size-pad)+5)

#create normal game screen question + graph
def normalScreen():
    global fromRest

    print(questionCounter)
    #create question

    questionSide = Frame(Qcontainer,bg="grey")
    questionSide.pack(side="left",padx=30)


    questionTxt = Label(questionSide,text=" ",justify="left")
    questionTxt.pack()

    entryHolder = Frame(questionSide)
    entryHolder.pack(side="bottom",padx=30)

    global answerEnt
    answerEnt = Entry(entryHolder)
    answerEnt.pack()

    Button(entryHolder,text="Submit Answer",command=questionCheck).pack(side="bottom")

    global correctLbl
    correctLbl = Label(entryHolder,text=" ")
    correctLbl.pack(side="bottom")

    pad = 30
    size = 300
    rad=2

    graphCanvas = Canvas(Qcontainer,width=300,height=300,bg="gray")
    graphCanvas.pack(side="right",padx=30)

    graphCanvas.create_line(pad,pad,pad,size-pad)
    graphCanvas.create_line(pad,size-pad,size-pad,size-pad)

    fromRest = choice([True,False])

    if fromRest == True:
        print("fromRest = "+str(fromRest))
        startingVel = 0
        accelVel = randint(3,10)
        accelTime = randint(2,5)
        maintainVelTime = randint(6,8)
        endTime = randint(15,20)

        print("endtime: " +str(endTime))
        print("vel before decel: "+str(accelTime+maintainVelTime))

        originy = size-pad
        getYU = ((accelVel/20)*(size-pad-pad))
        Ux = pad
        Uy = originy - getYU

        getX1 = pad+((accelTime/20)*(size-pad-pad))
        yval = ((accelVel/10)*(size-pad-pad))
        getY1 = (size-yval)
        print(str(getY1)+" pixels")


        getX2 = pad+(((accelTime+maintainVelTime)/20)*(size-pad-pad))

        getX3 = pad+((endTime/20)*(size-pad-pad))

        #create shaded area

        graphCanvas.create_polygon(pad,originy,getX3,originy,getX2,getY1,getX1,getY1,fill="#348ceb")

        #plot points on graph

        graphCanvas.create_oval(pad-rad,originy-rad,pad+rad,originy+rad,fill="black")

        graphCanvas.create_oval(getX1-rad,getY1-rad,getX1+rad,getY1+rad,fill="black")

        graphCanvas.create_oval(getX2-rad,getY1-rad,getX2+rad,getY1+rad,fill="black")

        graphCanvas.create_oval(getX3-rad,originy-rad,getX3+rad,originy+rad,fill="black")

        #create lines

        graphCanvas.create_line(pad,originy,getX1,getY1,getX2,getY1,getX3,originy,fill="black")

        graphCanvas.create_line(getX1,getY1,getX1,originy,dash=(2,1))
        graphCanvas.create_line(getX2,getY1,getX2,originy,dash=(2,1))

        Label(graphCanvas,text=endTime,bg="gray").place(x=(getX3-6),y=((size-pad)+5))
        Label(graphCanvas,text=accelTime,bg="gray").place(x=(getX1-6),y=((size-pad)+5))
        Label(graphCanvas,text=str(accelTime+maintainVelTime),bg="gray").place(x=(getX2-6),y=((size-pad)+5))
        Label(graphCanvas,text=accelVel,bg="gray").place(x=(pad/4),y=getY1-5)

        #update question info

        questionSent = str(questionCounter)+". A cyclist starts from rest and constantly accelerates until they\n reach " + str(accelVel) + "m/s² for " + str(accelTime) + " seconds. The cyclist then stays at this speed\n for " + str(maintainVelTime) + " seconds until they start to decelerate and come to rest\nat " + str(endTime) +" seconds. \nCalculate the displacement from the starting point."
        questionTxt["text"] = questionSent
        print("updated label")

        s = findS(maintainVelTime,endTime,accelVel,True)

        data = []
        with open("CurrentGameSession.txt","a") as file:
            data = str(questionCounter) + str(maintainVelTime)+", "+str(endTime)+", "+str(s)+"\n"
            file.write(data)







        





    else:
        print("fromRest = "+str(fromRest))
        u = randint(3,10)
        print(u)

        maintainVelTime = randint(4,8)
        print(str(maintainVelTime) + " seconds")

        endTime = randint(9,15)
        print("Rest at: "+str(endTime))


        originy = size-pad
        Ux = pad
        getYU = ((u/12)*(size-pad-pad))
        Uy = originy - getYU

        print(str(Ux)+ " pixels")

        print(str(Uy)+ " pixels")

        getTx = ((endTime/15)*(size-pad-pad))+pad

        getU2 = ((maintainVelTime/15)*(size-pad-pad))+pad

        #create shaded area

        graphCanvas.create_polygon(pad,originy,getTx,originy,getU2,Uy,Ux,Uy,fill="#348ceb",outline="black")

        graphCanvas.create_oval(Ux-rad,Uy-rad,Ux+rad,Uy+rad,fill="black")

        #create second velocity point

        

        graphCanvas.create_oval(getU2-rad,Uy-rad,getU2+rad,Uy+rad,fill="black")


        

        graphCanvas.create_oval(getTx-rad,originy-rad,getTx+rad,originy+rad,fill="black")

        #create lines

        graphCanvas.create_line(Ux,Uy,getU2,Uy,getTx,originy,width=1)

        graphCanvas.create_line(getU2,Uy,getU2,originy,dash=(2,1))

        #plot labels

        Label(graphCanvas,text=u,bg="gray").place(x=(pad/4),y=Uy-10)
        Label(graphCanvas,text=maintainVelTime,bg="gray").place(x=(getU2-6),y=((size-pad)+5))
        Label(graphCanvas,text=endTime,bg="gray").place(x=(getTx-6),y=((size-pad)+5))

        #update question info

        questionSent = str(questionCounter)+". A cyclist travels at " + str(u) + "m/s² for " + str(maintainVelTime) + " seconds. The cyclist then\ndecelerates uniformly at a constant rate, stopping after " + str(endTime-maintainVelTime) + " seconds. \nCalculate the displacement from the starting point."
        questionTxt["text"] = questionSent
        print("updated label")

        s = findS(maintainVelTime,endTime,u,False)

        data = []
        with open("CurrentGameSession.txt","a") as file:
            data = str(questionCounter) + str(maintainVelTime)+", "+str(endTime)+", "+str(u)+", "+str(s)+"\n"
            file.write(data)

#create hard game screen question + graph
def hardScreen():

    print(questionCounter)
    #create question

    questionSide = Frame(Qcontainer,bg="grey")
    questionSide.pack(side="left",padx=30)


    questionTxt = Label(questionSide,text=" ",justify="left")
    questionTxt.pack()

    entryHolder = Frame(questionSide)
    entryHolder.pack(side="bottom",padx=30)

    global answerEnt
    answerEnt = Entry(entryHolder)
    answerEnt.pack()

    Button(entryHolder,text="Submit Answer",command=questionCheck).pack(side="bottom")

    global correctLbl
    correctLbl = Label(entryHolder,text=" ")
    correctLbl.pack(side="bottom")

    pad = 40
    size = 300
    arcRad=30
    rad = 6

    graphCanvas = Canvas(Qcontainer,width=300,height=300,bg="gray")
    graphCanvas.pack(side="right",padx=30)
    graphCanvas.create_line(pad,size-pad,size-pad,size-pad)

    #create values

    midpointX = size/2
    yPoint = ((size-pad)-((0.75)*(size-pad-pad)))

    fromHeight = choice([True,False])
    
    if fromHeight == False:

        #create some lines

        graphCanvas.create_line(midpointX-arcRad,size-pad,midpointX-arcRad,size/2,arrow=LAST)
        graphCanvas.create_line(midpointX-arcRad,size/2,midpointX-arcRad,yPoint)

        graphCanvas.create_line(midpointX+arcRad,yPoint,midpointX+arcRad,(size/2)+10,arrow=LAST)
        graphCanvas.create_line(midpointX+arcRad,(size/2)+10,midpointX+arcRad,size-pad)

        #graphCanvas.create_line(midpointX-arcRad,size-pad,midpointX-arcRad,yPoint,midpointX,yPoint-arcRad,midpointX+arcRad,yPoint,midpointX+arcRad,size-pad,smooth=1)
        graphCanvas.create_line(midpointX-arcRad,yPoint,midpointX,yPoint-arcRad,midpointX+arcRad,yPoint,smooth=1)
        #graphCanvas.create_line(midpointX-arcRad,yPoint,midpointX-(arcRad/2),yPoint-((yPoint-arcRad)/2),midpointX,yPoint-arcRad,arrow=LAST,width=2 ,smooth=1)
        ##raphCanvas.create_line(midpointX+arcRad,yPoint,midpointX+(arcRad/2),yPoint-((yPoint-arcRad)/2),midpointX,yPoint-arcRad,smooth=1)
        #graphCanvas.create_arc(midpointX-arcRad,yPoint,midpointX+rad,yPoint,fill="black")

        #create arrows
        graphCanvas.create_line(pad+pad,size*0.55,pad+pad,(size*0.45),arrow=LAST)
        graphCanvas.create_line(pad+pad,(size*0.55)+10,pad+pad,(size*0.45)+10,arrow=LAST)

        graphCanvas.create_oval(midpointX-arcRad-rad,size-pad-rad-rad,midpointX-arcRad+rad,size-pad,fill="black")
        graphCanvas.create_oval(midpointX+arcRad-rad,size-pad-rad-rad,midpointX+arcRad+rad,size-pad,fill="black")
        graphCanvas.create_oval(midpointX,yPoint-arcRad,midpointX,yPoint-arcRad,fill="black")

        Label(graphCanvas,text="g m/s²",bg="gray").place(x=(pad/2),y=(size*0.5))

        u = round(uniform(20,25),1)
        print(u)

        g = 9.8
        s = 0

        disc = ((u**2) - (4*(4.9)*s))

        pos1 = (-u + sqrt(disc)) / (-9.8)
        pos1 = round(pos1,1)


        pos2 = (-u - sqrt(disc)) / (-9.8)
        pos2 = round(pos2,1)

        print(pos1)
        print(pos2)

        questionSent = str(questionCounter)+". A particle is projected vertically upwards with speed "+str(u)+"m/s.\nCalculate the total time of projection. "
        questionTxt["text"] = questionSent
        print("updated label")

        if pos1 > 0:
            t = pos1
        elif pos2 > 0:
            t = pos2

        with open("CurrentGameSession.txt","a") as file:
            data = str(questionCounter) + str(u)+", "+str(t)+"\n"
            file.write(data)

    elif fromHeight == True:
        graphCanvas.create_line(midpointX-arcRad,size-pad-50,midpointX-arcRad,size/2,arrow=LAST)
        graphCanvas.create_line(midpointX-arcRad,size/2,midpointX-arcRad,yPoint)

        graphCanvas.create_line(midpointX+arcRad,yPoint,midpointX+arcRad,(size/2)+10,arrow=LAST)
        graphCanvas.create_line(midpointX+arcRad,(size/2)+10,midpointX+arcRad,size-pad)

        
        graphCanvas.create_line(midpointX-arcRad,yPoint,midpointX,yPoint-arcRad,midpointX+arcRad,yPoint,smooth=1)
        

        #create arrows
        graphCanvas.create_line(pad+pad,size*0.55,pad+pad,(size*0.45),arrow=LAST)
        graphCanvas.create_line(pad+pad,(size*0.55)+10,pad+pad,(size*0.45)+10,arrow=LAST)

        graphCanvas.create_oval(midpointX-arcRad-rad,size-pad-rad-rad-50,midpointX-arcRad+rad,size-pad-50,fill="black")
        graphCanvas.create_oval(midpointX+arcRad-rad,size-pad-rad-rad,midpointX+arcRad+rad,size-pad,fill="black")
        graphCanvas.create_oval(midpointX,yPoint-arcRad,midpointX,yPoint-arcRad,fill="black")

        graphCanvas.create_rectangle(midpointX-arcRad,size-pad-50,midpointX-arcRad-50,size-pad,fill="#525252")

        Label(graphCanvas,text="g m/s²",bg="gray").place(x=(pad/2),y=(size*0.5))

        u = round(uniform(20,25),1)
        print("Inital velocity: "+str(u))

        g = 9.8
        s = (-randint(2,12))
        print("Displacement: "+str(-s))

        disc = ((u**2) - (4*(4.9)*(s)))

        pos1 = (-u + sqrt(disc)) / (-9.8)
        pos1 = round(pos1,1)


        pos2 = (-u - sqrt(disc)) / (-9.8)
        pos2 = round(pos2,1)

        print(pos1)
        print(pos2)

        questionSent = str(questionCounter)+". A particle is projected vertically upwards from a point "+str(-s)+"m\nabove the ground with speed "+str(u)+"m/s.\nCalculate the total time of projection. "
        questionTxt["text"] = questionSent
        print("updated label")

        if pos1 > 0:
            t = pos1
        elif pos2 > 0:
            t = pos2

        with open("CurrentGameSession.txt","a") as file:
            data = str(questionCounter) + str(u)+", "+str(t)+"\n"
            file.write(data)

#value question values and update student's total score
def returnAndReset():
    global score
    global questionCounter
    clear()
    

    data = []
    with open("CurrentUserData.txt","r") as file:
        data.append(file.read().split())

    print(data[0][1])

    username = data[0][1]
    print(username)


    cursor.execute("SELECT totalScore FROM tblStudent WHERE username='"+username+"'")
    scoreData = int(cursor.fetchone()[0])
    print(scoreData)


    scoreData += score


    print(scoreData)


    cursor.execute("UPDATE tblStudent SET totalScore ="+str(scoreData)+" WHERE username='"+str(username)+"'")
    print("updated totalScore")


    cursor.execute("SELECT totalScore FROM tblStudent WHERE username='"+username+"'")
    print(cursor.fetchone())

    connection.commit()

    returnToMenu()
    score=0
    questionCounter=0


#display end game screen
def endScreen():
    clear()
    Label(main,text="End",font=('Arial',20)).pack()
    Label(main,text="Your score: "+str(score),font=('Arial',20)).pack(pady=50)
    Button(main,text="Return to menu",command=returnAndReset).pack()
    pass








main = Tk()
#main.geometry("1280x720")
main.geometry("780x360")
main.resizable(False,False)
main.title("Login")



loginScreen()


main.mainloop()

