import psycopg2
import nltk
import pickle
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize # or use some other tokenizer

stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

db = psycopg2.connect(host="localhost",
                        port="5432",
                        database="enron_corpora",
                        user="postgres")

def tokensFromEmailBody(body):
    # Tokenize
    word_tokens = word_tokenize(body)

    # Stem
    stemed_sentence = [ps.stem(w) for w in word_tokens]

    # Filter stop words
    filtered_sentence = [w for w in stemed_sentence if not w in stop_words]

    # Filter punctuation
    alpha_sentence = [word.lower() for word in filtered_sentence if word.isalpha()]

    return alpha_sentence

def getMostRepresentativeTokens(token_count=1000):
      positives_count = token_count/2
      negatives_count = token_count/2

      cursor = db.cursor()

      cursor.execute( """
      SELECT word, positive_count, negative_count
      FROM clasification
      ORDER BY positive_count DESC
      LIMIT %s;
      """, [positives_count])
      positives = cursor.fetchall()

      cursor.execute( """
      SELECT word, positive_count, negative_count
      FROM clasification
      ORDER BY negative_count DESC
      LIMIT %s;
      """, [negatives_count])
      negatives = cursor.fetchall()

      return positives + negatives

def getTaggedEmails():
      sql = """
      SELECT body, tag
      FROM email_tags
      WHERE tag IS NOT NULL
      ORDER BY id
      """

      # Execute the SQL command
      cursor = db.cursor()
      cursor.execute(sql)
      # Fetch all the rows in a list of lists.
      return cursor.fetchall()

def find_features(tokens, interesting_words):
      words_in_body = set(tokens)
      features = {}
      for word in interesting_words:
            features[word] = (word in words_in_body)
      return features

def save_classifier(classifier, path='naive_bayes_classifier.picle'):
      f = open(path, 'wb')
      pickle.dump(classifier, f)
      f.close()

# test = searchWithoutCategories()
# print("SQL Test done")


interesting_words = [ word for word, positive_count, negative_count in getMostRepresentativeTokens()]
tagged_emails = getTaggedEmails()

feature_set = []
for body, tag in tagged_emails:
      tokens = tokensFromEmailBody(body)
      features = find_features(tokens, interesting_words)
      feature_set.append((features, tag))


classifier = nltk.NaiveBayesClassifier.train(feature_set)
classifier.show_most_informative_features(15)

save_classifier(classifier)
