# DataBases Project
# Team 8 - Evangelia Gkagka & Dimitrios Makris

import mysql.connector as mysql
from mysql.connector import errorcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk

class DbConnection():
    def __init__(self, dbname):
        self.dbname = dbname
        self.status = ''''''
        try:
            self.db = mysql.connect(host = 'localhost',
                                    user = 'db_project',
                                    password = 'password',
                                    database = dbname)
            self.cursor = self.db.cursor()

            self.cursor.execute("use discography_company;")
        
        except mysql.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                self.status = '''Connection Refused\nSomething is wrong with\nyour user name or password'''
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                self.status = '''Connection Refused\nDatabase does not exist'''
            else:
                self.status = "Connection Refused\nA connection error has occurred"
        else:
            self.status = '''Connection Established'''
    
    def close(self):
        self.db.commit()
        self.db.close()
            

    def executeQuery(self, query): 
        result = ''''''
        self.error = "notError"
        
        try :
            self.cursor.execute(query)
            rowsAffected = self.cursor.rowcount
            for row in self.cursor.fetchall():
                result += (" | ".join([str(item)for item in row]))
                result += '\n\n'
            self.db.commit()
        except mysql.Error as err:
            self.error = err
            result = ''' An error has occurred, please check your query '''
            rowsAffected = 0
        
        return result, rowsAffected
    
    def executeQuery2(self, query): 
        self.error = "notError"
        
        try :
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            desc = self.cursor.description
            self.db.commit()
        except mysql.Error as err:
            self.error = err
        
        return result, desc
    
    
class ScrollableImage(tk.Frame):
    def __init__(self, master=None, **kw):
        self.image = kw.pop('image', None)
        sw = kw.pop('scrollbarwidth', 10)
        super(ScrollableImage, self).__init__(master=master, **kw)
        self.cnvs = tk.Canvas(self, highlightthickness=0, **kw)
        self.cnvs.create_image(0, 0, anchor='nw', image=self.image)
        self.v_scroll = tk.Scrollbar(self, orient='vertical', width=sw)
        self.h_scroll = tk.Scrollbar(self, orient='horizontal', width=sw)
        self.cnvs.grid(row=0, column=0,  sticky='nsew')
        self.h_scroll.grid(row=1, column=0, sticky='ew')
        self.v_scroll.grid(row=0, column=1, sticky='ns')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.cnvs.config(xscrollcommand=self.h_scroll.set, yscrollcommand=self.v_scroll.set)
        self.v_scroll.config(command=self.cnvs.yview)
        self.h_scroll.config(command=self.cnvs.xview)
        self.cnvs.config(scrollregion=self.cnvs.bbox('all'))
    

class QueryDesc():
    def __init__(self, txt, query, ypos):
        '''
        input: string = text, string = query, rely = ypos
        '''
        
        #Label
        label = tk.Label(prepFrame, text = txt, font = largeFont, bg = 'black', fg = 'white').place(relx = 0.45, rely = ypos, anchor = 'center')

        #Button
        button = tk.Button(prepFrame, height = 2, width = 6, text = "View", bg = 'black', fg = 'white', font = smallFont, command = lambda: showResult(query))
        button.place(relx = 0.85, rely = ypos, anchor = 'center')
        
        

class LabelEntry():
    def __init__(self, text, pos, frame):
        '''
        input: string = text, list = pos = [relx, rely] (of the label), frame = frame
        '''

        self.userInput = tk.StringVar()

        label = tk.Label(frame, text = text + ":", font = middleFont, bg = 'black', fg = 'white').place(relx = pos[0], rely = pos[1], anchor = 'center')
        
        entry = tk.Entry(frame, textvariable = self.userInput, font = smallFont).place(relx = pos[0] + 0.15, rely = pos[1], anchor = 'center')
        

def deleteData():
    flag = 0
    delMemberQuery = '''DELETE FROM member WHERE person_AFM = '''
    
    delAfm = afmInput.get()
    
    delMemberQuery += "'" + delAfm + "'" + ';'
    
    result, rowsAffected = db.executeQuery(delMemberQuery)
    if(db.error != "notError"): flag = 1
    
    if(flag == 0 and rowsAffected != 0):
        deleteSuccess.place(relx = 0.5, rely = 0.8, anchor = 'center')
        deleteSuccessStrV.set("Member deleted successfully")
    
    if(flag == 1 or rowsAffected == 0):
        deleteFailure.place(relx = 0.5, rely = 0.8, anchor = 'center')
        deleteFailureStrV.set("An error has occurred, please check your input")
    
        
        
    afmInput.set('')   
    

def viewMembers():
    raiseFrame(membersFrame)
    
    title = tk.Label(membersFrame, text = "Details of Members", font = titleFont, bg = 'black', fg = 'white').place(relx = 0.5, rely = 0.1, anchor = 'center')
    menuBtn = tk.Button(membersFrame, text = "Menu", font = middleFont, command = back2MenuDelete, bg = 'black', fg = 'white').place(relx = 0.05, rely = 0.05)
    
    backBtn = tk.Button(membersFrame, text = "Back", font = middleFont, command = back2DeleteMember, bg = 'black', fg = 'white').place(relx = 0.12, rely = 0.05)
    
    membersQuery = '''SELECT person_AFM, fname, lname FROM member; '''
    
    membersBox = tk.Text(membersFrame, height = 30, width = 70, font = middleFont, bg = slate, fg = 'white')
    membersBox.place(relx = 0.5, rely = 0.5, anchor = 'center')
    
    result, rowsAffected = db.executeQuery(membersQuery)
    membersBox.insert('end', result)
    membersBox.config(state = 'disable')
    
        
    

def deleteMember():
    raiseFrame(delMemberFrame)
    
    global afmInput
    
    afmInput = tk.StringVar()
    
    title = tk.Label(delMemberFrame, text = "Delete member from database", font = titleFont, bg = 'black', fg = 'white').place(relx = 0.5, rely = 0.1, anchor = 'center')
    menuBtn = tk.Button(delMemberFrame, text = "Menu", font = middleFont, command = back2MenuDelete, bg = 'black', fg = 'white').place(relx = 0.05, rely = 0.05)
    
    delLabel = tk.Label(delMemberFrame, text = "Enter the member's AFM: ", font = largeFont, bg = 'black', fg = 'white').place(relx = 0.5, rely = 0.3, anchor = 'center')
    
    delAfmEntry = tk.Entry(delMemberFrame, textvariable = afmInput, font = smallFont).place(relx = 0.5, rely = 0.4, anchor = 'center')
    delAfmComment = tk.Label(delMemberFrame, text = '6-digit integer', font = commentFont, bg='black', fg='white').place(relx=0.5, rely=0.43, anchor = 'center')
    
    global deleteSuccessStrV, deleteSuccess
    deleteSuccessStrV = tk.StringVar()
    deleteSuccess = tk.Label(delMemberFrame, textvariable = deleteSuccessStrV, font = largeFont, bg = 'black', fg = 'white')

    global deleteFailureStrV, deleteFailure
    deleteFailureStrV = tk.StringVar()
    deleteFailure = tk.Label(delMemberFrame, textvariable = deleteFailureStrV, font = largeFont, bg = 'black', fg = 'white')
    
    delBtn = tk.Button(delMemberFrame, text = "DELETE", font = middleFont, command = deleteData, bg = 'black', fg = 'white').place(relx = 0.5, rely = 0.65, anchor = 'center')
    
    membersBtn = tk.Button(delMemberFrame, text = "See all members and their AFM", font = middleFont, command = viewMembers, bg = 'black', fg = 'white').place(relx = 0.5, rely = 0.5, anchor = 'center')
    
        
def insertData():
    
    flag = 0
    
    memberQuery = '''INSERT INTO member(person_AFM, fname, lname, email, telephone, birth_date, sex, street_number, street, city, zip_code, country, expertise) VALUES ('''
    contractQuery = '''INSERT INTO contract(start_date, end_date, songs_num, albums_num) VALUES ('''
    artistQuery = '''INSERT INTO artist(name, genre) VALUES ('''
    contractIDQuery = '''SELECT MAX(contract_ID) FROM contract;'''
    artistIDQuery = '''SELECT MAX(artist_ID) FROM artist;'''

    afm = afmEntry.userInput.get()
    fname = fnameEntry.userInput.get()
    lname = lnameEntry.userInput.get()
    email = emailEntry.userInput.get()
    tel = telEntry.userInput.get()
    birthdate = birthEntry.userInput.get()
    sex = sexStrV.get()
    address = addressEntry.userInput.get()
    addressNo = addressNoEntry.userInput.get()
    city = cityEntry.userInput.get()
    zipCode = zipCodeEntry.userInput.get()
    country = countryEntry.userInput.get()
    expertise = expertiseEntry.userInput.get()

    for el in (afm, fname, lname, email, tel, birthdate, sex, addressNo, address, city, zipCode, country):
        memberQuery += "'"
        memberQuery += el
        memberQuery += "'"
        memberQuery += ', '
    
    memberQuery += "'"
    memberQuery += expertise
    memberQuery += "'"
    memberQuery += ');'

    startDate = startDateEntry.userInput.get()
    endDate = endDateEntry.userInput.get()
    songsNo = songsNoEntry.userInput.get()
    albumsNo = albumsNoEntry.userInput.get()

    for el in (startDate, endDate, songsNo):
        contractQuery += "'"
        contractQuery += el
        contractQuery += "'"
        contractQuery += ', '

    contractQuery += "'"
    contractQuery += albumsNo
    contractQuery += "'"
    contractQuery += ');'

    artist = artistEntry.userInput.get()
    genre = genreEntry.userInput.get()

    artistQuery +=  "'" + artist + "'" + ', ' + "'" + genre + "'" + ');'
    
    db.executeQuery(memberQuery)
    if(db.error != "notError"): flag = 1
        
    db.executeQuery(contractQuery)
    if(db.error != "notError"): flag = 1
        
    db.executeQuery(artistQuery)
    if(db.error != "notError"): flag = 1
    
    contract_ID, rowsAffected = db.executeQuery(contractIDQuery)
    if(db.error != "notError"): flag = 1
        
    artist_ID, rowsAffected = db.executeQuery(artistIDQuery)
    if(db.error != "notError"): flag = 1
    
    mscQuery = "INSERT INTO Member_Signs_Contract(person_AFM, contract_ID) VALUES ({}, {});".format(afm, contract_ID)
    mhaQuery = "INSERT INTO Member_Has_Artist(person_AFM, artist_ID) VALUES ({}, {});".format(afm, artist_ID)
    
    db.executeQuery(mscQuery)
    if(db.error != "notError"): flag = 1
        
    db.executeQuery(mhaQuery)
    if(db.error != "notError"): flag = 1
    
    if(flag == 0):
        insertSuccess.place(relx = 0.5, rely = 0.8, anchor = 'center')
        insertSuccessStrV.set("Member, contract and artist were entered successfully")
    
    if(flag == 1):
        insertFailure.place(relx = 0.5, rely = 0.8, anchor = 'center')
        insertFailureStrV.set("An error has occurred, please check your inputs")
        
    for ent in (afmEntry, fnameEntry, lnameEntry, emailEntry, telEntry, birthEntry, addressEntry, addressNoEntry, cityEntry, zipCodeEntry, countryEntry, expertiseEntry, startDateEntry, endDateEntry, songsNoEntry, albumsNoEntry, artistEntry, genreEntry):
        ent.userInput.set('')   
    
    sexStrV.set('')    
    

def addMember():

    raiseFrame(memberFrame)
    

    title1 = tk.Label(memberFrame, text = "Insert new member to database", font = titleFont, bg = 'black', fg = 'white').place(relx = 0.5, rely = 0.1, anchor = 'center')
    menuBtn1 = tk.Button(memberFrame, text = "Menu", font = middleFont, command = back2MenuInsert, bg = 'black', fg = 'white').place(relx = 0.05, rely = 0.05)

    title2 = tk.Label(contArtFrame, text = "Insert member's contract details", font = titleFont, bg = 'black', fg = 'white').place(relx = 0.5, rely = 0.1, anchor = 'center')
    menuBtn2 = tk.Button(contArtFrame, text = "Menu", font = middleFont, command = back2MenuInsert, bg = 'black', fg = 'white').place(relx = 0.05, rely = 0.05)
    backBtn = tk.Button(contArtFrame, text = "Back", font = middleFont, command = back2NewMember, bg = 'black', fg = 'white').place(relx = 0.12, rely = 0.05)


    global afmEntry, fnameEntry, lnameEntry, emailEntry, telEntry, birthEntry, addressEntry, addressNoEntry, cityEntry, zipCodeEntry, countryEntry, expertiseEntry, sexStrV, startDateEntry, endDateEntry, songsNoEntry, albumsNoEntry, artistEntry, genreEntry 

    afmEntry = LabelEntry("AFM", [0.2, 0.2], memberFrame)
    afmComment = tk.Label(memberFrame, text = '6-digit integer', font = commentFont, bg='black', fg='white').place(relx=0.35, rely=0.23, anchor = 'center')
    fnameEntry = LabelEntry("First Name", [0.2, 0.3], memberFrame)
    lnameEntry = LabelEntry("Last Name", [0.2, 0.4], memberFrame)
    emailEntry = LabelEntry("Email", [0.2, 0.5], memberFrame)
    telEntry = LabelEntry("Telephone", [0.2, 0.6], memberFrame)
    birthEntry = LabelEntry("Date of Birth", [0.2, 0.7], memberFrame)
    dateComment = tk.Label(memberFrame, text = 'date format: YYYY-MM-DD', font = commentFont, bg='black', fg='white').place(relx=0.35, rely=0.73, anchor = 'center')

    sexLabel = tk.Label(memberFrame, text = "Sex:", font = middleFont, bg = 'black', fg = 'white').place(relx = 0.2, rely = 0.8, anchor='center')
    sexStrV = tk.StringVar()
    sexCombo = ttk.Combobox(memberFrame, width = 18, textvariable = sexStrV, state = "readonly", values = ("Male", "Female") ,font = smallFont)
    sexCombo.place(relx = 0.35, rely = 0.8, anchor = 'center')

    addressEntry = LabelEntry("Address", [0.6, 0.2], memberFrame)
    addressNoEntry = LabelEntry("Address no", [0.6, 0.3], memberFrame)
    cityEntry = LabelEntry("City", [0.6, 0.4], memberFrame)
    zipCodeEntry = LabelEntry("Zip Code", [0.6, 0.5], memberFrame)
    countryEntry = LabelEntry("Country", [0.6, 0.6], memberFrame)
    expertiseEntry = LabelEntry("Expertise", [0.6, 0.7], memberFrame)

    nextBtn = tk.Button(memberFrame, text = "NEXT", width = 10, font = middleFont, command = go2ContArt, bg = 'black', fg = 'white').place(relx = 0.75, rely = 0.8, anchor = 'center')

    startDateEntry = LabelEntry("Start date", [0.2, 0.2], contArtFrame)
    dateComment1 = tk.Label(contArtFrame, text = 'date format: YYYY-MM-DD', font = commentFont, bg='black', fg='white').place(relx=0.35, rely=0.23, anchor = 'center')
    songsNoEntry = LabelEntry("Songs no", [0.2, 0.3], contArtFrame)

    endDateEntry = LabelEntry("End date", [0.6, 0.2], contArtFrame)
    dateComment2 = tk.Label(contArtFrame, text = 'date format: YYYY-MM-DD', font = commentFont, bg='black', fg='white').place(relx=0.75, rely=0.23, anchor = 'center')
    albumsNoEntry = LabelEntry("Albums no", [0.6, 0.3], contArtFrame)

    title3 = tk.Label(contArtFrame, text = "Insert artist's details", font = titleFont, bg = 'black', fg = 'white').place(relx = 0.5, rely = 0.4, anchor = 'center')

    artistEntry = LabelEntry("Artist name", [0.2, 0.5], contArtFrame)
    genreEntry = LabelEntry("Genre", [0.6, 0.5], contArtFrame)
    
    global insertSuccessStrV, insertSuccess
    insertSuccessStrV = tk.StringVar()
    insertSuccess = tk.Label(contArtFrame, textvariable = insertSuccessStrV, font = largeFont, bg = 'black', fg = 'white')

    global insertFailureStrV, insertFailure
    insertFailureStrV = tk.StringVar()
    insertFailure = tk.Label(contArtFrame, textvariable = insertFailureStrV, font = largeFont, bg = 'black', fg = 'white')

    submitBtn = tk.Button(contArtFrame, text = "SUBMIT", width = 10, font = middleFont, bg = 'black', fg = 'white', command = insertData).place(relx = 0.5, rely = 0.65, anchor = 'center')
        
    
def raiseFrame(frame):
    frame.tkraise()
    

def showResultTable(query):
    
    raiseFrame(tableFrame)
    title = tk.Label(tableFrame, text = "Result Table:", font = titleFont, bg = 'black', fg = 'white').place(relx = 0.5, rely = 0.1, anchor='center')
    menuBtn = tk.Button(tableFrame, text = "Menu", font=middleFont, command = back2MenuTable, bg = 'black', fg = 'white').place(relx = 0.05, rely = 0.05)
    
    global trv
    trv = ttk.Treeview(tableFrame, selectmode = 'browse', height = 25)
    trv.place(relx = 0.5, rely = 0.55, anchor='center')
    
    res, desc = db.executeQuery2(query)
    
    columnsNum = len(desc)
    columnsNames = [i[0] for i in desc]
    
    collst = []
    
    for i in range(columnsNum):
        collst.append("{}".format(i))
        
    trv["columns"] = collst
    
    trv['show'] = 'headings'
    
    for i in range(columnsNum):
        trv.column("{}".format(i), width = 70, anchor ='c')
    
    j = 0
    for col in columnsNames:
        trv.heading("{}".format(j), text = "{}".format(col), anchor ='c')
        j += 1

    x = 0
    for i in res:
        trv.insert("", 'end', iid = x, values = i)
        x += 1
    
    
def showResult(query):
    '''
    input: string
    '''
    
    raiseFrame(resultFrame)
    title = tk.Label(resultFrame, text = "Result:", font = titleFont, bg = 'black', fg = 'white').place(relx = 0.5, rely = 0.1, anchor='center')
    menuBtn = tk.Button(resultFrame, text = "Menu", font=middleFont, command = back2Menu, bg = 'black', fg = 'white').place(relx = 0.05, rely = 0.05)
    
    questionBox = tk.Text(resultFrame, height = 6, width = 70, font = middleFont, bg = slate, fg = 'white')
    questionBox.place(relx = 0.5, rely = 0.25, anchor = 'center')
    
    questionBox.insert('end', query)
    questionBox.config(state = 'disable')
    
    resultBox = tk.Text(resultFrame, height = 15, width = 70, font = middleFont, bg = slate, fg = 'white')
    resultBox.place(relx = 0.5, rely = 0.6, anchor = 'center')
    
    result, rowsAffected = db.executeQuery(query)
    resultBox.insert('end', result)
    resultBox.config(state = 'disable') 
    
    global tableBtn
    if (db.error == 'notError'): 
        tableBtn = tk.Button(resultFrame, text = "View in table", font = largeFont, command = lambda: showResultTable(query), bg = 'black', fg = 'white')
        tableBtn.place(relx = 0.5, rely = 0.85, anchor = 'center')
    

def viewErd():
    raiseFrame(erdFrame)

    title = tk.Label(erdFrame, text = "Entity Relationship Diagram", font = titleFont, bg='black', fg='white').place(relx=0.5, rely=0.1, anchor='center')
    menuBtn = tk.Button(erdFrame, text = "Menu", font = middleFont,
                        command = back2Menu, bg = 'black', fg = 'white').place(relx = 0.05, rely = 0.05)

    erd_img = ImageTk.PhotoImage(Image.open("assets/erd.png"))

    erd = ScrollableImage(erdFrame, image = erd_img, scrollbarwidth = 15, width = 800, height = 600)
    erd.pack()

    erd.place(relx = 0.5, rely = 0.55, anchor='center')


def viewRelSchema():
    raiseFrame(schemaFrame)

    title = tk.Label(schemaFrame, text = "Relational Schema", font = titleFont, bg = 'black', fg = 'white').place(relx = 0.5, rely = 0.1, anchor = 'center')
    menuBtn = tk.Button(schemaFrame, text = "Menu", font = middleFont, command = back2Menu, bg = 'black', fg = 'white').place(relx = 0.05, rely = 0.05)

    schema_img = ImageTk.PhotoImage(Image.open("assets/schema.png"))

    schema = ScrollableImage(schemaFrame, image = schema_img, scrollbarwidth = 15, width = 800, height = 600)
    schema.pack()

    schema.place(relx = 0.5, rely = 0.55, anchor = 'center')


def commandLine():
    raiseFrame(cmdFrame)

    title = tk.Label(cmdFrame, text = "Write your query below", font = titleFont, bg = 'black', fg = 'white').place(relx = 0.5, rely = 0.1, anchor='center')
    menuBtn = tk.Button(cmdFrame, text = "Menu", font=middleFont, command = back2Menu, bg = 'black', fg = 'white').place(relx = 0.05, rely = 0.05)
    
    queryBox = tk.Text(cmdFrame, height = 15, width = 70, font = middleFont, bg = slate, fg = 'white')
    queryBox.place(relx = 0.5, rely = 0.45, anchor = 'center')

    submitBtn = tk.Button(cmdFrame, text = "Execute", font = largeFont, bg = 'black', fg = 'white', command = lambda: showResult(queryBox.get(1.0, 'end'))).place(relx = 0.5, rely = 0.8, anchor = 'center')


def preparedQueries():
    raiseFrame(prepFrame)
    
    title = tk.Label(prepFrame, text = "Select a query", font = titleFont, bg = 'black', fg='white').place(relx = 0.5, rely = 0.1, anchor = 'center')
    menuBtn = tk.Button(prepFrame, text = "Menu", font = middleFont, command = back2Menu, bg = 'black', fg='white').place(relx = 0.05, rely = 0.05)
    
    #Queries
    text1 = ''' Update every contract for one month '''
    query1 = ''' UPDATE contract  SET end_date  = DATE_ADD(end_date, INTERVAL 1 MONTH); '''
    QueryDesc(text1, query1, 0.2)
    
    text2 = ''' Number of members in each band (more than 1 member) '''
    query2 = ''' SELECT A.name, COUNT(M.fname) FROM artist AS A, Member_Has_Artist as MA, member as M WHERE A.artist_ID = MA.artist_ID AND MA.person_AFM = M.person_AFM GROUP BY A.artist_ID HAVING COUNT(M.fname) > 1 ORDER BY COUNT(fname) DESC; '''
    QueryDesc(text2, query2, 0.3)
    
    text3 = ''' Songs of each album '''
    query3 = ''' SELECT A.name, S.title FROM album AS A JOIN song AS S ON A.album_ID = S.album_ID ORDER BY A.name; '''
    QueryDesc(text3, query3, 0.4)

    text4 = ''' Albums that will be released in this year '''
    dropIndex = ''' ALTER TABLE album DROP INDEX relDateIndex; '''
    index = ''' CREATE INDEX relDateIndex ON album (released_date); '''
    query4 = ''' SELECT name, released_date FROM album WHERE YEAR(released_date) = YEAR(CURDATE()) ORDER BY released_date; '''
    QueryDesc(text4, query4, 0.5)

    text5 = ''' Collaborators whose contract ends in less than two years from now '''
    query5 = ''' SELECT Col.person_AFM, Col.fname, Col.lname, Con.end_date FROM collaborator AS Col, contract AS Con, Col_Signs_Contract AS ColCon WHERE Col.person_AFM = ColCon.person_AFM AND Con.contract_ID = ColCon.contract_ID AND DATEDIFF(end_date, CURDATE()) <= 730 ORDER BY DATEDIFF(end_date, CURDATE()); '''
    QueryDesc(text5, query5, 0.6)

    text6 = ''' Studio engineers that worked for each album '''
    query6 = ''' SELECT E.fname, E.lname, T.type, S.name FROM studio_engineer AS E, se_type AS T, SE_Has_SEType AS ET, studio AS S, SE_WorksAt_Studio AS ES WHERE E.se_AFM = ET.se_AFM AND T.se_type_ID = ET.se_type_ID  AND S.studio_ID = ES.studio_ID AND E.se_AFM = ES.se_AFM; '''
    QueryDesc(text6, query6, 0.7)
    
    text7 = ''' 10 most expensive studios and the studio engineers who work there '''
    query7 = ''' SELECT S.name, S.price_per_hour, SE.fname, SE.lname FROM studio AS S, studio_engineer AS SE, SE_WorksAt_Studio AS SES WHERE SE.se_AFM = SES.se_AFM AND S.studio_ID = SES.studio_ID ORDER BY price_per_hour DESC LIMIT 10; '''
    QueryDesc(text7, query7, 0.8)

    text8 = ''' All studios with price per hour less than 800$\nthat are not available after October 2023 '''
    query8 = ''' SELECT name, price_per_hour, available_start, available_end FROM studio WHERE price_per_hour < 800 AND MONTH(available_start) = 10  AND  YEAR(available_end) <=  2023; '''
    QueryDesc(text8, query8, 0.9)


def back2MenuInsert():
    raiseFrame(menuFrame)
    insertSuccessStrV.set('')
    insertFailureStrV.set('')
    

def back2MenuDelete():
    raiseFrame(menuFrame)
    deleteSuccessStrV.set('')
    deleteFailureStrV.set('')

    
def back2MenuTable():
    raiseFrame(menuFrame)
    trv.destroy()
    tableBtn.destroy()
    
    
def back2Menu():
    raiseFrame(menuFrame)  

    
def back2NewMember():
    raiseFrame(memberFrame)

def go2ContArt():
    raiseFrame(contArtFrame)
    
def back2DeleteMember():
    raiseFrame(delMemberFrame)
    
    
def createGUI():
    
    title0 = tk.Label(menuFrame, text = "RECORD COMPANY", font = titleFont, bg = 'black', fg='white').place(relx = 0.5, rely = 0.1, anchor = 'center')
    
    choice1 = tk.Button(menuFrame, text = "View ER Diagram", font = middleFont, command = viewErd, bg = 'black', fg='white').place(relx = 0.5, rely = 0.2, anchor = 'center')
    
    choice2 = tk.Button(menuFrame, text = "View Relational Schema", font = middleFont, command = viewRelSchema, bg = 'black', fg='white').place(relx = 0.5, rely = 0.3, anchor = 'center') 
    
    choice3 = tk.Button(menuFrame, text = "Write Query", font = middleFont, command = commandLine, bg = 'black', fg='white').place(relx = 0.5, rely = 0.4, anchor = 'center')
    
    choice4 = tk.Button(menuFrame, text = "Select Function", font = middleFont, command = preparedQueries, bg = 'black', fg='white').place(relx = 0.5, rely = 0.5, anchor = 'center') 
    
    choice5 = tk.Button(menuFrame, text = "Add New Member", font = middleFont, command = addMember, bg = 'black', fg='white').place(relx = 0.5, rely = 0.6, anchor = 'center')
    
    choice6 = tk.Button(menuFrame, text = "Delete Member", font = middleFont, command = deleteMember, bg = 'black', fg='white').place(relx = 0.5, rely = 0.7, anchor = 'center')
    
    statusTitle = tk.Label(menuFrame, text = "Status: ", font = middleFont, bg = 'black', fg = 'white').place(relx = 0.75, rely = 0.8)
    
    team = tk.Label(menuFrame, text = "Team #08\nEvangelia Gkagka\nDimitrios Makris", font = middleFont, bg = 'black', fg = 'white').place(relx = 0.18, rely = 0.84, anchor = 'center')
    
    statusBox = tk.Text(menuFrame, height = 3, width = 25, bg = 'black', fg = 'white', font = smallFont)
    statusBox.place(relx = 0.75, rely = 0.83)
    status = db.status
    statusBox.insert('end', status)
    statusBox.config(highlightthickness = 0, borderwidth=0)
    statusBox.config(state = 'disable') #read_only
    
    raiseFrame(menuFrame)
    root.mainloop()
            

        
        
if __name__ == "__main__":
    
    #Connection with DB
    curDb = 'discography_company'
    db = DbConnection(curDb)

    #Root Window
    root = tk.Tk()
    root.geometry("1024x768")
    root.resizable(0, 0)
    root.title("Discography Company Database")

    #Frames
    menuFrame = tk.Frame(root, width = 1024, height = 768, bg = 'black')
    prepFrame = tk.Frame(root, width = 1024, height = 768, bg = 'black')
    cmdFrame = tk.Frame(root, width = 1024, height = 768, bg = 'black')
    resultFrame = tk.Frame(root, width = 1024, height = 768, bg = 'black')
    erdFrame = tk.Frame(root, width = 1024, height = 768, bg = 'black')
    schemaFrame = tk.Frame(root, width = 1024, height = 768, bg = 'black')
    memberFrame = tk.Frame(root, width = 1024, height = 768, bg = 'black')
    contArtFrame = tk.Frame(root, width = 1024, height = 768, bg = 'black')
    delMemberFrame = tk.Frame(root, width = 1024, height = 768, bg = 'black')
    resultTestFrame = tk.Frame(root, width = 1024, height = 768, bg = 'black')
    membersFrame = tk.Frame(root, width = 1024, height = 768, bg = 'black')
    tableFrame = tk.Frame(root, width = 1024, height = 768, bg = 'black')
    
    for frame in (menuFrame, cmdFrame, prepFrame, resultFrame, erdFrame, schemaFrame, memberFrame, contArtFrame, delMemberFrame, resultTestFrame, membersFrame, tableFrame):
        frame.grid(row=0, column=0)

    menuFrame.pack_propagate(0)
    prepFrame.pack_propagate(0)
    cmdFrame.pack_propagate(0)
    resultFrame.pack_propagate(0)
    erdFrame.pack_propagate(0)
    schemaFrame.pack_propagate(0)
    memberFrame.pack_propagate(0)
    contArtFrame.pack_propagate(0)
    delMemberFrame.pack_propagate(0)
    resultTestFrame.pack_propagate(0)
    membersFrame.pack_propagate(0)
    tableFrame.pack_propagate(0)


    #Fonts
    titleFont = ('Calibri', 20)
    largeFont = ('Calibri', 18)
    middleFont = ('Calibri', 14)
    smallFont = ('Calibri', 12)
    commentFont = ('Calibri', 10)
    
    #Colors
    slate = '#26282A'
    
    #Functions

    #GUI
    createGUI()
    
    #Close Connection with Db
    db.close()