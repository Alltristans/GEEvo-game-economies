# GEEvo: Game Economy Evolution — Extended for Agent-Based Balancing

This repository is an extension of the [GEEvo Framework](https://github.com/FlorianRupp/GEEvo-game-economies) (Florian Rupp & Kai Eckert, IEEE CEC 2024) developed as an undergraduate thesis project at **Institut Teknologi Sepuluh Nopember (ITS)** by **Alridho Tristan Satriawan (NRP 5002221100)**.

The original GEEvo framework provides evolutionary algorithms for generating and balancing graph-based game economies. This extension introduces **agent-based player simulation** and **automatic GDD extraction** to make the balancing process more realistic and automated.

<div style="display: flex; flex-direction: row;">
<p align="center">
    <img src="img/mage.png" alt="Mage Economy" style="width: 44%; margin-right: 10px;">
    <img src="img/archer.png" alt="Archer Economy" style="width: 49%; margin-right: 10px;">
</p>
</div>


## Overview

With this extended GEEvo you can:
- **Generate** graph-based game economies using evolutionary graph generation (EGG)
- **Simulate** economies with agent-based player behavior (aggressive, passive, random)
- **Balance** economies against a target resource value using genetic optimization
- **Extract** economy graph configurations automatically from Game Design Documents (PDF)
- **Evaluate** balancing quality across multiple fitness metrics


## Extensions over Original GEEvo

| Feature | Original GEEvo | This Extension |
|---|---|---|
| Player simulation | None (pure graph simulation) | Agent-based: aggressive / passive / random |
| Fitness function | obj3: `min(s_t, x) / max(s_t, x)` | + obj4: tolerance-threshold variant (Eq. 2) |
| Economy configuration | Manual (code) | Manual **or** automatic from GDD PDF |
| Demo notebook | `demo.ipynb` | + `demo_agent.ipynb`, `evaluate_metrics.ipynb` |


## Project Structure

```
geevo/
├── graph.py              # Graf ekonomi G = (V, E, W)
├── nodes.py              # Tipe node: Source, Pool, Converter, RandomGate, Drain
├── simulation.py         # Base simulator (tanpa agen)
├── agent_simulation.py   # Agent + AgentSimulator (kontribusi TA)
├── gdd_extractor.py      # Ekstraksi konfigurasi dari PDF GDD (kontribusi TA)
└── evolution/
    ├── generator.py      # Evolutionary Graph Generation (EGG)
    └── balancer.py       # Genetic balancer (obj3 & obj4)

Gdd/                      # Dataset PDF Game Design Documents
demo.ipynb                # Demo original GEEvo
demo_agent.ipynb          # Demo dengan AgentSimulator (kontribusi TA)
evaluate_metrics.ipynb    # Evaluasi metrik fitness (kontribusi TA)
test_integration.py       # Integration test
coc_machinations.gml      # Contoh data GML (Clash of Clans)
```


## Agent Behavior

Tiga profil agen disimulasikan untuk merepresentasikan gaya bermain pemain yang berbeda:

- **Aggressive** — memicu semua Converter segera saat sumber daya tersedia (gaya *spammer*)
- **Passive** — menunggu seluruh sistem siap sebelum melakukan aksi (gaya *konservatif*)
- **Random** — keputusan acak dengan probabilitas 50% per langkah (baseline stokastik)


## Fitness Functions

Dua fungsi fitness tersedia di `Balancer`:

**obj3** (default, dari paper asli):
$$f = \frac{\min(s_t, x)}{\max(s_t, x)}$$

**obj4** (Eq. 2, kontribusi TA):
$$f = \begin{cases} 1.0 & \text{if } |x - s_t| \le \alpha \cdot x \\ \dfrac{\min(s_t, x)}{\max(s_t, x)} & \text{otherwise} \end{cases}$$

Di mana $s_t$ adalah nilai Pool target di akhir simulasi dan $x$ adalah nilai target yang diinginkan.


## Quick Start

```python
from geevo.evolution.generator import EvolutionaryGraphGeneration
from geevo.evolution.balancer import Balancer
from geevo.agent_simulation import Agent
from geevo.graph import Graph
from geevo import nodes as n

# 1. Definisikan konfigurasi ekonomi
conf = {n.Source: 2, n.RandomGate: 1, n.Pool: 3, n.Converter: 1}

# 2. Generate topologi graf
egg = EvolutionaryGraphGeneration(conf)
egg.run()
g = Graph(conf, egg.get_best())

# 3. Buat agen dan simulasikan
agent = Agent(behavior='aggressive')
g.simulate(steps=50, agent=agent)

# 4. Balance terhadap target nilai
balancer = Balancer(
    config=g.config, edge_list=g.edge_list,
    balance_pool_ids=[0], balance_value=30,
    agent=agent, fitness_func='obj4', alpha=0.01
)
balancer.run(steps=100)
```

Untuk ekstraksi otomatis dari GDD:

```python
from geevo.gdd_extractor import GDDGraphExtractor

extractor = GDDGraphExtractor('Gdd/MMORPG_GameDesign_v27.pdf', max_nodes=13)
g = extractor.extract()
```


## Notebooks

| Notebook | Deskripsi |
|---|---|
| `demo.ipynb` | Demo original GEEvo: generate, simulate, balance |
| `demo_agent.ipynb` | Demo dengan tiga profil agen + ekstraksi GDD otomatis |
| `evaluate_metrics.ipynb` | Evaluasi dan perbandingan metrik fitness antar konfigurasi |


## Citation

If you use the original GEEvo framework, please cite:

```bibtex
@inproceedings{rupp_geevo_2024,
    title     = {{GEEvo}: {Game} {Economy} {Generation} and {Balancing} with {Evolutionary} {Algorithms}},
    author    = {Rupp, Florian and Eckert, Kai},
    booktitle = {{IEEE} {Congress} on {Evolutionary} {Computation} ({CEC})},
    year      = {2024},
    url       = {http://arxiv.org/abs/2404.18574},
    pages     = {1--8}
}
```


## License

MIT License — see [LICENSE](LICENSE).
