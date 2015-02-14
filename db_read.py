from sqlalchemy.sql import select
from sqlalchemy import *
import numpy as np
import scipy as sp
from models import Loan
import random

def get_data():
  fields = "loan_amount, funded_amount, funded_amount_investors, term, interest_rate, installment, grade, sub_grade, employee_title, employment_length, home_ownership, annual_income, is_income_verified, loan_status, payment_plan, purpose, zip_code, address_state, debt_to_income, delinq_2yrs, inq_last_6mths, mths_since_last_delinq, open_credit_lines, public_records, revolving_balance, revolving_util, total_accounts, initial_list_status, outstanding_principal, outstanding_principal_investors, total_payment, total_payment_investors, total_received_principal, total_received_interest, total_received_late_fees, recoveries, collection_recovery_fee, last_payment_amount, collections_12_mths, mths_since_last_major_derog, policy_code, mths_since_last_record"


  meta = MetaData()

  engine = create_engine("postgresql://localhost/pythia_dev", isolation_level="READ UNCOMMITTED")
  sql = text("select %s from loans where loan_status != \'Current\'" % fields)
  result = engine.connect().execute(sql)
  loans = Table('loans', meta, autoload=True, autoload_with=engine)

  features = []

  for row in result:
    features.append(row)

  features = random.sample(features, 1000)

  labels = map(lambda vector: 1 if vector[16] == 'Fully Paid' else 0, features)

  # def toordinal(vector):
  #   d15 = vector[15].toordinal() if vector[15] != None else None
  #   d26 = vector[26].toordinal() if vector[26] != None else None
  #   d45 = vector[45].toordinal() if vector[45] != None else None
  #   d45 = vector[47].toordinal() if vector[47] != None else None
  #   d45 = vector[48].toordinal() if vector[48] != None else None
  #   return d15, d26, d45

  # date_ordinals = map(toordinal, features)
  # date_ordinals = np.array(date_ordinals)

  # features = np.array(features)
  # features = sp.delete(features, 15, 1)
  # features = sp.delete(features, 15, 1)
  # features = sp.delete(features, 24, 1)
  # features = sp.delete(features, 42, 1)
  # features = sp.delete(features, 43, 1)
  # features = sp.delete(features, 43, 1)
  # features = np.concatenate((features, date_ordinals), axis=1)

  return features, labels

