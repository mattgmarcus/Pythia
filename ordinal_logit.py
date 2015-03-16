#!/usr/bin/env python
import numpy as np
import warnings
from scipy import optimize
import sys

def fit(samples, labels):
  samples = np.asarray(samples)
  labels = np.asarray(labels)

  # Sort by order of labels
  idx = np.argsort(labels)
  samples = samples[idx]
  labels = labels[idx]

  # Labels are continuous and start at 0
  unique_labels = np.unique(labels)
  for i, u in enumerate(unique_labels):
      labels[labels == u] = i
  unique_labels = np.unique(labels)

  params0 = np.zeros(samples.shape[1] + unique_labels.size - 1)
  params0[samples.shape[1]:] = np.sort((unique_labels.size - 1) * np.random.rand(unique_labels.size - 1))


  def objective(params, samples, labels):
    """
    Minimize loss function -> minimize -log(p(y = j | X))
    p(y = j | X) = p(y < j | X) - p(y < j - 1 | X)
    """
    w, theta = np.split(params, [samples.shape[1]])
    #print theta
    loss = 0.
    for i in range(samples.shape[0]):
      k = unique_labels.size - 1 # Assuming sorted
      y = labels[i]
      wx = w.T.dot(samples[i])
      theta_upper = float("inf") if y == k else theta[y]
      theta_lower = float("-inf") if y == 0 else theta[y - 1]
      phi_diff = phi(theta_upper - wx) - phi(theta_lower - wx)
      if phi_diff > 0:
        loss -= np.log(phi_diff)
    return loss

  def phi(t):
    if t == float("inf"):
     return 1
    elif t == float("-inf"):
      return 0
    else:
     return 1. / (1 + np.exp(-t))

  def logistic(theta, w, samples):
    """
    t = theta_j - (w^T * X_i)
    phi(t) = 1 / (1 + exp(-t))
    """
    Xw = samples.dot(w)
    t = theta - Xw

    return phi(t)

  def log_logistic(theta, w, samples):
    """
    t = theta_j - (w^T * X_i)
    - log(phi(t)) = - log(1 / (1 + exp(-t)))
    """
    return np.log(logistic(theta, w, samples))

  def grad(params, samples, labels):
    """
    Return gradient for w and gradient for theta
    """
    w, theta = np.split(params, [samples.shape[1]])

    grad_w = np.zeros(w.shape)
    grad_theta = np.zeros(theta.shape)

    for i in range(0, samples.shape[0]):
      k = unique_labels.size - 1 # Assuming sorted
      y = labels[i]
      y0 = y - 1
      x = samples[i]
      wx = w.T.dot(x)
      theta_upper = float("inf") if y == k else theta[y]
      theta_lower = float("-inf") if y == 0 else theta[y - 1]

      e1 = np.zeros(k)
      e0 = np.zeros(k)
      if y < k:
        e1[y] = 1
      if y > 0:
        e0[y - 1] = 1

      grad_w += x * (1 - phi(theta_upper - wx) - phi(theta_lower - wx))
      grad_theta += e1 * np.nan_to_num((1 - phi(theta_upper - wx) - 1. / (1 - np.exp(theta_lower - theta_upper)))) + \
                    e0 * np.nan_to_num((1 - phi(theta_lower - wx) - 1. / (1 - np.exp(theta_upper - theta_lower))))

    return np.concatenate((grad_w, grad_theta))

  params = optimize.minimize(objective, params0, args=(samples, labels), method='TNC', jac=grad)

  if not params.success:
      warnings.warn(params.message)

  w, theta = np.split(params.x, [samples.shape[1]])

  return w, theta

# Credit: this code was copied closely from lines 242-245 here:
# https://github.com/fabianp/minirank/blob/master/minirank/logistic.py
def predict(w, theta, samples):
  xw = samples.dot(w)
  theta[-1] = float("inf")
  tmp = xw[:, None].repeat(theta.size, axis=1)
  return np.argmax(tmp < theta, axis=1)

