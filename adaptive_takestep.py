#adopted from adaptive take step.h
from mc import *

class AdaptiveTakeStep(TakeStep):
    def __init__(self, m_interval: size_t, m_total_steps: size_t, m_accepted_steps: size_t, m_factor: float, 
    m_min_acceptance_ratio: float, m_max_acceptance_ratio: float):
    #protected variables
    self._m_interval = m_interval
    self._m_total_steps = m_total_steps
    self._m_accepted_steps  = m_accepted_steps
    self._m_factor = m_factor
    self._m_min_acceptance_ratio = m_min_acceptance_ratio
    self._m_max_acceptance_ratio = m_max_acceptance_ratio

    #methods
    @abc.abstractclassmethod
    def get_min_acceptance_ratio():
        return m_min_acceptance_ratio
    
    @abc.abstractclassmethod
    def get_max_acceptance_ration(self):
        return m_max_acceptance_ratio
    
    @abc.abstractclassmethod
    def get_counters(self, counters: List[size_t]) ->List[size_t]:
        counters[0] = m_total_steps
        counters[1] = m_accepted_steps
        return counters
    
    @abc.abstractclassmethod
    def set_counters(counter: List[size_t]):
        m_total_steps = counters[0]
        m_accepted_steps = counters[1]
    

