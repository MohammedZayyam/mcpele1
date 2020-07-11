from mcpele1.montecarlo.template import *
#from mc import get_iterations_counts

class AdaptiveTakeStep(TakeStep):
    m_interval: size_t = None
    m_total_steps = None
    m_accepted_steps = None
    m_factor: float = None
    m_min_acceptance_ratio = None
    m_max_acceptance_ratio = None
    def __init__(self):
        self.m_interval = 100
        self.m_total_steps = 0
        self.m_accepted_steps = 0
        self.m_factor = 0.9
        self.m_min_acceptance_ratio = 0.2
        self.m_max_acceptance_ratio = 0.5
        try:
            self.m_factor <=0 or self.m_factor >=1
        except:
            print("AdaptiveTakeStep::AdaptiveTakeStep: input factor has illegal value")\

    def report(self, old_coords, old_energy, new_coords, new_energy, success):
        self.m_total_steps +=1
        if(success):
            self.m_accepted_steps +=1
        if(get_iterations_counts()%self.m_accepted_steps==0):
            acceptance_fraction = self.m_accepted_steps/self.m_total_steps
            self.m_accepted_steps = 0
            self.m_total_steps = 0
            if(acceptance_fraction< self.m_min_acceptance_ratio):
                RandomCoordsDisplacement.increase_acceptance(self.m_factor)
            if(acceptance_fraction> self.m_min_acceptance_ratio):
                RandomCoordsDisplacement.decrease_acceptance(self.m_factor)
            

class RandomCoordsDisplacement(TakeStep):
    
    m_step_size = None  
    @staticmethod
    def increase_acceptance(factor):
        m_step_size *= factor
    @staticmethod
    def decrease_acceptance(factor):
        m_step_size /= factor


        