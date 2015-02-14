from sqlalchemy.sql import select
from sqlalchemy import *
import numpy as np
import scipy as sp
from models import Loan

def get_data():
  meta = MetaData()

  engine = create_engine("postgresql://localhost/pythia_dev", isolation_level="READ UNCOMMITTED")
  sql = text("select * from loans where loan_status != \'Current\'")
  result = engine.connect().execute(sql)
  loans = Table('loans', meta, autoload=True, autoload_with=engine)

  features = []

  count = 0
  for row in result:
    # r = dict(row.items())
    # r['issue_date'] = r['issue_date'].toordinal()
    # r['earliest_credit_line'] = r['earliest_credit_line'].toordinal()
    # r['last_credit_pulled_date'] = r['last_credit_pulled_date'].toordinal()
    # features.append(r.values())
    if count == 1000:
      break
    features.append(row)
    count += 1

  labels = map(lambda vector: 1 if vector[16] == 'Fully Paid' else 0, features)

  def toordinal(vector):
    d15 = vector[15].toordinal() if vector[15] != None else None
    d26 = vector[26].toordinal() if vector[26] != None else None
    d45 = vector[45].toordinal() if vector[45] != None else None
    d45 = vector[47].toordinal() if vector[47] != None else None
    d45 = vector[48].toordinal() if vector[48] != None else None
    return d15, d26, d45

  date_ordinals = map(toordinal, features)
  date_ordinals = np.array(date_ordinals)

  features = np.array(features)
  features = sp.delete(features, 15, 1)
  features = sp.delete(features, 15, 1)
  features = sp.delete(features, 24, 1)
  features = sp.delete(features, 42, 1)
  features = sp.delete(features, 43, 1)
  features = sp.delete(features, 43, 1)
  features = np.concatenate((features, date_ordinals), axis=1)

  return features, labels

