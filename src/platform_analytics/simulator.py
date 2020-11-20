from collections import Counter
import logging

from agent import Agent
from task_creator import create_tasks_arrivals, sample_nodes, set_seed
from warehouse import Warehouse
from warehouse_manager import WarehouseManager

class Simulator:
  def __init__(self, rows, cols, edge_base_cost=1., occupancy_cost=0., n_agents=10, n_tasks=100, lam=1., seed=0):
    set_seed(s=seed)

    self._w = Warehouse(rows, cols, node_capacity=-1, edge_base_cost=edge_base_cost, occupancy_cost=occupancy_cost)
    self._w_manager = WarehouseManager(self._w, n_agents)
    nodes = self._w_manager.nodes()

    num_tasks_per_iteration = create_tasks_arrivals(n_tasks, lam)
    self._task_arrivals = []
    for x in num_tasks_per_iteration:
      self._task_arrivals.append([sample_nodes(nodes)] * x)

    self._processed_ticks = 0
    self._only_wip_ticks = 0

  def processed_ticks(self):
    return self._processed_ticks

  def only_wip_ticks(self):
    return self._only_wip_ticks

  def utilitarian_cost(self):
    return self._w_manager.cost()

  def task_assingments(self):
    return self._w_manager.task_assingments()

  def run(self):
    i = 0
    tasks_to_process = []
    while ( len(self._w_manager.assigned_agents()) > 0 or len(self._task_arrivals) > 0 or len(tasks_to_process) > 0 ):
      logging.debug('\t\tRunning the {}-th iteration.'.format(i))
      i += 1
      # Pick new tasks and add those to the pool
      if self._task_arrivals:
        tasks_to_process = tasks_to_process + self._task_arrivals.pop(0)
      else:
        # When there are no more tasks but we still need to process.
        self._only_wip_ticks += 1

      # Try to assign as many tasks as possible
      task_index = 0
      for task in tasks_to_process:
        logging.debug('\t\tTrying to process: {}'.format(task))
        if not self._w_manager.process_task(task):
          break
        task_index += 1
      tasks_to_process = tasks_to_process[task_index:]
      # Tick the system
      self._w_manager.tick()

    self._processed_ticks += i

