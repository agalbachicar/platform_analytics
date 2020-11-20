import sys
import logging

from agent import Agent
from warehouse import Warehouse
from task_creator import sample_nodes, set_seed

class WarehouseManager:
  '''
  Manages a Warehouse and a set of Agents.
  '''
  def __init__(self, w, n_agents=10):
    self._w = w
    self._utilitarian_cost = 0.

    nodes = self.nodes()
    self._unassigned_agents = []
    self._assigned_agents = []
    for i in range(0, n_agents):
      n = sample_nodes(nodes)
      nodes.remove(n)
      agent = Agent(WarehouseManager._agent_name(i), n)
      self._w.graph().nodes[n]['agents'] = [agent]
      self._unassigned_agents.append(agent)

    self._task_assingments = []

  def warehouse(self):
    '''
    Returns the underlying warehouse.
    '''
    return self._w

  def nodes(self):
    '''
    Returns the list of nodes in the warehouse.
    '''
    return list(self._w.graph().nodes)

  def assigned_agents(self):
    '''
    Returns the list of assigned agents.
    '''
    return self._assigned_agents

  def unassigned_agents(self):
    '''
    Returns the list of unassigned agents.
    '''
    return self._unassigned_agents

  def task_assingments(self):
    '''
    Returns the list of task assignments in the form of (agent, path)
    '''
    return self._task_assingments

  def cost(self):
    '''
    Returns the utilitarian cost of the manager because of its assignment
    decisions.
    It is computed by accumulating the flow cost for each iteration.
    '''
    return self._utilitarian_cost

  def process_task(self, task):
    '''
    Tries to process a task. When there are no available agents, it returns
    False.

    The assignment process follows:
    - A task is a node in graph to which an unassigned agent will be
      responsible.
    - All unassigned agents are queried for their proposed path and the current
      cost of that path.
    - The manager assigns to the agent that proposed the path with the least 
      cost the task.
    - The agent is moved to the assigned list.
    - The warehouse is updated because the of the new edge traffic in the next
      iteration.
    '''
    if not self._unassigned_agents:
      logging.debug('All agents are busy. Try next time...')
      return False

    logging.debug('\t\tComputing agents\' costs for task: {}...'.format(task))
    agent_path_bets = dict()
    for agent in self._unassigned_agents:
      agent_path_bets[agent] = dict()
      path, cost = agent.path_and_cost_to(task, self._w)
      agent_path_bets[agent]['path'] = path
      agent_path_bets[agent]['cost'] = cost
    logging.debug('\t\tFinished computing agents\' costs.')

    logging.debug('\t\tFinding the best path...')
    agent_path_bet = WarehouseManager._min_in_agents_path_bet(agent_path_bets)
    logging.debug('\t\tBest path was found.')

    logging.debug('\t\tUpdate the agent assignment lists.')
    self._unassigned_agents.remove(agent_path_bet[0])
    self._assigned_agents.append(agent_path_bet[0])

    logging.debug('\t\tAssigns the mission to the agent.')
    agent_path_bet[0].assign_mission(agent_path_bet[1]['path'])

    logging.debug('\t\tUpdate edge costs.')
    self._update_weights()

    logging.debug('\t\tRecord task solution: {}'.format((agent_path_bet[0].name(), [agent_path_bet[0].pos()] + agent_path_bet[1]['path'])))
    self._task_assingments.append((agent_path_bet[0].name(), [agent_path_bet[0].pos()] + agent_path_bet[1]['path']))
    return True

  def tick(self):
    '''
    Evolves all the assigned agents (unassigned agents will remain still).
    Moves to the unassigned list those agents that finished their work.
    Update the weights in the graph for the next iteration.
    '''
    logging.debug('\t\tTicking agents...')
    for agent in self._assigned_agents:
      agent.tick(self._w)
    logging.debug('\t\tFinished agents.')

    logging.debug('\t\tUpdating the assigned and unassigned agent lists...')
    self._unassigned_agents = self._unassigned_agents + [agent for agent in self._assigned_agents if not agent.is_assigned()]
    self._assigned_agents = [agent for agent in self._assigned_agents if agent.is_assigned()]

    logging.debug('\t\tUpdate total costs.')
    self._update_cost()

    logging.debug('\t\tUpdate edge costs.')
    self._update_weights()

  def _update_weights(self):
    # Clears all edge occupation
    self._w.clear_edges_occupancy()
    # Updates traffic based on edge occupation
    for agent in self._assigned_agents:
      edge = agent.next_move()
      if edge: self._w.increase_edge_occupancy(edge)

  def _update_cost(self):
    logging.debug('\t\tUpdating the assigned and unassigned agent lists...')
    for e in self._w.graph().edges:
      if self._w.graph().edges[e]['occupancy'] > 0:
        self._utilitarian_cost += self._w.get_edge_cost(*e)

  def _agent_name(i):
    return 'a_{}'.format(i)

  def _min_in_agents_path_bet(agent_path_bets):
    cost = sys.float_info.max
    key = None
    for k,v in agent_path_bets.items():
      if v['cost'] < cost:
        cost = v['cost']
        key = k
    return k, agent_path_bets[k]


if __name__ == '__main__':
  ROWS=3
  COLS=3
  NODE_CAPACITY=2
  N_AGENTS=2
  SEED=123

  set_seed(SEED)

  warehouse_manager = WarehouseManager(Warehouse(ROWS, COLS, NODE_CAPACITY), n_agents=N_AGENTS)
  print('- Nodes: {}'.format(warehouse_manager.nodes()))
  print('- Assigned agents: {}'.format(warehouse_manager.assigned_agents()))
  print('- Unassigned agents: {}'.format(warehouse_manager.unassigned_agents()))

  task_result = warehouse_manager.process_task('2_3')
  print('Processed task 1_1. Result: {}'.format(task_result))

  print('- Assigned agents: {}'.format(warehouse_manager.assigned_agents()))
  print('- Unassigned agents: {}'.format(warehouse_manager.unassigned_agents()))

  warehouse_manager.tick()

  print('- Assigned agents: {}'.format(warehouse_manager.assigned_agents()))
  print('- Unassigned agents: {}'.format(warehouse_manager.unassigned_agents()))

  print('- Assigned tasks: {}'.format(warehouse_manager.assigned_tasks()))
