import pandas as pd 
import matplotlib.pyplot as plt

SIMULATION_CASES = {
  'si_a10_atm': {
    'description': 'Standard 10x10 grid map. Inelastic to traffic. 10 agents. Standard task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.,
    'n_agents': 10,
    'n_tasks': 1000,
    'lam': 5,
  },
  'si_a10_atf': {
    'description': 'Standard 10x10 grid map. Inelastic to traffic. Fast arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.,
    'n_agents': 10,
    'n_tasks': 1000,
    'lam': 1
  },
  'si_a10_ats': {
    'description': 'Standard 10x10 grid map. Inelastic to traffic. Slow task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.,
    'n_agents': 10,
    'n_tasks': 1000,
    'lam': 10,
  },
  'se_a10_atm': {
    'description': 'Standard 10x10 grid map. Elastic to traffic. 10 agents. Standard task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 10,
    'n_tasks': 1000,
    'lam': 5,
  },
  'se_a10_atf': {
    'description': 'Standard 10x10 grid map. Elastic to traffic. Fast arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 10,
    'n_tasks': 1000,
    'lam': 1
  },
  'se_a10_ats': {
    'description': 'Standard 10x10 grid map. Elastic to traffic. Slow task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 10,
    'n_tasks': 1000,
    'lam': 10,
  },
  'sh_a10_atm': {
    'description': 'Standard 10x10 grid map. Highly elastic to traffic. 10 agents. Standard task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 10,
    'n_tasks': 1000,
    'lam': 5,
  },
  'sh_a10_atf': {
    'description': 'Standard 10x10 grid map. Highly elastic to traffic. Fast arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 1.,
    'n_agents': 10,
    'n_tasks': 1000,
    'lam': 1
  },
  'sh_a10_ats': {
    'description': 'Standard 10x10 grid map. Highly elastic to traffic. Slow task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 1.,
    'n_agents': 10,
    'n_tasks': 1000,
    'lam': 10,
  },

  'si_a25_atm': {
    'description': 'Standard 10x10 grid map. Inelastic to traffic. 25 agents. Standard task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.,
    'n_agents': 25,
    'n_tasks': 1000,
    'lam': 5,
  },
  'si_a25_atf': {
    'description': 'Standard 10x10 grid map. Inelastic to traffic. 25 agents. Fast arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.,
    'n_agents': 25,
    'n_tasks': 1000,
    'lam': 1
  },
  'si_a25_ats': {
    'description': 'Standard 10x10 grid map. Inelastic to traffic. 25 agents. Slow task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.,
    'n_agents': 25,
    'n_tasks': 1000,
    'lam': 10,
  },
  'se_a25_atm': {
    'description': 'Standard 10x10 grid map. Elastic to traffic. 25 agents. Standard task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 25,
    'n_tasks': 1000,
    'lam': 5,
  },
  'se_a25_atf': {
    'description': 'Standard 10x10 grid map. Elastic to traffic. 25 agents. Fast arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 25,
    'n_tasks': 1000,
    'lam': 1
  },
  'se_a25_ats': {
    'description': 'Standard 10x10 grid map. Elastic to traffic. 25 agents. Slow task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 25,
    'n_tasks': 1000,
    'lam': 10,
  },
  'sh_a25_atm': {
    'description': 'Standard 10x10 grid map. Highly elastic to traffic. 25 agents. Standard task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 0.1,
    'n_agents': 25,
    'n_tasks': 1000,
    'lam': 5,
  },
  'sh_a25_atf': {
    'description': 'Standard 10x10 grid map. Highly elastic to traffic. 25 agents. Fast arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 1.,
    'n_agents': 25,
    'n_tasks': 1000,
    'lam': 1
  },
  'sh_a25_ats': {
    'description': 'Standard 10x10 grid map. Highly elastic to traffic. Slow task arrival time.',
    'rows': 10,
    'cols': 10,
    'edge_base_cost': 1.,
    'occupancy_cost': 1.,
    'n_agents': 25,
    'n_tasks': 1000,
    'lam': 10,
  },
}

RESULTS = {
  'si_a10_atm': {'cost': 3971.0, 'processed_ticks': 644, 'only_wip_ticks': 438, 'average_path_length': 7.281437125748503},
  'si_a10_atf': {'cost': 6413.0, 'processed_ticks': 990, 'only_wip_ticks': 6, 'average_path_length': 8.054},
  'si_a10_ats': {'cost': 2077.0, 'processed_ticks': 580, 'only_wip_ticks': 480, 'average_path_length': 6.484158415841584},
  'se_a10_atm': {'cost': 5340.400000000071, 'processed_ticks': 644, 'only_wip_ticks': 438, 'average_path_length': 7.281437125748503},
  'se_a10_atf': {'cost': 7390.400000000745, 'processed_ticks': 990, 'only_wip_ticks': 6, 'average_path_length': 8.054},
  'se_a10_ats': {'cost': 3111.8999999999182, 'processed_ticks': 580, 'only_wip_ticks': 480, 'average_path_length': 6.484158415841584},
  'sh_a10_atm': {'cost': 5340.400000000071, 'processed_ticks': 644, 'only_wip_ticks': 438, 'average_path_length': 7.281437125748503},
  'sh_a10_atf': {'cost': 13894.0, 'processed_ticks': 989, 'only_wip_ticks': 5, 'average_path_length': 8.109},
  'sh_a10_ats': {'cost': 8659.0, 'processed_ticks': 579, 'only_wip_ticks': 479, 'average_path_length': 6.46039603960396},
  'si_a25_atm': {'cost': 4244.0, 'processed_ticks': 282, 'only_wip_ticks': 76, 'average_path_length': 7.738522954091817},
  'si_a25_atf': {'cost': 6315.0, 'processed_ticks': 992, 'only_wip_ticks': 8, 'average_path_length': 7.817},
  'si_a25_ats': {'cost': 2827.0, 'processed_ticks': 278, 'only_wip_ticks': 178, 'average_path_length': 7.56039603960396},
  'se_a25_atm': {'cost': 5500.200000000128, 'processed_ticks': 282, 'only_wip_ticks': 76, 'average_path_length': 7.738522954091817},
  'se_a25_atf': {'cost': 7185.700000000685, 'processed_ticks': 992, 'only_wip_ticks': 8, 'average_path_length': 7.817},
  'se_a25_ats': {'cost': 4062.5999999998776, 'processed_ticks': 278, 'only_wip_ticks': 178, 'average_path_length': 7.56039603960396},
  'sh_a25_atm': {'cost': 5500.200000000128, 'processed_ticks': 282, 'only_wip_ticks': 76, 'average_path_length': 7.738522954091817},
  'sh_a25_atf': {'cost': 13321.0, 'processed_ticks': 992, 'only_wip_ticks': 8, 'average_path_length': 7.817},
  'sh_a25_ats': {'cost': 10933.0, 'processed_ticks': 280, 'only_wip_ticks': 180, 'average_path_length': 7.7247524752475245}
}


def plot_utilitarian_cost_vs_demand(df):
  fig = plt.figure()
  ax1 = fig.add_subplot(211)

  x = df[(df.n_agents==10) & (df.occupancy_cost==0)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==10) & (df.occupancy_cost==0)].sort_values(by=['lam'], ascending=True).cost
  ax1.plot(x, y, color='b', alpha=0.5, label='Inelastic')
  x = df[(df.n_agents==10) & (df.occupancy_cost==0.1)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==10) & (df.occupancy_cost==0.1)].sort_values(by=['lam'], ascending=True).cost
  ax1.plot(x, y, color='r', alpha=0.5, label='Elastic')
  x = df[(df.n_agents==10) & (df.occupancy_cost==1)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==10) & (df.occupancy_cost==1)].sort_values(by=['lam'], ascending=True).cost
  ax1.plot(x, y, color='g', alpha=0.5, label='Highly elastic')
  ax1.grid()
  plt.legend()
  # plt.xlabel('Lambda')
  plt.ylabel('Cost')
  plt.title('Utilitarian cost - 10 agents', size=10)

  ax2 = fig.add_subplot(212)
  x = df[(df.n_agents==25) & (df.occupancy_cost==0)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==25) & (df.occupancy_cost==0)].sort_values(by=['lam'], ascending=True).cost
  ax2.plot(x, y, color='b', alpha=0.5, label='Inelastic')
  x = df[(df.n_agents==25) & (df.occupancy_cost==0.1)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==25) & (df.occupancy_cost==0.1)].sort_values(by=['lam'], ascending=True).cost
  ax2.plot(x, y, color='r', alpha=0.5, label='Elastic')
  x = df[(df.n_agents==25) & (df.occupancy_cost==1)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==25) & (df.occupancy_cost==1)].sort_values(by=['lam'], ascending=True).cost
  ax2.plot(x, y, color='g', alpha=0.5, label='Highly elastic')
  ax2.grid()
  plt.legend()
  plt.xlabel('Lambda')
  plt.ylabel('Cost')
  plt.title('Utilitarian cost - 25 agents', size=10)

  plt.show()

def plot_average_path_length_vs_demand(df):
  fig = plt.figure()
  ax1 = fig.add_subplot(211)

  x = df[(df.n_agents==10) & (df.occupancy_cost==0)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==10) & (df.occupancy_cost==0)].sort_values(by=['lam'], ascending=True).average_path_length
  ax1.plot(x, y, color='b', alpha=0.5, label='Inelastic')
  x = df[(df.n_agents==10) & (df.occupancy_cost==0.1)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==10) & (df.occupancy_cost==0.1)].sort_values(by=['lam'], ascending=True).average_path_length
  ax1.plot(x, y, color='r', alpha=0.5, label='Elastic')
  x = df[(df.n_agents==10) & (df.occupancy_cost==1)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==10) & (df.occupancy_cost==1)].sort_values(by=['lam'], ascending=True).average_path_length
  ax1.plot(x, y, color='g', alpha=0.5, label='Highly elastic')
  ax1.grid()
  plt.legend()
  # plt.xlabel('Lambda')
  plt.ylabel('Number of nodes')
  plt.title('Number of nodes - 10 agents', size=10)

  ax2 = fig.add_subplot(212)
  x = df[(df.n_agents==25) & (df.occupancy_cost==0)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==25) & (df.occupancy_cost==0)].sort_values(by=['lam'], ascending=True).average_path_length
  ax2.plot(x, y, color='b', alpha=0.5, label='Inelastic')
  x = df[(df.n_agents==25) & (df.occupancy_cost==0.1)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==25) & (df.occupancy_cost==0.1)].sort_values(by=['lam'], ascending=True).average_path_length
  ax2.plot(x, y, color='r', alpha=0.5, label='Elastic')
  x = df[(df.n_agents==25) & (df.occupancy_cost==1)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==25) & (df.occupancy_cost==1)].sort_values(by=['lam'], ascending=True).average_path_length
  ax2.plot(x, y, color='g', alpha=0.5, label='Highly elastic')
  ax2.grid()
  plt.legend()
  plt.xlabel('Lambda')
  plt.ylabel('Number of nodes')
  plt.title('Number of nodes - 25 agents', size=10)

  plt.show()

def plot_wip_vs_demand(df):
  fig = plt.figure()
  ax1 = fig.add_subplot(211)

  x = df[(df.n_agents==10) & (df.occupancy_cost==0)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==10) & (df.occupancy_cost==0)].sort_values(by=['lam'], ascending=True).only_wip_ticks
  ax1.plot(x, y, color='b', alpha=0.5, label='Inelastic')
  x = df[(df.n_agents==10) & (df.occupancy_cost==0.1)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==10) & (df.occupancy_cost==0.1)].sort_values(by=['lam'], ascending=True).only_wip_ticks
  ax1.plot(x, y, color='r', alpha=0.5, label='Elastic')
  x = df[(df.n_agents==10) & (df.occupancy_cost==1)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==10) & (df.occupancy_cost==1)].sort_values(by=['lam'], ascending=True).only_wip_ticks
  ax1.plot(x, y, color='g', alpha=0.5, label='Highly elastic')
  ax1.grid()
  plt.legend()
  # plt.xlabel('Lambda')
  plt.ylabel('Number of ticks to process WIP only')
  plt.title('Number of ticks to process WIP only - 10 agents', size=10)

  ax2 = fig.add_subplot(212)
  x = df[(df.n_agents==25) & (df.occupancy_cost==0)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==25) & (df.occupancy_cost==0)].sort_values(by=['lam'], ascending=True).only_wip_ticks
  ax2.plot(x, y, color='b', alpha=0.5, label='Inelastic')
  x = df[(df.n_agents==25) & (df.occupancy_cost==0.1)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==25) & (df.occupancy_cost==0.1)].sort_values(by=['lam'], ascending=True).only_wip_ticks
  ax2.plot(x, y, color='r', alpha=0.5, label='Elastic')
  x = df[(df.n_agents==25) & (df.occupancy_cost==1)].sort_values(by=['lam'], ascending=True).lam
  y = df[(df.n_agents==25) & (df.occupancy_cost==1)].sort_values(by=['lam'], ascending=True).only_wip_ticks
  ax2.plot(x, y, color='g', alpha=0.5, label='Highly elastic')
  ax2.grid()
  plt.legend()
  plt.xlabel('Lambda')
  plt.ylabel('Number of ticks to process WIP only')
  plt.title('Number of ticks to process WIP only - 25 agents', size=10)

  plt.show()

def main():
  # Loads the data
  df = pd.concat([pd.DataFrame(SIMULATION_CASES).T, pd.DataFrame(RESULTS).T], axis=1)

  plot_utilitarian_cost_vs_demand(df)
  plot_average_path_length_vs_demand(df)
  plot_wip_vs_demand(df)

if __name__ == '__main__':
  main()