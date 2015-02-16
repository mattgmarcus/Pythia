from tree import DecisionTreeClassifier
from joblib import Parallel, delayed
from collections import Counter
import numpy as np
from util import *
import sklearn.tree

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

class RandomForestClassifier():
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
			tree = DecisionTreeClassifier(self.max_depth)
			# tree = sklearn.tree.DecisionTreeClassifier(max_depth=self.max_depth, max_features="sqrt")
			self.trees.append(tree)

		# Fit trees in parallel
		self.trees = Parallel(n_jobs=self.n_jobs, backend="threading")\
			(delayed(bootstrap_build_tree)(t, samples, labels) for t in self.trees)
			# (delayed(self._parallel_helper)(self, "bootstrap_build_tree", t, samples, labels) for t in self.trees)

		# self.get_oob_score(samples, labels)

		return self


	def predict(self, samples):
		# Preds is a list where each element is a list of predicted values
		# for each decision tree
		predictions = Parallel(n_jobs=self.n_jobs, backend="threading")\
			(delayed(_parallel_helper)(t, "predict", samples) for t in self.trees)

		# Convert preds into a np array
		predictions = np.array(predictions)
		# num_col = preds_np.shape[1]

		# Get voted Y val for each col
		return np.apply_along_axis(mode, 0, predictions)


	def get_oob_score(self, samples, labels):

		# oob_preds is a list where each element is a list of predicted values
		oob_preds = []
		oob_score = 0.0

		all_sample_indices = np.array(range(samples.shape[0]))
		for i in range(self.n_trees):
			mask = np.ones(len(all_sample_indices), dtype=bool)
			mask[self.trees[i].indices] = False
			left_out_indices = all_sample_indices[mask]

			# This is a list of predicted values
			oob_preds.append(self.trees[i].predict(samples[left_out_indices,:]))

		# Convert oob_preds into a np array
		oob_preds_np = np.array(oob_preds)
		# num_col = oob_preds_np.shape[1]

		# Get voted Y val for each col
		voted_oob_preds = np.apply_along_axis(mode, 0, oob_preds_np)

		# oob_score = # of times common_oob_pred_y != actual y / number of oob cases
		n_outputs = labels.shape[0]
		for k in range(n_outputs):
			# Some inputs will not have an oob pred so just skip them
			if voted_oob_preds[k] == 0:
				continue

			# oob_score += (voted_oob_preds[k] != Y[k])
			oob_score += abs(voted_oob_preds[k] - labels[k])

		self.oob_score = oob_score / n_outputs

		return self.oob_score


	def score(self, test_samples, test_labels):
		predicted_labels = self.predict(test_samples)

		difference = 0.0
		for pred, actual in zip(predicted_labels, test_labels):
			difference += abs(pred - actual)

		return 1.0 - (difference / len(predicted_labels))


	def feature_relevances(self):
		pass
