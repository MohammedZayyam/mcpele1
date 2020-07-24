from mcpele1.montecarlo.template import ConfTest, np


class CheckSphericalContainer(ConfTest):
    """Check that the system is within a spherical container
    
    Parameters
    ----------
    radius2 : double
        radius of the spherical container, centered at **0**
    ndim : int
        dimensionality of the space (box dimensionality)
    """
    
    m_radius2: float = 0
    ndim = 0
    
    def __init__(self, radius: float, ndim):
        self.m_radius2 = radius
        self.ndim = ndim
        return None 

    def conf_test(self, trial_coords: np.ndarray) -> bool:
        """Check that the 'trial_coords' of the system is within a spherical container
    
        Parameters
        ----------
        trial_coords : NumPy Array
            'coords' of the system
        
        Return
        ------
        Bool
            True if the conf condition is satistified, False if not
        """
        N = len(trial_coords)
        r2: float = 0
        i =0
        while (i<N):
            j=i
            while (j< i+self.ndim):
                r2 = r2 + trial_coords[j]*trial_coords[j]
                j = j+1
            if (r2> self.m_radius2):
                return False
            i = i + self.ndim
        return True

#from mc import *









