from mcpele1.montecarlo.template import ConfTest, np

class CheckSphericalContainerConfig(ConfTest):
    """Check that the system is within a spherical container
    
    Parameters
    ----------
    radius : double
        radius of the spherical container, centered at **0**

    """
    
    #protected
    m_radius2: float
    def __init__(self, radius: float):
        self.m_radius2 = radius* radius
    
    def conf_test(self, trial_coords: np.ndarray) -> bool:
        """Check that the configuration point of the system is within a spherical container
    
        Parameters
        ----------
        trial_coords: NumPy Array
            'coords' of the system
        
        Return
        ------
        Bool
            True if the conf condition is satistified, False if not
        """
        return np.dot(trial_coords, trial_coords) <= self.m_radius2
