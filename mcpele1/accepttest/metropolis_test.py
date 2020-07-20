from mcpele1.montecarlo.template import AcceptTest
import random
import abc
import math


class MetropolisTest(AcceptTest):
    """Metropolis acceptance criterion
    
    This class is the Python interface for the c++ mcpele::MetropolisTest 
    acceptance test class implementation. The Metropolis acceptance criterion
    accepts each move with probability
    
    .. math:: P( x_{old} \Rightarrow x_{new}) = min \{ 1, \exp [- \\beta (E_{new} - E_{old})] \}
    
    where :math:`\\beta` is the reciprocal of the temperature.
    """
    rseed: float

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
        return self.rseed


    def set_generator_seed(self, inpt: float):
        random.seed(inpt)



