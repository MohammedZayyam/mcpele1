from mc import *

def CheckSphericalContainer(ConfTest):
    m_radius2: float = None
    m_ndim: size_t = None
    
    def __init__(self, radius: float, ndim: size_t):
        self.m_radius2 = radius
        self.m_ndim = ndim
        return None 

    @abc.abstractclassmethod
    def conf_test(trial_coords: np.ndarray) -> bool:
        N: size_t = len(rial_coords)
        r2: float = 0
        i: size_t = 0
        while (i<N):
            j=i
            while (j< i+m_ndim)
                r2 = r2 + trial_coords[j]*trial_coords[j]
                j = j+1
            if (r2> m_radius2):
                return False
            i = i + m_ndim
        return True







