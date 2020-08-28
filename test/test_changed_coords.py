import unittest
from mcpele1.montecarlo.template import np
from mcpele1.montecarlo.template import TakeStep
from mcpele1.montecarlo.mc import MC
from mcpele1.energy.base_potential import Base_Potential

class Example_Potential(Base_Potential):    

    def get_energy(self, x):
        return

class Example_TakeStep(TakeStep):
    """
    displaces the y coordinate by 1
    """
    old_coords = 0
    new_coords = 0
    def displace(self, coords, mcrunner):
        self.old_coords = coords
        x=  np.zeros(2) +[0, 1]
        coords += x
        mcrunner.trial_coords = coords
        self.new_coords = coords
    
    def get_changed_coords(self): 
        """
        return the changed in coordinates
        """  
        return self.new_coords - self.old_coords

class TestConfTestOR(unittest.TestCase):
    
    def setUp(self):
        self.bdim = 2
        self.point: np.ndarray= [1, 1]
        self.temp = 1
        self.potential = Example_Potential()
        self.nrsteps = 1
        self.mc = MC(self.potential, self.point, self.temp)
        self.step = Example_TakeStep()
        self.mc.set_take_step(self.step)
        
    
    #point in the circle but not in the square 
    def test_1(self):
        """
        to test if get_changed_coords can be accessed from Take_Step
        """
        self.mc.run(self.nrsteps)
        self.TakeStep = self.mc.get_take_step()
        self.changed_coords=self.TakeStep.get_changed_coords()
        self.x = np.zeros(2)+[0, 1]
        np.array_equal(self.changed_coords, self.x)


if __name__ == "__main__":
    unittest.main()
