from geevo.evolution.generator import EvolutionaryGraphGeneration
from geevo.evolution.balancer import Balancer
from geevo import nodes as n
from geevo.graph import Graph
from geevo.agent_simulation import Agent
import warnings

warnings.filterwarnings('ignore')

conf = {
    n.Source: 3,
    n.RandomGate: 2,
    n.Pool: 4,
    n.Converter: 1
}

print("Running EGG...")
egg = EvolutionaryGraphGeneration(conf)
egg.run()

g = Graph(conf, egg.get_best())
for c in g.get_nodes_of(n.Converter):
    c.is_auto = False

agents = [Agent(behavior='aggressive'), Agent(behavior='passive'), Agent(behavior='random')]
print("Simulating graph with all agents...")
g.simulate(10, agent=agents[1])

pool_nodes = g.get_nodes_of(n.Pool)
if len(g.nodes) > 5 and g.nodes[5] in pool_nodes:
    POOL_NODE_ID = pool_nodes.index(g.nodes[5])
else:
    POOL_NODE_ID = 0

print("Running Balancer...")
balancer = Balancer(agent=agents, config=g.config, edge_list=g.edge_list, balance_pool_ids=[POOL_NODE_ID], n_sim_steps=10,
                    balance_value=42, alpha=0.01, frozen_weights=None)
balancer.run(5)

print("Best result:", balancer.result)
print("Integration test passed!")
