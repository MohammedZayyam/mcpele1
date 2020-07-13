from mcpele1.montecarlo.template import AcceptTest
import random
import abc
import math


class MetropolisTest(AcceptTest):
    m_seed: float
    m_generator: float
    m_distribution: random.uniform(0, 1)

    def __init__(self, seeds):
        self.seeds = seeds
        self.i = 0

    def test(self, trial_energy,  old_energy, temperature):
        random.seed(self.seeds[self.i])
        self.i += 1
        dE = trial_energy - old_energy
        success = True
        if (dE > 0):
            w = math.exp(-dE / temperature)
            rand = random.uniform(0, 1)
            if (rand > w):
                success = False
        return success
    
    def get_seed(self):
        return self.m_seed


    def set_generator_seed(self, inpt: float):
        random.seed(inpt)



