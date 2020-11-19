from simulator import Simulator
import logging

SIMULATION_CASES = {
  'si_a10_atm': {
    'description': 'Standard 10x10 grid map. Inelastic to traffic. 10 agents. Standard task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.,
    'n_agents': 10,
    'n_tasks': 1000,
    'beta': 10.
  },
  'si_a10_atf': {
    'description': 'Standard 10x10 grid map. Inelastic to traffic. Fast arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.,
    'n_agents': 10,
    'n_tasks': 1000,
    'beta': 1
  },
  'si_a10_ats': {
    'description': 'Standard 10x10 grid map. Inelastic to traffic. Slow task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.,
    'n_agents': 10,
    'n_tasks': 1000,
    'beta': 100.
  },
  'se_a10_atm': {
    'description': 'Standard 10x10 grid map. Elastic to traffic. 10 agents. Standard task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 10,
    'n_tasks': 1000,
    'beta': 10.
  },
  'se_a10_atf': {
    'description': 'Standard 10x10 grid map. Elastic to traffic. Fast arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 10,
    'n_tasks': 1000,
    'beta': 1
  },
  'se_a10_ats': {
    'description': 'Standard 10x10 grid map. Elastic to traffic. Slow task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 10,
    'n_tasks': 1000,
    'beta': 100.
  },
  'sh_a10_atm': {
    'description': 'Standard 10x10 grid map. Highly elastic to traffic. 10 agents. Standard task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 10,
    'n_tasks': 1000,
    'beta': 10.
  },
  'sh_a10_atf': {
    'description': 'Standard 10x10 grid map. Highly elastic to traffic. Fast arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 1.,
    'n_agents': 10,
    'n_tasks': 1000,
    'beta': 1
  },
  'sh_a10_ats': {
    'description': 'Standard 10x10 grid map. Highly elastic to traffic. Slow task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 1.,
    'n_agents': 10,
    'n_tasks': 1000,
    'beta': 100.
  },

  'si_a25_atm': {
    'description': 'Standard 10x10 grid map. Inelastic to traffic. 25 agents. Standard task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.,
    'n_agents': 25,
    'n_tasks': 1000,
    'beta': 10.
  },
  'si_a25_atf': {
    'description': 'Standard 10x10 grid map. Inelastic to traffic. 25 agents. Fast arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.,
    'n_agents': 25,
    'n_tasks': 1000,
    'beta': 1
  },
  'si_a25_ats': {
    'description': 'Standard 10x10 grid map. Inelastic to traffic. 25 agents. Slow task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.,
    'n_agents': 25,
    'n_tasks': 1000,
    'beta': 100.
  },
  'se_a25_atm': {
    'description': 'Standard 10x10 grid map. Elastic to traffic. 25 agents. Standard task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 25,
    'n_tasks': 1000,
    'beta': 10.
  },
  'se_a25_atf': {
    'description': 'Standard 10x10 grid map. Elastic to traffic. 25 agents. Fast arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 25,
    'n_tasks': 1000,
    'beta': 1
  },
  'se_a25_ats': {
    'description': 'Standard 10x10 grid map. Elastic to traffic. 25 agents. Slow task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 25,
    'n_tasks': 1000,
    'beta': 100.
  },
  'sh_a25_atm': {
    'description': 'Standard 10x10 grid map. Highly elastic to traffic. 25 agents. Standard task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 25,
    'n_tasks': 1000,
    'beta': 10.
  },
  'sh_a25_atf': {
    'description': 'Standard 10x10 grid map. Highly elastic to traffic. 25 agents. Fast arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 1.,
    'n_agents': 25,
    'n_tasks': 1000,
    'beta': 1
  },
  'sh_a25_ats': {
    'description': 'Standard 10x10 grid map. Highly elastic to traffic. Slow task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 1.,
    'n_agents': 10,
    'n_tasks': 1000,
    'beta': 100.
  },
}

def average_path_length(agents_paths):
  num_paths = len(agents_paths)
  num_hops = sum([len(agent_path[1]) for agent_path in agents_paths])
  return num_hops / num_paths

def main():
  logging.basicConfig(level=logging.INFO,    
                      handlers=[logging.FileHandler("sim.log"), logging.StreamHandler()])
  
  results = dict()

  for key in SIMULATION_CASES:
    properties = SIMULATION_CASES[key]
    logging.info('Case: {}. Properties: {}'.format(key, properties))

    # rows, cols, node_capacity=-1, edge_base_cost=1., occupancy_cost=0., n_agents=10, n_tasks=100, beta=1.
    sim = Simulator(properties['rows'], properties['cols'],
                    properties['edge_base_cost'], properties['occupancy_cost'],
                    properties['n_agents'], properties['n_tasks'],
                    properties['beta'])
    logging.info('\tStarting simulation...')
    sim.run()
    logging.info('\tSimulation finished!')

    results[key] = dict()
    results[key]['cost'] = sim.utilitarian_cost()
    results[key]['processed_ticks'] = sim.processed_ticks()
    results[key]['operational_ticks'] = sim.operational_ticks()
    results[key]['average_path_length'] = average_path_length(sim.task_assingments())

  logging.info(results)

if __name__ == '__main__':
  main()