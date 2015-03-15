#!/usr/bin/env python
import csv
import os
from models import Loan
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.TestingConfig")
db = SQLAlchemy(app)


def read_accepted_loans(filename):
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


def read_rejected_loans(filename):
  with open(filename, "r") as csvfile:
    # Skip the first line of notes                                                                                                                                                                          
    csvfile.next()
    loanStatsReader = csv.DictReader(csvfile)
    for row in loanStatsReader:
      # Make sure the row's not empty. This choice of field is arbitrary                                                                                                                                    
      if not row["Employment Length"]:
        continue

      row = { k: strip_whitespace(v) for k, v in row.items() }

      loan = RejectedLoan(row)

      db.session.add(loan)
      db.session.commit()

def strip_whitespace(val):
  return val.strip()


if __name__=="__main__":
    read_accepted_loans("LoanStatsSmall.csv")
    read_rejected_loans("RejectedLoanStatsSmall.csv")
