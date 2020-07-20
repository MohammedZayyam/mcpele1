from mcpele1.montecarlo.template import *
import random

class UniformRectangularSampling():
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
    gen = None
    dist05 =None
    boxvec: np.ndarray = None
    cubic: bool = None
    def __init__(self, seed, boxvec):
        self.gen= seed
        random.seed(seed)
        self.dist05 = random.uniform(-0.5, 0.5)
        if  (isinstance(boxvec, np.ndarray)):
            self.boxvec =  boxvec
        else:
            self.boxvec = np.array([2. * boxvec])
        #print("uni inst")
        
    
    def set_generator_seed(self, inp):
        self.gen = inp

    def displace(self, coords, mcrunner):
        if(len(coords) %len(self.boxvec)):
            print("error")
        mr_particle = len(coords)/len(self.boxvec)
        dim = len(self.boxvec)
        i =0
        k=0
        #print(dim, mr_particle)
        while(i< mr_particle):
            k=0
            while(k< dim):  
                coords[i * dim + k] = self.boxvec[k] * random.uniform(-0.5,0.5)
                #print(" i:{}, k:{}, coords:{},",i, k, coords[i*dim +k])
                k= k+1
            i = i+ 1
        mcrunner.trial_coords = coords
