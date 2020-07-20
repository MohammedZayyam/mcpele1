from mcpele1.montecarlo.template import TakeStep

class AdaptiveTakeStep(TakeStep):
    interval = 0
    total_steps = 0
    accepted_steps = 0
    factor: float = 0
    min_acceptance_ratio = 0
    max_acceptance_ratio = 0

    def __init__(self, ts, interval, factor, min_acceptance_ratio, max_acceptance_ratio):
        self.ts = ts
        self.interval = interval
        self.total_steps = 0
        self.accepted_steps = 0
        self.factor = factor
        self.min_acceptance_ratio = min_acceptance_ratio
        self.max_acceptance_ratio = max

        try:
            self.factor <=0 or self.factor >=1
        except:
            print("AdaptiveTakeStep::AdaptiveTakeStep: input factor has illegal value")

    def report(self, old_coords, old_energy, new_coords, new_energy, success, mcrunner):

        self.total_steps +=1
        if(success):
            self.accepted_steps +=1
        if(mcrunner.get_iterations_counts()%self.interval ==0):
            acceptance_fraction = self.accepted_steps/self.total_steps
            self.accepted_steps = 0
            self.total_steps = 0
            if(acceptance_fraction< self.min_acceptance_ratio):
                self.ts.increase_acceptance(self.factor)
            if(acceptance_fraction> self.min_acceptance_ratio):
                self.ts.decrease_acceptance(self.factor)
            



        