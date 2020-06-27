from template import *
import random

class UniformRectangularSampling(TakeStep):
    m_gen = None
    m_dist05 =None
    m_boxvec: np.ndarray = None
    m_cubic: bool = None
    def __init__(self, seed, boxvec):
        self.m_gen= seed
        self.m_dist05 = random.uniform(-0.5, 0.5)
        self.m_boxvec =  boxvec
    
    def set_generator_seed(self, inp):
        self.m_gen = inp

    @abc.abstractmethod
    @classmethod
    def displace(cls, coords):
        if(len(coords) %len(cls.m_boxvec)):
            print("error")
        mr_particle = len(coords)/len(cls.m_boxvec)
        dim = len(cls.m_boxvec)
        i =0
        k=0
        while(i< mr_particle):
            while(k< dim):
                coords[i * dim + k] = cls.m_boxvec[k] * cls.m_dist05.seed(m_gen)
                k+=1
            i +=1
