from mc import *
import random

class MetropolisTest(AcceptTest):
    m_seed: size_t
    m_generator: float
    m_distribution: random.uniform(0, 1)
    def __init__(rseed: size_t):
        self.rseed = rseed
    
    @abc.abstractclassmethod
    def test(trial_coords, trial_energy: float, old_coords, old_energy: float, temperature: float):
        return None

    @abc.abstractclassmethod
    def get_seed() ->  size_t:
        return m_seed

    def set_generator_seed(inpt: float):
        random.seed(inp)



