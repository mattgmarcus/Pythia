from sklearn.feature_extraction import DictVectorizer
from collections import Counter

def sanitize_samples(samples):
  samples = [dict(enumerate(sample)) for sample in samples]
  vect = DictVectorizer(sparse=False)
  return vect.fit_transform(samples)

# Assume input col is a col from an np array
def mode(col):
  common = Counter(col)
  return common.most_common(1)[0][0]
