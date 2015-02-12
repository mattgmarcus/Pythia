#!/usr/bin/env python
import csv
from models import Loan


def read_loans():
  with open('LoanStats3a.csv', 'r') as csvfile:
    # Skip the first line of notes
    csvfile.next()
    loanStatsReader = csv.DictReader(csvfile)
    for row in loanStatsReader:
      print row
      if not row["mths_since_last_delinq"]:
        continue

      row = { k: strip_whitespace(v) for k, v in row.items() }
      print row
      loan = Loan(row)
      print loan

def strip_whitespace(val):
  return val.strip()


if __name__=="__main__":
  read_loans()
