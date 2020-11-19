import networkx as nx
from warehouse import Warehouse

class Agent:
  def __init__(self, name, pos):
    self._name = name
    self._pos = pos
    self._acc_cost = 0
    self._path = []

  def name(self):
    return self._name

  def pos(self):
    return self._pos

  def path_and_cost_to(self, node, w):
    class WeightFn:
      def __init__(self, w):
        self._w = w
      def __call__(self, u, v, d):
        return w.get_edge_cost(u, v)
    weight_fn = WeightFn(w)
    path = nx.dijkstra_path(w.graph(), self._pos, node, weight=weight_fn)
    return path[1:], w.path_cost(path)

  def is_assigned(self):
    return False if not self._path else True

  def assign_mission(self, path):
    self._path = path

  def cost(self):
    return self._acc_cost

  def next_move(self):
    return (self._pos, self._path[0]) if self.is_assigned() else None

  def tick(self, w):
    if self.is_assigned():
      # Computes the step cost
      p_s = self._pos
      p_f = self._path.pop(0)
      step_cost = w.get_edge_cost(p_s, p_f)
      # Updates the total cost
      self._acc_cost += step_cost
      # Updates the position
      self._pos = p_f

  def __repr__(self):
    return '[name: {}, position: {}, is_assigned: {}, path: {}, acc_cost:{}]'.format(self._name, self._pos, self.is_assigned(), self._path, self._acc_cost)

if __name__ == "__main__":
  ROWS=4
  COLS=8
  NODE_CAPACITY=2
  w = Warehouse(ROWS, COLS, NODE_CAPACITY, edge_base_cost=1., occupancy_cost=0.1)
  n_0 = '1_1'
  agent = Agent('dut', '1_1')
  print('Agent {} is at <{}>'.format(agent.name(), agent.pos()))
  target = '2_7'
  path, cost = agent.path_and_cost_to(target, w)
  print('Proposed path to <{}>: {}. Cost: {}'.format(target, path, cost))
  agent.assign_mission(path)
  i = 0
  while agent.is_assigned():
    agent.tick(w)
    print('Iter {}: agent position: {}'.format(i, agent.pos()))
    i += 1
  print('Agent total cost: {}'.format(agent.cost()))

