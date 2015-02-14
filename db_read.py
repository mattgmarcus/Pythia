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

  for row in result:
    features.append(row)

  labels = map(lambda vector: 1 if vector[16] == 'Fully Paid' else 0, features)

  features = np.array(features)
  features = sp.delete(features, 16, 1)

  return features, labels
