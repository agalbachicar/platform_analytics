import networkx as nx
import matplotlib.pyplot as plt

class Warehouse:
  def __init__(self, rows, cols, node_capacity):
    self._rows = rows
    self._cols = cols
    self._graph = nx.Graph()
    # Add nodes
    for i in range(0, rows):
      for j in range(0, cols+1):
        name = Warehouse._get_node_name(i, j)
        self._graph.add_node(name)
        self._graph.nodes[name]['capacity'] = node_capacity
        self._graph.nodes[name]['available_capacity'] = node_capacity

    # Add row edges
    for i in range(0, rows):
      for j in range(0, cols):
        self._graph.add_edge(Warehouse._get_node_name(i, j), Warehouse._get_node_name(i, j+1))
  
    # Add column edges
    for i in range(0, rows-1):
      for j in range(0, cols+1):
        self._graph.add_edge(Warehouse._get_node_name(i, j), Warehouse._get_node_name(i+1, j))

  def graph(self):
    return self._graph

  def node_capacity(self, name):
    return self._graph.nodes[name]['available_capacity']

  def plot(self):
    plt.figure()
    pos = {node_name: Warehouse._get_node_index(node_name) for node_name in self._graph.nodes}
    nx.draw(self._graph, pos=pos, with_labels=True, font_weight='bold')
    plt.show()

  def _get_node_name(row, col):
    return '{}_{}'.format(row, col)
  
  def _get_node_index(node_name):
    return tuple(node_name.split('_'))

  def _get_edge_name(row_i, col_i, row_j, col_j):
    return '{}_{}'.format(get_node_name(row_i, col_i), get_node_name(row_j, col_j))

if __name__ == "__main__":
  ROWS=4
  COLS=8
  NODE_CAPACITY=2
  w = Warehouse(ROWS, COLS, NODE_CAPACITY)
  w.plot()
