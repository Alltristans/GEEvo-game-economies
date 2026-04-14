import json

code_cell_1 = """import time
import random
import numpy as np
import pandas as pd
from geevo.evolution.generator import EvolutionaryGraphGeneration
from geevo.evolution.balancer import Balancer
from geevo import nodes as n
from geevo.graph import Graph
from geevo.agent_simulation import Agent
import warnings
warnings.filterwarnings('ignore')

def generate_graph_from_conf(conf):
    egg = EvolutionaryGraphGeneration(conf)
    if egg.run(steps=50):
        return Graph(conf, egg.get_best())
    egg.run(steps=50) 
    return Graph(conf, egg.get_best())

def run_evaluation(graphs, alphas):
    results = {}
    behaviors = ['aggressive', 'passive', 'random']
    agents_dict = {b: Agent(behavior=b) for b in behaviors}

    for alpha in alphas:
        for b_name, agent in agents_dict.items():
            metrics = {
                "Total Runs": 0, "Initial Balanced": 0, "Balanced": 0,
                "Improved": 0, "Execution Times": [], "Generations": []
            }
            
            for g in graphs:
                pools = g.get_nodes_of(n.Pool)
                if not pools: continue
                
                pool_id = random.randint(0, len(pools) - 1)
                t = random.randint(10, 30)
                x = random.randint(20, 100)
                
                metrics["Total Runs"] += 1
                
                b = Balancer(agent=agent, config=g.config, edge_list=g.edge_list, balance_pool_ids=[pool_id], 
                             n_sim_steps=t, balance_value=x, alpha=alpha, fitness_func="obj4", pop_size=20, n_sim=10)
                
                initial_fitness = b.get_ind_fitness(b.init_ind())
                if initial_fitness >= b.threshold:
                    metrics["Initial Balanced"] += 1
                    
                start_time = time.time()
                final_fitness, iterations = b.run(steps=500)
                end_time = time.time()
                
                if final_fitness is None:
                    final_fitness = b.get_ind_fitness(b.population[0])
                
                metrics["Execution Times"].append(end_time - start_time)
                metrics["Generations"].append(iterations)
                
                if final_fitness >= b.threshold:
                    metrics["Balanced"] += 1
                if final_fitness > initial_fitness:
                    metrics["Improved"] += 1
                    
            total = metrics["Total Runs"]
            if total > 0:
                results[(f"\u03b1 = {alpha}", b_name.capitalize())] = {
                    "Balanced (%)": round((metrics["Balanced"] / total) * 100, 1),
                    "Improved (%)": round((metrics["Improved"] / total) * 100, 1),
                    "Initial balanced (%)": round((metrics["Initial Balanced"] / total) * 100, 1),
                    "Median generations": np.median(metrics["Generations"]),
                    "Median execution time (s)": round(np.median(metrics["Execution Times"]), 1)
                }
                
    return pd.DataFrame(results)"""

code_cell_2 = """print("Mempersiapkan Dataset (Abstract EGG + GDD)...\\n")

# 1. Abstract Dataset
base_conf = {n.Source: 3, n.RandomGate: 2, n.Pool: 4, n.Converter: 1}
abstract_graphs = [generate_graph_from_conf(base_conf) for _ in range(3)]

# 2. GDD Dataset based on pdf_results.txt spatial distribution 
mmorpg_conf = {n.Source: 2, n.RandomGate: 3, n.Pool: 5, n.Converter: 3}
vhs_conf = {n.Source: 1, n.RandomGate: 2, n.Pool: 3, n.Converter: 1}

gdd_graphs = [generate_graph_from_conf(mmorpg_conf), generate_graph_from_conf(vhs_conf)]
for _ in range(2): gdd_graphs.append(generate_graph_from_conf(mmorpg_conf))

alphas = [0.05, 0.01, 0.0]"""

code_cell_3 = """print("[1] Evaluasi Dataset Generator Abstrak GEEvo")
df_abstract = run_evaluation(abstract_graphs, alphas)
display(df_abstract)"""

code_cell_4 = """print("[2] Evaluasi Dataset GDD (MMORPG & Horror)")
df_gdd = run_evaluation(gdd_graphs, alphas)
display(df_gdd)"""

notebook = {
    "cells": [
        {"cell_type": "markdown", "metadata": {}, "source": ["# Evaluasi Metrik dan Toleransi (Eq 2) \n", "Notebook untuk mensimulasikan keseimbangan grafik sesuai paparan Paper (Table II)."]},
        {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [code_cell_1]},
        {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [code_cell_2]},
        {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [code_cell_3]},
        {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [code_cell_4]}
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.8.0"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open("evaluate_metrics.ipynb", "w", encoding="utf-8") as f:
    json.dump(notebook, f, indent=1)
