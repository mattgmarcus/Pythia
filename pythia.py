#!/usr/bin/env python
import numpy as np
import scipy as sp
from sklearn.ensemble import RandomForestClassifier

if __name__=="__main__":
  """
  train_features: size (m, n) matrix of m samples of n features
  train_labels: size (m, 1) vector of the m training samples
  test_features: size (k, n) matrix of k samples of n features
  train_labels: size (k, 1) vector of the k training samples
  """
  classifier = RandomForestClassifier(n_estimators=100, \
                                      n_jobs=-1, \
                                      verbose=1)
  classifier.fit(train_features, train_labels)
  print "Random forest predicted with ", \
        "{0:.0f}%".format(classifier(test_features, test_labels)), \
        "accuracy."
