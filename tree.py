import numpy as np
import scipy as sp
import collections import Counter

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
	def __init__(self):
		self.split_feature = None
    self.split_test = None
    self.samples = None
		self.left_child = None
		self.right_child = None

class Leaf(object):
	def __init__(self):
		self.value = None

class DecisionTreeClassifier(self):
	"""Decision Tree using CART method"""
	def __init__(self):
		self.classes = None
		self.n_classes = None
		self.m_outputs = None
		self.d_features = None
		self.feature_relevances = None
		self.splitter = None
		self.class_weights = None

	def fit(self, X, Y, sample_weight=None):
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


		m_samples, self.d_features = X.shape

		Y = np.atleast_1d(Y)

		self.m_outputs = Y.shape[0]

		self.classes = np.unique(Y)
		self.n_classes = self.classes.shape[0]


	def _gini_impurity(labels):
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
    gini = 0
    for label in labels:
      f = count(label) / len(labels)
      gini += f * ( 1 - f)
    return gini


  def _split(samples, split_test):
    """
    Split samples given a function that represents the feature split test

    Parameters:
      samples: the samples we are interested in splitting, usually probably Node.samples
      split_test: function (feature_vector -> {true, false})

    Returns:
      pass_index: index of samples that passed split_test
      fail_index: index of samples that failed split_test
    """
    pass_index = []
    fail_index = []
    for i in range(0, len(samples)):
      if split_test(samples[i]):
        pass_index.append(i)
      else:
        fail_index.append(i)
    return pass_index, fail_index
