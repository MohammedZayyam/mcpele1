from mcpele1.montecarlo.template import *
import random
#import abc

class MetropolisTest(AcceptTest):
    m_seed: size_t
    m_generator: float
    m_distribution: random.uniform(0, 1)
    def __init__(self, rseed: size_t):
        self.rseed = rseed
    
    @staticmethod
    def test( trial_coords, trial_energy: float, old_coords, old_energy: float, temperature: float):
        w: float =None
        rand: float = None
        success: bool = True
        dE: float = trial_energy- old_energy
        if (dE> 0 ):
            w = math.exp(-dE/ temperature)
            rand = random.uniform(0,1)
            if (rand>w):
                success= False
        return success
    @abc.abstractclassmethod
    def get_seed(self) ->  size_t:
        return self.m_seed

    def set_generator_seed(self, inpt: float):
        random.seed(inpt)



