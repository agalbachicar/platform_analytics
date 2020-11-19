from collections import Counter
import logging

from agent import Agent
from task_creator import create_tasks_arrivals, sample_nodes, set_seed
from warehouse import Warehouse
from warehouse_manager import WarehouseManager

class Simulator:
  def __init__(self, rows, cols, edge_base_cost=1., occupancy_cost=0., n_agents=10, n_tasks=100, beta=1., seed=0):
    set_seed(s=seed)

    self._w = Warehouse(rows, cols, node_capacity=-1, edge_base_cost=edge_base_cost, occupancy_cost=occupancy_cost)
    self._w_manager = WarehouseManager(self._w, n_agents)
    nodes = self._w_manager.nodes()

    self._task_arrival_times = dict()
    arrival_times = Counter(create_tasks_arrivals(n_tasks, beta))
    for t in arrival_times:
      self._task_arrival_times[t] = [sample_nodes(nodes)] * arrival_times[t]

    self._processed_ticks = 0
    self._operational_ticks = 0

  def processed_ticks(self):
    return self._processed_ticks

  def operational_ticks(self):
    return self._operational_ticks

  def utilitarian_cost(self):
    return self._w_manager.cost()

  def task_assingments(self):
    return self._w_manager.task_assingments()

  def run(self):
    i = 0
    tasks_to_process = []
    while ( len(self._w_manager.assigned_agents()) > 0 or len(self._task_arrival_times) > 0 or len(tasks_to_process) > 0 ):
      logging.debug('\t\tRunning the {}-th iteration.'.format(i))
      i += 1
      # Pick tasks
      if i in self._task_arrival_times:
        tasks_to_process = tasks_to_process + self._task_arrival_times.pop(i)
      # Try to assign as many tasks as possible
      task_index = 0
      for task in tasks_to_process:
        logging.debug('\t\tTrying to process: {}'.format(task))
        if not self._w_manager.process_task(task):
          break
        task_index += 1
      tasks_to_process = tasks_to_process[task_index:]
      # Increase the amount of operational ticks when there are assigned agents
      if len(self._w_manager.assigned_agents()) > 0:
        self._operational_ticks += 1
      # Tick the system
      self._w_manager.tick()

    self._processed_ticks += i

