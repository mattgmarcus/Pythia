from sklearn.feature_extraction import DictVectorizer
from collections import Counter

def sanitize_samples(samples):
  samples = [dict(enumerate(sample)) for sample in samples]
  vect = DictVectorizer(sparse=False)
  return vect.fit_transform(samples)

# Assume input col is a col from an np array
def mode(col):
  pred_labels, _ = zip(*col)
  common = Counter(pred_labels)
  return common.most_common(1)[0][0]

def sum_posterior(col):
  _, posteriors = zip(*col)
  return sum(posteriors)
