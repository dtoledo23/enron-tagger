import psycopg2
import nltk
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

def getEmailBatch(limit):
    sql = """
    SELECT id, body,tag
    FROM email_tags
    WHERE tag IS NOT NULL AND processed IS NULL
    ORDER BY id
    LIMIT %s
    """

    cursor = db.cursor()
    # Execute the SQL command
    cursor.execute(sql, [limit])
    # Fetch all the rows in a list of lists.
    result = cursor.fetchall()

    cursor.close()
    return result

def insertWordsIfNotExist(words):
    cursor = db.cursor()

    sql = """
    INSERT INTO clasification(word)
    VALUES (%s)
    ON CONFLICT DO NOTHING;
    """

    for word in words:
        cursor.execute(sql, [word])

    db.commit()
    cursor.close()

def updateTags(words, tag):
    cursor = db.cursor()

    sql = ""

    if tag == "positive":
        sql = """
        UPDATE clasification
        SET positive_count=positive_count+1
        WHERE word=%s;
        """

    elif tag == "negative":
        sql = """
        UPDATE clasification
        SET negative_count=negative_count+1
        WHERE word=%s;
        """

    else:
        print("Tag not supported", tag)
        return

    for word in words:
        cursor.execute(sql, [word])

    db.commit()
    cursor.close()

def markEmailsAsProcessed(ids):
    cursor = db.cursor()

    sql = """
        UPDATE email_tags
        SET processed=True
        WHERE id=%s
        """

    for id in ids:
        cursor.execute(sql, [id])

    db.commit()
    cursor.close()

def processEmailBatch(emails):
    ids = []
    for id, body, tag in emails:
        words = tokensFromEmailBody(body)

        # Create words
        insertWordsIfNotExist(words)

        # Set counter according received tag
        updateTags(words, tag)

        ids.append(id)

    markEmailsAsProcessed(ids)

def main():
    batchSize = 100
    emailCount = 0
    emailLimit = 5000

    while emailCount < emailLimit:
        emails = getEmailBatch(batchSize)
        processEmailBatch(emails)
        emailCount = emailCount + batchSize
        print("Processed emails:", emailCount)

main()