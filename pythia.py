#!/usr/bin/env python
import numpy as np
import scipy as sp
from db_read import get_data
#from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import Imputer
from tree import *
from forest import RandomForestClassifier
import sklearn.tree

if __name__=="__main__":
  feature_fields = [
      #"loan_status",
      "loan_amount",
      "funded_amount",
      "funded_amount_investors",
      "term",
      "interest_rate",
      "installment",
      #"grade",
      #"sub_grade",
      #"employee_title",
      "employment_length",
      "home_ownership",
      "annual_income",
      #"is_income_verified",
      #"payment_plan",
      #"purpose",
      #"zip_code",
      #"address_state",
      "debt_to_income",
      "delinq_2yrs",
      "inq_last_6mths",
      "mths_since_last_delinq",
      "open_credit_lines",
      "public_records",
      "revolving_balance",
      "revolving_util",
      "total_accounts",
      #"initial_list_status",
      #"outstanding_principal",
      #"outstanding_principal_investors",
      #"total_payment",
      #"total_payment_investors",
      #"total_received_principal",
      #"total_received_interest",
      #"total_received_late_fees",
      #"recoveries",
      #"collection_recovery_fee",
      #"last_payment_amount",
      "collections_12_mths",
      "mths_since_last_major_derog",
      #"policy_code",
      "mths_since_last_record"
  ]
  label_fields = [
      "loan_status"
  ]
  features, labels = get_data(feature_fields=feature_fields,
                              label_fields=label_fields,
                              shuffle=True,
                              testing=True)
  #print features, labels

  # features = [dict(r.iteritems()) for r in features]
  # vect = DictVectorizer()
  # vectorized_sparse = vect.fit_transform(features)
  # features = vectorized_sparse.toarray()

  features = [dict(enumerate(feature)) for feature in features]
  vect = DictVectorizer(sparse=False)
  #print features
  features = vect.fit_transform(features)
  #print features.shape

  # imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
  # imp.fit(features)
  # features = imp.transform(features)
  # print features.shape

  train_features, test_features, train_labels, test_labels =\
  train_test_split(features, labels, test_size=.3)

  """
  train_features: size (m, n) matrix of m samples of n features
  train_labels: size (m, 1) vector of the m training samples
  test_features: size (k, n) matrix of k samples of n features
  train_labels: size (k, 1) vector of the k training samples
  """
  # classifier = RandomForestClassifier(n_estimators=1000, \
  #                                     n_jobs=-1, \
  #                                     verbose=3,
  #                                     oob_score=True,
  #                                     max_features=None)

  # classifier = DecisionTreeClassifier(10000)
  # classifier = sklearn.tree.DecisionTreeClassifier()

  classifier = RandomForestClassifier(n_trees=100,
    n_jobs=8,
    max_depth=10000)

  classifier.fit(train_features, train_labels)
  # importances = classifier.feature_importances_
  # print zip(vect.get_feature_names(), importances)
  # print vect.feature_names_
  # print vect.vocabulary_
  # print vect.inverse_transform(importances)
  # print importances
  # print importances.shape

  print classifier.score(test_features, test_labels)
