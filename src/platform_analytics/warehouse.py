import networkx as nx
import matplotlib.pyplot as plt

class Warehouse:
  def __init__(self, rows, cols, node_capacity=-1, edge_base_cost=1., occupancy_cost=0.):
    self._rows = rows
    self._cols = cols
    self._edge_base_cost = edge_base_cost
    self._occupancy_cost = occupancy_cost
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
        e = (Warehouse._get_node_name(i, j), Warehouse._get_node_name(i, j+1))
        self._graph.add_edge(Warehouse._get_node_name(i, j), Warehouse._get_node_name(i, j+1))
        self._graph.edges[e]['weight'] = self._edge_base_cost
        self._graph.edges[e]['occupancy'] = 0
  
    # Add column edges
    for i in range(0, rows-1):
      for j in range(0, cols+1):
        e = (Warehouse._get_node_name(i, j), Warehouse._get_node_name(i+1, j))
        self._graph.add_edge(Warehouse._get_node_name(i, j), Warehouse._get_node_name(i+1, j))
        self._graph.edges[e]['weight'] = self._edge_base_cost
        self._graph.edges[e]['occupancy'] = 0

  def graph(self):
    return self._graph

  def node_capacity(self, name):
    return self._graph.nodes[name]['available_capacity']

  def clear_edges_occupancy(self):
    for e in self._graph.edges:
      self._graph.edges[e]['occupancy'] = 0

  def increase_edge_occupancy(self, edge):
    self._graph.edges[edge]['occupancy'] = self._graph.edges[edge]['occupancy'] + 1

  def decrease_edge_occupancy(self, edge):
    e = self._graph.edges[edge]
    e['occupancy'] = max(0, e['occupancy'] - 1)

  def path_cost(self, path):
    cost = 0
    for i in range(0, len(path)-1):
      cost += self.get_edge_cost(path[i], path[i+1])
    return cost

  def plot(self):
    plt.figure()
    pos = {node_name: Warehouse._get_node_index(node_name) for node_name in self._graph.nodes}
    nx.draw(self._graph, pos=pos, with_labels=True, font_weight='bold')
    plt.show()

  def get_edge_cost(self, n_i, n_j):
    return self._graph.edges[(n_i, n_j)]['weight'] + self._occupancy_cost * self._graph.edges[(n_i, n_j)]['occupancy']

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
