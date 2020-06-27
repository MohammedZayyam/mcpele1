from mc import *
 
class TakeStepPattern(TakeStep):
    m_steps: list = None
    m_step_storage: list  = None

    def add_step(self, step_input):
        self.m_steps.append(step_input)
    
    def displace(self, coords):
        return None

    def report(self, old_coords, old_energy:float, new_coords, new_energy: float, success: bool):

