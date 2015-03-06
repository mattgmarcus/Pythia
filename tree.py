import numpy as np
import scipy as sp
from collections import Counter
from operator import itemgetter
from util import *
import math

"""
Psuedocode for growing decision tree

node_split(): given set of features determine which feature to split on by minimizing the
gini index in the child nodes and provides the best feature test

Parameters:
samples: training samples
features: features for each training sample
default: a default tree

fit(samples, features, default):
if samples is empty: return default
elif all samples have same class: return class
elif features is empty: return majority vote
else
  feature_test = node_split()
  tree <- root node of new tree using feature_test
  for each value Vi of feature_test:
    sub_samples <- elements of samples with Vi
    subtree <- fit(sub_samples, features - feature_test, MODE(samples) aka majority vote)
    tree.add_branch with label Vi and subtree

  return tree

"""

class Node():
  def __init__(self, splitter, left_child, right_child):
    self.splitter = splitter #(feature_index, threshold)
    self.left_child = left_child
    self.right_child = right_child

  def __str__(self):
    print self.left_child
    print self.right_child
    return str(self.splitter)


class Leaf(Node):
  def __init__(self, posterior_label, labels):
    counts = Counter(labels)
    most_common_label = counts.most_common(1)[0][0]
    self.value = most_common_label
    self.posterior = float(counts[posterior_label]) / len(labels)

  def __str__(self):
    return self.value


class DecisionTreeClassifier():
  """Decision Tree using CART method"""
  def __init__(self, max_depth):
    self.classes = None
    self.n_classes = None
    self.d_features = None
    self.feature_relevances = None
    self.class_weights = None

    self.root_node = None
    self.max_depth = max_depth

    self.indices = None

  def fit(self, samples, labels, sample_weight=None, sanitize=True, randomize=None):
    """
    Build decision tree using the training data

    Parameters:
      X: m x d matrix where each row vector represents a feature vector.
      m training samples and each have d features

      Y: m x 1 vector where each scalar value represents the correct value for
      the corresponding training sample

    Return:
      self (DecisionTreeClassifier)
    """

    # TODO: we'll have to figure out a way to take advantage of column indexing here.
    # May have to convert back to nparray as passed in later
    if sanitize:
      samples = sanitize_samples(samples)
      samples = np.array(samples)

    self.d_features = samples.shape[1]
    self.classes = np.unique(labels)
    self.n_classes = self.classes.shape[0]

    self.root_node = self.root_node or self._fit(samples, labels, randomize)



  # def _sanitize_samples(self, samples):
    # TODO: Finish. Deal with issue where arrays with mixed types have all values
    # as strings
    # columns_to_delete = []
    # for index, feature in enumerate(samples[0]):
    #   if type(feature) is str:
    #     columns_to_delete.append(index)
    #     samples = self._vectorize_string(samples, index)

    # for col in columns_to_delete.reverse():
    #   samples = np.delete(samples, col, 1)

  # Function to take categorical feature and convert to binary values in features
  # def _vectorize_string(self, samples, column_num):
  #   feature_values = list(set(samples[:,column_num]))
  #   index = { key: val for val, key in enumerate(feature_values) }

  #   vectors = []
  #   for sample in samples:
  #     vector = [0] * len(index)
  #     vector[index[sample[column_num]]] = 1
  #     vectors.append(vector)

  #   # samples = np.delete(samples, column_num, 1)
  #   samples = np.append(samples, np.array(vectors), 1)
  #   return samples


  # function (feature_vector -> {true, false})
  def split_compare(self, sample, (feature_index, threshold)):
    return sample[feature_index] < threshold

  def _fit(self, samples, labels, randomize, current_depth=1, posterior_label=1):
    # Base cases
    # No samples/labels
    if len(labels) == 0:
      return None

    # all labels are same
    #    return label same
    elif (len(set(labels))) == 1:
      return Leaf(posterior_label, labels)

    # current_depth >= max_depth || len(samples) < 5
    #   return leaf node, where value=mode(current labels)
    elif (current_depth >= self.max_depth) or (len(samples) < 10): #TODO: Change min # samples
      return Leaf(posterior_label, labels)

    # Recursive case
    else:
      gini_scores = {}
      while len(gini_scores) == 0:
        if randomize == "sqrt":
          d = self.d_features
          num_features = math.floor(math.sqrt(d))
          feature_indices = np.random.choice(d, num_features, replace=False)
        else:
          feature_indices = range(self.d_features)

        for feature_index in feature_indices:
          for threshold in set(samples[:,feature_index]):
            splitter = (feature_index, threshold)
            num_samples = float(len(samples))

            pass_index, fail_index = self._split(samples, splitter)

            if (len(pass_index) > 0) and (len(fail_index) > 0):
              gini_scores[splitter] = ((len(pass_index) / num_samples) * self._gini_impurity([labels[i] for i in pass_index]) +
                                       (len(fail_index) / num_samples) * self._gini_impurity([labels[i] for i in fail_index]))

      best_splitter = min(gini_scores)
      pass_index, fail_index = self._split(samples, best_splitter)

      return Node(
        splitter = best_splitter,
        left_child = self._fit(samples[pass_index,:], [labels[i] for i in pass_index], randomize, current_depth + 1),
        right_child = self._fit(samples[fail_index,:], [labels[i] for i in fail_index], randomize, current_depth + 1)
      )

  def _gini_impurity(self, labels):
    """
    Measures how often randomly chosen element from set would be incorrectly labeled if it were randomly labeled
    using label distribution in subset.
    Sum probability of each item being chosen times probability of mistake in categorizing item

    Parameters:
      labels: labels of the samples we are testing gini impurity

    Y -> set of all classes
    sum for all y in Y
    P(y) * (1 - P(y))

    aka prob. of choosing * prob. of mistake
    """

    # Aggregate counts
    count = Counter(labels)
    gini = 0.0
    for label in set(labels):
      f = float(count[label]) / len(labels)
      gini += f * ( 1.0 - f)

    return gini


  def _split(self, samples, splitter):
    """
    Split samples given a function that represents the feature split test

    Parameters:
      samples: the samples we are interested in splitting, usually probably Node.samples
      splitter: tuple of (feature_index, threshold)

    Returns:
      pass_index: index of samples that passed split_test
      fail_index: index of samples that failed split_test
    """
    pass_index = []
    fail_index = []
    for i, sample in enumerate(samples):
      if self.split_compare(sample, splitter):
        pass_index.append(i)
      else:
        fail_index.append(i)
    return pass_index, fail_index


  def predict(self, test_samples):
    # TODO: we'll have to figure out a way to take advantage of column indexing here.
    # May have to convert back to nparray as passed in later
    samples = sanitize_samples(test_samples)
    samples = np.array(samples)

    return [self._predict(sample, self.root_node) for sample in samples]


  def _predict(self, sample, current_node):
    # Base Case: Node is a leaf
    if isinstance(current_node, Leaf):
      return current_node.value, current_node.posterior

    else:
      if self.split_compare(sample, current_node.splitter):
        return self._predict(sample, current_node.left_child)
      else:
        return self._predict(sample, current_node.right_child)

  def score(self, test_samples, test_labels):
    predicted_labels = self.predict(test_samples)
    difference = 0.0
    for pred, actual in zip(predicted_labels, test_labels):
      difference += abs(pred - actual)

    return 1.0 - (difference / len(test_labels))
