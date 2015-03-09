from sqlalchemy.sql import select
from sqlalchemy import *
import numpy as np
import scipy as sp
from models import Loan
import random
import os

def get_data(db, feature_fields=None, label_fields=None, sql=None,
             label_mapping=None, features_processing=None,
             shuffle=False, testing=False, num_samples=1000):
  """
  Grabs information from the database and returns them as a multi-dimensional list of features and
  a list of labels

  Parameters:
    feature_fields: list of the columns to include in the feature list
    label_fields: list of the columns to include in the label fields

    @optional
    label_mapping: a function to transform the labels in some way
    shuffle: bool determine whether to shuffle data
    testing: bool determine whether in testing mode

  Returns:
    features: (m, n) multidimensional list of m samples with n features
    labels: (m, 1) list of m labels

  """

  #fields = ','.join(label_fields) + ',' + ','.join(feature_fields)
  meta = MetaData()
  engine = create_engine(os.environ['DATABASE_URL'], isolation_level="READ UNCOMMITTED")
  # TODO need to make the WHERE a parameter?
  #sql = text("select %s from %s where loan_status in ('Charged Off', 'Fully Paid')" % (fields, db))

  result = engine.connect().execute(sql)

  features = []
  labels = []

  for row in result:
    features.append(row)

  if shuffle:
    random.shuffle(features)

  labels = map(label_mapping, features)
  features = map(features_processing, features)

  return features[:num_samples], labels[:num_samples]

