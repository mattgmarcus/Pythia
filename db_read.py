from sqlalchemy.sql import select
from sqlalchemy import *
import numpy as np
import scipy as sp
from models import Loan
import random
from random import shuffle

def sort_labels(vector):
  r = dict(vector.items())
  if r["loan_status"] == "Fully Paid":
    return 1
  else:
    return 0

def get_data():
  fields_with_loan_status = "loan_amount, funded_amount, funded_amount_investors, term, interest_rate, installment, grade, sub_grade, employee_title, employment_length, home_ownership, annual_income, is_income_verified, loan_status, payment_plan, purpose, zip_code, address_state, debt_to_income, delinq_2yrs, inq_last_6mths, mths_since_last_delinq, open_credit_lines, public_records, revolving_balance, revolving_util, total_accounts, initial_list_status, outstanding_principal, outstanding_principal_investors, total_payment, total_payment_investors, total_received_principal, total_received_interest, total_received_late_fees, recoveries, collection_recovery_fee, last_payment_amount, collections_12_mths, mths_since_last_major_derog, policy_code, mths_since_last_record"
  fields = "loan_amount, funded_amount, funded_amount_investors, term, interest_rate, installment, grade, sub_grade, employee_title, employment_length, home_ownership, annual_income, is_income_verified, payment_plan, purpose, zip_code, address_state, debt_to_income, delinq_2yrs, inq_last_6mths, mths_since_last_delinq, open_credit_lines, public_records, revolving_balance, revolving_util, total_accounts, initial_list_status, outstanding_principal, outstanding_principal_investors, total_payment, total_payment_investors, total_received_principal, total_received_interest, total_received_late_fees, recoveries, collection_recovery_fee, last_payment_amount, collections_12_mths, mths_since_last_major_derog, policy_code, mths_since_last_record"
  # fields = "grade, sub_grade"
  # fields_with_loan_status = "grade, sub_grade, loan_status"
  # fields = 'loan_status'
  # fields_with_loan_status = 'loan_status'

  # fields = "purpose"
  # fields_with_loan_status = "purpose, loan_status"

  meta = MetaData()

  engine = create_engine("postgresql://localhost/pythia_dev", isolation_level="READ UNCOMMITTED")
  # sql_with_loan_status = text("select %s from loans where loan_status in ('Charged Off', 'Fully Paid')" % fields_with_loan_status)
  sql_for_charged_off_with_loan_status = text("select %s from loans where loan_status in ('Charged Off')" % fields_with_loan_status)
  sql_for_paid_off_with_loan_status = text("select %s from loans where loan_status in ('Fully Paid')" % fields_with_loan_status)
  sql_for_charged_off = text("select %s from loans where loan_status in ('Charged Off')" % fields)
  sql_for_paid_off = text("select %s from loans where loan_status in ('Fully Paid')" % fields)
  # sql = text("select %s from loans where loan_status in ('Charged Off', 'Fully Paid')" % fields)
  # result_with_loan_status = engine.connect().execute(sql_with_loan_status)
  # result = engine.connect().execute(sql)
  result_charged_with_loan_status = engine.connect().execute(sql_for_charged_off_with_loan_status)
  result_paid_with_loan_status = engine.connect().execute(sql_for_paid_off_with_loan_status)
  result_charged = engine.connect().execute(sql_for_charged_off)
  result_paid = engine.connect().execute(sql_for_paid_off)
  loans = Table('loans', meta, autoload=True, autoload_with=engine)

  features = []
  features_with_loan_status = []

  half_sample_size = 500

  count = 0
  for row in result_charged:
    print row[0]
    i
    if count == half_sample_size:
      break
    features.append(row)
    count += 1

  count = 0
  for row in result_paid:
    if count == half_sample_size:
      break
    features.append(row)
    count += 1

  count = 0
  for row in result_charged_with_loan_status:
    if count == half_sample_size:
      break
    features_with_loan_status.append(row)
    count += 1

  count = 0
  for row in result_paid_with_loan_status:
    if count == half_sample_size:
      break
    features_with_loan_status.append(row)
    count += 1


  # for row in result:
  #   features.append(row)

  # for row2 in result_with_loan_status:
  #   features_with_loan_status.append(row2)

  #features = random.sample(features, 10000)
  # features = features[0:10000]
  # features_with_loan_status = features_with_loan_status[0:10000]

  labels = map(sort_labels, features_with_loan_status)


  f1 = []
  f2 = []
  index_shuf = range(len(features))
  shuffle(index_shuf)
  for i in index_shuf:
    f1.append(features[i])
    f2.append(labels[i])

  features = f1
  labels = f2
  return features, labels

