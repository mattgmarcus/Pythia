import numpy as np
import scipy as sp

def gini_impurity():
	"""
	Measures how often randomly chosen element from set would be incorrectly labeled if it were randomly labeled
	using label distribution in subset.
	Sum probability of each item being chosen times probability of mistake in categorizing item

	1 - sum i = 1 -> m (fi^2)
	fi = fraction of items labeled with value i in set
	"""

	