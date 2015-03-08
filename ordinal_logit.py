#!/usr/bin/env python
import numpy as np

def obj(theta, w, sampels, labels):
	"""
	Minimize loss function -> minimize -log(p(y = j | X))
	p(y = j | X) = p(y < j | X) - p(y < j - 1 | X)
	"""
	phi_j1 = logistic()

def logistic(theta, w, samples):
	"""
	t = theta_j - (w^T * X_i)
	phi(t) = 1 / (1 + exp(-t))
	"""
	wX = w.T.dot(samples)
	t = theta - wX

	return 1.0 / (1 + np.exp(-t))

def log_logistic(theta, w, samples):	
	"""
	t = theta_j - (w^T * X_i)
	- log(phi(t)) = - log(1 / (1 + exp(-t)))
	"""
	return np.log(logistic(theta, w, samples))

def grad(samples, labels):
	"""
	Return gradient for w and gradient for theta
	"""
	pass

def fit(samples, labels):
	pass

def predict(samples):
	pass

def score(test_samples, test_labels):
	pass



