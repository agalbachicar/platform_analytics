import sys
import logging

from agent import Agent
from warehouse import Warehouse
from task_creator import sample_nodes, set_seed

class WarehouseManager:
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
    return self._w

  def nodes(self):
    return list(self._w.graph().nodes)

  def assigned_agents(self):
    return self._assigned_agents

  def task_assingments(self):
    return self._task_assingments

  def unassigned_agents(self):
    return self._unassigned_agents

  def cost(self):
    return self._utilitarian_cost

  def process_task(self, task):
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
