# Platform and Network Analytics

## What is this?

This is a small simulation of a network with agents and we are interested in
identifying and analyzing the costs incurred when routing those agents and
assigning tasks to them.

The output is a set of metrics for each simulation case. Those are later
processed to derive some conclusions out of them.

## What do I need?

This project runs with:

- python 3.7
- networkx 2.5
- numpy 1.17.2
- matplotlib 3.1.1
- pandas 0.25.1

## Code structure

### Classes

#### `Warehouse`

Builds and holds a non directed graph that mimics a grid of MxN nodes. Each
node is connected to the left, right, above and below to another node except
those that are on the boundaries. The picture below shows what you would expect:

![Sample warehouse](/doc/img/sample_warehouse.png)

It has tools to manipulate the cost of an edge and that sort. At the moment,
only an affine cost function is used: `a x + b` where `a` is the cost per number
of agents `x` plus a base cost `b`.

At the moment, it has not capacity restrictions.

#### `Agent`

Can be a person, robot, or anything you would like to that can go from one place
in the warehouse to another. By doing so, the *agent* is assigned with a *task*
and affects the traffic of the edge that it will traverse.

It relies on the *current* traffic state of the graph to compute the potential
cost of their trajectory for a *task*. It uses Dijkstra algorithm to find the
path.

The decision whether to take or not the task assignment is not done by the
*agent*. Instead, the *manager* will do so.

#### `WarehouseManager`

Holds a certain amount of *agents* and orchestrates the task assignment. It is
responsible of:

- Querying *agents* to know path proposals and their cost.
- Assign an *agent* with a *task* that minimizes the utilitarian cost of the
  system.
- Update the *warehouse* edge cost because of their occupation (traffic) after
  task assignment.
- Keeps track of some performance metrics.


#### `Simulator`

Instantiates all the entities, creates a task demand profile with a Poisson
distribution for each tick. The system evolves at constant discrete time units.
At the end, it collects some metrics about the test.


### Executables

Run the following in a console:

```sh
cs src/platform_analytics
python simulation_sample.py
```

And you will run several simulations. A file called `sim.log` will be generated
with all the output.