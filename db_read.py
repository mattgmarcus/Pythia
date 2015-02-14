from sqlalchemy.sql import select
from sqlalchemy import *
import numpy as np
import scipy as sp
from models import Loan

def get_data(table):
	# return Loan.query.filter(Loan.loan_status == 'Current').all()
	sql = text("select * from loans where loan_status != \'Current\'")
	result = c.execute(sql)

	test = []

	for row in result:
		test.append(row)

	return test

engine = create_engine("postgresql://localhost/pythia_dev",
	isolation_level="READ UNCOMMITTED")

c = engine.connect()

meta = MetaData()

loans = Table('loans', meta, autoload=True, autoload_with=engine)

test_data = get_data(loans)
labels = map(lambda vector: 1 if vector[16] == 'Fully Paid' else 0, test_data)

test_array = np.array(test_data)
test_array = sp.delete(test_array, 16, 1)

# print test_array
# print test_array.shape
# print labels