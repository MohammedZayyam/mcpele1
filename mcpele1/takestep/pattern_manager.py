#incomple
from mcpele1.montecarlo.template import *
from typing import NewType

vec_t = NewType('vec_t', list)
class PatternManager:
    m_step_repetitions: vec_t =None
    m_current_step_index: size_t = None
    m_current_step_count: size_t = None
    m_initialized: bool = None
    
    def __init__(self):
        self.m_initialized = False
    """
    overloading method not translated to python for now"""
    def add(self, index_input, repetitions_input = 1):
        if (repetitions_input<1):
            print("error")
            exit(0)
        new = [repetitions_input, index_input]
        self.m_step_repetitions.append(new)
        self.m_current_step_index = 0
        self.m_current_step_count =self.m_step_repetitions[0][0]
        if(self.m_initialized ==False):
            self.m_initialized = True
        