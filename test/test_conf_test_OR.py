import unittest
from mcpele1.montecarlo.template import np
from mcpele1.montecarlo.mc import MC
from mcpele1.conftest.conf_test_OR import ConfTestOR
from mcpele1.conftest.check_spherical_container_config import CheckSphericalContainerConfig
from mcpele1.conftest.check_square_container import CheckSquareContainerConfig

class NoTakeStep:
    def displace(self, coords, mcrunner):
        mcrunner.trial_coords = coords

class NoPotential:
    def get_energy( self, x):
        return 1

class TestConfTestOR(unittest.TestCase):
    
    
    def setUp(self):
        self.bdim = 3
        self.point: np.ndarray= [3, 0, 0]
        self.temp = 1
        self.potential = NoPotential()
        self.nrsteps = 1
        self.conftest_1 = CheckSphericalContainerConfig(5)
        self.conftest_2 = CheckSquareContainerConfig(2)
        self.conftest_final = ConfTestOR()
        self.mc = MC(self.potential, self.point, self.temp)
        self.conftest_final.add_test( self.conftest_1)
        self.conftest_final.add_test( self.conftest_2)
        self.step = NoTakeStep()
        self.mc.set_take_step(self.step)
        self.mc.add_conf_test(self.conftest_final)
        
    
    #point in the circle but not in the square 
    def test_1(self):
        self.mc.run(self.nrsteps)
        self.assertEqual(self.mc.accept_count, self.nrsteps)
    
    #point in both the circle and square
    def test_2(self):
        x = np.zeros(self.bdim)
        self.mc.set_coordinates(x, 1)
        self.mc.run(self.nrsteps)
        self.assertEqual(self.mc.accept_count, self.nrsteps)
    
    #point outside both the circle and quare
    def test_3(self):
        x = np.ones(self.bdim)*10
        self.mc.set_coordinates(x, 1)
        #print(self.mc.get_coords())
        self.mc.run(self.nrsteps)
        self.assertEqual(self.mc.accept_count, 0)


        

if __name__ == "__main__":
    unittest.main()



