from template import *

class CheckSphericalContainerConfig(ConfTest):
    #protected
    m_radius2: float
    def __init__(self, radius: float):
        self.m_radius2 = radius* radius
    
    def conf_test(self, trial_coords: np.ndarray) -> bool:
        return np.dot(trial_coords, trial_coords) <= self.m_radius2
