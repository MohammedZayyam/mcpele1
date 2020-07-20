#test this out
from mcpele1.montecarlo.template import *
from mcpele1.conftest.check_spherical_container import CheckSphericalContainer

class ConfTestOR(ConfTest):
    tests: list = []

    def add_test(self, test_input):
        self.tests.append(test_input)

    def conf_test(self, trial_coords):
        if (len(self.tests) == 0 ):
            print("no conf test specified")
        i=0
        for test in self.tests:
            result = test.conf_test(trial_coords)
            if(result):
                return True
        return False
