from mcpele1.montecarlo.template import AcceptTest

class EnergyWindowTest(AcceptTest):
    min_energy: float
    max_energy: float
    
    def __init__(self, min_energy: float, max_energy: float):
        self.min_energy = min_energy
        self.max_energy = max_energy
    
    def test(self, trial_energy: float, min_energy: float, max_energy: float) -> bool:
        return ((trial_energy >= min_energy) and (trial_energy <= max_energy))