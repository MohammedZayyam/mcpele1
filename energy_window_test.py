from mc import *

class EnergyWindowTest(AcceptTest):
    m_min_energy: float
    m_max_energy: float
    def __init__(self, min_energy: float, max_energy: float):
        self.min_energy = min_energy
        self.max_energy = max_energy
    
    @abc.abstractclassmethod
    def test(trial_coords, trial_energy: float, old_coords, old_energy:float, temperature: float) -> bool:
        return None