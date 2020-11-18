import networkx as nx

class Agent:
  def __init__(self, name, pos):
    self._name = name
    self._pos = pos

  def get_name(self):
    return self._name

  def get_pos(self):
    return self._pos

  def path_to(self, nodes, graph):
    path = []
    nn = [self._pos] + nodes
    for i in range(0, len(nn)-1):
      path = path + nx.astar_path(graph, nn[i], nn[i+1])[1:]
    return path

if __name__ == "__main__":
  g = nx.path_graph(5)
  agent = Agent('dut', 2)
  print('Agent is at {}. Path to 4 and then 1 is: {}'.format(agent.get_pos(), agent.path_to([4,1], g)))