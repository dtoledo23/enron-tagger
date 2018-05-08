import psycopg2
import nltk
from nltk.tokenize import word_tokenize # or use some other tokenizer

db = psycopg2.connect(host="10.43.103.33", port="5432",database="enron_corpora", user="postgres")
cursor = db.cursor()

def searchCategories():

      sql = "SELECT body,tag FROM email_tags WHERE tag IS NOT NULL order by id limit 50"
      try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            return cursor.fetchall()

      except:
            print ("Error: unable to fecth data")


#print("Papaya de celaya")

train = searchCategories()
print("SQL Train done")


def searchWithoutCategories():

      sql = "SELECT body, datetime FROM email_tags WHERE tag IS NULL order by id"
      try:
            # Execute the SQL command
            cursor.execute(sql)
            # Fetch all the rows in a list of lists.
            return cursor.fetchall()

                 
      except:
            print ("Error: unable to fecth data")




test = searchWithoutCategories()
print("SQL Test done")


all_words = set(word.lower() for passage in train for word in word_tokenize(passage[0]))
t = [({word: (word in word_tokenize(x[0])) for word in all_words}, x[1]) for x in train]
classifier = nltk.NaiveBayesClassifier.train(t)
print("Train done")
classifier.show_most_informative_features()


def applyClassifier():
      for row in test:
            date = row[1]
            test_sentence = row[0]
            test_sent_features = {word.lower(): (word in word_tokenize(test_sentence.lower())) for word in all_words}
            print(classifier.classify(test_sent_features))


applyClassifier()
print("Papaya")
db.close()