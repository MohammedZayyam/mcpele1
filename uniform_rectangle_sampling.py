from template import *
import random

class UniformRectangularSampling():
    m_gen = None
    m_dist05 =None
    m_boxvec: np.ndarray = None
    m_cubic: bool = None
    def __init__(self, seed, boxvec):
        self.m_gen= seed
        random.seed(seed)
        self.m_dist05 = random.uniform(-0.5, 0.5)
        if  (isinstance(boxvec, np.ndarray)):
            self.m_boxvec =  boxvec
        else:
            self.m_boxvec = np.array([2. * boxvec])
        #print("uni inst")
        
    
    def set_generator_seed(self, inp):
        self.m_gen = inp

    def displace(self, coords):
        if(len(coords) %len(self.m_boxvec)):
            print("error")
        mr_particle = len(coords)/len(self.m_boxvec)
        dim = len(self.m_boxvec)
        i =0
        k=0
        #print(dim, mr_particle)
        while(i< mr_particle):
            k=0
            while(k< dim):  
                coords[i * dim + k] = self.m_boxvec[k] * random.uniform(-0.5,0.5)
                #print(" i:{}, k:{}, coords:{},",i, k, coords[i*dim +k])
                k= k+1
            i = i+ 1
            #print("i:", i)
