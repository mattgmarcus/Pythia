#!/usr/bin/env python
import csv

with open('LoanStats3a.csv', 'r') as csvfile:
  # Skip the first line of notes
  csvfile.next()
  loanStatsReader = csv.DictReader(csvfile)
  for row in loanStatsReader:
    print row['id'], row['annual_inc']

