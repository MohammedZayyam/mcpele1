from mcpele1.montecarlo.template import TakeStep
import numpy as np
import random

class UniformSphericalSampling(TakeStep):
    """Sample uniformly at random inside N-ball.

    Implements the method described here:
    http://math.stackexchange.com/questions/87230/picking-random-points-in-the-volume-of-sphere-with-uniform-probability
    Variates $X_1$ to $X_N$ are sampled independently from a standard
    normal distribution and then rescaled as described in the reference.
    See also, e.g. Numerical Recipes, 3rd ed, page 1129.

    Parameters
    ----------
    rseed : pos int
        seed for the random number generator (std:library 64 bits Merseene Twister)
    radius : double
        radius of ball
    """
    radius =0
    origin: np.ndarray = [] 

    def __init__(self, seed1, radius):
        random.seed(seed1)
        self.radius = radius
    
    def set_generator_seed(self, input):
        random.seed(input)
    
    def set_origin(self, origin):
        self.origin = origin

    def displace(self, coords: np.ndarray, mcrunner):
        i =0
        while(i < len(coords)):
            coords[i] = random.normalvariate(0,1)
            i +=1
        tmp = 1/np.linalg.norm(coords)

        tmp = tmp*self.radius*(random.uniform(0,1)^(1/len(coords)))

        if(len(self.origin) ==0):
            coords = coords*tmp
        elif(len(self.origin)== len(coords)):
            i =0
            while(i< len(coords)):
                coords[i] = origin[i] + (coords[i]*tmp)
                i +=1
        else:
            print("Error: make sure the origin and coordinates have the same dimension")
        mcrunner.trial_coords = coords
