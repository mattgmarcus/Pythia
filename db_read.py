from sqlalchemy.sql import select
from sqlalchemy import *
import numpy as np
import scipy as sp
from models import Loan
import random
import os

def loan_status_labels(label):
  if label[0] == "Fully Paid":
    return 1
  else:
    return 0

def get_data(feature_fields=["purpose"], label_fields=["loan_status"], label_mapping=loan_status_labels,
             shuffle=True, testing=True):
  """
  Grabs information from the database and returns them as a multi-dimensional list of features and
  a list of labels

  Parameters:
    feature_fields: list of the columns to include in the feature list
    label_fields: list of the columns to include in the label fields

    @optional
    label_mapping: a function to transform the labels in some way
    shuffle: bool determine whether to shuffle data
    testing: bool determine whether in testing mode

  Returns:
    features:
    labels:

  Fields include "loan_status, loan_amount, funded_amount, funded_amount_investors, term,
  interest_rate, installment, grade, sub_grade, employee_title, employment_length, home_ownership,
  annual_income, is_income_verified, payment_plan, purpose, zip_code, address_state, debt_to_income,
  delinq_2yrs, inq_last_6mths, mths_since_last_delinq, open_credit_lines, public_records, revolving_balance,
  revolving_util, total_accounts, initial_list_status, outstanding_principal, outstanding_principal_investors,
  total_payment, total_payment_investors, total_received_principal, total_received_interest,
  total_received_late_fees, recoveries, collection_recovery_fee, last_payment_amount, collections_12_mths,
  mths_since_last_major_derog, policy_code, mths_since_last_record"

  """

  fields = ','.join(label_fields) + ',' + ','.join(feature_fields)
  meta = MetaData()
  engine = create_engine(os.environ['DATABASE_URL'], isolation_level="READ UNCOMMITTED")
  # TODO need to make the WHERE a parameter?
  sql = text("select %s from loans where loan_status in ('Charged Off', 'Fully Paid')" % fields)
  result = engine.connect().execute(sql)
  loans = Table('loans', meta, autoload=True, autoload_with=engine)

  features = []
  labels = []

  for row in result:
    features.append(row[len(label_fields):])
    labels.append(row[:len(label_fields)])

  labels = map(label_mapping, labels)

  if shuffle:
    combined = zip(features, labels)
    random.shuffle(combined)
    features, labels = zip(*combined)

  if testing:
    half_sample_size = 1000
    num_charged_off = 0
    num_paid = 0

    features_prime = []
    labels_prime = []
    for index, label in enumerate(labels):
      if (label == 1) and (num_paid < half_sample_size):
        features_prime.append(features[index])
        labels_prime.append(label)
        num_paid += 1
      elif (label == 0) and (num_charged_off < half_sample_size):
        features_prime.append(features[index])
        labels_prime.append(label)
        num_charged_off += 1
      elif (num_paid >= half_sample_size) and (num_charged_off >= half_sample_size):
        break
    features = features_prime
    labels = labels_prime

  return features, labels

