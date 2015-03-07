from tree import DecisionTreeClassifier
from tree import DecisionTreeRegressor
from joblib import Parallel, delayed
from collections import Counter
import numpy as np
from util import *
# import sklearn.tree

# Borrowed from scikit because of an annoying bug
def _parallel_helper(obj, methodname, *args, **kwargs):
  return getattr(obj, methodname)(*args, **kwargs)

def bootstrap_build_tree(tree, samples, labels):
  """
  Generate random indices by sampling with replacement and
  then generate random subset from training set using those indices

  Parameters:
  X: Training samples, each with d features; m x d 2D array
  Y: Training labels; 1 x m array

  Return:
  Fitted tree (DecisionTreeClassifier)
  """
  n_samples = samples.shape[0]
  random_indices = np.random.choice(n_samples, n_samples, replace=True)

  tree.fit(samples[random_indices,:], labels[random_indices], sanitize=False, randomize="sqrt")
  # tree.fit(samples[random_indices,:], labels[random_indices])
  tree.indices = random_indices

  print "Finished growing tree"
  return tree

class RandomForest(object):
  def __init__(self, n_trees, n_jobs, max_depth=10000):
    self.n_trees = n_trees
    self.n_jobs = n_jobs
    self.trees = None
    self.oob_score = None
    self.d_features = None
    self.feature_importances = None
    self.max_depth = max_depth

  def fit(self, samples, labels):
    """
    Create forest of trees from training set

    Given training set D
    n_trees = # of trees
    in parallel:
    for i to n_estimators:
      bootstrap_build_tree

    """

    samples = sanitize_samples(samples)
    samples = np.array(samples)
    labels = np.array(labels)

    self.d_features = samples.shape[1]

    # Initialize all trees
    self.trees = []
    for i in range(self.n_trees):
      tree = self.make_tree()
      self.trees.append(tree)

    # Fit trees in parallel
    self.trees = Parallel(n_jobs=self.n_jobs, backend="threading")\
      (delayed(bootstrap_build_tree)(t, samples, labels) for t in self.trees)
      # (delayed(self._parallel_helper)(self, "bootstrap_build_tree", t, samples, labels) for t in self.trees)

    self.get_oob_score(samples, labels)

    return self

  def make_tree(self):
    pass

  def predict(self, samples):
    # Preds is a list where each element is a list of predicted values
    # for each decision tree
    predictions = Parallel(n_jobs=self.n_jobs, backend="threading")\
      (delayed(_parallel_helper)(t, "predict", samples) for t in self.trees)

    # Convert preds into a np array
    predictions = np.array(predictions)
    # num_col = preds_np.shape[1]

    pred_labels = self._predict(predictions)
    # Get voted Y val for each col
    # return np.apply_along_axis(mode, 0, predictions)
    return pred_labels

  def _predict(self, predictions):
    pass

  def get_oob_score(self, samples, labels):
    n_outputs = labels.shape[0]

    predictions = np.zeros((self.n_trees, n_outputs))

    all_sample_indices = np.array(range(samples.shape[0]))
    # oob_set = []
    for i in range(self.n_trees):
      mask = np.ones(len(all_sample_indices), dtype=bool)
      mask[self.trees[i].indices] = False
      left_out_indices = all_sample_indices[mask]
      # oob_set += list(set(left_out_indices) - set(oob_set))
      predictions[i, left_out_indices] = self.trees[i].predict(samples[left_out_indices,:])

    prediction_mask = np.all(np.equal(predictions, 0), axis=0)
    predictions[:,~prediction_mask]

    posteriors = predictions.astype(float).sum(axis=0) / (predictions != 0).sum(axis=0)

    pred_labels = [1 if posterior > .5 else 0 for posterior in posteriors]

    oob_score = 0.0
    for pred, actual in zip(pred_labels, labels):
      oob_score += (1 if (pred - actual != 0) else 0)

    # oob_score = sum(abs(pred_labels - np.array(labels)))

    self.oob_score = 1.0 - (oob_score / n_outputs)

    return self.oob_score


  def score(self, test_samples, test_labels):
    predicted_labels = self.predict(test_samples)

    difference = 0.0
    for pred, actual in zip(predicted_labels, test_labels):
      difference += (1 if (pred - actual != 0) else 0)

    return 1.0 - (difference / len(predicted_labels))


  # TODO: no one got time for this
  # But if we do, this will replace the dictvectorizer stuff
  def feature_relevances(self):
    pass

class RandomForestClassifier(RandomForest):
  def __init__(self, n_trees, n_jobs, max_depth=10000, use_posterior=False):
    super(RandomForestClassifier, self).__init__(n_trees, n_jobs, max_depth)
    self.use_posterior = use_posterior

  def make_tree(self):
    # return sklearn.tree.DecisionTreeClassifier(max_depth=self.max_depth, max_features="sqrt")
    return DecisionTreeClassifier(self.max_depth, use_posterior=self.use_posterior)

  def _predict(self, predictions):
    #TODO: ATTN YONDON: np magic for summing along axis
    posteriors = np.apply_along_axis(sum_posterior, 0, predictions)
    k = self.n_trees / 2
    return np.array([1 if posterior > k else 0 for posterior in posteriors])
