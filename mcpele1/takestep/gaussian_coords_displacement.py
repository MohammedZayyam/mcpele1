from mcpele1.montecarlo.template import TakeStep, size_t, np, abc
import random

class GaussianTakeStep(TakeStep):
    """Take a uniform random step in a ``bdim`` dimensional hypersphere of radius ``stepsize``

    this class is the Python interface for the c++ GaussianCoordsDisplacement implementation.
    Takes a step by sampling uniformly a ``bdim`` dimensional hypersphere or radius ``stepsize``

    Parameters
    ----------
    rseed : pos int
        seed for the random number generator (std:library 64 bits Merseene Twister)
    stepsize : double
        size of step in each dimension
    ndim : int
        dimensionality of coordinates array
    """
    rseed =0
    mean: float =0
    stdev: float =0
    generator=0
    #m_distribution: float = random.normalvariate(0, 1) =None
    stepsize =0
    count =0 
    ndim =0
    normal_vec: np.ndarray =[]

    def m_sample_normal_vec(self):
        i=0
        self.normal_vec = np.zeros(self.ndim)
        while i < self.ndim:
            self.normal_vec[i] = random.normalvariate(0, 1)
            i +=1 
        return self.normal_vec

    def __init__(self, rseed: size_t, stepsize: float, ndim: size_t):
        self.rseed = rseed
        self.stepsize = stepsize
        self.ndim = ndim
        

    @abc.abstractclassmethod
    def displace(coords):
        return None

    def get_seed(self):
        """return random number generator seed

        Returns
        -------
        int
            random number generator seed
        """
        return self.rseed
    
    def set_generator_seed(self, inp):
        """sets the random number generator seed

        Parameters
        ----------
        input : pos int
            random number generator seed
        """
        random.seed(inp)

    def get_stepsize(self) -> float:
        """get the step size

        Returns
        -------
        double
            stepsize
        """
        return self.m_stepsize
    
    def set_stepsize(self, input: float):
        """set the step size
        
        Parameters
        ----------
        input: float
            stepsize to set
        """
        self.m_stepsize = input

    def get_count(self):
        """get the total count of the number of steps taken

        Returns
        -------
        int
            total count of steps taken
        """
        return self.count

    def set_count(self, input):
        """set the count
        
        Parameters
        ----------
        input: float
            total count of steps
        """
        self.count = input

    def expected_mean(self) -> float:
        return 0

    def expected_variance(self, ss: float) -> float:
        return ss*ss

class GaussianCoordsDisplacement(GaussianTakeStep):

    def __init__(self, rseed, stepsize, ndim):
        self.rseed = rseed
        self.stepsize = stepsize
        self.ndim = ndim
        #print(ndim)
    
    def displace(self, coords, mcrunner):
        self.m_sample_normal_vec()
        self.normal_vec = self.normal_vec/np.linalg.norm(self.normal_vec)
        i=0
        while(i<self.ndim):
            coords[i] = coords[i] +(self.normal_vec[i] * self.stepsize)
            #mcrunner.trial_coords[i] = coords[i]
            i+=1
        mcrunner.trial_coords  = coords
        #print(self.stepsize)
        self.count = self.count +1
        
    
    def get_stepsize(self):
        return self.stepsize

class SimpleGaussian(GaussianTakeStep):
    def __init__(self, rseed,  ndim):
        self.ndim = ndim
        random.seed(rseed)  

    def displace(self, coords, mcrunner):
        mcrunner.trial_coords = self.m_sample_normal_vec()
        self.count = self.count +1
        #print(coords)

class SampleGaussian(GaussianTakeStep):

    m_origin: np.ndarray

    def __init__(self, rseed, stepsize: float, origin: np.ndarray):
        self.rseed = rseed
        self.stepsize = stepsize
        self.origin = origin
   
    def displace(self, coords: np.ndarray, mcrunner):
        self.m_sample_normal_vec()
        self.normal_vec = self.normal_vec/np.linalg.norm(self.normal_vec)
        i=0
        while(i<self.ndim):
            coords[i] = coords[i] +(self.normal_vec[i] * self.m_stepsize)
            i=i+1
        self.count = self.count +1
        mcrunner.trial_coords = coords
    



