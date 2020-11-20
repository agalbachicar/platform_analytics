import numpy as np
import random
import math

def set_seed(s=0):
  np.random.seed(s)
  random.seed(s)

def create_tasks_arrivals(n_tasks=10, lam=1.):
  '''
  Returns a list of samples of a Poisson distribution with lambda = lam 
  parameter. The summatory of the resulting vector is n_tasks
  '''
  result = []
  acc_tasks = 0
  while acc_tasks < n_tasks:
    sample = np.random.poisson(lam=lam)
    if acc_tasks + sample < n_tasks:
      result.append(sample)
    else:
      # Yes, I know... the last sample is not Poisson...
      result.append(acc_tasks + sample - n_tasks)
    acc_tasks += result[-1]
  return result

def sample_nodes(nodes):
  return random.sample(nodes, 1)[0]

if __name__ == "__main__":
  set_seed(0)

  nodes = ['a', 'b', 'c', 'd']
  print('Two random samples from nodes:{} are <{}> and <{}>'.format(nodes, sample_nodes(nodes), sample_nodes(nodes)))

  import matplotlib.pyplot as plt
  beta = 10.
  n = 1000
  x = create_tasks_arrivals(n, beta)
  plt.figure()
  plt.plot(x)
  plt.grid()
  plt.show()
