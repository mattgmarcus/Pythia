#!/usr/bin/env python
import csv
from models import Loan

with open('LoanStats3a.csv', 'r') as csvfile:
  # Skip the first line of notes
  csvfile.next()
  loanStatsReader = csv.DictReader(csvfile)
  for row in loanStatsReader:
    loan = Loan(row)
    print loan

