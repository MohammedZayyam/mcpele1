from mcpele1.montecarlo.template import TakeStep
from mcpele1.takestep.pattern_manager import PatternManager
from typing import List
    
class TakeStepPattern(TakeStep):
    """Takes multiple steps in a repeated pattern

    Python interface for c++ TakeStepPattern. This move
    takes multiple steps in a repeated deterministic pattern.

    .. warning:: breaks detailed balance locally
    """
    steps = PatternManager()
    step_storage: List[TakeStep]  = []

    def add_step(self, step_input, repetitions_input):
        """add a step to a pattern

        Parameters
        ----------
        step : :class:`TakeStep`
            object of class :class:`TakeStep` constructed beforehand
        nr_repetitions: int
            number of Monte Carlo iterations in a row for which this
            move is performed
        """
        self.steps.add( len(self.step_storage), repetitions_input)
        self.step_storage.append(step_input) 
        
    def displace(self, coords, mcrunner):
        self.steps.increment()
        self.step_storage[self.steps.get_index()].displace(coords, mcrunner)

    #do other stuff
    
