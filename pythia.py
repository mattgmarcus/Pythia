#!/usr/bin/env python
import argparse
import numpy as np
import scipy as sp
from db_read import *
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import Imputer
from tree import DecisionTreeClassifier
from tree import DecisionTreeRegressor
# from forest import RandomForestClassifier
# from forest import RandomForestRegressor
# from ordinal_logit import OrdinalLogisticRegressor
#import sklearn.tree
import ordinal_logit
# import sys
# sys.path.append("../minirank")
# from minirank import logistic
import pickle

def accept(args):
  feature_fields = [
      "loan_amount",
      "debt_to_income",
      "zip_code",
      "address_state",
      "employment_length",
      # "policy_code"
  ]
  feature_string = ",".join(feature_fields)

  label_fields = []

  rej_sql = text("select %s from rejected_loans" % feature_string)
  rej_features, _ = get_data("rejected", sql=rej_sql, num_samples=args.numsamples, shuffle=True, testing=True)
  rej_labels = [0] * len(rej_features) # label 0 for rejected

  acc_sql = text("select %s from loans" % feature_string)
  acc_features, _ = get_data("loans", sql=acc_sql, num_samples=args.numsamples, shuffle=True, testing=True)
  acc_labels = [1] * len(acc_features) # label 1 for accepted

  # TODO concatenate together and feed to classifier
  features, labels = rej_features + acc_features, rej_labels + acc_labels

  features = [dict(enumerate(feature)) for feature in features]
  vect = DictVectorizer(sparse=False)
  #print features
  features = vect.fit_transform(features)
  #print features.shape

  # score = 0.0
  # oob_score = 0.0

  for i in range(args.numiters):
    train_features, test_features, train_labels, test_labels = \
      train_test_split(features, labels, test_size=.3)

    # classifier = RandomForestClassifier(n_trees=args.numtrees,
    #   n_jobs=8,
    #   max_depth=10000,
    #   use_posterior=args.posterior)

    classifier = RandomForestClassifier(n_estimators=args.numtrees, \
                                        n_jobs=-1, \
                                        verbose=0,
                                        oob_score=True,
                                        max_features=None)

    classifier.fit(train_features, train_labels)

    # score += classifier.score(test_features, test_labels)
    # oob_score += classifier.oob_score_

    # print "Score: " + str(classifier.score(test_features, test_labels))
    # print "OOB Score: " + str(classifier.oob_score)
    print "Score: " + str(classifier.score(test_features, test_labels))
    print "OOB Score: " + str(classifier.oob_score)
    # s = pickle.dump(classifier, open('loan_accept_rfc.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

    # importances = classifier.feature_importances_
    # print zip(vect.get_feature_names(), importances)

  # print "Score: " + str(score / args.numiters)
  # print "OOB Score: " + str(oob_score / args.numiters)

def loan_status_labels(features):
  if features[0] == "Fully Paid":
    return 1
  else:
    return 0

def loan_grade_labels(features):
  grade_dict = {"A": 0, "B": 1, "C": 2,
                "D": 3, "E": 4, "F": 5, "G": 6}

  label = features[0]
  # Examples: A1 = 1, G5 = 35, C2=12
  return grade_dict[label[0]]*5 + int(label[1]) - 1
  # return grade_dict[label[0]]
  # return features[0]

def remove_label(features, last_label_index):
  return features[last_label_index+1:]

def remove_loan_status(features):
  return remove_label(features, 0)

def remove_loan_grade(features):
  return remove_label(features, 0)

def get_R_squared(predicted_labels, test_labels):
  predicted_labels = np.asarray(predicted_labels)
  test_labels = np.asarray(test_labels)

  reg_ssd = ((test_labels - predicted_labels) ** 2).sum()
  res_ssd = ((test_labels - test_labels.mean()) ** 2).sum()

  return 1.0 - (reg_ssd / res_ssd)

def grade(args):
  feature_fields = [
    "loan_amount",
    # "funded_amount",
    # "funded_amount_investors",
    "term",
    # "interest_rate",
    # "installment",
    "employment_length",
    "is_income_verified",
    "home_ownership",
    "annual_income",
    "debt_to_income",
    "delinq_2yrs",
    "open_credit_lines",
    "public_records",
    "revolving_balance",
    "revolving_util",
    "total_accounts",
    "mths_since_last_delinq",
    "mths_since_last_record"
  ]
  label_fields = [
    # "grade",
    "sub_grade",
    # "interest_rate"
  ]

  feature_string = ",".join(label_fields + feature_fields)
  sql = text("select %s from loans" % feature_string)
  features, labels = get_data("loans",
                              sql=sql,
                              num_samples=args.numsamples,
                              label_mapping=loan_grade_labels,
                              features_processing=remove_loan_grade,
                              shuffle=True,
                              testing=True)

  features = [dict(enumerate(feature)) for feature in features]
  vect = DictVectorizer(sparse=False)
  #print features
  features = vect.fit_transform(features)
  #print features.shape

  # imp = Imputer(missing_values='NaN', strategy='mean', axis=0)
  # imp.fit(features)
  # features = imp.transform(features)
  # print features.shape

  # min_label = min(labels)
  # labels = [round(label - min_label) for label in labels]

  score = 0.0

  for i in range(args.numiters):

    train_features, test_features, train_labels, test_labels =\
    train_test_split(features, labels, test_size=.3)

    """
    train_features: size (m, n) matrix of m samples of n features
    train_labels: size (m, 1) vector of the m training samples
    test_features: size (k, n) matrix of k samples of n features
    train_labels: size (k, 1) vector of the k training samples
    """
    if args.test == "grade":
      classifier = RandomForestRegressor(n_estimators=args.numtrees, \
                                          n_jobs=-1, \
                                          verbose=0,
                                          oob_score=True,
                                          max_features=None)

      # classifier = DecisionTreeClassifier(10000)
      # classifier = sklearn.tree.DecisionTreeClassifier()

      # classifier = RandomForestRegressor(n_trees=args.numtrees,
      #   n_jobs=8,
      #   max_depth=10000)

      classifier.fit(train_features, train_labels)
      score += classifier.score(test_features, test_labels)

      # importances = classifier.feature_importances_
      # print zip(vect.get_feature_names(), importances)
      # print vect.feature_names_
      # print vect.vocabulary_
      # print vect.inverse_transform(importances)
      # print importances
      # print importances.shape

      # print "Score: " + str(classifier.score(test_features, test_labels))
      #print classifier.oob_score
    elif args.test == "grade_logit":
      w, theta = logistic.ordinal_logistic_fit(train_features, train_labels)
      pred_labels = logistic.ordinal_logistic_predict(w, theta, test_features)
      # w, theta = ordinal_logit.fit(train_features, train_labels)
      # pred_labels = ordinal_logit.predict(w, theta, test_features)
      print "R squared score " + str(get_R_squared(pred_labels, test_labels))

  # For printing average for scikit runs
  # print "Score: " + str(score / args.numiters)



def quality(args):
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
  feature_string = ",".join(label_fields + feature_fields)
  sql = text("select %s from loans" % feature_string)
  features, labels = get_data("loans",
                              sql=sql,
                              num_samples=args.numsamples,
                              label_mapping=loan_status_labels,
                              features_processing=remove_loan_status,
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

  # score = 0.0
  # oob_score = 0.0

  for i in range(args.numiters):

    train_features, test_features, train_labels, test_labels =\
    train_test_split(features, labels, test_size=.3)

    """
    train_features: size (m, n) matrix of m samples of n features
    train_labels: size (m, 1) vector of the m training samples
    test_features: size (k, n) matrix of k samples of n features
    train_labels: size (k, 1) vector of the k training samples
    """
    classifier = RandomForestClassifier(n_estimators=args.numtrees, \
                                        n_jobs=-1, \
                                        verbose=0,
                                        oob_score=True,
                                        max_features=None)

    # classifier = DecisionTreeClassifier(10000)
    # classifier = sklearn.tree.DecisionTreeClassifier()

    # classifier = RandomForestClassifier(n_trees=args.numtrees,
    #   n_jobs=8,
    #   max_depth=10000)

    classifier.fit(train_features, train_labels)
    # importances = classifier.feature_importances_
    # print zip(vect.get_feature_names(), importances)
    # print vect.feature_names_
    # print vect.vocabulary_
    # print vect.inverse_transform(importances)
    # print importances
    # print importances.shape
    # score += classifier.score(test_features, test_labels)
    # oob_score += classifier.oob_score_
    print "Score: " + str(classifier.score(test_features, test_labels))
    print "OOB Score: " + str(classifier.oob_score_)

  # print "Score: " + str(score / args.numiters)
  # print "OOB Score: " + str(oob_score / args.numiters)

    # s = pickle.dump(classifier, open('data/loan_quality_rfc.pkl', 'wb'), protocol=pickle.HIGHEST_PROTOCOL)

if __name__=="__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("test", help="the test to run, one of: accept, grade, grade_logit, quality",
                      type=str)
  parser.add_argument("-t", "--numtrees", help="number of trees in the forest",
                      type=int, default=16)
  parser.add_argument("-n", "--numiters", help="number of iterations",
                      type=int, default=1)
  parser.add_argument("-m", "--numsamples", help="number of samples to run on",
                      type=int, default=1000)
  parser.add_argument("-p", "--posterior", help="use posterior probability instead of mode",
                      default=True)
  parser.add_argument("-s", "--usesklearn", help="use sklearn")
  args = parser.parse_args()
  #print args.test
  if args.test == "accept":
    accept(args)
  elif args.test == "quality":
    quality(args)
  elif args.test == "grade" or args.test == "grade_logit":
    grade(args)
  else:
    parser.print_help()

