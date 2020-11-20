import networkx as nx
from warehouse import Warehouse

class Agent:
  '''
  Holds the behavior of an agent that would perform a task.
  '''
  def __init__(self, name, pos):
    self._name = name
    self._pos = pos
    self._path = []

  def name(self):
    return self._name

  def pos(self):
    return self._pos

  def path_and_cost_to(self, node, w):
    '''
    Returns the path and the cost of going from its position to node given a 
    Warehouse w.
    '''
    class WeightFn:
      def __init__(self, w):
        self._w = w
      def __call__(self, u, v, d):
        return w.get_edge_cost(u, v)
    weight_fn = WeightFn(w)
    path = nx.dijkstra_path(w.graph(), self._pos, node, weight=weight_fn)
    return path[1:], w.path_cost(path)

  def is_assigned(self):
    '''
    Returns True when it has nodes to cover from its assignment.
    '''
    return False if not self._path else True

  def assign_mission(self, path):
    '''
    Sets a list of nodes to traverse.
    '''
    self._path = path

  def next_move(self):
    '''
    Returns the next edge to traverse when it is assigned
    '''
    return (self._pos, self._path[0]) if self.is_assigned() else None

  def tick(self, w):
    '''
    When it has an assignment, it moves to the next node.
    '''
    if self.is_assigned():
      # Computes the step cost
      p_s = self._pos
      p_f = self._path.pop(0)
      # Updates the position
      self._pos = p_f

  def __repr__(self):
    return '[name: {}, position: {}, is_assigned: {}, path: {}]'.format(self._name, self._pos, self.is_assigned(), self._path)

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

