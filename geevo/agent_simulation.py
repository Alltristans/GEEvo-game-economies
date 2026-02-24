import random
from geevo.nodes import Converter
from geevo.simulation import Simulator

class Agent:
    def __init__(self, behavior="random"):
        """
        behavior: 'aggressive', 'passive', 'random'
        """
        self.behavior = behavior

    def play_step(self, graph, call_chain):
        manual_converters = []
        for n in graph:
            if isinstance(n, Converter) and getattr(n, 'is_auto', True) is False:
                # Exclude converters driven by RandomGate (push-based, no pool)
                if n.input_edges and type(n.input_edges[0].node).__name__ == "RandomGate":
                    continue
                manual_converters.append(n)

        if not manual_converters:
            return

        if self.behavior == "aggressive":
            # Spam skills: trigger any converter that has enough resources
            for c in manual_converters:
                c.consume(call_chain, force_agent=True)
                
        elif self.behavior == "passive":
            # Wait until ALL manual converters are ready (all skills cooldown finished)
            all_ready = True
            for c in manual_converters:
                if getattr(c, 'called', False):
                    # Already cast in this turn or loop
                    all_ready = False
                    break
                    
                ready = True
                for input_e in c.input_edges:
                    if not input_e.node.pool >= input_e.value:
                        ready = False
                        break
                if not ready:
                    all_ready = False
                    break
            
            if all_ready:
                for c in manual_converters:
                    c.consume(call_chain, force_agent=True)
                    
        elif self.behavior == "random":
            # 50% chance to cast a manual converter if it is ready
            for c in manual_converters:
                if random.random() < 0.5:
                    c.consume(call_chain, force_agent=True)


class AgentSimulator(Simulator):
    def __init__(self, graph, agent):
        super().__init__(graph)
        self.agent = agent

    def run(self, steps=10):
        for _ in range(steps):
            for source in self.sources:
                source.step([])
                
            self.agent.play_step(self.graph, [])
            
            self.monitor()

            # reset converters
            for c in self.converters:
                c.called = False
                
        # reset pool values after simulation
        [p.reset() for p in self.pools]
