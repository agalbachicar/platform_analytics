import numpy as np

def create_tasks_arrivals(n_tasks=10, beta=1.):
  return sorted([np.random.exponential(beta) for i in range(0, n_tasks)])


if __name__ == "__main__":
  import matplotlib.pyplot as plt
  beta = 10.
  n = 1000
  np.random.seed(0)
  x = create_tasks_arrivals(n, beta)
  plt.figure()
  plt.plot(x)
  plt.grid()
  plt.show()
