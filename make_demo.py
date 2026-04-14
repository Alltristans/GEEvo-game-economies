import json

# Membaca format struktur cell dari file ipynb Jupyter Notebook
with open("c:/Users/MSI THIN 15 I7/Downloads/GEEvo-game-economies/demo.ipynb", "r", encoding="utf-8") as f:
    nb = json.load(f)

# Melakukan iterasi modifikasi AST dan source text dari cell JSON
# Proses ini mengotomasi pencarian text term tertentu menggunakan syntax dasar array
for cell in nb.get("cells", []):
    if cell["cell_type"] == "code":
        src = "".join(cell.get("source", [])) # Gabungan string antar baris
        
        # Penggantian subtitusi modul dasar import Agen (Agent Node)
        if "from geevo import nodes as n" in src:
            src = src.replace("from geevo import nodes as n", "from geevo import nodes as n\nfrom geevo.agent_simulation import Agent")
            
        # Penambahan iterasi graph array untuk mengatur variabel boolean Converter Is Default Auto
        elif "g = Graph(conf, egg.get_best())" in src:
            src = src + "\n\n# Set manual control on Converter nodes (Memungkinkan agen mengatur aksi manual pada fungsi transfer matriks persamaan)\nfor c in g.get_nodes_of(n.Converter):\n    c.is_auto = False"
            
        # Inject kode pembuatan model array agen stokastik (behaviour functions) dan mensimulasikannya
        elif "g.simulate(10)" in src:
            src = src.replace("g.simulate(10)", "agents = [Agent('aggressive'), Agent('passive'), Agent('random')]\ng.simulate(10, agent=agents[1])")
            
        # Inject argumen parameter array `agents` kepada obyek class Balancer GEEvo 
        elif "balancer = Balancer(" in src:
            src = src.replace("balancer = Balancer(config=g.config", "balancer = Balancer(agent=agents, config=g.config")
            
        # Modifikasi sel blok simulasi akhir untuk menggunakan state node termanual
        elif "balanced_graph.simulate(10)" in src:
            src = src.replace("balanced_graph.simulate(10)", "for c in balanced_graph.get_nodes_of(n.Converter):\n    c.is_auto = False\nbalanced_graph.simulate(10, agent=agents[1])")
            
        # Merekonstruksi kembali struktur teks dengan memasang pemisah escape (newline \n) kepada cell format iPython Notebook 
        cell["source"] = [line + ("\n" if idx < len(src.split("\n")) - 1 else "") for idx, line in enumerate(src.split("\n"))]

# Melakukan dump map hash dictionary Python kembali kepada wujud encoding file disk JSON JSON (.ipynb)
with open("c:/Users/MSI THIN 15 I7/Downloads/GEEvo-game-economies/demo_agent.ipynb", "w", encoding="utf-8") as f:
    json.dump(nb, f, indent=1)
print("demo_agent.ipynb created successfully.")
