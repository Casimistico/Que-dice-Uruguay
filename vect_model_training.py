"""This module trains the model for sentimient predictions"""
from datetime import datetime
#import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from parameter_search import parameter_search
from confusion_matrix import plot_confusion_matrix
from database_cleaner import clean_for_training

def fit_model():
    df = pd.read_excel('Tweets etiquetados para training.xlsx')
    df = clean_for_training(df)
    df.dropna(axis=0, inplace=True)

    def parameter_optimization():
        """Returns optimal parameters for model, once called"""
        parameter_search(df, "text", "Value")
    X_train, X_test, y_train, y_test = train_test_split(df["text"], df["Value"],
                                                        test_size=0.33,
                                                        random_state=42)
    vect = CountVectorizer(max_df=0.75, ngram_range=(1, 3)).fit(X_train)
    X_train_vectorized = vect.transform(X_train)
    model = SGDClassifier(alpha=1e-06, max_iter=80, penalty='elasticnet', tol=1e-3)
    model.fit(X_train_vectorized, y_train)

    y_pred = model.predict(vect.transform(X_test))
    ## Transfor values series to numpy array
    y_test = y_test.values
    X_test = X_test.values
    plot_confusion_matrix(y_test, y_pred, [-1, 0, 1], normalize=True)

    #Unhash all for saveing the model
    #save_vectorizer = open("tweet_vectorizer.pickle", "wb")
    #pickle.dump(vect, save_vectorizer)
    #save_vectorizer.close()

    #save_classifier = open("tweet_classifier.pickle", "wb")
    #pickle.dump(model, save_classifier)
    #save_classifier.close()

if __name__ == "__name__":
    fit_model()
print("The script takes ", (datetime.now()- START_TIME).total_seconds(), " sec")
