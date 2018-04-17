import nltk
import random
from nltk.corpus import movie_reviews

def find_features(document):
    words = set(document)
    features = { }
    for w in word_features:
        features[w] = (w in words)
    return features

documents = [(list(movie_reviews.words(fileid)), category)
            for category in movie_reviews.categories()
            for fileid in movie_reviews.fileids(category)]

print(documents)
random.shuffle(documents)

#all_words_tokenized = word_tokenize(all_words)
all_words = nltk.FreqDist(w.lower() for w in movie_reviews.words())
word_features = list(all_words)[:3000]
featuresets = [(find_features(rev), category) for (rev, category) in documents]

training_set = featuresets[:1900]
testing_set = featuresets[1900:]

classifier = nltk.NaiveBayesClassifier.train(training_set)

print("Classifier accuracy percent: ", (nltk.classify.accuracy(classifier, testing_set)) * 100)

classifier.show_most_informative_features(15)