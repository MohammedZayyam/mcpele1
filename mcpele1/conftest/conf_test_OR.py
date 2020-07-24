#test this out
from mcpele1.montecarlo.template import ConfTest, np

class ConfTestOR(ConfTest):
    """Creates a union of multiple configurational tests
    
    This configurational
    test takes multiple conf tests and generates an union,
    therefore it is sufficient to satisfy one of these
    subtests to pass their union.
    
    """
    tests = []
    def __init__(self):
        self.tests =[]

    def add_test(self, test_input):
        self.tests.append(test_input)
        #print(test_input)

    def conf_test(self, trial_coords):
        if (len(self.tests) == 0 ):
            print("no conf test specified")
        for test in self.tests:
            result = test.conf_test(trial_coords)
            if(result):
                return True
        return False
