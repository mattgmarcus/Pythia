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

class Node(object):
  def __init__(self, splitter, left_child, right_child):
    self.splitter = splitter #(feature_index, threshold)
    self.left_child = left_child
    self.right_child = right_child

  def __str__(self):
    print self.left_child
    print self.right_child
    return str(self.splitter)


class Leaf(Node):
  def __init__(self, value):
    self.value = value

  def __str__(self):
    return self.value


class LeafClassifier(Leaf):
  def __init__(self, labels, posterior_label=None):
    counts = Counter(labels)
    most_common_label = counts.most_common(1)[0][0]
    self.value = most_common_label

    if posterior_label:
      self.posterior = float(counts[posterior_label]) / len(labels)


class LeafRegressor(Leaf):
  def __init__(self, labels):
    self.unrounded_value = float(sum(labels)) / len(labels)
    self.value = round(self.unrounded_value)


class DecisionTree(object):
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

    if sanitize:
      samples = sanitize_samples(samples)
      samples = np.array(samples)

    self.d_features = samples.shape[1]
    self.classes = np.unique(labels)
    self.n_classes = self.classes.shape[0]

    self.root_node = self.root_node or self._fit(samples, labels, randomize)



  def _fit(self, samples, labels, randomize, current_depth=1):
    # Base cases
    # No samples/labels
    if len(labels) == 0:
      return None

    # all labels are same
    #    return label same
    elif (len(set(labels))) == 1:
      return self.make_leaf(labels)

    # current_depth >= max_depth || len(samples) < 20
    #   return leaf node, where value=mode(current labels)
    elif (current_depth >= self.max_depth) or (len(samples) < 20):
      return self.make_leaf(labels)

    # Recursive case
    else:
      errors = {}
      while len(errors) == 0:
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

            num_passed = len(pass_index)
            num_failed = len(fail_index)
            if (num_passed > 0) and (num_failed > 0):
              errors[splitter] = ((num_passed / num_samples) * self.get_error([labels[i] for i in pass_index]) +
                                       (num_failed / num_samples) * self.get_error([labels[i] for i in fail_index]))

      best_splitter = min(errors)
      pass_index, fail_index = self._split(samples, best_splitter)

      return Node(
        splitter = best_splitter,
        left_child = self._fit(samples[pass_index,:], [labels[i] for i in pass_index], randomize, current_depth + 1),
        right_child = self._fit(samples[fail_index,:], [labels[i] for i in fail_index], randomize, current_depth + 1)
      )

  def get_error(self, labels):
    pass

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
      # samples[feature_index] < threshold
      if sample[splitter[0]] < splitter[1]:
        pass_index.append(i)
      else:
        fail_index.append(i)
    return pass_index, fail_index


  def predict(self, test_samples):
    samples = sanitize_samples(test_samples)
    samples = np.array(samples)

    return [self._predict(sample, self.root_node) for sample in samples]


  def _predict(self, sample, current_node):
    # Base Case: Node is a leaf
    if isinstance(current_node, Leaf):
      return self.get_leaf_value(current_node)
    else:
      if sample[current_node.splitter[0]] < current_node.splitter[1]:
        return self._predict(sample, current_node.left_child)
      else:
        return self._predict(sample, current_node.right_child)

  def get_leaf_value(self, current_node):
    pass

  def score(self, test_samples, test_labels):
    predicted_labels = self.predict(test_samples)
    difference = 0.0
    for pred, actual in zip(predicted_labels, test_labels):
      difference += (1 if (pred - actual != 0) else 0)

    return 1.0 - (difference / len(test_labels))

class DecisionTreeClassifier(DecisionTree):
  def __init__(self, max_depth, use_posterior=False, posterior_label=None):
    super(DecisionTreeClassifier, self).__init__(max_depth)
    self.use_posterior = use_posterior
    self.posterior_label = posterior_label

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

  def get_leaf_value(self, current_node):
    return current_node.posterior if self.use_posterior else current_node.value

  def make_leaf(self, labels):
    return LeafClassifier(labels, self.posterior_label)

  def get_error(self, labels):
    return self._gini_impurity(labels)


class DecisionTreeRegressor(DecisionTree):
  def __init__(self, max_depth):
    super(DecisionTreeRegressor, self).__init__(max_depth)

  def get_error(self, labels):
    return self._msd_error(labels)

  def _msd_error(self, labels):
    return np.array(labels).var()

  def get_leaf_value(self, current_node):
    return current_node.value

  def make_leaf(self, labels):
    return LeafRegressor(labels)

