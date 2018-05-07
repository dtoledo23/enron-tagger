#!/usr/bin/python

import re
import os
import MySQLdb

# Open database connection
db = MySQLdb.connect(host="enron-corpora.c9hkwqr7bv7z.us-east-1.rds.amazonaws.com",port=51153,user="whitegirl",passwd="CompilersProject",db="tags" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# execute SQL query using execute() method.
#cursor.execute("SELECT VERSION()")

def readEmailFromDirectory(path):

    file=open(path,"r")

    content=file.readline()

    while content:
        if content.startswith("Date:") :
            date=content.replace("Date:","")
            print(date)
        elif content.startswith("From:") :
            fr=content.replace("From:","")
            print(fr)
        elif content.startswith("To:") :
            to=content.replace("To:","")
            print(to)
        elif content.startswith("X-From:") :
            Xfr=content.replace("X-From:","")
            print(Xfr)
        elif content.startswith("X-To:") :
            Xto=content.replace("X-To:","")
            print(Xto)
        elif content.startswith("Subject:") :
            subject=content.replace("Subject:","")
            print(subject)
        elif content.startswith("X-FileName:") :
            break
        content=file.readline()

    content=file.read()
    body=content.split("\n\n\n")[0]
    print(body)

    #insert into database
    # query="INSERT INTO enron (Date,FromC,ToC,XFrom,XTo,Subject,Body) Values ('"+date+"','"+fr+"','"+to+"','"+Xfr+"','"+Xto+"','"+subject+"','"+body+"')"

    query="INSERT INTO enron (Date,FromC,ToC,XFrom,XTo,Subject,Body) Values (%s,%s,%s,%s,%s,%s,%s)"
    # print(query)
    cursor.execute(query, (date, fr, to, Xfr, Xto, subject, body))
    db.commit()


myPath="/Users/toledo/Desktop/maildir"
files=[]

for path, dirs, files in os.walk(myPath):
    for filename in files:
        fullpath = os.path.join(path, filename)
        print(fullpath)
        readEmailFromDirectory(fullpath)

#close database
db.close()
