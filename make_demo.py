import json

with open("c:/Users/MSI THIN 15 I7/Downloads/GEEvo-game-economies/demo.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

for cell in nb.get("cells", []):
    if cell["cell_type"] == "code":
        src = "".join(cell.get("source", []))
        if "from geevo import nodes as n" in src:
            src = src.replace("from geevo import nodes as n", "from geevo import nodes as n\nfrom geevo.agent_simulation import Agent")
            
        elif "g = Graph(conf, egg.get_best())" in src:
            src = src + "\n\n# Set manual control on Converter nodes\nfor c in g.get_nodes_of(n.Converter):\n    c.is_auto = False"
            
        elif "g.simulate(10)" in src:
            src = src.replace("g.simulate(10)", "agents = [Agent('aggressive'), Agent('passive'), Agent('random')]\ng.simulate(10, agent=agents[1])")
            
        elif "balancer = Balancer(" in src:
            src = src.replace("balancer = Balancer(config=g.config", "balancer = Balancer(agent=agents, config=g.config")
            
        elif "balanced_graph.simulate(10)" in src:
            src = src.replace("balanced_graph.simulate(10)", "for c in balanced_graph.get_nodes_of(n.Converter):\n    c.is_auto = False\nbalanced_graph.simulate(10, agent=agents[1])")
            
        cell["source"] = [line + ("\n" if idx < len(src.split("\n")) - 1 else "") for idx, line in enumerate(src.split("\n"))]

with open("c:/Users/MSI THIN 15 I7/Downloads/GEEvo-game-economies/demo_agent.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)
print("demo_agent.ipynb created successfully.")
