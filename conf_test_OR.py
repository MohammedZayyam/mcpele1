from mc import *

class ConfTestOR(ConfTest):
    m_tests: List[bool]

    #check the variables for this method
    @abc.abstractclassmethod
    def add_test():
        return None

    @abc.abstractclassmethod
    def conf_test(trial_coords):
        return None
    
