import pickle

filename = 'ML/misinformation_detector.sav'
features = 'ML/feature.pkl'
model = pickle.load(open(filename, 'rb'))



def check_tweet(tweet):
    
    import re
    from nltk.corpus import stopwords
    from nltk.stem.porter import PorterStemmer
    corpus = []

    tweet = re.sub('[^a-zA-Z]', ' ', tweet)
    tweet = tweet.lower()
    tweet = tweet.split()
    ps = PorterStemmer()
    tweet = [ps.stem(word) for word in tweet if not word in set(stopwords.words('english'))]
    tweet = ' '.join(tweet)
    corpus.append(tweet)
        
    from sklearn.feature_extraction.text import CountVectorizer
    cv = CountVectorizer(vocabulary=pickle.load(open(features, 'rb')))
    X = cv.fit_transform(corpus).toarray()

    y_pred = bool(model.predict(X))

    return y_pred