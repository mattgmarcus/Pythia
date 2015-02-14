#!/usr/bin/env python
import numpy as np
import scipy as sp
from db_read import get_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import Imputer

if __name__=="__main__":
  features, labels = get_data()
  # features = [dict(r.iteritems()) for r in features]
  # vect = DictVectorizer()
  # vectorized_sparse = vect.fit_transform(features)
  # features = vectorized_sparse.toarray()
  
  features = [dict(enumerate(feature)) for feature in features]
  vect = DictVectorizer(sparse=False)
  features = vect.fit_transform(features)

  imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
  imp.fit(features)
  features = imp.transform(features)

  train_features, test_features, train_labels, test_labels =\
  train_test_split(features, labels, test_size=.3)

  """
  train_features: size (m, n) matrix of m samples of n features
  train_labels: size (m, 1) vector of the m training samples
  test_features: size (k, n) matrix of k samples of n features
  train_labels: size (k, 1) vector of the k training samples
  """
  classifier = RandomForestClassifier(n_estimators=50, \
                                      n_jobs=-1, \
                                      verbose=1)
  classifier.fit(train_features, train_labels)
  print "Random forest predicted with ", \
        "{0:.0f}%".format(classifier.score(test_features, test_labels)), \
        "accuracy."
  # print features, labels
