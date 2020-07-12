from mcpele1.montecarlo.template import AcceptTest
import random
import abc
import math


class MetropolisTest(AcceptTest):
    m_seed: float
    m_generator: float
    m_distribution: random.uniform(0, 1)
    def __init__(self, rseed: float):
        self.m_seed = rseed
        self.set_generator_seed(self.m_seed)
    @staticmethod
    def test(trial_energy,  old_energy, temperature):
        dE = trial_energy- old_energy
        success=True
        print(dE)
        if (dE> 0 ):
            w = math.exp(-dE/ temperature)
            rand = random.uniform(0,1)
            print(rand)
            print(w)
            if (rand>w):
                success= False
        return success
    
    def get_seed(self):
        return self.m_seed


    def set_generator_seed(self, inpt: float):
        random.seed(inpt)



