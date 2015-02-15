from tree import DecisionTreeClassifier
from joblib import Parallel, delayed
from collections import Counter
import numpy as np

def bootstrap_build_tree(tree, X, Y):
	"""
	Generate random indices by sampling with replacement and
	then generate random subset from training set using those indices

	Parameters:
	X: Training samples, each with d features; m x d 2D array
	Y: Training labels; 1 x m array

	Return:
	Fitted tree (DecisionTreeClassifier)
	"""
	n_samples = X.shape[0]

	random_indices = np.random.choice(n_samples, n_samples, replace=True)
	random_subset = X[random_indices,:]
	random_subset_labels = Y[random_indices]

	tree.fit(random_subset, random_subset_labels)

	return tree, random_indices

def parallel_predict_tree(tree, X):

	return tree.predict(X)

class RandomForestClassifier(self):
	def __init__(self, n_trees, n_jobs):
		self.n_trees = n_trees
		self.n_jobs = n_jobs
		self.trees = None
		self.tree_indices = None
		self.oob_score = None
		self.n_outputs = None
		self.classes = None
		self.n_classes = None
		self.d_features = None
		self.feature_importances = None

	def fit(self, X, Y):
		"""
		Create forest of trees from training set
		
		Given training set D
		n_trees = # of trees
		in parallel:
		for i to n_estimators:
			bootstrap_build_tree

		Pass D into forest
		Majority vote

		"""

		m_samples, self.d_features = X.shape

		self.n_outputs = Y.shape[0]

		self.classes = np.unique(Y)
		self.n_classes = classes.size

		self.trees = []
		for i in range(self.n_trees):
			tree = DecisionTreeClassifier()
			self.trees.append(tree)

		"""
		Fit trees in parallel
		"""

		self.trees, self.tree_indices = Parallel(n_jobs=self.n_jobs, backend="threading")\
			(delayed(bootstrap_build_tree)(t, X, Y) for t in enumerate(self.trees))

	# Assume input col is a col from an np array
	def mode(col):
		common = Counter(col)
		return common.most_common(1)[0][0]

	def predict(self, X):

		# Preds is a list where each element is a list of predicted values
		# for each decision tree
		preds = Parallel(n_jobs=self.n_jobs, backend="threading")\
			(delayed(parallel_predict_tree)(t, X) for t in enumerate(self.trees))

		# Convert preds into a np array
		preds_np = np.array(preds)
		# num_col = preds_np.shape[1]
		
		# Get voted Y val for each col
		return np.apply_along_axis(mode, 0, preds_np)

		# voted_preds = []
		# for i in range(num_col):
		# 	common_preds = Counter(preds_np[:,i])
		# 	voted_preds[i] = common_preds.most_common(1)[0][0]

		# return voted_preds


	def get_oob_score(self, X, Y):
		
		# oob_preds is a list where each element is a list of predicted values
		oob_preds = []
		oob_score = 0.0

		all_sample_indices = X.shape[0]
		for i in self.n_trees:
			mask = np.ones(len(all_sample_indices), dtype=bool)
			mask[self.tree_indices[i]] = False
			left_out_indices = all_sample_indices[mask]

			# This is a list of predicted values
			oobs_preds[i] = self.trees[i].predict(X[left_out_indices,:])

		# Convert oob_preds into a np array
		oob_preds_np = np.array(oob_preds)
		# num_col = oob_preds_np.shape[1]

		# Get voted Y val for each col
		voted_oob_preds = np.apply_along_axis(mode, 0, oob_preds_np)

		# voted_oob_preds = []
		# for i in range(num_col):
		# 	common_oob_preds = Counter(oob_preds_np[:,i])
		# 	voted_oob_preds[i] = common_oob_preds.most_common(1)[0][0]

		# oob_score = # of times common_oob_pred_y != actual y / number of oob cases
		for k in range(self.n_outputs):
			# Some inputs will not have an oob pred so just skip them
			if voted_oob_preds[k] == 0:
				continue

			oob_score += (voted_oob_preds[k] != Y[k])

		self.oob_score = oob_score / n_outputs

		return self.oob_score

	def feature_relevances(self):
		pass


