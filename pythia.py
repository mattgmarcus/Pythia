#!/usr/bin/env python
import csv
import os
from models import Loan
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ["APP_SETTINGS"])
db = SQLAlchemy(app)


def read_loans(filename):
  with open(filename, "r") as csvfile:
    # Skip the first line of notes
    csvfile.next()
    loanStatsReader = csv.DictReader(csvfile)
    for row in loanStatsReader:
      # Make sure the row's not empty. This choice of field is arbitrary
      if not row["mths_since_last_delinq"]:
        continue

      row = { k: strip_whitespace(v) for k, v in row.items() }

      loan = Loan(row)

      db.session.add(loan)
      db.session.commit()

def strip_whitespace(val):
  return val.strip()


if __name__=="__main__":
  approved_loan_files = ["LoanStats3a.csv", "LoanStats3b.csv", "LoanStats3c.csv"]
  for filename in approved_loan_files:
    read_loans(filename)
