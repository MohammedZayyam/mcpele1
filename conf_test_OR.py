from template import *
import check_spherical_container

class ConfTestOR(ConfTest):
    m_tests: list = None

    #check the variables for this method
    @abc.abstractclassmethod
    def add_test(self, test_input):
        self.m_tests.append(test_input)

    @abc.abstractclassmethod
    def conf_test(self, trial_coords):
        if (len(self.m_tests) == 0 ):
            print("no conf test specified")
        i=0
        while(i < len(self.m_tests)) :
            result: bool =  check_spherical_container.conf_test(trial_coords)
            if(result):
                return True
        return False
