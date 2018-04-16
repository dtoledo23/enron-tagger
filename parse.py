#!/usr/bin/python

import MySQLdb
file=open("/Users/lrocg/Desktop/104.", "r")



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
