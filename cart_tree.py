import numpy as np
import scipy as sp

class Node(object):
	def __init__(self):
		self.split_feature = None
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




	def gini_impurity():
		"""
		Measures how often randomly chosen element from set would be incorrectly labeled if it were randomly labeled
		using label distribution in subset.
		Sum probability of each item being chosen times probability of mistake in categorizing item

		1 - sum i = 1 -> m (fi^2)
		fi = fraction of items labeled with value i in set
		"""



	