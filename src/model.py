"""
Module containing model fitting code for a web application that implements a
income classification model.
When run as a module, this will load a MySQL dataset, train a random forest model, 
and then pickle the resulting model object to disk.
"""
import etl as etl
import one_hot_encode_pipeline as ONE

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

class MyModel():
    def __init__(self):
        self._classifier = RandomForestClassifier(n_estimators=100)

    def fit(self, X, y):
        """Parameters
        ----------
        X: A numpy array or list, to be used as predictors.
        y: A numpy array or python list of labels, to be used as responses.
        Returns
        -------
        self: The fit model object.
        """
        # Code to fit the model.
        self._classifier.fit(X, y)
        return self
    
    def predict_proba(self, X):
        """Make probability predictions on new data."""
        return self._classifier.predict_proba(X.values)

    def predict(self, X):
        """Return a class on new data."""
        return self._classifier.predict(X.values)

    def score(self, X, y):
        """Return a classification accuracy score on new data."""
        return self._classifier.score(X.values, y)

if __name__ == '__main__':
    location = 'data/public_data.csv'
    df_original = pd.read_csv(location, encoding = "ISO-8859-1")
    df_etl = etl.transform_dataframe(df_original)
    df = etl.split_categories(df_etl, df_etl.category)

    y = df.income.values
    X = df.drop(['income'], axis=1).values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=4612)

    all_categories, one_hot_df = ONE.one_hot_get_dummies_train(X_train, 
                            column_selection=['category_1','category_2','category_3'],
                            column_names=df.columns.drop('income'))

    tfidf_vectorizer = TfidfVectorizer(analyzer='word',
                                    stop_words='english',
                                    token_pattern=r'\b[^\d\W]{3,}\b', #u'(?![0-9]{4,})(?!\d+-\d+)(?!\d+/\d+)(?:^\S*)',
                                    lowercase=True)

    X_train_df = pd.DataFrame(X_train, columns=df.columns.drop('income')).drop(['category_1',
                                                                            'category_2',
                                                                            'category_3'],axis=1)
    X_train_names = X_train_df.description
    tfidf_fit = tfidf_vectorizer.fit_transform(X_train_names) 
    tfidf_df = pd.DataFrame(tfidf_fit.toarray(), columns=tfidf_vectorizer.get_feature_names())
    X_train_hot_tfidf = pd.concat([X_train_df.drop(['description'], axis=1), one_hot_df, tfidf_df], axis=1).values 
    
    model = MyModel()
    model.fit(X_train_hot_tfidf, y_train)
    with open('../data/model.pkl', 'wb') as f:
        # Write the model to a file.
        pickle.dump(model, f)