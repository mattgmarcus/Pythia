from sqlalchemy.sql import select
from sqlalchemy import *
import numpy as np
import scipy as sp
from models import Loan
import random
from random import shuffle

def sort_labels(label):
  if label == "Fully Paid":
    return 1
  else:
    return 0

def get_data():
  # First field of fields has to be loan_status
  # fields = "loan_status, loan_amount, funded_amount, funded_amount_investors, term, interest_rate, installment, grade, sub_grade, employee_title, employment_length, home_ownership, annual_income, is_income_verified, payment_plan, purpose, zip_code, address_state, debt_to_income, delinq_2yrs, inq_last_6mths, mths_since_last_delinq, open_credit_lines, public_records, revolving_balance, revolving_util, total_accounts, initial_list_status, outstanding_principal, outstanding_principal_investors, total_payment, total_payment_investors, total_received_principal, total_received_interest, total_received_late_fees, recoveries, collection_recovery_fee, last_payment_amount, collections_12_mths, mths_since_last_major_derog, policy_code, mths_since_last_record"
  #fields = "loan_status, grade, sub_grade"
  # fields = 'loan_status'
  fields = "loan_status, purpose"
  # fields = "loan_status, funded_amount, total_received_late_fees, inq_last_6mths, delinq_2yrs, mths_since_last_major_derog, is_income_verified, debt_to_income, grade, sub_grade, purpose, employment_length, home_ownership, annual_income, interest_rate, term"

  meta = MetaData()

  engine = create_engine("postgresql://localhost/pythia_dev", isolation_level="READ UNCOMMITTED")
  sql = text("select %s from loans where loan_status in ('Charged Off', 'Fully Paid')" % fields)
  result = engine.connect().execute(sql)
  loans = Table('loans', meta, autoload=True, autoload_with=engine)

  features = []
  loan_statuses = []

  half_sample_size = 1000

  for row in result:
    features.append(row[1:])
    loan_statuses.append(row[0])


  labels = map(sort_labels, loan_statuses)

  shuffled_features = []
  shuffled_labels = []
  index_shuf = range(len(features))
  shuffle(index_shuf)
  for i in index_shuf:
    shuffled_features.append(features[i])
    shuffled_labels.append(labels[i])

  features = []
  labels = []

  num_charged_off = 0
  num_paid = 0
  for index, label in enumerate(shuffled_labels):
    if (label == 1) and (num_paid < half_sample_size):
      features.append(shuffled_features[index])
      labels.append(label)
      num_paid += 1
    elif (label == 0) and (num_charged_off < half_sample_size):
      features.append(shuffled_features[index])
      labels.append(label)
      num_charged_off += 1
    elif (num_paid >= half_sample_size) and (num_charged_off >= half_sample_size):
      break


  return features, labels

