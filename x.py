import numpy as np
from sklearn.feature_extraction import DictVectorizer

x = [[1, 2, 'a'], [2,3, 'b']]
def _sanitize_samples(self, samples):
  samples = [dict(enumerate(sample)) for sample in samples]
  vect = DictVectorizer(sparse=False)
  return vect.fit_transform(samples)
