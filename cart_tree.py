import numpy as np
import scipy as sp

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
		self.left_child = None
		self.right_child = None

class Leaf(object):
	def __init__(self):
		self.value = None

class CartTree(self):
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
		self (CartTree)

		"""


		m_samples, self.d_features = X.shape

		Y = np.atleast_1d(Y)

		self.m_outputs = Y.shape[0]

		self.classes = np.unique(Y)
		self.n_classes = self.classes.shape[0]


	def _gini_impurity(samples, split_test):
		"""
		Measures how often randomly chosen element from set would be incorrectly labeled if it were randomly labeled
		using label distribution in subset.
		Sum probability of each item being chosen times probability of mistake in categorizing item

    Parameters:
      samples: set of samples at each node level
      split_test: callback function that returns true if pass, false if fail

		Y -> set of all classes
		sum for all y in Y
		P(y) * (1 - P(y))

		aka prob. of choosing * prob. of mistake
		"""

    pass_samples, fail_samples = _split(samples, split_test)


  def _split(samples, split_test):
    pass_samples = []
    fail_samples = []
    for sample in samples:
      if split_test(sample):
        pass_samples.append(sample)
      else:
        fail_samples.append(sample)
    return np.array(pass_samples), np.array(fail_samples)

