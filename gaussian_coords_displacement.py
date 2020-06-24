from mc import *
import random

class GaussianTakeStep(TakeStep):
    m_seed: size_t
    m_mean: float
    m_stdev: float
    m_generator: float
    m_distribution: float = random.normalvariate(0, 1)
    stepsize: float
    m_count: size_t
    m_ndim: size_t
    m_normal_vec: np.ndarray

    def m_sample_normal_vec(self):
        i=0
        while i < m_ndim:
            m_normal_vec[i] = random.normalvariate(0, 1)
            i +=1 

    def __init__(self, rseed: size_t, stepsize: float, ndim: size_t):
        self.rseed = rseed
        self.stepsize = stepsize
        self.ndim = ndim

    @abc.abstractclassmethod
    def displace(coords):
        return None

    def get_seed(self) -> size_t:
        return m_seed
    
    def set_generator_seed(self, inp: size_t):
        random.seed(inp)

    def get_stepsize(self) -> float:
        return m_stepsize
    
    def set_stepsize(input: float):
        m_stepsize = input

    def get_count() -> size_t:
        return m_count

    def set_count(input: size_t):
        m_count = input

    @abc.abstractclassmethod
    def expected_mean() -> float:
        return 0

    @abc.abstractclassmethod
    def expected_variance(ss: float) -> float:
        return ss*ss

class GaussianCoordsDisplacement(GaussianTakeStep):

    def __init__(self, rseed: size_t, stepsize: float, ndim: size_t):
        self.rseed = rseed
        self.stepsize = stepsize
        self.ndim = ndim
    
    @abc.abstractclassmethod
    def displace(coords: np.ndarray):
        return None

class SampleGaussian(GaussianTakeStep):

    m_origin: np.ndarray

    def __init__(self, rseed: size_t, stepsize: float, origin: np.ndarray):
        self.rseed = rseed
        self.stepsize = stepsize
        self.origin = origin
    



