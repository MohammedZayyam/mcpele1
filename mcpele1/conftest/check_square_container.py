from mcpele1.montecarlo.template import ConfTest, np
import sys

class CheckSquareContainerConfig(ConfTest):
    """Check that the system is within a square shape container with origins at **0**
    
    Parameters
    ----------
    side : double
        side length of the square container, centered at **0**

    """
    
    #protected
    side: float
    def __init__(self, side: float):
        if (side<0):
            print("side length cannot be negative")
            sys.exit()
        else:
            self.side = side
    
    def conf_test(self, trial_coords: np.ndarray) -> bool:
        """Check that the configuration point of the system is within a square container
    
        Parameters
        ----------
        trial_coords: NumPy Array
            'coords' of the system
        
        Return
        ------
        Bool
            True if the conf condition is satistified, False if not
        """
        x = np.absolute(trial_coords)
        return  (x<=(self.side/2)).all() 
