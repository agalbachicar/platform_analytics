import numpy as np
import random

def create_tasks_arrivals(n_tasks=10, beta=1.):
  return sorted([np.random.exponential(beta) for i in range(0, n_tasks)])

def sample_nodes(nodes):
  return random.sample(nodes, 1)

if __name__ == "__main__":
  random.seed(0)
  nodes = {'a', 'b', 'c', 'd'}
  print('Two random samples from nodes:{} are <{}> and <{}>'.format(nodes, sample_nodes(nodes), sample_nodes(nodes)))

  import matplotlib.pyplot as plt
  np.random.seed(0)
  beta = 10.
  n = 1000
  x = create_tasks_arrivals(n, beta)
  plt.figure()
  plt.plot(x)
  plt.grid()
  plt.show()
