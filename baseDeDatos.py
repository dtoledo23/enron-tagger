import MySQLdb
#file=open("/Users/toledo/Desktop/maildir/skilling-j/_sent_mail/1.", "r")

# Open database connection
db = MySQLdb.connect(host="enron.c9hkwqr7bv7z.us-east-1.rds.amazonaws.com",port=3306,user="enron_tagger",passwd="CompilersProject",db="enron_tags" )

# prepare a cursor object using cursor() method
cursor = db.cursor()
sql = "SELECT * FROM enron WHERE tag IS NOT NULL"
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      date = row[1]
      body = row[7]
      tag = row[8]

      # Now print fetched result
      print ("Date =" + date + "\nBody = " + body + "\nTag = " + tag)
except:
   print ("Error: unable to fecth data")

# disconnect from server
db.close()

#print("Papaya de celaya")