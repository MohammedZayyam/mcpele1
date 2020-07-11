from mcpele1.montecarlo.template import *
import random

class GaussianTakeStep(TakeStep):
    m_seed: size_t=     None
    m_mean: float =None
    m_stdev: float =None
    m_generator: float =None
    #m_distribution: float = random.normalvariate(0, 1) =None
    stepsize: float =None
    m_count: size_t =None
    m_ndim: size_t =None
    m_normal_vec: np.ndarray =None

    def m_sample_normal_vec(self):
        i=0
        while i < self.m_ndim:
            self.m_normal_vec[i] = random.normalvariate(0, 1)
            i +=1 

    def __init__(self, rseed: size_t, stepsize: float, ndim: size_t):
        self.rseed = rseed
        self.stepsize = stepsize
        self.ndim = ndim

    @abc.abstractclassmethod
    def displace(coords):
        return None

    def get_seed(self) -> size_t:
        return self.m_seed
    
    def set_generator_seed(self, inp: size_t):
        random.seed(inp)

    def get_stepsize(self) -> float:
        return self.m_stepsize
    
    def set_stepsize(self, input: float):
        self.m_stepsize = input

    def get_count(self) -> size_t:
        return self.m_count

    def set_count(self, input: size_t):
        self.m_count = input

    @abc.abstractclassmethod
    def expected_mean(self) -> float:
        return 0

    def expected_variance(self, ss: float) -> float:
        return ss*ss

class GaussianCoordsDisplacement(GaussianTakeStep):

    def __init__(self, rseed: size_t, stepsize: float, ndim: size_t):
        self.rseed = rseed
        self.stepsize = stepsize
        self.ndim = ndim
    @classmethod
    def displace(cls, coords: np.ndarray):
        cls.m_sample_normal_vec
        cls.m_normal_vec = cls.m_normal_vec/np.linalg.norm(cls.m_normal_vec)
        i=0
        while(i<cls.m_ndim):
            coords[i] = coords[i] +(cls.m_normal_vec[i] * cls.m_stepsize)
            i=i+1
        cls.m_count = cls.m_count +1





class SampleGaussian(GaussianTakeStep):

    m_origin: np.ndarray

    def __init__(self, rseed: size_t, stepsize: float, origin: np.ndarray):
        self.rseed = rseed
        self.stepsize = stepsize
        self.origin = origin
    @classmethod
    def displace(cls, coords: np.ndarray):
        cls.m_sample_normal_vec
        cls.m_normal_vec = cls.m_normal_vec/np.linalg.norm(cls.m_normal_vec)
        i=0
        while(i<cls.m_ndim):
            coords[i] = coords[i] +(cls.m_normal_vec[i] * cls.m_stepsize)
            i=i+1
        cls.m_count = cls.m_count +1
    



