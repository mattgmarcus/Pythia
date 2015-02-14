from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import *
from sqlalchemy import *
from models import Loan
import os
from random import shuffle

if __name__=="__main__":
  engine = create_engine(os.environ['DATABASE_URL'], isolation_level="READ UNCOMMITTED")
  Session = sessionmaker(bind=engine)
  session = Session()
  all_loans = session.query(Loan).all()
  loan_ids = []
  for loan in all_loans:
      loan_ids.append(loan.id)

  shuffle(loan_ids)

  train_ids = tuple(loan_ids[0:124037])
  test_ids = tuple(loan_ids[124037:177196])

  train_sql = "UPDATE loans SET is_test_data=FALSE WHERE id IN " + str(train_ids)
  test_sql = "UPDATE loans SET is_test_data=FALSE WHERE id IN " + str(test_ids)

  engine.connect().execute(train_sql)
  engine.connect().execute(test_sql)
