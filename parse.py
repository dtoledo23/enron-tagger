#!/usr/bin/python

import re
import os
import psycopg2
# import MySQLdb

# Open database connection

conn = psycopg2.connect(host="localhost",database="enron_corpora", user="postgres")

# prepare a cursor object using cursor() method
cursor = conn.cursor()

# execute SQL query using execute() method.
#cursor.execute("SELECT VERSION()")

def readEmailFromDirectory(path):

    try:
        file=open(path,"r")

        content=file.readline()

        while content:
            if content.startswith("Date:") :
                date=content.replace("Date:","")
            elif content.startswith("From:") :
                fr=content.replace("From:","")
            elif content.startswith("To:") :
                to=content.replace("To:","")
            elif content.startswith("X-From:") :
                Xfr=content.replace("X-From:","")
            elif content.startswith("X-To:") :
                Xto=content.replace("X-To:","")
            elif content.startswith("Subject:") :
                subject=content.replace("Subject:","")
            elif content.startswith("X-FileName:") :
                break
            content=file.readline()

        content=file.read()
        body=content.split("\n\n\n")[0].strip()

        query="INSERT INTO email_tags (datetime, body) VALUES (to_timestamp(%s, 'DY, DD Mon YYYY HH24:MI:SS'),%s)"
        cursor.execute(query, (date, body))
        conn.commit()
    except:
        print("An error happened with", path)


myPath="/Users/toledo/Desktop/maildir"
handles = [ "lay-k", "skilling-j", "fastow-a", "whalley-l", "whalley-g", "sanders-r", "symes-k", "germany-c", "white-s", "presto-k"]
files=[]

for handle in handles:
    path = myPath + "/" + handle
    print("Processing ", handle)
    for path, dirs, files in os.walk(path):
        for filename in files:
            fullpath = os.path.join(path, filename)
            readEmailFromDirectory(fullpath)

#close database
conn.close()
