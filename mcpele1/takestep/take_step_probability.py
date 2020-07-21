from mcpele1.montecarlo.template import TakeStep
import random
import numpy as np

class TakeStepProbability(TakeStep):
    """Takes multiple steps in a repeated pattern

    Python interface for c++ TakeStepProbabilities. This move
    takes multiple steps, each with some probability thus
    not affecting the detailed balance condition.

    .. note:: it does NOT break detailed balance
              hence it is the recommended choice
    """
    
    steps = []
    weights: np.ndarray= []
    distributions = 0
    probability= []
    generator = 0
    current_index = 0

    def __init__(self, seed):
        self.generator = seed
        random.seed(self.generator)

    def add_step(self, step_input, weight_input):
        """add a step to a pattern

        all the weights are combined in a normalised discrete distribution

        Parameters
        ----------
        step : :class:`TakeStep`
            object of class :class:`TakeStep` constructed beforehand
        weight: double
            weight to assign to each move
        """
        #print("weight_input", weight_input)
        self.steps.append(step_input)
        self.weights.append( weight_input)
        sum_weights = np.sum(np.array(self.weights))
        self.probability.clear()
        for i in range(0, len(self.weights)):
            self.probability.append((self.weights[i])/sum_weights)
        #print("here", self.probability)
        
    def displace(self, coords, mcrunner):
        """ displace the coords according to the Takesteps choosen by randomvalues
        with probabilities

        Paramters
        ---------
        coords: NumPy array
            coordinates
        mcrunner: :class 'MC'
            the Base Monte Carlo class initialized object
        """
        try:
            len(self.steps) == 0
        except:
            print("there are no Takesteps added to TakeStepProbability")
        stepstemp = np.random.choice(self.steps, 1, p=np.array(self.probability))
        stepstemp[0].displace(coords, mcrunner)

        #more to do
    
