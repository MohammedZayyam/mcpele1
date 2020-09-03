import unittest
from mcpele1.montecarlo.template import np
from mcpele1.montecarlo.template import TakeStep
from mcpele1.montecarlo.mc import MC
from mcpele1.energy.base_potential import Base_Potential

class Example_Potential(Base_Potential):    

    def get_energy(self, x, mcrunner):
        if self.use_changed_coords == False or mcrunner.niter ==1:
            """
            energy when the flag for using changed coords is False
            """
            print("iteration no:", mcrunner.niter)
            print("false", np.dot(x, x))
            return np.dot(x, x)
            
        if self.use_changed_coords == True:
            """
            energy when the flag for using changed coords is True
            """
            Takestep = mcrunner.take_steps
            old_coords = Takestep.old_coords
            old_energy = mcrunner.trial_energy
            y= Takestep.get_changed_coords()
            #boolean array of non-zero vectors
            g= (np.square(y[y>0]))+ 2*old_coords[y>0]*y[y>0]
            return g + old_energy
            

class Example_TakeStep(TakeStep):
    """
    displaces the y coordinate by 1
    """
    old_coords = 0
    new_coords = 0
    x=  np.zeros(2) +[0, 1]
    change_vector = np.zeros(2)
    def displace(self, coords, mcrunner):
        #print(coords)
        self.old_coords = coords
        coords = coords+ self.x
        mcrunner.trial_coords = coords
        #print(coords)
        self.new_coords = coords
    
    def get_changed_coords(self): 
        """
        return the changed in coordinates
        """  
        print("new:", self.new_coords, "old", self.old_coords, "new-old:", self.new_coords-self.old_coords)
        return self.new_coords - self.old_coords

class TestConfTestOR(unittest.TestCase):
    
    def setUp(self):
        self.bdim = 2
        self.point: np.ndarray= [1, 1]
        self.temp = 1
        self.potential = Example_Potential()
        self.nrsteps = 4
        self.mc = MC(self.potential, self.point, self.temp)
        self.step = Example_TakeStep()
        self.mc.set_take_step(self.step)
        self.potential1 = Example_Potential()
        """
        flag for using changed coords is on in mc1 simulation
        """
        self.potential1.set_flag(True)
        self.mc1 = MC(self.potential1, self.point, self.temp)
        self.step1 = Example_TakeStep()
        self.mc1.set_take_step(self.step1)
        

    def test_1(self):
        
        #to test if get_changed_coords can be accessed from Take_Step
        
        self.mc.run(self.nrsteps)
        self.TakeStep = self.mc.get_take_step()
        self.changed_coords=self.TakeStep.get_changed_coords()
        self.x = np.zeros(2)+[0, 1]
        print(self.changed_coords, self.x)
        np.array_equal(self.changed_coords, self.x)

    def test_2(self):
        """
        check if changed_coords and normal energy calculation return 
        the same values
        """
        self.mc.run(self.nrsteps)
        self.mc1.run(self.nrsteps)
        self.assertEqual(self.mc1.get_energy() , self.mc.get_energy())



if __name__ == "__main__":
    unittest.main()
